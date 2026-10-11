# Intro to the Docker CLI

The **Docker engine** (daemon) manages every image and container. It exposes an **API**.
Docker Desktop's UI and the `docker` command are both just **clients** of that API. The
UI isn't on a production server, so you learn the CLI.

---

## Topic at a glance

```text
        Docker engine                        Listing
            \                                  /
  daemon manages all ──\       docker ps ──/
                        \                  /
  exposes an API ───────\   docker images ─/
                          ►   DOCKER CLI
  docker run ───────────/      docker version / info ──\
                        /                               \
  --help everywhere ───/        engine stopped = error ──\
            /                                              \
       Commands                                        System
```

---

## 🟢 Beginner — who talks to whom

```text
  docker run -it ubuntu  ──┐
  (CLI, terminal)          ├──► DOCKER ENGINE API ──► creates / deletes / pulls / lists
  Docker Desktop UI     ──┘      (daemon, the "magic")
```

| Client | Where you have it | Why learn it |
|---|---|---|
| **Docker Desktop UI** | your laptop only | handy for dev, shows the same data |
| **`docker` CLI** | laptop **and** any server over SSH | the only thing available in production |

Proof: `docker ps` output and the Desktop's Containers tab show the **same id and name**.
Same API, two views.

```bash
docker            # no args → lists every command with a one-line description
docker ps --help  # every command has --help
```

---

## 🟡 Intermediate — the first commands

### Containers

| Command | Shows |
|---|---|
| `docker ps` | **running** containers only |
| `docker ps -a` / `docker ps --all` | all containers, including **exited** ones |

```text
$ docker ps
CONTAINER ID   IMAGE    COMMAND       CREATED         STATUS         PORTS   NAMES
ece05a1b2c3d   ubuntu   "/bin/bash"   7 seconds ago   Up 6 seconds           quirky_moore
```

Empty table = nothing running. Exit a container with `Ctrl+D` and it moves to `-a` only.

**Aliases**, all identical:

```bash
docker ps
docker container ls
docker container list
docker container ps
```

`docker ps` is the shorthand because listing containers is the most common thing you do.

### Images

| Command | Shows |
|---|---|
| `docker images` | images downloaded to this machine, with size |
| `docker images -a` | include intermediate (build) layers |

```text
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
ubuntu       latest    3f2a9c1b7d4e   2 weeks ago    78MB
busybox      latest    9e4f5a6b7c8d   3 weeks ago    4.3MB
```

Aliases: `docker image ls`, `docker image list`. Useful flags: `--digests`, `--format`,
`-q` (ids only), `--tree`.

### System

| Command | What it tells you |
|---|---|
| `docker version` | client + server (engine) versions. Verify install |
| `docker info` | system-wide: image count, running / stopped / total containers, storage driver, OS, CPUs, memory |
| `docker login` / `docker logout` | Docker Hub auth. Only needed for private or push |

---

## 🔴 Expert — the daemon and the socket

Inside `docker info` you'll see a line like:

```text
 Docker Root Dir: /var/lib/docker
 ...
 unix:///var/run/docker.sock
```

That **Unix socket** is where the daemon listens. Every CLI command and every UI click is
a request sent over it. Later topic, but it explains everything.

### Engine stopped = nothing works

```text
$ docker run -it ubuntu
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

| Platform | Start the engine |
|---|---|
| Mac / Windows | open **Docker Desktop** (pausing it may auto-resume; quitting fully stops it) |
| Linux | `sudo systemctl start docker` |

### Command families

The CLI is organized as `docker <object> <verb>`. The shorthands are just aliases:

| Shorthand | Full form | Object |
|---|---|---|
| `docker ps` | `docker container ls` | containers |
| `docker images` | `docker image ls` | images |
| `docker run` | `docker container run` | containers |
| `docker build` | `docker image build` | images (Dockerfile lecture) |
| `docker exec` | `docker container exec` | run a command in a running container (later) |

---

## Gotchas & best practices

- **`docker ps` hides exited containers.** Use `-a` when something "disappeared".
- **Read `--help`.** The instructor literally reads the docs on screen. So can you.
- **UI is optional, CLI is not.** Servers have no Docker Desktop.
- **"Cannot connect to the daemon"** means the engine is off, not that Docker is broken.
- **Next:** `docker run` in depth.

> **Interview angle:** *"What is the Docker engine and how does the CLI relate to it?"*
> The engine is a daemon that manages images and containers and exposes a REST API over a
> Unix socket. The `docker` CLI and Docker Desktop are both clients of that API. That's why
> the CLI works identically on a laptop and on a headless server.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Docker engine / daemon** | background process that manages containers and images |
| **CLI vs UI** | two clients of the same engine API; only the CLI exists on servers |
| **`docker ps` / `-a`** | running containers / all containers |
| **`docker images`** | images on this machine |
| **`docker version`** | client + engine versions |
| **`docker info`** | system-wide stats and config |
| **`docker.sock`** | the Unix socket the daemon listens on |
| **`systemctl start docker`** | start the engine on Linux; Mac/Windows use Docker Desktop |
