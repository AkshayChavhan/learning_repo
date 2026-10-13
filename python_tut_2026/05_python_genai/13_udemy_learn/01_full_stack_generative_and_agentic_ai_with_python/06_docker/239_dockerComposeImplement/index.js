// A tiny web app that needs Postgres and Redis.
//
// Where are they? It depends on where THIS process runs:
//   - inside Compose (the normal case): the `environment:` block in docker-compose.yml
//     gives the SERVICE NAMES and CONTAINER ports -> db:5432, redis:6379
//   - on your Mac (`npm start`, with the db/redis ports: lines uncommented):
//     nothing is set, so it falls back to localhost + the PUBLISHED ports.
//
// "localhost" inside a container means that container itself - which is exactly
// why the hardcoded-localhost version breaks the moment it runs in Compose.
const express = require("express");
const { Client } = require("pg");
const Redis = require("ioredis");

const DB_HOST = process.env.DB_HOST || "localhost";
const DB_PORT = Number(process.env.DB_PORT || 5431);
const REDIS_HOST = process.env.REDIS_HOST || "localhost";
const REDIS_PORT = Number(process.env.REDIS_PORT || 6379);
const PORT = Number(process.env.PORT || 8000);

// Client factories: a pg Client can't be reused after a failed connect(), and an
// ioredis instance keeps internal state too - so every attempt gets a fresh one.
const makePg = () =>
  new Client({
    host: DB_HOST,
    port: DB_PORT,
    user: "postgres",           // POSTGRES_USER     (from the db service's environment)
    password: "postgres",       // POSTGRES_PASSWORD
    database: "postgres",       // POSTGRES_DB
  });

const makeRedis = () => {
  const r = new Redis({
    host: REDIS_HOST,
    port: REDIS_PORT,
    lazyConnect: true,          // connect explicitly so a failure is a clear error
    retryStrategy: () => null,  // we do our own retrying below
  });
  // ioredis reports a refused connection as an 'error' EVENT (unhandled = noisy
  // stack trace) and rejects connect() with a vague "Connection is closed."
  // Keep the real reason so the log says ECONNREFUSED and where.
  r.on("error", (err) => { r.lastError = err; });
  return r;
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const reason = (err) =>
  err.message || (err.errors && err.errors[0] && err.errors[0].message) || String(err);

// depends_on only controls START ORDER - Postgres can still be initialising when
// the backend's first connect fires. Retry a few times instead of dying instantly.
async function connectWithRetry(name, make, attempts = 15) {
  for (let i = 1; i <= attempts; i++) {
    const client = make();
    try {
      await client.connect();
      console.log(`${name} connected`);
      return client;
    } catch (err) {
      const why = reason(client.lastError || err);
      if (client.disconnect) client.disconnect();   // ioredis: stop any pending socket
      if (i === attempts) throw new Error(`${name}: ${why}`);
      console.log(`${name} not ready (${why}), retry ${i}/${attempts}...`);
      await sleep(1000);
    }
  }
}

let pg;
let redis;

async function connect() {
  redis = await connectWithRetry("Redis", makeRedis);
  pg = await connectWithRetry("Postgres", makePg);
  await pg.query(
    "CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, at TIMESTAMPTZ DEFAULT now())"
  );
}

const app = express();

// Every request records a visit in BOTH stores and reports the totals.
app.get("/", async (req, res) => {
  try {
    await pg.query("INSERT INTO visits DEFAULT VALUES");
    const { rows } = await pg.query("SELECT count(*)::int AS n FROM visits");
    const redisVisits = await redis.incr("visits");
    res.json({
      status: "success",
      postgres_visits: rows[0].n,
      redis_visits: redisVisits,
      connected_to: { db: `${DB_HOST}:${DB_PORT}`, redis: `${REDIS_HOST}:${REDIS_PORT}` },
    });
  } catch (err) {
    res.status(500).json({ status: "error", message: reason(err) });
  }
});

connect()
  .then(() => app.listen(PORT, () => console.log(`Server is running on port ${PORT}`)))
  .catch((err) => {
    console.error("Error:", reason(err));
    console.error(
      "Running inside Compose? Then connect by SERVICE NAME on the CONTAINER port:\n" +
        "  DB_HOST=db DB_PORT=5432 REDIS_HOST=redis REDIS_PORT=6379   (see docker-compose.yml)\n" +
        "Running on your Mac? Then the stack must be up: docker compose up -d"
    );
    process.exit(1);
  });
