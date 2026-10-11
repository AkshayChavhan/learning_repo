# Docker Image vs Docker Container

A **Docker image** is like a Windows install CD: all the configuration, nothing running.
A **container** is the laptop you install it on. The image can't run by itself, one image
can run on many containers, and each container keeps its **own data**.

---

## Topic at a glance

```text
        Image                                 Container
            \                                     /
  configuration only ──\        runs an image ──/
                        \                      /
  can't run alone ──────\    random name + id
                          ►   IMAGE vs CONTAINER
  one image, many ──────/      own files, isolated ──\
                        /                             \
  stays after delete ──/       delete = data gone ─────\
            /                                            \
      Reuse                                         Isolation
```

---

## 🟢 Beginner — the laptop analogy

| Real world | Docker |
|---|---|
| Windows install CD / ISO | **image** (e.g. `ubuntu`) |
| a laptop running Windows | **container** |
| can a CD run without a laptop? **No** | can an image run without a container? **No** |
| one CD → many laptops | one image → **many containers** |
| your laptop's files ≠ your friend's files | each container's files are **its own** |
| laptop destroyed → its files gone | container deleted → its data **gone** |

```text
            ┌──────────────┐
            │ image: ubuntu│   ← configuration, read-only, shared
            └──────┬───────┘
         ┌─────────┼─────────┐
         ▼         ▼         ▼
   ┌───────────┐ ┌───────────┐ ┌───────────┐
   │ container │ │ container │ │ container │   ← each one a separate "machine"
   │  1fdd9    │ │  26d79    │ │   ...     │      with its own files
   └───────────┘ └───────────┘ └───────────┘
```

> **Key idea:** `docker run ubuntu` doesn't "run Ubuntu". It **starts a container** from
> the Ubuntu image.

---

## 🟡 Intermediate — the two-terminal demo

Fresh start: no images, no containers.

```bash
# terminal 1
docker run -it ubuntu
```

```text
Unable to find image 'ubuntu:latest' locally   ← pulled from the cloud once
root@1fdd9...:/#                                ← inside container 1fdd9, name "mystifying_lima"
```

```bash
# terminal 2, same command
docker run -it ubuntu
```

```text
root@26d79...:/#                                ← a SECOND container, name "focused_easley"
```

| Now you have | |
|---|---|
| images | 1: `ubuntu` |
| containers | 2: `1fdd9`, `26d79`, both from the same image |

### Prove they're isolated

| Terminal 1 (`1fdd9`) | Terminal 2 (`26d79`) |
|---|---|
| `touch myfile.txt` → `ls` shows it | `ls` → **nothing** |
| `ls` → still no `secret.txt` | `touch secret.txt` → `ls` shows it |
| `cd /home/ubuntu && touch this_is_my_file.txt` | `cd /home/ubuntu && ls` → **empty** |

Same image, same configuration, **different machines**. Docker Desktop → Containers →
Files shows each container's own filesystem.

### Delete the container

```text
container 26d79 removed  →  secret.txt is gone
image ubuntu              →  still there, untouched
```

The image never held your data. Data lives in the container, and dies with it.

---

## 🔴 Expert — what each one really is

| | Image | Container |
|---|---|---|
| Nature | **template**: filesystem + config, read-only | **running instance** of an image |
| Can run alone | ❌ | ✅ (it *is* the running thing) |
| Count | one per image name | as many as you start |
| Identity | name:tag (`ubuntu:latest`) | **random name** + **id** (`1fdd9…`) |
| State | never changes | gets its own writable layer: your files |
| On delete | stays, reusable | **its data is destroyed** |
| Where it comes from | pulled from a registry (cloud) once | `docker run <image>` |

```text
  docker run -it ubuntu
       │          │
       │          └── which IMAGE to use
       └── start a CONTAINER (interactive terminal)
```

### Why isolation is a feature

- Two containers from one image can't see each other's files, processes or changes.
- You can start, kill and delete containers freely. The image is never harmed.
- Need data to survive? That's a **volume**, a later lecture. By default, nothing persists.

---

## Gotchas & best practices

- **Image ≠ container.** Image is the CD, container is the laptop. Say it until it sticks.
- **Images can't run.** `docker run` always creates a container.
- **Containers are disposable.** Anything you write inside is lost on delete unless you
  mount a volume.
- **Same image, separate data.** Don't expect one container to see another's files.
- **The pull happens once.** The second `docker run ubuntu` didn't download anything.

> **Interview angle:** *"Image vs container?"* An image is a read-only template holding the
> filesystem and configuration. A container is a running, isolated instance of that image
> with its own writable layer. One image can back many containers; deleting a container
> destroys its data but leaves the image intact.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Image** | read-only configuration/template, like an OS install CD |
| **Container** | isolated environment that runs an image, like a laptop |
| **`docker run -it <image>`** | start a new container from an image, with a terminal |
| **Container id / name** | unique id (`1fdd9…`) plus a random name (`mystifying_lima`) |
| **Isolation** | each container has its own files; nothing is shared |
| **Delete container** | its data is gone; the image remains |
