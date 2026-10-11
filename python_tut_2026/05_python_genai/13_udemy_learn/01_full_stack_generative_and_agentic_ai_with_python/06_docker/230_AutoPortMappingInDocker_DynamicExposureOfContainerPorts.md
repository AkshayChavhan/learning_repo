# EXPOSE, -P, --rm, -d — The CLI Flags That Actually Matter

Four small things that solve four real annoyances: manually mapping
every port, containers piling up uncleaned, and a terminal stuck
attached to a running container.

---

## 🟢 Beginner — `EXPOSE` is documentation, not a port-opener

```dockerfile
EXPOSE 8080
```

**Verified live:** adding this line and running the container with
*no* `-p` or `-P` flag - `curl http://localhost:8080/` fails outright
(connection refused), even though the app is running perfectly inside.
`EXPOSE` doesn't open anything. It's metadata - visible later via:

```bash
docker inspect my-app --format '{{.Config.ExposedPorts}}'
# map[8080/tcp:{}]
```

It tells the next developer (or a tool) *which* ports this image is
designed to use - nothing more.

---

## 🟡 Intermediate — `-P` (capital): auto-map every exposed port

```bash
docker run -d -P --name my-app my-app npm start
docker ps --filter name=my-app --format "{{.Ports}}"
# 0.0.0.0:55000->8080/tcp
```

Docker picked a **random free host port** (55000 here) and mapped it
to the `EXPOSE`d container port automatically. Verified: that random
port actually works -`curl http://localhost:55000/` returns the real
health response. No need to pick a host port yourself.

**A whole range exposes and maps just as easily:**

```dockerfile
EXPOSE 8080-8082
```

```bash
docker run -d -P my-app
# 0.0.0.0:55002->8080/tcp, 0.0.0.0:55003->8081/tcp, 0.0.0.0:55004->8082/tcp
```

Three `EXPOSE`d ports, three random host ports, all mapped in one `-P`.

---

## 🔴 Expert — `--rm` and `-d`: two problems most tutorials skip

**The problem:** stopped containers don't disappear on their own.
`docker ps -a` accumulates every container you've ever run until you
clean them up by hand.

```bash
docker run -d --rm --name my-app my-app npm start
docker stop my-app
docker ps -a --filter name=my-app          # empty - it's really gone
```

**Verified live:** the container is listed while running, and
completely absent from `docker ps -a` the moment it's stopped - `--rm`
deletes the container (and its anonymous volumes) automatically on exit.

**The second problem:** running interactively blocks your terminal -
you can't do anything else in that window until the container exits.

```bash
docker run -d my-app npm start
# prints just a container ID, control returns immediately
```

`-d` (detached) runs the container in the background and hands your
terminal straight back. This is the normal way to run anything on a
real server, where you don't want one container occupying your only
session.

**Combined, this is the practical default for running something
long-lived:**

```bash
docker run -d -P --rm --name my-app my-app npm start
```

---

## Quick recap

| Term | One-line definition |
|---|---|
| **`EXPOSE <port>`** | documentation only - does not open any port by itself |
| **`-P`** | auto-maps every `EXPOSE`d port to a random free host port |
| **`EXPOSE <start>-<end>`** | exposes a whole range of ports at once |
| **`--rm`** | deletes the container automatically when it exits |
| **`-d`** | runs detached - background, returns your terminal immediately |
