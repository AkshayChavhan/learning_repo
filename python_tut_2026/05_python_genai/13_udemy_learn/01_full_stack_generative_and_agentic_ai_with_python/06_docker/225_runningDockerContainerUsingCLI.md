# Docker CLI — Command Reference by Object

Every `docker` command you'll use daily, grouped by **what it acts on** (Image, Container,
System) and **what you want to do** (run, delete, rename…). Click a topic below to expand
it, then click an action to jump to that command. Each section ends with a link back here.

---

## Navigation

<details>
<summary><b>🖼️ Image</b> — the template (install, list, run, rename, delete)</summary>

| Action | Jump to |
|---|---|
| Install / download | [Image pull](#image-pull) |
| List what's installed | [Image list](#image-list) |
| Run (creates a container) | [Container run](#container-run) |
| Rename / version tag | [Image tag](#image-tag) |
| Search Docker Hub | [Image search](#image-search) |
| Delete | [Image delete](#image-delete) |
| Clean up unused | [Image prune](#image-prune) |

</details>

<details>
<summary><b>📦 Container</b> — the running instance (run, stop, enter, rename, delete)</summary>

| Action | Jump to |
|---|---|
| Run / create | [Container run](#container-run) |
| Run flags: name, background, ports, env, volumes | [Container run flags](#container-run-flags) |
| List | [Container list](#container-list) |
| Stop / start / restart / kill | [Container stop and start](#container-stop-and-start) |
| Rename | [Container rename](#container-rename) |
| Enter a running one (shell) | [Container exec](#container-exec) |
| See output / logs | [Container logs](#container-logs) |
| Inspect, resources, processes | [Container inspect](#container-inspect) |
| Copy files in / out | [Container copy](#container-copy) |
| Delete | [Container delete](#container-delete) |
| Clean up stopped | [Container prune](#container-prune) |

</details>

<details>
<summary><b>⚙️ System</b> — the engine itself (version, info, disk, clean everything)</summary>

| Action | Jump to |
|---|---|
| Check install / versions | [System version and info](#system-version-and-info) |
| Disk usage | [System disk](#system-disk) |
| Delete everything unused | [System prune](#system-prune) |
| Engine not running | [System engine](#system-engine) |
| Read the prompt (am I inside a container?) | [Where am I](#where-am-i) |
| Mistakes we hit | [Common mistakes](#common-mistakes) |

</details>

<details>
<summary><b>🔁 Full lifecycle</b> — pull → run → exec → stop → start → rm, end to end</summary>

[Lifecycle walkthrough](#lifecycle-walkthrough)

</details>

---

## Basics first

```bash
docker <object> <action> [flags] [target]
```

| Part | Example | Meaning |
|---|---|---|
| object | `image`, `container`, `system` | what you act on (often omitted via shorthand) |
| action | `run`, `ls`, `rm`, `stop` | what to do |
| target | `ubuntu`, `mybox`, `085f` | image name, container **name** or **id** (first few chars are enough) |

Shorthands you'll see everywhere: `docker ps` = `docker container ls`,
`docker images` = `docker image ls`, `docker run` = `docker container run`.

### Where am I

```text
rtlecl910010@RTLECs-MacBook-Air ~ %    ← your Mac. docker commands work here
root@085f32d348da:/#                    ← INSIDE a container. "docker" doesn't exist here
```

Inside a container, run Linux commands. Run `docker` commands on your Mac, in a second
terminal tab if the first is inside a container. `Ctrl+D` or `exit` leaves the container.

### Common mistakes

| What happened | Why | Fix |
|---|---|---|
| `docker run -it ubantu` → *pull access denied… repository does not exist* | typo. Docker says "access denied" for **any** unknown name | spell it `ubuntu`. Don't `docker login` for this |
| `root@…:/# docker ps` → *bash: docker: command not found* | you're inside the container | `Ctrl+D` out, or use another tab |
| ran `docker run -it ubuntu` 5 times, now 5 containers | `run` creates a **new** container every time | use `docker start -ai <name>` to resume, `--rm` for throwaways |

[⬆ back to menu](#navigation)

---

# 🖼️ Image commands

### Image pull

**Meaning:** download an image from Docker Hub to your machine **without** running it.
`docker run` does this automatically if the image is missing.

```bash
docker pull ubuntu            # latest tag
docker pull ubuntu:22.04      # a specific version (tag)
docker pull python:3.12-slim
```

```text
latest: Pulling from library/ubuntu
...
Status: Downloaded newer image for ubuntu:latest
```

| Tip | |
|---|---|
| No tag = `latest` | `latest` changes over time. Pin a tag in real projects |
| Already pulled? | second pull is instant, nothing re-downloads |

[⬆ back to menu](#navigation)

### Image list

**Meaning:** show every image on this machine with its size.

```bash
docker images
docker image ls          # same
docker images -q         # ids only (useful in scripts)
docker images -a         # include intermediate build layers
```

```text
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
ubuntu       latest    3f2a9c1b7d4e   2 weeks ago    78MB
busybox      latest    9e4f5a6b7c8d   3 weeks ago    4.3MB
```

[⬆ back to menu](#navigation)

### Image tag

**Meaning:** give an image another name or version label. Used before pushing to a
registry, or to "rename" an image.

```bash
docker tag ubuntu:latest myubuntu:v1
docker images                           # both names, SAME image id
```

An image can have many names. `tag` adds one, it doesn't copy anything.

[⬆ back to menu](#navigation)

### Image search

**Meaning:** search Docker Hub from the terminal.

```bash
docker search redis
```

```text
NAME             DESCRIPTION                        STARS   OFFICIAL
redis            Redis is the world's fastest...    13000   [OK]
```

Prefer **OFFICIAL** images. hub.docker.com shows tags and docs for each.

[⬆ back to menu](#navigation)

### Image delete

**Meaning:** remove an image from your machine.

```bash
docker rmi ubuntu
docker image rm ubuntu          # same
docker rmi 3f2a                 # by id
docker rmi -f ubuntu            # force
```

```text
Error response from daemon: conflict: unable to remove repository reference
"ubuntu" (must force) - container 085f32d348da is using its referenced image
```

That error means a **container** still uses the image. Delete the container first
([Container delete](#container-delete)), then the image.

[⬆ back to menu](#navigation)

### Image prune

**Meaning:** delete images nothing uses.

```bash
docker image prune         # dangling (untagged) images only
docker image prune -a      # every image not used by a container
```

[⬆ back to menu](#navigation)

---

# 📦 Container commands

### Container run

**Meaning:** create a **new** container from an image and start it. Pulls the image first
if needed. The most-used command in Docker.

```bash
docker run -it ubuntu              # new container + interactive shell
docker run ubuntu ls /             # run one command, then the container exits
docker run -it ubuntu bash         # explicit shell
```

```text
Unable to find image 'ubuntu:latest' locally     ← only the first time
root@085f32d348da:/#                              ← you're inside
```

| Flag | Meaning |
|---|---|
| `-i` | keep input open |
| `-t` | give me a real terminal |
| `-it` | both: a normal shell experience (details in note 224) |

> `run` = **new** container every time. To get back into one you already made, use
> [Container stop and start](#container-stop-and-start) or [Container exec](#container-exec).

[⬆ back to menu](#navigation)

### Container run flags

**Meaning:** options that shape the container at creation.

```bash
docker run [flags] <image> [command]
```

| Flag | Meaning | Example |
|---|---|---|
| `--name <n>` | pick a name instead of `quirky_moore` | `docker run -it --name mybox ubuntu` |
| `-d` | **detached**: background, prompt comes back | `docker run -d nginx` |
| `--rm` | **auto-delete** when it stops | `docker run -it --rm alpine` |
| `-p host:cont` | **publish a port**: Mac port → container port | `docker run -d -p 8080:80 nginx` |
| `-e KEY=val` | set an **env var** inside | `docker run -e OPENAI_API_KEY=... myapp` |
| `-v host:cont` | **mount a folder**: data survives deletion | `docker run -v $(pwd)/data:/data ubuntu` |
| `-w /path` | working directory inside | `docker run -w /app myapp` |
| `--restart always` | restart if it crashes or Docker restarts | servers |

```bash
docker run -d --name web -p 8080:80 nginx
```

```text
9f1c3e7a2b4d...            ← container id, you're back on your prompt
```

Open `http://localhost:8080` → nginx welcome page. Mac port 8080 → container port 80.

[⬆ back to menu](#navigation)

### Container list

**Meaning:** show containers. By default only **running** ones.

```bash
docker ps                 # running
docker ps -a              # all, including Exited
docker ps -q              # ids only
docker container ls -a    # same as ps -a
```

```text
CONTAINER ID   IMAGE    COMMAND       CREATED          STATUS                     PORTS                  NAMES
9f1c3e7a2b4d   nginx    "nginx -g…"   2 minutes ago    Up 2 minutes               0.0.0.0:8080->80/tcp   web
085f32d348da   ubuntu   "/bin/bash"   10 minutes ago   Exited (0) 3 minutes ago                          mybox
```

| STATUS | Meaning |
|---|---|
| `Up …` | running |
| `Exited (0)` | stopped normally |
| `Exited (1)` or other | stopped with an error, check [logs](#container-logs) |

[⬆ back to menu](#navigation)

### Container stop and start

**Meaning:** stopping keeps the container and its files. Starting resumes it.

| Command | Meaning |
|---|---|
| `docker stop <name>` | graceful stop (SIGTERM, 10 s grace, then kill) |
| `docker start <name>` | start a stopped container, same files |
| `docker start -ai <name>` | start **and** get the shell back |
| `docker restart <name>` | stop + start |
| `docker kill <name>` | immediate, no grace period |
| `docker pause` / `unpause <name>` | freeze / resume processes |

```bash
docker run -it --name mybox ubuntu     # create files inside, then Ctrl+D
docker ps -a                           # mybox: Exited
docker start -ai mybox                 # back inside, files still there
```

```text
  run ──► (running) ──stop──► (exited) ──start──► (running)
```

[⬆ back to menu](#navigation)

### Container rename

**Meaning:** change a container's name. Works on running or stopped containers.

```bash
docker rename quirky_moore mybox
docker ps -a                            # NAMES now shows mybox
```

Names must be unique. If `mybox` exists, delete or rename it first.

[⬆ back to menu](#navigation)

### Container exec

**Meaning:** run a command, usually a shell, **inside a running container** without
stopping it. The safe way to "go inside".

```bash
docker exec -it web bash               # second shell in the running container
docker exec web ls /usr/share/nginx/html   # one command, prints, returns
docker exec -it mybox sh               # alpine/busybox have sh, not bash
```

```text
root@9f1c3e7a2b4d:/#        ← new shell. Ctrl+D leaves, container KEEPS running
```

| `exec` vs `attach` | |
|---|---|
| `docker exec -it X bash` | separate process. `Ctrl+D` leaves only your shell. **Use this** |
| `docker attach X` | connect to the **main** process. `Ctrl+D` **stops** the container |

Container must be **running**. For a stopped one, use `docker start -ai`.

[⬆ back to menu](#navigation)

### Container logs

**Meaning:** the stdout / stderr of the container's main process. Essential for `-d`
containers you can't see.

```bash
docker logs web
docker logs -f web            # follow live, Ctrl+C to stop following
docker logs --tail 50 web     # last 50 lines
docker logs -t web            # with timestamps
```

[⬆ back to menu](#navigation)

### Container inspect

**Meaning:** details, resources and processes of a container.

| Command | Shows | Use when |
|---|---|---|
| `docker inspect <name>` | full JSON: IP, mounts, env, ports, command | debugging config or networking |
| `docker stats` | live CPU / memory per container | "why is my laptop slow" |
| `docker top <name>` | processes inside | |
| `docker port <name>` | port mappings | "which port did I publish" |
| `docker diff <name>` | files changed since the image | "what did I modify" |

```bash
docker inspect web | grep IPAddress
```

[⬆ back to menu](#navigation)

### Container copy

**Meaning:** copy files between your Mac and a container (running or stopped).

```bash
docker cp web:/var/log/nginx/access.log ./access.log     # container → Mac
docker cp ./index.html web:/usr/share/nginx/html/        # Mac → container
```

Changes made this way are lost when the container is deleted. For persistent data use
`-v` ([run flags](#container-run-flags)).

[⬆ back to menu](#navigation)

### Container delete

**Meaning:** remove a container. Its files are **gone**. The image stays.

```bash
docker rm mybox                 # must be stopped
docker rm -f web                # force: stop + delete
docker rm $(docker ps -aq)      # delete ALL containers
```

```text
Error response from daemon: cannot remove container "web": container is running
```

Stop it first, or use `-f`.

[⬆ back to menu](#navigation)

### Container prune

**Meaning:** delete every **stopped** container in one go.

```bash
docker container prune
```

```text
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N]
```

[⬆ back to menu](#navigation)

---

# ⚙️ System commands

### System version and info

**Meaning:** verify the install and see engine-wide stats.

```bash
docker version      # Client + Server versions. Both present = working
docker info         # images, running/stopped containers, storage, OS, CPUs, RAM
```

[⬆ back to menu](#navigation)

### System disk

**Meaning:** how much disk Docker is using, by images, containers and volumes.

```bash
docker system df
```

```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          4         2         1.2GB     800MB (66%)
Containers      6         1         120MB     110MB (91%)
Local Volumes   2         1         300MB     150MB (50%)
```

[⬆ back to menu](#navigation)

### System prune

**Meaning:** the big cleanup.

```bash
docker system prune          # stopped containers + unused networks + dangling images
docker system prune -a       # also every image not used by a running container
docker system prune -a --volumes   # also unused volumes (DATA LOSS, be sure)
```

[⬆ back to menu](#navigation)

### System engine

**Meaning:** every command fails if the engine (daemon) isn't running.

```text
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

| Platform | Start it |
|---|---|
| Mac / Windows | open **Docker Desktop** |
| Linux | `sudo systemctl start docker` |

[⬆ back to menu](#navigation)

---

## Lifecycle walkthrough

The whole life of a container, one command per step.

```bash
docker pull nginx                              # 1. image: download
docker run -d --name web -p 8080:80 nginx      # 2. container: create + run in background
docker ps                                      # 3. list: it's Up
docker logs -f web                             # 4. watch output (Ctrl+C)
docker exec -it web bash                       # 5. go inside (Ctrl+D to leave, still running)
docker rename web website                      # 6. rename
docker stop website                            # 7. stop (files kept)
docker start website                           # 8. resume
docker rm -f website                           # 9. delete container
docker rmi nginx                               # 10. delete image
```

```text
  pull ──► run ──► (running) ──stop──► (exited) ──start──► (running)
                       │                   │
                     exec                  rm ──► gone (image stays until rmi)
```

[⬆ back to menu](#navigation)

---

## Gotchas & best practices

- **`run` creates, `start` resumes.** Check `docker ps -a` before re-running an image.
- **Name your containers.** `docker stop web` beats `docker stop quirky_moore`.
- **`--rm` for throwaway shells.** Nothing piles up.
- **`exec`, not `attach`.** Attach + `Ctrl+D` kills the main process.
- **Stopped ≠ deleted.** Data survives `stop`, dies on `rm`. Use `-v` for data you care about.
- **Pin tags.** `python:3.12`, not `python`.
- **Delete containers before images.** `rmi` fails while a container uses the image.

> **Interview angle:** *"Difference between `run`, `start`, `exec` and `attach`?"*
> `run` creates a new container from an image and starts it. `start` restarts an existing
> stopped container. `exec` runs an extra process (usually a shell) inside a running
> container. `attach` connects to the container's main process, so exiting it stops the
> container.

[⬆ back to menu](#navigation)
