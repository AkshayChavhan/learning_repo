# Writing a Dockerfile — Packaging a Node App

This is the actual answer to the problem from the very first video:
a Dockerfile captures the whole environment - OS, runtime version,
dependencies, source code - into one image anyone can run identically.

---

## 🟢 Beginner — the file, and the basic instructions

The file is named **exactly** `Dockerfile` - capital D, no extension.

```dockerfile
FROM ubuntu                              # base image to start from

COPY index.js /home/app/index.js         # copy a local file into the image
COPY package.json /home/app/package.json

RUN apt-get update
RUN apt-get install -y curl              # the base image has nothing pre-installed
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs            # now Node.js exists inside the image

WORKDIR /home/app                        # change directory for what follows

RUN npm install                          # regenerates node_modules INSIDE the image
```

| Instruction | Does |
|---|---|
| `FROM <image>` | the starting point - here, plain Ubuntu, with nothing extra installed |
| `COPY <local path> <image path>` | copies a file from your machine into the image - can rename it on the way in |
| `RUN <command>` | runs a shell command while building the image - this is how Node.js gets installed |
| `WORKDIR <path>` | sets the working directory for every instruction after it |

**`node_modules` is never copied** - it's regenerated with `npm install`
inside the image instead, from the copied `package.json`.

---

## 🟡 Intermediate — building it, and the two real bugs

```bash
docker build -t my-app .
```

| Part | Does |
|---|---|
| `-t my-app` | tags/names the resulting image |
| `.` | the **build context** - current directory, where Docker looks for the Dockerfile and any `COPY`-referenced files |

**Two real failures hit while building this, worth knowing in advance:**

1. `RUN curl ...` failed with *"curl: command not found"* - the base
   Ubuntu image doesn't ship `curl`. Fix: `RUN apt-get update` and
   `RUN apt-get install -y curl` **before** the curl step.
2. `apt-get install nodejs` failed without the `-y` flag - package
   managers need explicit confirmation in a non-interactive build. This
   isn't a Docker quirk - it's how `apt` works on Ubuntu generally.

**`COPY` makes a copy, not a live reference.** Editing your local
`index.js` after the image is built does **not** change what's inside
that image - the file inside the container is frozen at build time. To
pick up local changes, rebuild the image.

---

## 🔴 Expert — layers, caching, and proving the isolation actually works

**Every instruction in the Dockerfile becomes a layer.** This build had
around 9-11 layers (`FROM`, each `COPY`, each `RUN`, `WORKDIR`...).

**Docker caches layers that haven't changed.** Rebuild after fixing the
curl bug, and the build doesn't start from scratch - it skips every
layer up to the one that actually changed, and resumes exactly from
there:

```text
  first build:   [1][2][3][4][5] FAIL at layer 6
  fix layer 6, rebuild:
                 [1 cached][2 cached][3 cached][4 cached][5 cached][6 fixed][7][8]...
```

This is the entire reason Dockerfile **instruction order** matters -
put things that change often (your source code) after things that
rarely change (installing Node.js), so edits don't invalidate and
re-run everything below them. (Optimizing this ordering is explicitly
the next lecture.)

**Proof the isolation is real:** the host machine has Node 18 installed.
Changing the Dockerfile's install step to Node 20 and rebuilding gives a
container where `node -v` reports **20** - while the host machine,
checked at the same time, still reports **18**. The image's environment
is genuinely independent of whatever is installed on the machine running it.

---

## Where this leaves off — the deliberate cliffhanger

The app server starts fine *inside* the container (`npm start` works,
and the container is visibly running in Docker Desktop) - but
`localhost:8000` from the host browser doesn't reach it. **A
container's ports are private by default.** Reaching it from outside
needs explicit **port mapping** - not covered in this video, on purpose.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Dockerfile** | the exact filename (capital D, no extension) describing how to build an image |
| **`FROM`** | the base image everything else builds on top of |
| **`COPY`** | copies a local file into the image - a one-time snapshot, not a live link |
| **`RUN`** | executes a shell command during the build - how dependencies get installed |
| **`WORKDIR`** | sets the directory context for later instructions |
| **Layer** | one instruction's result - cached, so unchanged layers aren't rebuilt |
| **`docker build -t <name> .`** | builds and tags an image from the Dockerfile in the current directory |
