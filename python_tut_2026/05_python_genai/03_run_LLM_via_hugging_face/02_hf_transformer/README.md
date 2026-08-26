# HuggingFace Transformers — Running Pre-Trained Models Locally

HuggingFace is a **model hub**. The `transformers` library is a standardized interface to
download, authenticate, and run millions of pre-trained models **on your machine** — no API keys
sent to a cloud service, no monthly bills.

**Mental model:** Transformers = PyPI for machine learning. Each model lives on huggingface.co as a
*namespace/name* (e.g., `google/gemma-2-2b-it`). The library downloads it once, caches it locally,
and runs it.

```text
                    HUGGINGFACE ECOSYSTEM
                             │
    ┌────────────────┬────────┴────────┬────────────────┐
    ▼                ▼                 ▼                ▼
  ACCOUNT          API KEY            CLI              MODELS
  (human)          (token)            (auth)           (weights)
  user + pwd       proves you         huggingface-cli  LLMs, vision,
  accept license   login locally      login            audio, etc.
                                      stores token
```

Two-line summary:

- **HuggingFace** is the host; **transformers** is the client.
- One line of code downloads a model; one more line runs it — the complexity is *authentication*
  and understanding **what model fits your hardware**.

---

> **Environment:** this project needs **no `.env` and no environment variable.**
> `huggingface-cli login` stores a token at `~/.cache/huggingface/token`, and the
> library reads it from there — so nothing to set up when you clone onto a new
> machine except running `login` again. Only *gated* models need it at all;
> everything in Part 1 downloads anonymously.
>
> See [ENVIRONMENT.md](../../../../ENVIRONMENT.md) for the projects that do use keys.

---

## Part 0 — Setup (step by step)

### Step 1: Create a HuggingFace account

