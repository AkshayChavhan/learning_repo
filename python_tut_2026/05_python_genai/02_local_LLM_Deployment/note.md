# Local LLM Deployment — Ollama + Open WebUI on Docker

Running an LLM on **your own machine** instead of calling a cloud API.
**Mental model:** `Ollama` = the engine (runs the model, speaks HTTP).
`Open WebUI` = the dashboard (a ChatGPT-like browser UI that talks to Ollama).
Both run as Docker containers so nothing pollutes your system.

---

## 🟢 Beginner — Why deploy locally?

Local is **not** universally better. It's a trade, and knowing which side you're on matters.

| ✅ What you gain | ❌ What you give up |
|---|---|
| **Privacy** — data never leaves your machine | **Hardware cost** — you supply the RAM/GPU |
| **No per-token cost** — unlimited calls, free | **Speed** — a cloud GPU beats your laptop |
| **Works offline** — no internet needed | **Quality** — a 3B local model ≪ GPT-4/Gemini |
| **No rate limits / quotas** | **Maintenance** — updates are your job |
| **No vendor lock-in** | **Scalability** — one machine, few users |

> ⚠️ **Correction to a common misconception:** local deployment does *not* fix
> scalability, reliability, or maintainability — it makes them **worse**. A cloud
> API is run by a team with redundancy; your laptop is one machine that you patch
> yourself. Choose local for **privacy, cost, and offline**, not for robustness.

### The whole picture

```text
                  Privacy                Cost
                     \                    /
   no data leaves ────\      free per-call
                       \                /
                        \              /
   offline use ─────────►  RUN LLM LOCALLY
                        /              \
                       /                \
   you buy the GPU ───/       slower than cloud
                     /                    \
                 Hardware              Performance
```

---

## 🟢 Beginner — The two pieces

```text
   Browser                Docker
  ┌─────────┐        ┌──────────────────────────────┐
  │localhost│───────►│ open-webui   :8080 (internal)│
  │  :3000  │        │      │                       │
  └─────────┘        │      │ OLLAMA_BASE_URL       │
                     │      ▼                       │
                     │ ollama       :11434          │
                     │      │                       │
                     │      ▼  volume: ollama       │
                     │  llama3.2:3b (model files)   │
                     └──────────────────────────────┘
```

Open WebUI is **only a front-end**. Without Ollama running behind it, the UI loads
but shows zero models.

---

## 🟡 Intermediate — Setup, step by step

