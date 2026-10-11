# Port Mapping — Why `localhost:8080` Doesn't Just Work

This resolves the cliffhanger from the Dockerfile lecture: the app runs
fine *inside* the container, but the host machine still can't reach it
without being told how.

---

## 🟢 Beginner — containers are isolated, like a separate machine

If a friend runs a server on port 8000 on *their* laptop, you can't
reach it on yours just by visiting `localhost:8000` - it's running on
a different machine. A Docker container is the same kind of separate
machine, even though it's running on your own computer.

```text
   your computer ("the host machine")
        │
        │   (isolated boundary)
        ▼
   container  ──► app listening on port 8080
```

Port 8080 being open *inside* the container says nothing about whether
port 8080 is open on the host. By default, it isn't.

---

## 🟡 Intermediate — `-p <host port>:<container port>`

```bash
docker run -d -p 3000:8080 --name my-app my-app npm start
```

| Side | What it means |
|---|---|
| `3000` (first, before the colon) | the port **you** pick on the host |
| `8080` (second, after the colon) | the port the app **actually listens on inside the container** - fixed by the code, not your choice |

**Verified live:** with `-p 3000:8080`, `curl http://localhost:3000/`
returns the real health response. `curl http://localhost:8080/` on the
host returns nothing - port 8080 was never opened on the host, only 3000 was.

---

## 🔴 Expert — one side is flexible, the other is not

**The host-side port is arbitrary.** Pick 3000, 4000, 9999 - anything
free on your machine works, because it's just how *you* choose to
expose the container locally.

**The container-side port is not arbitrary.** It must match exactly
what the app listens on inside the container. Get it wrong, and nothing
works - not a wrong answer, a dead connection:

```bash
docker run -d -p 3000:9000 --name broken my-app npm start
curl http://localhost:3000/        # connection fails outright - nothing
                                    # inside the container listens on 9000
```

Verified live: this returns `HTTP status 000` - curl can't even
establish a connection, despite the container running and the app
working fine internally. The mismatch is entirely on the container
side of the mapping.

**Multiple ports map with multiple `-p` flags:**

```bash
docker run -p 3000:8080 -p 3001:9000 -p 3002:8001 my-app
```

Each `-p host:container` pair is independent - map as many as the app
actually exposes.

**Visual confirmation:** Docker Desktop's container view shows the
exact host→container port mapping for any running container.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Host machine** | the actual computer running Docker - isolated from containers by default |
| **`-p host:container`** | opens a host port and forwards it to a specific port inside the container |
| **Host-side port** | arbitrary - pick anything free |
| **Container-side port** | must match exactly what the app listens on inside the container |
| **Multiple `-p` flags** | map as many container ports to host ports as needed, in one `docker run` |
