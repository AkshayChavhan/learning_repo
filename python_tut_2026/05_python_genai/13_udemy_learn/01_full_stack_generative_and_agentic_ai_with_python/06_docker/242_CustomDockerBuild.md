# Building Your App Inside Docker Compose

So far Postgres and Redis ran in Compose while the app ran on your Mac. Now the app runs
in Compose too, built from your Dockerfile with `build: .`. Once it's inside the network,
it connects to `redis` and `db` **by name**, and the databases no longer need published
ports.

---

## 1. Two ways to put your app in Compose

| Way | In the file | Downside |
|---|---|---|
| **A. Use a published image** | `image: <username>/backend-app` | every code change = build, push to Docker Hub, pull. Overkill for dev |
| **B. Build from the Dockerfile** | `build: .` | none for dev. Compose builds the image locally |

```yaml
  backend:
    build: .                       # ← B. read ./Dockerfile, build an image, run it
    container_name: backend
    ports:
      - "8000:8000"
```

`build: .` means "the Dockerfile is in this folder". Longer form if it's elsewhere:

```yaml
    build:
      context: .
      dockerfile: Dockerfile
```

---

## 2. First run: it breaks

```bash
docker compose up
```

```text
backend  | Error: connect ECONNREFUSED 127.0.0.1:6379     ← can't reach Redis
```

### Why

```text
   ecommerce_default network
   ├── backend   "connect to localhost:6379"  ──► looks INSIDE ITSELF. Nothing there.
   ├── redis     (listening on 6379, in its own container)
   └── db        (listening on 5432, in its own container)
```

`localhost` inside a container means **that container**. The app worked on your Mac
because `localhost` was your Mac, where the published ports were. Inside Compose, Redis is
a **different container**.

---

## 3. Fix 1: connect by service name

| Before (app on Mac) | After (app in Compose) |
|---|---|
| `localhost:6379` | `redis:6379` |
| `localhost:5431` | `db:5432` |

```text
redis://redis:6379
postgres://postgres:postgres@db:5432/postgres
```

Two things changed for Postgres:

| Change | Why |
|---|---|
| host `localhost` → `db` | service name resolves inside the network (note 240) |
| port `5431` → `5432` | 5431 was the **published** host port. Inside the network you talk to the container's **real** port |

---

## 4. Fix 2: rebuild after code changes

```bash
docker compose down
docker compose up --build       # rebuild the backend image, then start
```

```text
backend  | Redis connected
backend  | Postgres connected
```

Compose **caches** the image. Change code, run plain `up`, and you get the **old** image
with the old `localhost`. The instructor hit this twice. `--build` forces a rebuild.

---

## 5. Remove the ports the databases don't need

Now that the app is inside, nothing on your Mac needs to reach Postgres or Redis.

```yaml
services:
  backend:
    build: .
    container_name: backend
    ports:
      - "8000:8000"              # ✅ keep: the world needs the app

  db:
    image: postgres:16
    container_name: postgres
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
    # ports: removed            # ❌ nobody outside should reach the database
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis
    container_name: redis
    # ports: removed            # ❌ same
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

```bash
docker compose up --build
curl localhost:8000            # ✅ app answers
```

```text
   INTERNET ──► localhost:8000 ──► backend ──► db:5432     (private)
                                          └──► redis:6379  (private)
```

Only the app is reachable from outside. Postgres and Redis are invisible to the world and
reachable only by containers on the same network. That's the security win from note 234.

---

## Remember

| Term | One line |
|---|---|
| **`build: .`** | build the service's image from the local Dockerfile |
| **`image:`** | use a prebuilt image instead (from Docker Hub) |
| **`localhost` inside a container** | means that container itself, not your Mac |
| **connect by service name** | `redis:6379`, `db:5432` |
| **container port, not host port** | inside the network use 5432, not the published 5431 |
| **`docker compose up --build`** | rebuild after code changes; plain `up` reuses the old image |
| **drop `ports:` on databases** | expose only the app |

> **If someone asks in an interview:** "Why can't my app in Compose reach Redis on
> localhost?" Each container has its own `localhost`. Services on the Compose network reach
> each other by **service name** on the **container's** port. Then you publish only the
> public-facing service and leave databases unexposed.
