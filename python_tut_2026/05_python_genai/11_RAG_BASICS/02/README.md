# 11 — RAG Basics: Data Ingestion

The first stage of RAG, in a notebook: get documents off disk and into a uniform
`Document` shape. No embeddings, no vector DB, no API key — yet.

**Mental model:** every loader, whatever the file type, produces the same thing —
a `Document` with `page_content` (the text) and `metadata` (where it came from).
Everything downstream only ever sees that shape.

```text
   .txt ──► TextLoader ─────┐
                            ├──► [ Document(page_content, metadata) ] ──► split ──► embed
   .pdf ──► PyMuPDFLoader ──┘
```

---

## Layout

| Path | Contents |
|---|---|
| `notebook/document.ipynb` | The lesson — 10 cells |
| `data/text_files/` | `sample.txt`, written by the notebook itself |
| `data/pdf_files/` | `01_sample.pdf`, `02_sample.pdf` |
| `02.md` | Notes file (currently empty) |

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then pick `.venv` as the notebook kernel and run the cells top to bottom.

### Environment

**None required.** Every loader in this notebook reads local files. `.env`
becomes necessary only when you reach the embeddings section — see
[ENVIRONMENT.md](../../../../ENVIRONMENT.md).

---

## What the notebook covers

| Cell | Topic |
|---|---|
| 2 | `Document` — the `page_content` + `metadata` structure everything else assumes |
| 3–4 | Write a sample `.txt` to load |
| 5 | `TextLoader` — one file |
| 6 | `DirectoryLoader` with `glob="**/*.txt"` and `loader_cls=TextLoader` |
| 7 | `PyMuPDFLoader` over `data/pdf_files/` |
| 8 | *(next)* embeddings + vector store |

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **Relative paths assume the notebook's cwd** | Cells use `../data/...`, which resolves from `notebook/`. Running them from the project root silently creates the wrong folders |
| **`langchain.document_loaders` is the old path** | Cell 5 uses it and it still works, but the maintained import is `langchain_community.document_loaders` — cell 6 shows the current form |
| **`DirectoryLoader` needs `loader_cls`** | Without it, LangChain reaches for `unstructured`, a heavy dependency this project does not install |
| **`show_progress=True` needs `tqdm`** | Pinned in `requirements.txt` for that reason |
| **PyPDF vs PyMuPDF** | Both are installed. `PyMuPDFLoader` is faster and preserves layout better; `PyPDFLoader` has fewer native dependencies |
| **`encoding="utf-8"` is not the default** | `TextLoader` uses the platform default otherwise, which bites on Windows |

---

## About `requirements.txt`

It lists **direct dependencies only**. The previous version was a bare
`pip freeze` captured *outside* the venv, so 151 lines pinned the whole machine —
`apturl`, `python-apt`, `dell-recovery`, `ubuntu-drivers-common`, `xkit` and
dozens more Ubuntu system packages. Those are shipped by `apt`, not PyPI, so
`pip install -r` died on the first one:

```text
ERROR: Could not find a version that satisfies the requirement apturl==0.5.2
       (from versions: none)
```

The heavy next-section libraries (`sentence-transformers`, `faiss-cpu`,
`chromadb`) are listed but commented out — `sentence-transformers` pulls torch,
a ~2GB download. Uncomment them when you reach cell 8.

Always run `pip freeze` **inside** the activated venv.
