# Multi-Stage Docker Builds — Lean Production Images

Building code needs tools (TypeScript, gcc, the Rust toolchain) and the **source**.
Running it needs only the **output**. A **multi-stage build** uses one stage to build and a
second, clean stage to run, copying across just the artifacts. The last stage is the image
you ship: no source, no compilers, small.

---

## Topic at a glance

```text
        The problem                          The fix
            \                                  /
  source + tools in image ──\   stage 1: builder ──/
                             \                    /
  TypeScript in prod ────────\   stage 2: runner ─/
                               ►   MULTI-STAGE BUILD
  163 MB vs much less ───────/    COPY --from=builder ──\
                             /                           \
  secure, no source ────────/     last stage = the image ─\
            /                                               \
       Result                                            Syntax
```

---

## 🟢 Beginner — build-time vs run-time needs

The TypeScript Express app:

| Phase | Needs | Command |
|---|---|---|
| **Build** | `typescript`, `@types/node`, `@types/express`, `tsconfig.json`, `src/` | `npm run build` → creates `dist/` |
| **Run** | `dist/`, `express`, `package.json` | `npm start` → `node dist/index.js` |

After the build, TypeScript and the types are **never used again**. Same for any compiled
language: C needs gcc and 30 source files to produce one binary, then only the binary runs.

> **Key idea:** build tools and source belong to **development**. Production needs the
> **output** only.

### The naive Dockerfile (works, but fat)

```dockerfile
FROM node:20.17-alpine
WORKDIR /home/app
COPY package*.json ./
COPY tsconfig.json ./
RUN npm install              # installs TypeScript + types + express
COPY src/ ./src/
RUN npm run build            # creates dist/
CMD ["npm", "start"]
```

```bash
docker build -t ts-app-old -f Dockerfile.old .
docker run -it -p 8000:8000 ts-app-old     # localhost:8000 → "Hello from TypeScript server"
```

Open the container's files in Docker Desktop: `/home/app` has **src/**, **dist/**, and a
`node_modules` with TypeScript inside. All shipped to production for nothing.

---

## 🟡 Intermediate — why not just build on your Mac and copy dist?

| Idea | Problem |
|---|---|
| build locally, `COPY dist/` only | ❌ TypeScript and dev deps still get installed by `npm install` in the image |
| build locally, `COPY dist/` only | ❌ built on **macOS**, may not behave on Linux. Compiled languages (Rust, Go, C) are platform-specific. Build **inside** the target image |

So the build must happen in the image, **and** the final image must not contain the build
leftovers. That's exactly what multi-stage gives you.

### The multi-stage Dockerfile

```dockerfile
FROM node:20.17-alpine AS base          # a named base, like a variable

# ---- Stage 1: builder ----
FROM base AS builder
WORKDIR /home/build
COPY package*.json ./
COPY tsconfig.json ./
RUN npm install                         # TypeScript, types, everything
COPY src/ ./src/
RUN npm run build                       # → /home/build/dist

# ---- Stage 2: runner (final image) ----
FROM base AS runner
WORKDIR /home/app
COPY --from=builder /home/build/dist ./dist
COPY --from=builder /home/build/package*.json ./
RUN npm install --omit=dev              # express only, no TypeScript
CMD ["npm", "start"]
```

| Line | Meaning |
|---|---|
| `FROM base AS builder` | start a stage named `builder` from the shared base image |
| `COPY --from=builder <path> <dest>` | copy **from the builder stage's filesystem**, not from your machine |
| `npm install --omit=dev` | skip `devDependencies` (TypeScript, `@types/*`) |
| last `FROM` | **this** stage becomes the image. Everything before it is thrown away |

```bash
docker build -t ts-node .                # default Dockerfile, no -f needed
docker run -it -p 8000:8000 ts-node
```

Inspect `/home/app` now: `dist/`, `package.json`, `node_modules` with **only express**.
No `src/`, no `tsconfig.json`, no TypeScript.

