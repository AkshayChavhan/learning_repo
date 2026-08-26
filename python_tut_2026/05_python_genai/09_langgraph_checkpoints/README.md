# 09 — LangGraph Checkpoints

Project [08](../08_lang_graph/) forgot everything the moment it finished — every
run started from an empty message list. This one adds a **checkpointer**: after
each step LangGraph saves the state to MongoDB, so the next run picks the
conversation back up.

```text
START ──► chatbot ──► END        (state saved to MongoDB after each step)
```

**The key idea is `thread_id`.** Same `thread_id` → same history. A new one
starts a fresh conversation. That single string is how a real chat app keeps
thousands of users' conversations apart.

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate    # or: uv venv --seed --python 3.12
pip install -r requirements.txt
```

`--seed` matters if you use `uv` — it puts a real `pip` inside the venv.

### 1. Start MongoDB

The checkpointer writes there, so it must be up before you run anything.

```bash
docker compose up -d          # start in background
docker compose ps             # confirm it is running
nc -z localhost 27017 && echo open
```

| Command | Effect |
|---|---|
| `docker compose down` | stop, **keep** saved conversations |
| `docker compose down -v` | stop and **wipe** them (drops the named volume) |

Conversations survive `down` because `docker-compose.yml` declares a
`mongodb_data` volume. Only `-v` deletes them.

### 2. Environment

| Variable | Where |
|---|---|
| `OPENAI_API_KEY` | `.env` in this folder |

```bash
# from the repo root
export OPENAI_API_KEY='sk-proj-...'
./scripts/setup_env.sh
```

`chat3_checkpoint.py:76` calls `load_dotenv()`.

**Mongo connection** is hardcoded at `chat3_checkpoint.py:141`:
`mongodb://admin:admin@localhost:27017/lg`. Credentials come from
`docker-compose.yml`. Fine on localhost; never expose it.

---

## Run

```bash
python chat3_checkpoint.py
```

**Run it twice with the same `thread_id`.** The second run still knows your name
— that is the whole point.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`docker-compose.yml` vs `docker-composer.yml`** | This folder's file uses the name Docker looks for, so a bare `docker compose up` works. Project 05's is spelled `docker-composer.yml` (with an r) and *needs* `-f` |
| **Mongo must be up first** | The checkpointer connects on graph construction — a connection error here means the container is not running |
| **New `thread_id` = amnesia** | Change the string and you get a blank conversation. Reuse it to see the memory work |
| **`down -v` is destructive** | It drops the volume and every saved conversation. Plain `down` is what you usually want |
| **`python-dotenv`, not `dotenv`** | The stub package installs cleanly and then does nothing |
