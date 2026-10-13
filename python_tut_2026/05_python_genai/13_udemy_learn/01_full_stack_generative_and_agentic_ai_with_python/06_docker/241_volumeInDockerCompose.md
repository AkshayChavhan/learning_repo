# Volumes in Docker Compose

`docker compose down` removes the containers **and their data**. Your Postgres tables are
gone. To keep them, declare a **named volume** in the file and mount it where the database
writes its files. Containers come and go on every `up` / `down`; the volume stays.

---

## 1. The problem

```bash
docker compose up -d      # postgres starts, you insert rows
docker compose down       # containers removed → rows gone
docker compose up -d      # fresh, empty postgres
```

Compose containers are still just containers (note 222): their files die with them.

---

## 2. The fix: two additions to the file

```yaml
name: ecommerce

services:
  db:
    image: postgres:16
    container_name: postgres
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
    ports:
      - "5431:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data      # ① mount it here

  redis:
    image: redis
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data                            # ① mount it here

volumes:                                            # ② declare the volumes
  postgres_data:
  redis_data:
```

| Part | Meaning |
|---|---|
| top-level `volumes:` with `postgres_data:` | "Compose, create a named volume called this". No settings needed |
| `volumes:` inside a service | "mount that volume at this path inside the container" |
| `postgres_data:/var/lib/postgresql/data` | same `name:/path` shape as `-v` in note 238 |

---

## 3. Where does each image keep its data?

The container path isn't guessed. Each image's **Docker Hub page** says where it writes:

| Image | Data lives at | Mount line |
|---|---|---|
| `postgres` | `/var/lib/postgresql/data` | `postgres_data:/var/lib/postgresql/data` |
| `redis` | `/data` | `redis_data:/data` |
| `mongo` | `/data/db` | `mongo_data:/data/db` |
| `mysql` | `/var/lib/mysql` | `mysql_data:/var/lib/mysql` |

Mount the wrong path and the database still writes inside the container, and you lose it.

---

## 4. Prove it survives

```bash
docker compose up -d
```

```text
 ✔ Network ecommerce_default        Created
 ✔ Volume  ecommerce_postgres_data  Created      ← named <project>_<volume>
 ✔ Volume  ecommerce_redis_data     Created
 ✔ Container postgres               Started
 ✔ Container redis                  Started
```

```bash
docker compose down
```

```text
 ✔ Container redis            Removed
 ✔ Container postgres         Removed
 ✔ Network ecommerce_default  Removed
                                            ← no "Volume ... Removed" line
```

```bash
docker volume ls | grep postgres
```

```text
local     ecommerce_postgres_data            ← still here
```

Next `docker compose up -d` mounts the same volume. Your tables are back.

```text
   up ──► container writes to /var/lib/postgresql/data ──► ecommerce_postgres_data
   down ──► container removed                               volume untouched
   up ──► new container, same volume ──► same data
```

---

## 5. When you really want a clean slate

```bash
docker compose down -v      # also delete the volumes declared in the file
```

Use it when you want to reset the database. Otherwise never add `-v`.

---

## Remember

| Term | One line |
|---|---|
| **`down` deletes container data** | by default nothing persists |
| **top-level `volumes:`** | declare named volumes, one per database |
| **service `volumes:`** | `name:/container/path`, mount it where the image writes |
| **data path** | read it from the image's Docker Hub page |
| **`<project>_<volume>`** | the real volume name Compose creates |
| **`down` keeps volumes** | `down -v` deletes them |

> **If someone asks in an interview:** "How do you persist database data in Compose?"
> Declare a named volume under the top-level `volumes:` key and mount it in the service at
> the path where the image stores its data, e.g. `/var/lib/postgresql/data` for Postgres.
> `docker compose down` removes containers and the network but leaves volumes, so the data
> is there on the next `up`.
