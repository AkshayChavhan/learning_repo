# Networking in Docker Compose

Compose does the networking for you. `docker compose up` creates **one user-defined bridge
network** and puts every service on it. So services reach each other **by service name**:
the app connects to `db:5432`, not to an IP. You almost never need to touch this.

---

## 1. What happens on `docker compose up`

```yaml
name: ecommerce
services:
  web:
    build: .
  db:
    image: postgres:16
```

| Step | What Compose does |
|---|---|
| 1 | creates a network called **`ecommerce_default`** (project name + `_default`), driver bridge |
| 2 | creates a container from `web` and joins it to that network |
| 3 | creates a container from `db` and joins it to the same network |

```bash
docker network ls          # before: no ecommerce network
docker compose up -d
docker network ls
```

```text
NETWORK ID     NAME                DRIVER    SCOPE
...            ecommerce_default   bridge    local     ← made by Compose
```

It's exactly the **user-defined bridge** from note 235. Same rules apply.

---

## 2. Talk by name

Because it's a user-defined bridge, every container can look up every other **by service
name**. Compose keeps the phone book.

```text
   ecommerce_default
   ├── web    ──── "connect to db:5432" ────►  db
   └── db                                      (Compose resolves "db" to its IP)
```

In the app's config:

```text
postgres://postgres:postgres@db:5432/postgres
                             ^^
                     the service name, not an IP, not localhost
```

| From inside a Compose container | Use |
|---|---|
| reach Postgres | `db:5432` |
| reach Redis | `redis:6379` |
| reach the app | `web:8000` |

Spiderman pinged Ironman by name. Here `web` calls `db` by name. Same thing.

> **Key idea:** the name on the left of a service block (`db:`, `redis:`) **is** its
> hostname inside the network.

---

## 3. Your own networks (optional)

You can define networks and choose who joins which. Only containers on the **same**
network can talk.

```yaml
services:
  web:
    image: myapp
    networks:
      - frontend
      - backend          # web is on both

  db:
    image: postgres:16
    networks:
      - backend          # db is only on backend

  proxy:
    image: nginx
    networks:
      - frontend         # proxy is only on frontend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

```text
   frontend: proxy ◄──► web
   backend:          web ◄──► db
   proxy ✗ db   (not on a shared network)
```

| Use this when | |
|---|---|
| you want the database unreachable from the public-facing layer | put db on `backend` only |
| you're mirroring a real production layout | frontend / backend split |
| otherwise | **don't bother**. One default network does the job |

Also in the docs: `links` (legacy, avoid) and multi-host networking with overlay (advanced).

---

## Remember

| Term | One line |
|---|---|
| **`<project>_default`** | the bridge network Compose creates on `up` |
| **every service joins it** | automatically |
| **service name = hostname** | `db`, `redis`, `web` resolve to the right container |
| **connection strings** | use the service name, never `localhost` or an IP |
| **`networks:`** | optional; define your own and assign services to them |
| **same network = can talk** | different networks = cannot |
| **usually** | leave networking alone; the default is what you want |

> **If someone asks in an interview:** "How do Compose services find each other?" Compose
> creates a user-defined bridge network per project and attaches every service to it.
> Docker's built-in DNS resolves each **service name** to its container, so services connect
> with hostnames like `db` or `redis` instead of IPs. You can define extra networks to
> isolate groups of services.
