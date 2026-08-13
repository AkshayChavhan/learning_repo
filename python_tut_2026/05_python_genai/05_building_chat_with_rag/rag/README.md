# Chat with RAG — setup

Commands to get this folder running, in order.

---

## 1. Start the vector database

```bash
docker compose -f docker-composer.yml up -d
```

> **Pass `-f`.** The file is named `docker-composer.yml` (with an *r*). Docker only
> auto-discovers `compose.yaml`, `compose.yml`, `docker-compose.yaml` and
> `docker-compose.yml` — so a bare `docker compose up` will not find it.

Qdrant then runs on port **6333**:

| URL | What |
|---|---|
| http://localhost:6333/dashboard | Web dashboard |
| http://localhost:6333/collections | Collections, as JSON |

Stop it later with `docker compose -f docker-composer.yml down`.

---

## 2. Create the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

You are in the venv when your prompt starts with `(venv)`. Leave it with `deactivate`.

---

## 3. Install dependencies

```bash
pip install -qU langchain-community pypdf
```

| Flag | Means |
|---|---|
| `-q` | quiet — hide the download spam |
| `-U` | upgrade if already installed |

### Save what you installed

```bash
pip freeze > requirements.txt
```

Rebuild that exact environment later — on another machine, or after deleting `venv/`:

```bash
pip install -r requirements.txt
```

> Run `pip freeze` **inside the activated venv**. Against system python it dumps every
> package on the machine. It also writes every transitive dependency you never asked for —
> **45 lines here, not 2** — each pinned with `==`.

---

## 4. Run

```bash
python3 index.py
```

```text
loaded 12 pages from sample.pdf

metadata: {'source': '/.../rag/sample.pdf', 'page': 0}
first 300 characters:
Topic 42 — RAG: Retrieval Augmented Generation
...
```

---

## What actually got installed

`langchain-community` now requires Python **3.10+**, and this machine has **3.8.10**, so pip
quietly resolved older versions instead of failing:

| Package | Installed here | Current latest |
|---|---|---|
| langchain-community | 0.2.19 | 0.4.2 |
| langchain-core | 0.2.43 | 1.5.4 |
| langchain | 0.2.17 | 1.3.15 |
| pypdf | 5.9.0 | 6.15.0 |

`PyPDFLoader` works fine on these. But newer LangChain moved a lot of imports around, so a
current tutorial may not match what's installed. Python 3.11+ would fix that.

---

## Files

| File | What |
|---|---|
| `docker-composer.yml` | Qdrant vector database |
| `sample.pdf` | 12-page test document (Topic 42 — RAG) |
| `index.py` | `read_pdf()` — loads the PDF into one Document per page |
| `requirements.txt` | pinned output of `pip freeze` |
| `venv/` | virtual environment (git-ignored) |

Next in the pipeline: split the pages into chunks, embed them, and write them into Qdrant.
