# Volumes 1 — Mounting a Host Folder into a Container

A container's files **die with the container**. To keep data, or to share a folder between
your laptop and a container, you **mount** a folder from your laptop into the container with
`-v`. Both sides see the same files. Delete the container, the folder is still on your laptop.

---

## 1. The problem

```bash
docker run -it --rm ubuntu
cd /home/ubuntu
echo "I am a secret" > secret.txt
cat secret.txt            # I am a secret
# Ctrl+D
```

Start a new container, look again:

```bash
docker run -it --rm ubuntu
ls /home/ubuntu           # empty. secret.txt is gone
```

| Two problems | |
|---|---|
| **Data is lost** when the container stops | the container's files live only inside it |
| **No way in** | a file on your laptop (`~/Downloads/my_data/index.js`) can't be seen from inside |

---

## 2. The idea: mount a folder

```text
   YOUR LAPTOP                               CONTAINER
   /Users/you/Downloads/my_data   ◄──────►   /home/ubuntu/piyush
   ├── index.js                               ├── index.js      (same file)
   └── secret.txt                             └── secret.txt   (same file)
```

A mount is a **link**, not a copy. Write on either side, the other side sees it
immediately. The real files stay on your laptop.

---

## 3. The command

```bash
docker run -it --rm -v /Users/you/Downloads/my_data:/home/ubuntu/piyush ubuntu
```

```text
-v  <host path> : <container path>
     your laptop   where it appears inside
```

Same pattern as ports: `-p host:container`, `-v host:container`.

| Part | Example | Note |
|---|---|---|
| host path | `/Users/you/Downloads/my_data` | must be the **full** path. Get it with `pwd` in that folder |
| container path | `/home/ubuntu/piyush` | created automatically if it doesn't exist |

Docker Desktop on Mac may ask "allow access to your Downloads folder". Say yes.

### Try it

```bash
# inside the container
ls /home/ubuntu/piyush        # index.js  secret.txt   ← your laptop's files
cat /home/ubuntu/piyush/secret.txt
rm /home/ubuntu/piyush/index.js
```

Check your laptop's Downloads folder: `index.js` is really gone. The container edited your
real folder.

### Long command? Split it

```bash
docker run -it --rm \
  -v /Users/you/Downloads/my_data:/home/ubuntu/piyush \
  ubuntu
```

A `\` at the end of a line continues the command. Easier to read, easier to spot a missing
`-it` or a missing space.

---

## 4. One folder, many containers

```bash
docker run -it --rm -v /Users/you/Downloads/my_data:/home/ubuntu/piyush ubuntu
docker run -it --rm -v /Users/you/Downloads/my_data:/home/ubuntu/piyush busybox
```

```text
   my_data on laptop
       ▲        ▲
       │        │
    ubuntu   busybox       ← both read and write the same folder
```

Different images, same data. Each container can use its own tools on the files. When both
containers are gone, the files are still there.

---

## 5. Why this is useful

| Situation | Mount gives you |
|---|---|
| data must survive container restarts | files live on the laptop, not in the container |
| you edit code on your Mac, run it in Linux | mount your project folder; no rebuild to see changes |
| a tool only exists in Ubuntu | run it in a container, keep the output on your laptop |
| several containers need the same files | mount the same folder into each |

---

## Remember

| Term | One line |
|---|---|
| **container files are temporary** | gone when the container is removed |
| **mount** | link a laptop folder to a path inside the container |
| **`-v /host/path:/container/path`** | the flag. Full host path, then container path |
| **both sides see the same files** | it's a link, not a copy |
| **one folder, many containers** | same `-v` in each `docker run` |
| **`\`** | split a long command over lines |

> **If someone asks in an interview:** "How do you keep data when a container is deleted?"
> Mount storage from outside the container. The simplest form is a **bind mount** with
> `-v /host/folder:/container/folder`, which links a folder on the host into the container.
> The data lives on the host and survives the container.

**Next:** Docker-managed volumes (`docker volume create`), where Docker picks the location
for you.
