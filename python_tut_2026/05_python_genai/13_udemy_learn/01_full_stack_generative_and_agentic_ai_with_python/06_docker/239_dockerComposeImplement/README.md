# Docker Compose example — a Node app + Postgres + Redis, all in one file

A small, runnable demo of **Docker Compose**: the app is **built from its Dockerfile and runs
inside Compose** next to the databases it needs, finds them **by service name**, keeps its data
in **named volumes**, and is the **only thing published** to the outside world.

```text
   INTERNET ──► localhost:8000 ──► backend ──► db:5432     (private, not published)
                 the only           │     └──► redis:6379  (private, not published)
                 published port     │
                                    └── ecommerce_default network, created by Compose

   named volumes (survive down/up):  ecommerce_postgres_data   ecommerce_redis_data
```

---

## 1. Prerequisites

| Need | Check | Install (macOS) |
|---|---|---|
| **Docker Desktop** running | `docker info` prints server info | `brew install --cask docker`, then open the Docker app once |
| **Docker Compose v2** (ships with Docker Desktop) | `docker compose version` → `v2.x` | — |
| Port **8000** free on your machine | `lsof -nP -iTCP:8000 -sTCP:LISTEN` prints nothing | stop whatever is listening, or change the host side of `"8000:8000"` |

Node.js is **not** required on your machine — the app is built and run inside Docker.

---

## 2. What's in this folder

| File | What it does |
|---|---|
| `docker-compose.yml` | three services: `backend` (built from `./Dockerfile`, published on 8000), `db` (`postgres:16`) and `redis` — plus two named volumes. Every line is commented. |
| `Dockerfile` | how to build the app image: `node:20-alpine`, `npm install`, copy `index.js`, `npm start` |
| `.dockerignore` | keeps `node_modules/` out of the build context |
| `index.js` | an Express server. On startup it connects to Redis and Postgres (retrying while they boot), then every `GET /` records a visit in both and returns the totals |
| `package.json` | `express`, `pg`, `ioredis` |

---

## 3. Run it

Open a terminal **in this folder**.

```bash
docker compose up --build -d     # step 1 - build the app image, start all three
curl localhost:8000              # step 2 - hit the app (repeat: counters go up)
docker compose logs backend      # step 3 - see the startup sequence
docker compose ps                # step 4 - only backend has a host port

docker compose down              # step 5 - remove containers + network; volumes are KEPT
docker compose up -d             # step 6 - no --build needed, code didn't change
curl localhost:8000              #          counters CONTINUE where they were

docker compose down -v           # step 7 - the reset: also delete the volumes
```

| Step | You should see |
|---|---|
| 1 | `✔ Image ecommerce-backend  Built` <br> `✔ Volume ecommerce_postgres_data  Created` · `✔ Volume ecommerce_redis_data  Created` <br> `✔ Container postgres  Started` · `✔ Container redis  Started` · `✔ Container backend  Started` |
| 2 | `{"status":"success","postgres_visits":1,"redis_visits":1,"connected_to":{"db":"db:5432","redis":"redis:6379"}}` — note `db:5432` and `redis:6379`, service names, container ports |
| 3 | `Redis connected` <br> `Postgres not ready (connect ECONNREFUSED 172.20.0.2:5432), retry 1/15...` ← Postgres was still booting <br> `Postgres connected` <br> `Server is running on port 8000` |
| 4 | `backend   0.0.0.0:8000->8000/tcp` <br> `postgres  5432/tcp` ← no host mapping <br> `redis     6379/tcp` ← no host mapping |
| 5 | `Container … Removed`, `Network ecommerce_default Removed` — **no** `Volume … Removed` line |
| 6 | the JSON again, with the counts continuing (e.g. `4`, `5`) — the data outlived the containers |
| 7 | `✔ Volume ecommerce_postgres_data  Removed` · `✔ Volume ecommerce_redis_data  Removed` |

---

## 4. The three ideas this demonstrates

### a) `build: .` — the app is a service too

```yaml
  backend:
    build: .                 # read ./Dockerfile, build an image, run it
    ports:
      - "8000:8000"
```

| Way to put your app in Compose | In the file | When |
|---|---|---|
| build from the Dockerfile | `build: .` | development — Compose builds locally |
| use a published image | `image: <username>/backend-app` | deploying what you pushed to Docker Hub |

**After changing code, run `docker compose up --build`.** Plain `up` reuses the old image and
you'll chase a bug that's already fixed.

### b) Inside the network, connect by **service name** on the **container port**

