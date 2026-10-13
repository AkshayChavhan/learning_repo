# Publishing a Docker Image to Docker Hub

A **container registry** is GitHub for Docker images: a central server you push images
to and others pull from. Docker Hub is the official one. To publish, the image's name
must be `<your-username>/<repo>`, you must be logged in, then `docker push`.

---

## Topic at a glance

```text
        Registry                            Naming rule
            \                                   /
  GitHub for images ──\      username/repo ──/
                       \                    /
  Hub, ECR, GCR, DO ───\   build -t or tag ─/
                         ►   PUBLISH AN IMAGE
  docker login ────────/       :v1, :latest ──────\
                       /                           \
  docker push ────────/        docker pull anywhere ─\
            /                                          \
       Commands                                    Versioning
```

---

## 🟢 Beginner — what a registry is

| GitHub | Container registry |
|---|---|
| central server for **code** | central server for **images** |
| `git push` / `git clone` | `docker push` / `docker pull` |
| repositories under your username | repositories under your **namespace** (username) |
| public or private repos | public or private repos |

| Registry | Who |
|---|---|
| **hub.docker.com** | official, default. Where `ubuntu`, `alpine`, `node` came from |
| ECR | AWS |
| Artifact Registry | Google Cloud |
| DigitalOcean Container Registry | DigitalOcean |

> **Key idea:** every `docker run ubuntu` you've done was a **pull** from Docker Hub.
> Now you push your own.

---

## 🟡 Intermediate — the publish flow

### 1. Create the repository on Docker Hub

Sign up → Profile → Repositories → **Create repository**.

| Field | Example |
|---|---|
| Name | `node-application` |
| Description | what it is, how to run it |
| Visibility | **Public** (free plan allows unlimited public, **one** private) |

Result: a repo named **`<username>/node-application`**, e.g. `piyushgarg/node-application`.

### 2. Name the image to match

A local image called `myapp` **cannot** be pushed. Thousands of people have a `myapp`.
The image must carry your namespace. Two ways:

| Way | Command | When |
|---|---|---|
| **A. Build with the right name** | `docker build -t <username>/node-application .` | you know you'll publish |
| **B. Tag an existing image** | `docker tag myapp <username>/node-application` | image already built as `myapp` |

`docker tag` doesn't copy anything. It adds a second name pointing at the **same** image id.

### 3. Log in and push

```bash
docker login                                    # username + password / token, once
docker push <username>/node-application
```

```text
The push refers to repository [docker.io/<username>/node-application]
5f70bf18a086: Pushed
...
latest: digest: sha256:9a1c... size: 1234
```

Refresh Docker Hub: the image is there under **Tags** as `latest`.

### 4. Anyone can pull it now

```bash
docker run -it <username>/node-application
```

```text
Unable to find image '<username>/node-application:latest' locally
latest: Pulling from <username>/node-application
...
```

Works on any machine with Docker. The Hub page also shows the **Dockerfile layers**, base
images used, and a **vulnerability scan**.

### What happens if you skip the naming rule

```bash
docker push myapp
```

```text
denied: requested access to the resource is denied
```

Docker tries `docker.io/library/myapp`, the official namespace. You don't own it.
Fix: `docker tag myapp <username>/myapp`, then push that.

---

## 🔴 Expert — tags and versioning

A repository holds **many tags**. No tag means `latest`.

```bash
docker tag myapp <username>/node-application:v1
docker push <username>/node-application:v1
```

| On Docker Hub | Pull command |
|---|---|
| `node-application:latest` | `docker pull <username>/node-application` |
| `node-application:v1` | `docker pull <username>/node-application:v1` |

```text
  local image id 3f2a9c...
       │
       ├── myapp                              (local name only)
       ├── <username>/node-application        (pushed as :latest)
       └── <username>/node-application:v1    (pushed as :v1)
   one image, three names
```

### Full image name, decoded

```text
  docker.io / <username> / node-application : v1
  ─────────   ──────────   ────────────────   ──
  registry    namespace    repository         tag
  (default)   (your user)  (the repo name)    (default: latest)
```

Official images like `ubuntu` are really `docker.io/library/ubuntu:latest`. That's why a
bare name can't be pushed by you.

### Clean up

Docker Hub → repository → Settings → **Delete repository**. Type the name to confirm.
Local images with that name stay on your machine until `docker rmi`.

---

## Gotchas & best practices

- **`docker login` first.** Push fails with "access denied" otherwise.
- **Name = `username/repo`.** A bare name targets the official `library/` namespace.
- **Tag versions.** Push `:v1`, `:v2` as well as `latest`, so users can pin.
- **Public means public.** No `.env`, keys or private data baked into the image.
- **`docker tag` is free.** Add as many names as you like, nothing is copied.
- **Check the Hub page** after pushing: layers, base images, vulnerabilities.

> **Interview angle:** *"How do you publish a Docker image?"* Create a repo on a registry,
> name the image `registry/namespace/repo:tag` (build with `-t` or `docker tag` an existing
> image), `docker login`, then `docker push`. Others pull it by the same name. A bare name
> like `myapp` resolves to the official `library/` namespace and is rejected.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Container registry** | GitHub for images: Docker Hub, ECR, GCR, DigitalOcean |
| **Namespace** | your Docker Hub username, prefix of every image you publish |
| **`docker build -t user/repo .`** | build with the publishable name |
| **`docker tag local user/repo:tag`** | add a publishable name to an existing image |
| **`docker login`** | authenticate before pushing |
| **`docker push user/repo:tag`** | upload to the registry |
| **`docker pull user/repo:tag`** | download; `docker run` does it automatically |
| **Tag** | version label; `latest` is the default |
