# Docker Compose — Your Whole Infrastructure in One File

Your app needs Postgres and Redis. Instead of installing them on every developer's laptop,
you write **one file** that says "I need these containers, with these versions, these
settings, these ports". Then `docker compose up` starts all of them, and
`docker compose down` removes all of them.

---

## 1. The problem

The TypeScript app now connects to Redis and Postgres on startup. Without them:

```bash
npm start
```

```text
Error: connection closed            ← no Redis, no Postgres, app dies
```

| Fix without Compose | Why it hurts |
|---|---|
| install Postgres + Redis on your Mac | takes space, you don't want them as system services |
| tell all 10 developers to install the same | everyone must pick the **same version** by hand |
| a new dev joins next year | you must say "install Postgres 14, not 16" and hope they do |

Same "works on my machine" problem from note 219, now for databases.

---

## 2. The fix: docker-compose.yml

One file at the project root, **exactly** this name: `docker-compose.yml`.

```yaml
name: ecommerce                      # friendly name; also names the network

services:
  db:                                # service name, you choose it
    image: postgres:16               # docker run postgres:16
    container_name: postgres         # --name postgres
    environment:                     # -e ...
      POSTGRES_PASSWORD: postgres
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
    ports:
      - "5431:5432"                  # -p 5431:5432   host:container

  redis:
    image: redis
    container_name: redis
    ports:
      - "6379:6379"
    depends_on:
      - db                           # start only after db is up
```

Every line is a `docker run` flag you already know, written in YAML:

| Compose | docker run |
|---|---|
| `image: postgres:16` | `docker run postgres:16` |
| `container_name: postgres` | `--name postgres` |
| `environment:` | `-e POSTGRES_PASSWORD=postgres` |
| `ports: - "5431:5432"` | `-p 5431:5432` |
| `depends_on: - db` | start order |

Which env vars and which port? Look at the image's page on Docker Hub. Postgres documents
`POSTGRES_PASSWORD`, `POSTGRES_USER`, `POSTGRES_DB` and listens on **5432**. Redis listens
on **6379**.

---

## 3. The three commands

```bash
docker compose up        # start everything, logs in your terminal. Ctrl+C stops it
docker compose up -d     # start everything in the background
docker compose down      # stop AND remove every container in the file
```

```text
$ docker compose up -d
[+] Running 3/3
 ✔ Network ecommerce_default  Created
 ✔ Container postgres         Started
 ✔ Container redis            Started
```

Docker Desktop → Containers shows an **ecommerce** stack with both containers inside.

### Then run the app on your Mac

```bash
npm run build && npm start
```

```text
Postgres connected
Redis connected
```

The app connects to `localhost:5431` and `localhost:6379`, which are the published ports.
Stop the stack with `docker compose down` and the app fails again. Bring it back with
`docker compose up -d`.

---

## 4. What a new developer does now

```bash
git clone <repo>
docker compose up -d
npm install && npm run build && npm start
```

No Postgres install, no Redis install, no version questions. The versions are **in the
file**. Add MongoDB tomorrow? Add a service block. Everyone gets it on the next `up`.

---

## 5. Compose makes a network (preview)

`docker compose up` creates a **user-defined bridge** (note 235) and puts every service on
it. So `redis` can reach the database just by saying `db`, like Spiderman pinging Ironman
by name.

```text
   ecommerce_default network
   ├── db      (postgres)   ◄── reachable as "db"
   ├── redis                ◄── reachable as "redis"
   └── (your app, next lecture)
```

Right now the app runs **outside**, on your Mac. That's the only reason the `ports:` lines
exist. Once the app also runs inside Compose, Postgres and Redis won't need published
ports at all. Next lecture.

---

## Remember

| Term | One line |
|---|---|
| **docker-compose.yml** | one file listing every container your project needs |
| **service** | one container definition inside the file (`db`, `redis`) |
| **`docker compose up -d`** | start all services in the background |
| **`docker compose down`** | stop and remove all of them |
| **image / environment / ports** | the same things as `docker run` flags |
| **`depends_on`** | start this service after that one |
| **versions in the file** | every developer gets the same Postgres 16 |
| **built-in network** | services reach each other by service name |

> **If someone asks in an interview:** "What is Docker Compose for?" Defining a
> multi-container setup in one YAML file (images, env vars, ports, dependencies) and
> starting or stopping it with one command. It gives every developer an identical
> environment and puts all services on a shared network where they resolve each other by
> name.