| Before (app on your Mac) | Now (app in Compose) | Why |
|---|---|---|
| `localhost:5431` | **`db:5432`** | `db` is the service name → resolves to that container. 5431 was the *published host* port; inside you use the container's real port |
| `localhost:6379` | **`redis:6379`** | same |

`localhost` inside a container means **that container itself**. Prove it — run the backend with
`localhost` instead of the service names:

```bash
docker compose run --rm --no-deps -e DB_HOST=localhost -e DB_PORT=5432 -e REDIS_HOST=localhost backend
```
```text
Redis not ready (connect ECONNREFUSED ::1:6379), retry 1/15...
...
Error: Redis: connect ECONNREFUSED ::1:6379
Running inside Compose? Then connect by SERVICE NAME on the CONTAINER port:
  DB_HOST=db DB_PORT=5432 REDIS_HOST=redis REDIS_PORT=6379   (see docker-compose.yml)
```

The app looked for Redis inside its own container. Nothing there. That's why the real config
lives in the `environment:` block of the `backend` service:

```yaml
    environment:
      DB_HOST: db
      DB_PORT: "5432"
      REDIS_HOST: redis
      REDIS_PORT: "6379"
```

### c) Publish only the app

The `ports:` lines on `db` and `redis` are gone (left commented in the file). Nothing on your
machine needs them any more — only `backend` talks to them, over the private network. Postgres
and Redis are invisible from outside; the app is the single front door.

---

## 5. Why the data survives: named volumes

`docker compose down` deletes containers **and everything written inside them**. Two additions
keep the data outside:

```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data   # (1) mount it where the image writes
  redis:
    volumes:
      - redis_data:/data                         # (1)

volumes:                                         # (2) declare them
  postgres_data:
  redis_data:
```

| | |
|---|---|
| real volume names | `<project>_<volume>` → `ecommerce_postgres_data` |
| `docker compose down` | keeps volumes |
| `docker compose down -v` | deletes them — the only way to reset the data |
| mount path | from each image's Docker Hub page: postgres `/var/lib/postgresql/data`, redis `/data`, mongo `/data/db`, mysql `/var/lib/mysql` |

No host path is needed: Docker manages where a named volume lives (`docker volume inspect
ecommerce_postgres_data`). A path on the left (`./data:/var/lib/postgresql/data`) would be a
bind mount instead — handy for files you want to open yourself, not needed for databases.

---

## 6. One more thing the logs teach: `depends_on` is start order, not readiness

Step 3's log shows `Postgres not ready … retry 1/15`. `depends_on` only makes Compose **start**
`db` before `backend`; Postgres still needs a second or two to initialise. `index.js` retries
with a fresh client each second instead of crashing. (Compose's `healthcheck` +
`depends_on: condition: service_healthy` is the declarative version of the same idea.)

---

## 7. Look inside (optional)

```bash
docker compose logs -f backend                                       # follow the app's logs
docker exec -it postgres psql -U postgres -c 'select * from visits;'  # rows the app inserted
docker exec -it redis redis-cli get visits                            # the counter
docker exec -it backend sh -c 'getent hosts db redis'                 # service names → IPs
docker volume inspect ecommerce_postgres_data                        # where the volume lives
```

### Run the app on your Mac instead (the earlier lessons)

Uncomment the two `ports:` blocks on `db` and `redis`, then:

```bash
docker compose up -d db redis     # only the databases
npm install && npm start          # app on your Mac; defaults = localhost:5431 / localhost:6379
curl localhost:8000
```

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop isn't running | open the Docker app, wait for "running", retry |
| `Bind for 0.0.0.0:8000 failed: port is already allocated` | another container/process owns 8000 | `docker ps` → `docker rm -f <it>`, or change the host side of `"8000:8000"` |
| you changed `index.js` but the container runs old code | plain `up` reused the cached image | `docker compose up --build` |
| `ECONNREFUSED 127.0.0.1:6379` / `::1:6379` in the backend logs | the app uses `localhost` inside the container | connect by service name: `redis`, `db` (the `environment:` block) |
| `ECONNREFUSED …:5432` once, then `Postgres connected` | Postgres still booting on the first attempt | normal — the retry handles it |
| changed `POSTGRES_PASSWORD` / `POSTGRES_DB` but Postgres ignores it | those are read only on **first** init; the existing volume already has a database | `docker compose down -v`, then `up -d` |
| counters didn't reset | `down` keeps volumes | `down -v` |
| `curl: (52) Empty reply` right after `up` | backend still connecting | wait 2–3 s, retry |

---

## 9. Clean up

```bash
docker compose down -v                 # containers + network + volumes
docker rmi ecommerce-backend           # the image Compose built
docker rmi postgres:16 redis           # optional
```