Go to [huggingface.co](https://huggingface.co/) and sign up (email, username, password).

**Why:** some models (Gemma, Llama, Mistral, Phi) are **gated** — you must accept a license before
downloading. Without an account, you get `401 Unauthorized`.

### Step 2: Generate an API key

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Name: anything (e.g., "local-ml")
4. Role: **Read** (you only need to download)
5. Copy the token (`hf_...`), then **immediately save it somewhere safe** (password manager,
   not chat or email)

**Why:** this token proves you're you, and it's **as sensitive as a password**. Never paste it in
chat, commit it to git, or hardcode it. One rotation = one new token.

### Step 3: Install the libraries

```powershell
python -m pip install huggingface_hub transformers torch pillow
```

| Package | What |
|---|---|
| `huggingface_hub` | CLI + caching + auth |
| `transformers` | the model interface (`pipeline`, `AutoModel`, etc.) |
| `torch` | the AI framework (weights, inference) |
| `pillow` | image processing (for vision models) |

### Step 4: Authenticate locally

```powershell
huggingface-cli login
```

Paste your token when prompted. It saves to `~/.cache/huggingface/token` (Windows:
`C:\Users\<you>\.cache\huggingface\token`). From now on, `transformers` can download gated
models.

```text
   _|    _|  _|    _|    _|_|_|    _|_|_|  _|_|_|  _|      _|
   _|    _|  _|    _|  _|        _|          _|    _|_|    _|
   _|    _|  _|    _|  _|  _|_|  _|  _|_|    _|    _|  _|  _|
   _|    _|  _|    _|  _|    _|  _|    _|    _|    _|    _|_|
     _|_|      _|_|      _|_|_|    _|_|_|  _|_|_|  _|      _|

   To authenticate, `huggingface_hub` requires a user access token. You can find
   one here: https://huggingface.co/settings/tokens

   Token: hf_...
   Add token as git credential? (Y/n) n
   Token is valid (permission: read).
   Your token has been saved to /home/user/.cache/huggingface/token
```

Say **`n`** to "git credential" — you're not pushing code to HF repos, just downloading models.

---

## Part 1 — Your first model (text-only, CPU-friendly)

**Goal:** run a model that actually works on CPU. Gemma-4 31B (your original code) needs 60+ GB
RAM or a GPU. We'll start smaller.

```python
# main_text.py
from transformers import pipeline

# Load a small model that runs on CPU
model_name = "gpt2"  # 124M params, ~350 MB, runs in ~1 second on CPU
pipe = pipeline("text-generation", model=model_name)

# Generate text
prompt = "Once upon a time"
result = pipe(prompt, max_length=50, do_sample=True, temperature=0.7)
print(result[0]["generated_text"])
```

```powershell
python main_text.py
```

**First run:** downloads the model (~350 MB), caches it, runs inference (~1 sec).

```text
Once upon a time, there was a boy who loved to play in the rain. He would go out
every day and splash in the puddles. One day, it was raining so hard that he
```

**Second run:** no download, just uses the cached model.

| Model | Size | Speed on CPU | Gated? |
|---|---|---|---|
| `gpt2` | 124M params, ~350 MB | ~1 sec | No |
| `gpt2-medium` | 355M, ~1.5 GB | ~3 sec | No |
| `distilbert-base-uncased` | 66M, ~268 MB | instant | No |
| `meta-llama/Llama-2-7b-hf` | 7B, ~13 GB | **~30 min on CPU** | Yes (gated) |
| `google/gemma-2-2b-it` | 2B, ~5 GB | ~3–5 min on CPU | Yes (gated) |
| `google/gemma-4-31b-it` | 31B, ~62 GB | **not runnable on CPU** | Yes (gated) |

**Rule:** for CPU, stay under **2–3 GB** for reasonable speeds. Anything 7B+ needs a GPU with
CUDA.

---

## Part 2 — Understanding `pipeline()`

A **pipeline** is a convenience wrapper. It handles tokenization, inference, and decoding for you.

```python
from transformers import pipeline

pipe = pipeline(task, model=name, device=device_number)
```

| Parameter | What |
|---|---|
| `task` | what the model does: `"text-generation"`, `"sentiment-analysis"`, `"image-to-text"`, etc. |
| `model` | which weights to use (namespace/name on HuggingFace) |
| `device` | `-1` = CPU, `0` = GPU 0, `1` = GPU 1, etc. (omit for auto-detect) |

When you call `pipe(input)`, it:
1. **Tokenizes** input (text → token IDs)
2. **Runs inference** (forward pass through the model)
3. **Decodes** output (token IDs → text)

All three steps are hidden — that's why `pipeline()` is called "the easy way."

---

## Part 3 — Image-to-text (requires a vision model)

The original `main.py` uses `"image-text-to-text"` with Gemma-4. Here's a **working version** with
a smaller model:

```python
# main_vision.py
from transformers import pipeline
from PIL import Image
import requests

# Smaller vision model that actually runs on CPU
# But still slow: ~30–60 seconds on CPU
pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# Load an image from URL
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"
image = Image.open(requests.get(url, stream=True).raw)

# Generate caption
result = pipe(image)
print(result[0]["generated_text"])
```

```powershell
python main_vision.py
```

```text
downloading blip model (~990 MB)...
a pink candy with a dog on it
```

| Vision Model | Size | Speed on CPU | What it does |
|---|---|---|---|
| `Salesforce/blip-image-captioning-base` | 990M, ~1.7 GB | ~30 sec/image | describe an image |
| `google/gemma-2-2b-it` | 2B, ~5 GB | ~2–3 min/image | image Q&A (vision + chat) |
| `Qwen/Qwen2-VL-2B-Instruct` | 2B, ~5 GB | ~2–3 min/image | image Q&A |
| `google/gemma-4-31b-it` | 31B, ~62 GB | ❌ GPU only | image Q&A |

**Why slower?** Vision models process the image through an encoder (extra forward pass), then
generate text. That's two models' worth of computation.

---

## Part 4 — Authentication deep dive (why it matters)

When you call `pipeline("...", model="google/gemma-2-2b-it")`:

1. **Resolves** the model card on huggingface.co
2. **Checks** if the model is gated
3. **If gated:** reads your token from `~/.cache/huggingface/token`
4. **Downloads** the weights (first time only)
5. **Loads** weights into RAM + runs inference

If step 3 fails (no token, wrong token, token expired), you get:

```text
huggingface_hub.utils._errors.HfHubHTTPError: 401 Client Error: Unauthorized for url:
https://huggingface.co/google/gemma-2-2b-it/resolve/main/model.safetensors
```

**The token is NOT sent to the model.** It's only used for authentication to *download* weights.
Once loaded, inference is local.

---

## Part 5 — Writing your own code (beginner pattern)

```python
from transformers import pipeline

# 1. Pick a task and model
TASK = "text-generation"
MODEL = "gpt2"  # or any model from huggingface.co

# 2. Load the pipeline (first time: downloads the model)
pipe = pipeline(TASK, model=MODEL)

# 3. Prepare your input
text = "The future of AI is"

# 4. Call the pipeline
result = pipe(text, max_length=50, do_sample=True)

# 5. Extract and print
print(result[0]["generated_text"])
```

**Key patterns:**

| Task | Input | Output | Use case |
|---|---|---|---|
| `text-generation` | `"prompt text"` | `[{"generated_text": "..."}, ...]` | creative writing, completions |
| `sentiment-analysis` | `"text to classify"` | `[{"label": "POSITIVE", "score": 0.99}, ...]` | opinions, reviews |
| `image-to-text` | `PIL.Image` | `[{"generated_text": "caption"}, ...]` | captions, descriptions |
| `question-answering` | `{"question": "...", "context": "..."}` | `{"answer": "...", "score": 0.95}` | Q&A over documents |
| `summarization` | `"long text"` | `[{"summary_text": "..."}, ...]` | TL;DR |

---

## Part 6 — Downloading models manually (expert)

By default, models go to `~/.cache/huggingface/hub/`. You can change this:

```python
import os
os.environ["HF_HOME"] = "C:\\MyModels"  # use a different cache dir

from transformers import pipeline
pipe = pipeline("text-generation", model="gpt2")
```

Or pre-download a model without running it:

```powershell
huggingface-cli download google/gemma-2-2b-it
```

This downloads the model but doesn't load it into RAM. Useful for:
- Pre-staging models before deployment
- Checking available disk space
- Offline setup

---

## Gotchas & best practices

| Gotcha | Do this |
|---|---|
| `401 Unauthorized` on gated model | run `huggingface-cli login` first |
| Token pasted in code / chat | rotate it immediately at hf.co/settings/tokens |
| `CUDA out of memory` on GPU | use a smaller model or reduce `batch_size` |
| Model takes forever to download | normal — large models are 10–60 GB. Use `huggingface-cli download` in advance |
| `transformers` not found | `python -m pip install transformers` (not `pip install transformers` — remember the PATH issue!) |
| Different results each run (with `do_sample=True`) | that's intentional — sampling adds randomness. Set `seed` for reproducibility |
| Want to use a GPU? | install `torch` with CUDA: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118` (adjust cu118 for your CUDA version) |

**Command reference**

| Command | Purpose |
|---|---|
| `huggingface-cli login` | authenticate with your token |
| `huggingface-cli whoami` | check logged-in user |
| `huggingface-cli download <model>` | pre-download a model without loading it |
| `huggingface-cli scan-cache` | see what's cached locally |
| `huggingface-cli cache-system` | show cache dir (usually `~/.cache/huggingface/hub`) |

---

## Fishbone — why HuggingFace models fail

```text
                   AUTHENTICATION           HARDWARE
                         \                     /
   Token not set ────────\            GPU not found ──/
   Model is gated ───────\          Insufficient RAM /
   Wrong token ──────────\                          /
                          \                        /
                           ►  MODEL LOAD FAILS ◄
                          /                        \
   Model not found ─────/        Disk full ────────\
   Typo in model name─/          Network error ─────\
                   NETWORK                DISK SPACE
```

---

## Next steps

1. **Try `main_text.py`** — runs in ~1 sec, no GPU needed.
2. **Try `main_vision.py`** — downloads a vision model, ~30 sec on CPU.
3. **Pick a task** from Part 5's table, find a model on [huggingface.co/models](https://huggingface.co/models),
   and write your own script.
4. **For production:** learn `AutoModel` + `AutoTokenizer` (the advanced way) instead of `pipeline()`.

**Interview angle:** *"How does HuggingFace compare to OpenAI's API?"* — HF models run locally
(privacy, free, no API key leak), but you pay in compute (your GPU/CPU). OpenAI is remote (privacy
risk, costs money, instant). Trade-off: **local = free + private + slow**; **cloud = fast + paid +
risk**.