### Size

| Image | Contents | Size |
|---|---|---|
| `ts-app-old` | source + TypeScript + types + express + dist | ~163 MB |
| `ts-node` | dist + express | noticeably smaller |

---

## 🔴 Expert — how Docker processes stages

```text
  Stage 1 "builder"                         Stage 2 "runner"
  ┌──────────────────────────────┐          ┌─────────────────────────┐
  │ node + npm                    │          │ node + npm              │
  │ src/  tsconfig.json           │          │ dist/        ◄──────────┼── COPY --from=builder
  │ node_modules (ts, types, expr)│ ──────►  │ package.json ◄──────────┼── COPY --from=builder
  │ dist/   ← npm run build       │          │ node_modules (express)  │
  └──────────────────────────────┘          └─────────────────────────┘
            DISCARDED                              THE IMAGE
```

1. Docker builds stage 1 completely.
2. Starts stage 2 from a **fresh** base.
3. `COPY --from=builder` pulls only the named paths across.
4. Stage 1's filesystem is **discarded**. Thousands of files, gone.
5. The **last stage** is what `docker build -t` tags and what you push.

### Same pattern, other languages

| Language | Stage 1 (builder) | Stage 2 (runner) |
|---|---|---|
| **TypeScript** | `node` + TypeScript, `npm run build` | `node` + prod deps, run `dist/` |
| **Rust** | full Rust toolchain, `cargo build --release`, ~1 GB | copy the **one binary**, run it. No Rust installed |
| **Go** (official docs example) | `golang` image, `go build` | `FROM scratch` (no OS at all), copy the binary, run |
| **C** | gcc + 30 source files | copy `a.out`, run |

```dockerfile
# Go, from the Docker docs
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN go build -o /bin/app

FROM scratch
COPY --from=build /bin/app /bin/app
ENTRYPOINT ["/bin/app"]
```

`scratch` is an empty image. The final image is literally one executable.

### Why it matters beyond size

| Benefit | Why |
|---|---|
| **Smaller** | no compilers, no dev deps, no source |
| **Faster to pull / deploy** | MBs instead of hundreds of MBs |
| **More secure** | no source code to read, fewer packages = fewer vulnerabilities |
| **Correct platform** | built inside the Linux image it runs in |
| **One Dockerfile** | no separate build script; readable and maintainable |

---

## Gotchas & best practices

- **The last `FROM` wins.** Only the final stage is tagged. Put the runner last.
- **Name your stages** (`AS builder`). `COPY --from=0` works but `--from=builder` is readable.
- **`--omit=dev`** (npm 9+) or `--only=production` (older npm) in the runner. Otherwise
  TypeScript sneaks back in.
- **Build inside the image**, not on your laptop. Platform matters for compiled output.
- **`-f Dockerfile.old`** when the file isn't named `Dockerfile`. The `.` context is still needed.
- **Check the result**: open the container's files, confirm no `src/`, no dev deps.

> **Interview angle:** *"What is a multi-stage build and why use it?"* A Dockerfile with
> several `FROM` stages. Early stages install toolchains and compile; the final stage starts
> from a clean base and copies only the build output with `COPY --from`. The result is a
> smaller, more secure image with no source or compilers, built on the target platform,
> all in one readable Dockerfile.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Multi-stage build** | several `FROM` stages in one Dockerfile; only the last becomes the image |
| **`FROM <image> AS <name>`** | start a named stage |
| **`COPY --from=<stage> src dest`** | copy files from an earlier stage, not from your machine |
| **Builder stage** | has toolchain + source, produces the artifact (`dist/`, binary) |
| **Runner stage** | clean base + artifact + runtime deps only |
| **`npm install --omit=dev`** | production dependencies only |
| **`FROM scratch`** | empty base; final image = just a binary |
| **Why** | smaller, faster, more secure, platform-correct |
