# Volumes 2 — Named Volumes Managed by Docker

Last time you mounted a folder from your laptop. This time **Docker makes the folder for
you**. You give it a name, mount it by that name, and Docker keeps it safe somewhere on
disk. Containers come and go, the volume stays. No host path to type, no folder to create.

---

## 1. Bind mount vs named volume

| | Bind mount (note 237) | Named volume (this note) |
|---|---|---|
| Who owns the folder | **you**, on your laptop | **Docker** |
| In `-v` | `/Users/you/Downloads/my_data:/server` | `custom_data:/server` |
| Setup | create the folder, find its full path | `docker volume create custom_data` |
| Where the data lives | wherever you put it | Docker's storage area, managed for you |
| Best for | editing code on your Mac, run in container | databases, app data, anything the container owns |

> **Key idea:** if the first part of `-v` starts with `/`, it's a path on your laptop. If
> it's just a name, it's a Docker volume.

---

## 2. Create a volume

```bash
docker volume create custom_data
docker volume ls | grep custom
```

```text
local     custom_data
```

Docker Desktop → **Volumes** shows it too, with its files and which containers use it.

---

## 3. Mount it in a container

```bash
docker run -it --rm -v custom_data:/server ubuntu
```

```text
-v  custom_data : /server
    volume name   path inside the container
```

```bash
# inside ubuntu
cd /server
echo "created by ubuntu" > ubuntu.txt
# Ctrl+D  → container gone (--rm)
```

Docker Desktop → Volumes → custom_data → **ubuntu.txt is still there**.

---

## 4. Another container, same volume

```bash
docker run -it --rm -v custom_data:/server busybox
```

```bash
# inside busybox
ls /server                   # ubuntu.txt       ← from the previous container
cat /server/ubuntu.txt       # created by ubuntu
echo "created by busybox" > /server/busybox.txt
# Ctrl+D
```

Now the volume holds both files. Two different images, two containers that no longer
exist, one shared volume.

```text
   custom_data (Docker volume, lives on)
   ├── ubuntu.txt      ← written by an ubuntu container, now gone
   └── busybox.txt     ← written by a busybox container, now gone
```

---

## 5. Two containers at the same time

The path inside each container can be **different**. The volume is the same.

```bash
# terminal 1
docker run -it --rm -v custom_data:/server ubuntu

# terminal 2
docker run -it --rm -v custom_data:/home/ubuntu/custom ubuntu
```

```bash
# terminal 2
echo hi > /home/ubuntu/custom/test.txt

# terminal 1
ls /server          # ubuntu.txt  busybox.txt  test.txt   ← appears immediately
```

Docker Desktop shows the volume as **in use by 2 containers**.

---

## 6. Volume commands

| Command | Meaning |
|---|---|
| `docker volume create <name>` | make a volume |
| `docker volume ls` | list volumes |
| `docker volume inspect <name>` | details, including where Docker stores it |
| `docker volume rm <name>` | delete it (fails while a container uses it) |
| `docker volume prune` | delete all volumes no container uses |

The volume is **not** deleted when a container is removed, even with `--rm`. Only
`docker volume rm` or `prune` deletes it. That's the whole point.

---

## Remember

| Term | One line |
|---|---|
| **named volume** | a folder Docker creates and manages, referred to by name |
| **`docker volume create X`** | make it |
| **`-v X:/path`** | mount it; a name, not a path, means a volume |
| **survives containers** | `--rm`, `docker rm`, nothing touches the volume |
| **shared** | many containers, one after another or at the same time |
| **different paths OK** | each container picks where the volume appears |
| **`docker volume rm / prune`** | the only ways the data goes away |

> **If someone asks in an interview:** "Bind mount vs named volume?" A bind mount maps a
> specific host folder you manage into the container. A named volume is storage Docker
> creates and manages; you reference it by name, it persists across container lifetimes,
> and it's the recommended way to keep data for databases and app state.
