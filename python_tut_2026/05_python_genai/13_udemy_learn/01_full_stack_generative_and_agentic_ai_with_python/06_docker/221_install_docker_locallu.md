# Installing Docker Locally

Installing Docker means installing the **Docker engine**. On Mac and Windows it comes
bundled with **Docker Desktop**, a GUI that also runs the engine for you. On Linux you
install the engine directly with a few commands. Verify with `docker version`.

---

## 🟢 Beginner — pick your platform

Official page: **docs.docker.com** → *Install Docker Engine*. Every platform is supported.

| Platform | What you do |
|---|---|
| **macOS** | download Docker Desktop. Pick **Apple Silicon** (M-series) or **Intel** |
| **Windows** | download Docker Desktop. Pick **x86-64** or **ARM** |
| **Linux (Ubuntu)** | follow the docs page for Ubuntu: a short list of `apt` commands. Run them in order |

Mac / Windows: download → run installer → open Docker Desktop. It will ask you to sign in.
**Skip it.** Signing in is optional.

```text
  Docker Desktop (GUI)
  ├── Containers   ← empty on a fresh install
  ├── Images       ← empty on a fresh install
  └── Docker engine running in the background   ← this is the actual install
```

---

## 🟡 Intermediate — verify it works

Docker Desktop must be **running** (whale icon in the menu bar / tray) before any
`docker` command works.

```bash
docker version
```

```text
Client:
 Version:    27.x.x
 ...
Server: Docker Desktop
 Engine:
  Version:   27.x.x
 ...
```

| Output | Meaning |
|---|---|
| Client **and** Server sections | ✅ installed and engine running |
| Client only, `Cannot connect to the Docker daemon` | engine not running. Start Docker Desktop |
| `command not found: docker` | install didn't add `docker` to PATH, or isn't installed |

### First run, for fun

```bash
docker run -it ubuntu
```

```text
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
...
root@1fdd9c3a7b21:/#          ← you're inside Ubuntu now
```

| What happened | |
|---|---|
| image not found locally | Docker **pulled** it from **hub.docker.com**, the public image registry |
| a container started | Docker Desktop → Containers now shows one running |
| the prompt changed | `root@<container-id>` means your terminal is inside the container |

Try `ls`, `cd /home`, any Linux command. `Ctrl+D` to exit.

---

## 🔴 Expert — what you actually installed

| Piece | Role |
|---|---|
| **Docker engine** (daemon) | the thing that builds and runs containers. The only hard requirement |
| **Docker CLI** (`docker`) | the client. Sends commands to the engine |
| **Docker Desktop** | GUI + bundled engine for Mac / Windows. On Mac it also runs the small Linux VM that supplies the kernel |
| **Docker Hub** | cloud registry images are pulled from by default |

```text
  docker run -it ubuntu
       │
       ▼
  docker CLI ──► Docker engine ──► image local? no ──► pull from hub.docker.com
                                        │
                                        ▼
                                  start container
```

On Linux there is no Desktop layer. The CLI talks straight to the engine on the host kernel.

---

## Gotchas & best practices

- **Engine not running = every command fails.** Open Docker Desktop first.
- **Match your chip.** Apple Silicon vs Intel, x86 vs ARM. The wrong build won't run.
- **Skip the sign-in.** You don't need an account to pull public images.
- **Linux: run the docs commands in order.** Adding the repo key before installing matters.
- **Stuck?** The course has a Discord server linked in the video description.
- **Next:** image vs container, then the Docker CLI.

> **Interview angle:** *"What does Docker Desktop install?"* The Docker engine (daemon)
> plus the CLI client and a GUI. On Mac and Windows it also provides the Linux kernel
> containers need, via a lightweight VM. On Linux you install the engine directly.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Docker engine** | the daemon that runs containers; the actual install |
| **Docker Desktop** | Mac / Windows app bundling the engine with a GUI |
| **`docker version`** | verify install; Client + Server sections = working |
| **Docker Hub** | hub.docker.com, where images are pulled from |
| **`docker run -it ubuntu`** | pull the Ubuntu image and open a shell in a new container |
