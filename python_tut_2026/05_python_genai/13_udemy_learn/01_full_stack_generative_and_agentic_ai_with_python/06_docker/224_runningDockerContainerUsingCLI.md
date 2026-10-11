# docker run -it — What's Actually Happening

`docker run` is one command doing two things: create a container from an
image, then run it. The flags control how you can talk to it once it's running.

---

## 🟢 Beginner — the shape of the command

```bash
docker run [options] <image> [command]
```

| Part | Example | What it is |
|---|---|---|
| `run` | - | create **and** run a new container from an image |
| options | `-i`, `-t` | how you connect to the running container |
| image | `ubuntu`, `alpine` | the last positional argument - what to run |

---

## 🟡 Intermediate — `-i` vs `-t` vs `-it`, precisely

This is the part everyone glosses over. They're two separate flags doing
two separate things:

| Flag | Full name | Does |
|---|---|---|
| `-i` | **interactive** | keeps **stdin** open - you *can* send input |
| `-t` | **tty** | allocates a pseudo-terminal - connects your actual terminal session to the one inside the container |

```text
docker run ubuntu           →  starts, then you're immediately disconnected -
                                no stdin open, nothing to type into

docker run -i ubuntu        →  stdin is open - you CAN type commands and get
                                output back, but it's not a real terminal session

docker run -i -t ubuntu     →  (usually written -it) a full, real interactive
docker run -it ubuntu          shell - exactly like SSH-ing into a normal machine
```

**`-i` alone is not enough for a normal shell experience.** You need
both - `-i` for the input, `-t` for the actual terminal. That's why
`-it` is the combination everyone actually uses.

---

## 🔴 Expert — where images come from, and checking what's on your machine

**Image resolution is local-first.** `docker run <image>` checks your
machine before touching the network:

```text
  docker run -it ubuntu
          │
          ▼
  is "ubuntu" already pulled locally?
     │                    │
    yes                   no
     │                    │
     ▼                    ▼
  run it directly    pull it first (one-time), THEN run it
```

Run the same command again and there's no re-pull - it's already there.

```bash
docker pull <image>      # pre-pull an image WITHOUT running a container
docker ps -a              # list ALL containers - including stopped ones
docker images             # list every image currently on this machine
```

**Docker Hub (hub.docker.com)** is the default public registry - "like
GitHub, but for Docker images." This is where `ubuntu`, `alpine`, and
`busybox` actually come from. It hosts thousands of official images,
including ones for most major tools: TensorFlow, PyTorch, LangChain,
Ollama, Nginx, Memcache, and more. Each image page lists its available
**tags** - the way to pin a specific version instead of always pulling
the latest.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **`docker run`** | create + run a container from an image, in one command |
| **`-i`** | keeps stdin open - you can send input |
| **`-t`** | allocates a pseudo-terminal - a real interactive shell |
| **`-it`** | both together - the combination for a normal-feeling shell session |
| **`docker pull`** | fetch an image without running it |
| **Docker Hub** | the default public registry - thousands of official images, versioned by tag |
