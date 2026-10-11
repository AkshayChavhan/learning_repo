# Node Health App — Dockerized

A tiny Express server with one route (`GET /`) returning a health
check, packaged with the `Dockerfile` in this folder.

---

## 1. Install Docker

**Mac (Homebrew):**

```bash
brew install --cask docker
```

**Or via the website:** [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
— the page auto-detects Apple Silicon vs Intel.

After installing, **open Docker Desktop once** (Spotlight → "Docker" →
Enter) and wait for the whale icon in the menu bar to say *"Docker
Desktop is running"*. The `docker` CLI isn't on your `PATH` until the
app has actually launched.

Confirm it worked:

```bash
docker --version
```

---

## 2. Build the image

From this folder:

```bash
docker build -t node-health-app .
```

| Part | Does |
|---|---|
| `-t node-health-app` | names the image |
| `.` | build context — current folder, where the `Dockerfile` lives |

---

## 3. Run it

**The Dockerfile has no `CMD`**, so running the image with no command
does nothing visible — it starts the Ubuntu base, finds nothing to do,
and exits immediately. The server has to be started explicitly:

```bash
docker run -d -p 8080:8080 --name health-app node-health-app npm start
```

| Flag | Does |
|---|---|
| `-d` | run in the background (detached) |
| `-p 8080:8080` | map the container's port 8080 to the host's port 8080 — **without this, `localhost:8080` won't reach it**, even though the server is running fine inside the container |
| `--name health-app` | a name to refer to the container by, instead of its random ID |
| `npm start` | the command to run inside the container — overrides the (missing) default |

Verify it's actually working:

```bash
curl http://localhost:8080/
# {"status":"success","message":"Server is healthy"}
```

Check the logs or stop it:

```bash
docker logs health-app
docker stop health-app
```

---

## Gotchas

- **No `CMD` in the Dockerfile** — the container does nothing until you
  explicitly pass a command (`npm start`) to `docker run`. Adding
  `CMD ["npm", "start"]` as the last line of the `Dockerfile` would make
  `docker run -p 8080:8080 node-health-app` alone sufficient — not done
  here, so the command above is required every time.
- **Forgetting `-p 8080:8080`** is the single most common trip-up — the
  app runs fine inside the container and still looks unreachable from
  the host.
- **Rebuild after changing `index.js`** — `COPY` takes a one-time
  snapshot at build time; editing the local file doesn't change what's
  already inside a built image.