### 1. Install Docker Desktop
Download from [docker.com](https://www.docker.com/products/docker-desktop/) and let it start.

### 2. Run Ollama

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 \
  --restart unless-stopped --name ollama ollama/ollama
```

Check it: open `http://localhost:11434/` → should say `Ollama is running`.

### 3. Pull a model

```bash
docker exec ollama ollama pull llama3.2:3b
```

### 4. Run Open WebUI

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --restart unless-stopped \
  --name openwebui ghcr.io/open-webui/open-webui:main
```

Open `http://localhost:3000`.

### 5. First login
There are **no default credentials**. The **first account you register becomes the
admin** — you invent the email and password. It's local-only, so anything works.

Then pick your model from the **model dropdown at the top of the chat**.

---

## 🟡 Intermediate — Decoding the flags

| Flag | Meaning |
|---|---|
| `-d` | **Detached** — run in background, return the terminal |
| `-p 3000:8080` | **Port map** — `HOST:CONTAINER`. Browser hits 3000, container hears 8080 |
| `-v ollama:/root/.ollama` | **Volume** — `NAME:PATH_INSIDE`. Survives container deletion |
| `--name ollama` | Friendly name, so you don't need the container ID |
| `-e KEY=value` | **Env var** passed into the container |
| `--add-host=...:host-gateway` | Lets the container resolve `host.docker.internal` → your PC |
| `--restart unless-stopped` | Auto-start after reboot or Docker restart |

### ⚠️ The `-p` gotcha that bites everyone

```text
  -p 3000:8080
     ────  ────
     HOST  CONTAINER   ← these are NOT interchangeable
```

Open WebUI listens on **8080 inside** the container. Verify any image yourself:

```bash
docker inspect ghcr.io/open-webui/open-webui:main --format "{{json .Config.ExposedPorts}}"
```

```text
{"8080/tcp":{}}
```

Using `-p 3000:3000` gives the **worst kind of bug**: the container starts,
`docker ps` looks healthy, and `localhost:3000` silently serves nothing.

---

## 🟡 Intermediate — Picking a model

Sizes are the **quantized download**; you need roughly that much free RAM too.

| Model | Size | Runs well on |
|---|---|---|
| `llama3.2:1b` | ~1.3 GB | Any laptop, CPU-only |
| `llama3.2:3b` | ~2.0 GB | **CPU-only, 8 GB RAM** ← good default |
| `llama3.1:8b` | ~4.7 GB | 16 GB RAM, GPU preferred |
| `gemma3:4b` | ~3.3 GB | CPU-capable |
| `llama3.1:70b` | ~40 GB | Serious GPU only |

> ⚠️ **These tags don't exist:** `llama3.1:13b`, `llama3.2:8b`, `llama3.2:13b`,
> `llama3.2:70b`. Llama **3.2** ships as **1b / 3b** (plus 11b/90b vision);
> Llama **3.1** ships as **8b / 70b / 405b**. Always confirm on
> [ollama.com/library](https://ollama.com/library) — a wrong tag fails the pull.

**No GPU?** Expect a few tokens/second. Stay at **1b–3b**. Check what you have:

```bash
docker logs ollama | Select-String "inference compute"
```

```text
inference compute id=cpu library=cpu ... total="7.5 GiB"   ← CPU-only, no GPU
```

---

## 🔴 Expert — Command reference

| Command | Description |
|---|---|
| `docker pull ollama/ollama` | Download the Ollama image |
| `docker ps` | List **running** containers |
| `docker ps -a` | List **all** containers, including stopped |
| `docker start ollama` | Start an existing container |
| `docker stop ollama` | Stop it (data in the volume survives) |
| `docker restart ollama` | Stop + start |
| `docker logs --tail 25 ollama` | Last 25 log lines — **first stop when debugging** |
| `docker exec ollama ollama list` | List installed models |
| `docker exec ollama ollama pull <model>` | Download a model |
| `docker exec -it ollama ollama run llama3.2:3b` | Chat in the terminal, no UI |
| `docker inspect ollama` | Full config: ports, mounts, env, exit code |
| `docker rm ollama` | Remove the **container** (volume survives) |
| `docker rmi ollama/ollama` | Remove the **image** |
| `docker volume ls` | List volumes — where models actually live |
| `docker system df` | Disk used by images / containers / volumes |

### Container vs Image vs Volume

```text
  IMAGE      read-only template downloaded from a registry   (ollama/ollama)
    │  docker run
    ▼
  CONTAINER  a running instance; delete it and it's gone     (ollama)
    │  -v
    ▼
  VOLUME     storage that OUTLIVES the container             (ollama volume)
```

Deleting a container does **not** delete your models — they're in the volume.
That's why `-v` matters: without it, `docker rm` destroys every downloaded model.

---

## 🔴 Expert — Gotchas & troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `localhost:3000` blank, container "Up" | `-p 3000:3000` instead of `3000:8080` | Recreate with the right port |
| UI loads, **no models listed** | Open WebUI can't reach Ollama | Set `OLLAMA_BASE_URL` + `--add-host` |
| Chats/account vanish after `docker rm` | No volume mounted | Add `-v open-webui:/app/backend/data` |
| Container gone after reboot | Default `--restart no` | `docker update --restart unless-stopped <name>` |
| Open WebUI shows `(unhealthy)` but works | Its internal healthcheck errors on `jq` | **Cosmetic** — ignore if HTTP 200 |
| `Exited (255)`, clean logs | Docker Desktop was shut down | `docker start ollama` |
| Pull seems frozen at "Pulling fs layer" | Image is multi-GB, just slow | **Wait** — don't Ctrl+C |
| `no space left on device` | Disk full | `docker system prune`, remove unused images |

### Verify the whole chain

```bash
curl http://localhost:11434/api/tags                                  # Ollama alive?
docker exec openwebui curl -s http://host.docker.internal:11434/api/tags  # UI → Ollama?
curl http://localhost:3000                                            # UI serving?
```

All three returning data = working stack. Test **inside** the container too — the
UI reaching Ollama is a different network path than your browser reaching Ollama.

### Disk reality check

| Item | Size |
|---|---|
| `ollama/ollama` image | ~8.4 GB |
| `open-webui` image | ~7.2 GB |
| `llama3.2:3b` model | ~2.0 GB |

Roughly **18 GB before your first chat**. Check with `docker system df` and keep
several GB spare — Windows misbehaves under ~5 GB free.

---

## Best practices

- **Always mount a volume** for both containers — otherwise `docker rm` = total data loss
- **Always `--restart unless-stopped`** so the stack survives reboots
- **Start small** (1b–3b), scale up only if the speed is acceptable
- **`docker logs` before Googling** — the answer is usually right there
- **Never trust a healthcheck over a real request** — curl the endpoint yourself
- Open WebUI has **no auth by default from the network** — don't expose port 3000 to the internet
