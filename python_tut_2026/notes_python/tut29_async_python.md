# Python — Async (asyncio)

Async is the tool for **thousands of I/O operations** happening at once — HTTP requests, database queries, websocket clients, chat servers. This chapter goes deeper than the intro in tut26 Part 3: what the event loop actually is, how coroutines pause and resume, cancellation, timeouts, `asyncio.Queue`, real HTTP with `aiohttp`, and how it plays with threads and the GIL.

```text
                  ┌──────────────────────────┐
                  │         ASYNCIO          │
                  │  one thread, one loop,   │
                  │  many pausing tasks      │
                  └──────────────────────────┘
                              │
    ┌──────────────┬──────────┴──────────┬──────────────────┐
    ▼              ▼                     ▼                  ▼
  EVENT LOOP    COROUTINES            TASKS               PATTERNS
  runs tasks    async def / await     create_task         gather / TaskGroup
  when they're  pause on I/O          background jobs     Queue / Semaphore
  ready         resume on data        cancel / timeout    streams / aiohttp
```

Two-line summary:

- **asyncio** runs many tasks on **one thread**, using an **event loop** that hands control from one task to another every time one hits `await` on something slow (I/O).
- It's not parallelism — it's **cooperative multitasking**. Great for I/O, useless for CPU.

---

## Part 1 — What the event loop actually is

An **event loop** is a simple loop that does one thing on repeat: pick a task that's ready to run, run it until it hits `await`, then pick the next one.

```text
┌──────────────── EVENT LOOP ────────────────┐
│                                            │
│  while there are tasks:                    │
│    for task in ready_queue:                │
│      run it until it awaits something      │
│    check which awaits have finished        │
│      -> put those tasks back in ready      │
│    if nothing ready, sleep until an event  │
│                                            │
└────────────────────────────────────────────┘
```

Only **one task runs at any instant** — same as any single-threaded program. But because each task **pauses** whenever it hits a slow operation, the loop can juggle thousands of tasks that are all "in flight" but mostly waiting.

### The one-thread rule ★

The whole event loop lives on **one thread**. Every task shares that thread. If you block the thread (e.g., `time.sleep(1)`), **every task stops** for that second. That's the #1 bug in async code (covered in Part 8).

### Where does asyncio actually fit?

| Tool             | Uses many threads? | Uses many cores? | Best for                            |
|------------------|--------------------|------------------|-------------------------------------|
| `threading`      | Yes                | No (GIL)         | Dozens of blocking I/O calls        |
| `multiprocessing`| Yes (processes)    | Yes              | CPU-heavy math over big inputs      |
| **`asyncio`**    | **No — one thread**| **No**           | **Thousands of tiny I/O ops**       |

Rule: if you have 5,000 open HTTP requests, threading crushes your memory (1 MB per thread) and asyncio doesn't blink.

---

## Part 2 — Coroutines — `async def` and `await`

A **coroutine** is a function that can pause.

```python
async def hello():
    print("start")
    await asyncio.sleep(1)     # pause here — let the loop run someone else
    print("end")
```

Two new words:

- **`async def name():`** — this function is a coroutine. Calling it does NOT run it — it returns a coroutine **object**.
- **`await something`** — pause here until `something` is ready. Only usable inside `async def`.

### Calling ≠ running (the #1 gotcha)

```python
async def hi():
    print("hi")

hi()               # ← nothing prints. You got back a coroutine object.
```

You must **do one of three things** to actually run it:

- `asyncio.run(hi())` — top-level launcher
- `await hi()` — from inside another coroutine
- `asyncio.create_task(hi())` — schedule on the running loop

If you see the warning `RuntimeWarning: coroutine 'hi' was never awaited`, you called it without awaiting.

### `asyncio.run(coro)` — the entry point

```python
import asyncio

async def main():
    print("running")
    await asyncio.sleep(0.5)
    print("done")

asyncio.run(main())
```

`asyncio.run` creates a fresh event loop, runs your coroutine, and shuts the loop down. Call it **once**, at the top level of your program.

Rule ★: **never call `asyncio.run` inside another `async` function** — that would try to nest event loops. Use `await` instead.

---

## Part 3 — Tasks — `create_task` and `gather`

A **task** is a coroutine that's been scheduled on the event loop and is running in the background.

### `create_task` — fire and forget (until you `await` it)

```python
import asyncio

async def work(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} done"

async def main():
    t1 = asyncio.create_task(work("A", 1))     # already running from here
    t2 = asyncio.create_task(work("B", 2))     # already running from here

    print("both scheduled")
    print(await t1)                            # 1s in — 'A done'
    print(await t2)                            # 2s in — 'B done'

asyncio.run(main())
```

```text
both scheduled
A done
B done
```

Between the `create_task` calls and the `await`s, both tasks are running concurrently on the loop.

### `gather` — launch many, wait for all

```python
async def fetch(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} content"

async def main():
    results = await asyncio.gather(
        fetch("A", 1),
        fetch("B", 1),
        fetch("C", 1),
    )
    print(results)                             # in the order you passed

asyncio.run(main())
```

Three 1-second fetches → total ≈ **1 second**, not 3. Results come back **in input order** regardless of which finished first.

### `create_task` vs `gather`

| You want to…                                    | Use              |
|-------------------------------------------------|------------------|
| Launch N and wait for all in one call           | `gather`         |
| Start something in the background, do other work, then wait later | `create_task` |
| Cancel a running task                           | `create_task` + `.cancel()` |
| Any exception should cancel the rest            | `TaskGroup` (3.11+, see Part 4) |

### `gather(return_exceptions=True)`

By default, `gather` re-raises the first exception and drops the rest. Sometimes you want ALL of them:

```python
async def flaky(i):
    if i == 1:
        raise ValueError("boom")
    return i

async def main():
    results = await asyncio.gather(
        flaky(0), flaky(1), flaky(2),
        return_exceptions=True,
    )
    print(results)          # [0, ValueError('boom'), 2]
```

Successful results and exceptions come back mixed. You inspect them yourself.

---

## Part 4 — `TaskGroup` (Python 3.11+) — the modern way ★

`asyncio.TaskGroup` is the recommended replacement for `gather` from 3.11 onwards. It gives you **structured concurrency** — if any task fails, all sibling tasks are cancelled and the error propagates cleanly.

```python
# Python 3.11+ only:
import asyncio

async def worker(name, s):
    await asyncio.sleep(s)
    return name

async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(worker("A", 1))
        t2 = tg.create_task(worker("B", 2))
    # when we leave the `with` block, all tasks are done
    print(t1.result(), t2.result())

# asyncio.run(main())
```

Why it's better than `gather`:

- If any one task raises, **all the others are cancelled automatically**. `gather` would silently keep them running.
- The `async with` block **cannot be exited early** with dangling tasks. Cleaner shutdown.
- Multiple exceptions become an `ExceptionGroup` — you can inspect all of them at once.

You're on Python 3.8 so this is not available yet — stick to `gather` for now. When you upgrade to 3.11+, switch to `TaskGroup` by default.

---

## Part 5 — Timeouts and cancellation

Never let a network call hang forever. Two levels: `wait_for` (with a deadline) and `.cancel()` (from the outside).

### `asyncio.wait_for` — deadline for one coroutine

```python
async def slow():
    await asyncio.sleep(5)
    return "eventually"

async def main():
    try:
        result = await asyncio.wait_for(slow(), timeout=1.0)
    except asyncio.TimeoutError:
        print("timed out")

asyncio.run(main())
```

```text
timed out
```

`wait_for` runs the coroutine, sets a 1-second timer, and if the coroutine hasn't finished, it **cancels the coroutine and raises `TimeoutError`**.

Rule ★: **every network call in production should have a timeout.** Otherwise a dead server freezes your program forever.

### Manual cancellation with `.cancel()`

```python
async def worker():
    try:
        while True:
            print("tick")
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("cancelled cleanly")
        raise            # re-raise so the loop knows we accepted the cancel

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(1.5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

asyncio.run(main())
```

```text
tick
tick
tick
cancelled cleanly
```

What happens: `task.cancel()` sends a `CancelledError` **into** the task at its next `await`. The task can catch it, do cleanup, then re-raise. You **should always re-raise** — swallowing `CancelledError` is a common bug that makes tasks impossible to stop.

### `asyncio.timeout()` (Python 3.11+) — context-manager form

```python
# Python 3.11+ only:
async with asyncio.timeout(1.0):
    await slow()
```

Cleaner than `wait_for` for wrapping multi-line async blocks. Not available in 3.8.

---

## Part 6 — Concurrency primitives — Queue, Semaphore, Event, Lock

Async versions of the classic thread-sync tools. Same names, different behavior — they yield to the loop while waiting.

### `asyncio.Queue` — producer/consumer

```python
import asyncio

async def producer(q):
    for i in range(5):
        await q.put(i)
        await asyncio.sleep(0.1)
    await q.put(None)                # sentinel: "no more"

async def consumer(q):
    while True:
        item = await q.get()
        if item is None:
            return
        print("got:", item)

async def main():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))

asyncio.run(main())
```

Same producer/consumer pattern as `multiprocessing.Queue`, but staying in one thread and one loop.

### `asyncio.Semaphore` — limit concurrency ★

The single most useful primitive. Cap how many tasks run at once — for rate-limiting an API, controlling a download pool, avoiding "too many open files" errors.

```python
import asyncio

async def fetch(url, sem):
    async with sem:                  # at most N concurrent
        await asyncio.sleep(1)       # pretend to hit the URL
        return f"{url} OK"

async def main():
    urls = [f"http://site/{i}" for i in range(20)]
    sem = asyncio.Semaphore(5)       # 5 concurrent fetches max
    results = await asyncio.gather(*[fetch(u, sem) for u in urls])
    print("all done, got", len(results))

asyncio.run(main())
```

20 fetches, cap of 5 at a time → total ≈ 4 seconds (4 batches × 1s), not 1s (all-at-once) and not 20s (serial).

### `asyncio.Event` — one-time signal

```python
import asyncio

async def waiter(ev):
    print("waiting")
    await ev.wait()                  # blocks until ev.set()
    print("go!")

async def main():
    ev = asyncio.Event()
    asyncio.create_task(waiter(ev))
    await asyncio.sleep(1)
    ev.set()
    await asyncio.sleep(0.1)         # let waiter print

asyncio.run(main())
```

Simple "start-when-I-say-go" pattern.

### `asyncio.Lock` — mutual exclusion

Only needed if two async tasks would race on a shared mutable object. Because tasks only switch at `await`, most single-threaded async code doesn't need locks. When you do:

```python
lock = asyncio.Lock()
async with lock:
    shared_state += 1
```

---

## Part 7 — Real HTTP concurrency with `aiohttp`

The classic use case. `requests` is **blocking** — it holds the event-loop thread hostage. `aiohttp` is async-native.

```python
# Requires: pip install aiohttp
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return resp.status, await resp.text()

async def main():
    urls = [f"https://httpbin.org/delay/1" for _ in range(20)]
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch(session, u) for u in urls])
    print("got", len(results), "responses")

asyncio.run(main())
```

20 requests to an endpoint that sleeps 1 second → total **~1 second**, not 20. That's the shape of nearly all real async code.

Rate-limit with a semaphore:

```python
sem = asyncio.Semaphore(10)                 # 10 in-flight max
async def fetch(session, url):
    async with sem:
        async with session.get(url) as r:
            return await r.text()
```

That combo (`aiohttp` + `asyncio.gather` + `asyncio.Semaphore`) covers 90% of real-world async scrapers.

---

## Part 8 — The blocking-code rule ★

The single most-common async bug: putting a blocking call inside a coroutine.

```python
# BAD
async def download(url):
    time.sleep(1)                    # blocks the event loop!
    requests.get(url)                # blocks too (sync library)
```

Because the event loop lives on ONE thread, `time.sleep` freezes the entire program. Every other task waits. All the "concurrency" you thought you had disappears.

### Fixes

**1. Use an async-native library.**

- `requests` → `aiohttp` / `httpx`
- `sqlite3` → `aiosqlite`
- `psycopg2` → `asyncpg`
- `open(...).read()` → `aiofiles`
- `time.sleep` → `asyncio.sleep`

**2. Delegate to a thread pool.**

For any blocking library you can't replace:

```python
import asyncio

def blocking(n):
    time.sleep(n)                    # sync, blocking
    return f"slept {n}"

async def main():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, blocking, 1)
    # None → use the default ThreadPoolExecutor
    print(result)

asyncio.run(main())
```

The blocking call runs **on a background thread** so the event loop stays free. On Python 3.9+, the shorter `asyncio.to_thread(blocking, 1)` does the same thing.

### How to spot the bug

If your "async" code is no faster than plain sync code, you almost certainly have a blocking call in there. Common culprits:

- Reading a file with `open(...)`
- Any `requests.` call
- Any DB query with a non-async driver
- `time.sleep` (obvious in hindsight)
- CPU-heavy loops — no library will help; those need `multiprocessing`

---

## Part 9 — Streams — high-level networking

`asyncio` ships an async TCP/UDP API without any extra library. Two examples.

### Simple echo client

```python
import asyncio

async def main():
    reader, writer = await asyncio.open_connection("example.com", 80)
    writer.write(b"GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")
    await writer.drain()

    data = await reader.read(200)     # first 200 bytes
    print(data.decode(errors="replace"))
    writer.close()
    await writer.wait_closed()

# asyncio.run(main())
```

For real HTTP you want `aiohttp`, but streams are perfect for custom protocols, redis clients, chat servers.

### Simple TCP server

```python
import asyncio

async def handle(reader, writer):
    data = await reader.read(100)
    writer.write(data)                # echo back
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle, "127.0.0.1", 8888)
    async with server:
        await server.serve_forever()

# asyncio.run(main())
```

Handles thousands of connections in one thread, one process.

---

## Part 10 — Async and the GIL

Same GIL story as tut28 — with one twist.

- **asyncio runs on one thread**, so the GIL is basically always held by that thread. There's no contention with other Python threads.
- Every `await` yields to the event loop, which then picks another **task** to run — still on the same thread, still holding the GIL.
- Removing the GIL (free-threaded Python 3.13+) does **not** parallelize an asyncio program. It's one thread by design.

The only time GIL matters for async is when you use `run_in_executor` — that spawns real threads (or processes), and those threads follow the usual GIL rules.

---

## Part 11 — Async vs threads vs processes — pick the tool ★

| Situation                                          | Best fit         | Why                              |
|----------------------------------------------------|------------------|----------------------------------|
| A few dozen HTTP calls                             | `threading`      | Simple, no async library needed  |
| Thousands of HTTP calls / sockets                  | **`asyncio`**    | Cheap tasks, small memory        |
| Long-lived chat/game server (many clients)         | **`asyncio`**    | Handles 10k+ clients easily      |
| Reading many files                                 | `threading` or `asyncio` + `aiofiles` | Both work |
| Heavy CPU work (image processing, ML)              | `multiprocessing`| Bypass the GIL                   |
| Mix of I/O and CPU                                 | `asyncio` + `run_in_executor` for the CPU part | Best of both |
| Single script, one URL to fetch                    | `requests`       | Async isn't worth the ceremony   |

Rule ★: **async wins on scale.** 100 tasks is fine anywhere; 10,000 is only comfortable in asyncio.

---

## Part 12 — Common pitfalls

### 1. Calling `async` functions without awaiting

```python
async def do(): print("hi")
do()                                # coroutine created but never runs
```

Fix: `asyncio.run(do())`, `await do()`, or `asyncio.create_task(do())`.

### 2. Blocking calls inside a coroutine

```python
async def bad():
    time.sleep(1)                    # freezes the loop
```

Fix: `await asyncio.sleep(1)`, or `run_in_executor` for third-party sync libs.

### 3. Swallowing `CancelledError`

```python
async def worker():
    try:
        ...
    except asyncio.CancelledError:
        pass                         # BAD — task can't be cancelled
```

Fix: log if you want, then `raise`.

### 4. Nesting `asyncio.run`

```python
async def outer():
    asyncio.run(inner())             # RuntimeError: cannot be called from a running event loop
```

Fix: `await inner()`.

### 5. Forgetting to `await` an `async with`

```python
# BAD — TypeError: coroutine object is not iterable
with session.get(url) as r:          # missing async
    ...
```

Fix: `async with session.get(url) as r:`.

### 6. Sharing an aiohttp `ClientSession` across many tasks... wait, do share it

That's the correct pattern. **One session per program** (or per request lifecycle), passed to all tasks. Creating a new session per request is the bug.

### 7. CPU-heavy loop inside a coroutine

```python
async def bad():
    total = 0
    for i in range(10**7):           # no awaits — one long block
        total += i * i
```

Fix: offload with `loop.run_in_executor(None, cpu_hog)`, or use processes.

### 8. Fire-and-forget tasks that get garbage-collected

```python
async def main():
    asyncio.create_task(work())      # task reference lost — may get GC'd
    await asyncio.sleep(2)
```

Fix: keep a reference (`task = asyncio.create_task(...)`, keep it in a list).

---

## Part 13 — Interview angle ★

- **What is asyncio?** A single-threaded, single-loop framework for running many I/O-bound coroutines concurrently.
- **How does it differ from threading?** No OS threads — cooperative pausing at `await` points. Cheap: one task ~ 1 KB vs one thread ~ 1 MB.
- **What is a coroutine?** A function that can pause with `await` and resume later.
- **What is the event loop?** A loop that runs ready tasks one at a time, resumes them when their awaited thing is done.
- **Why can `time.sleep` break my async program?** It's a synchronous, blocking call — the event loop can't switch to another task while it runs.
- **Can asyncio use multiple CPU cores?** No — it's single-threaded. For CPU parallelism, use `multiprocessing` (or offload with `run_in_executor(ProcessPoolExecutor())`).
- **What is `gather` vs `create_task`?** `create_task` launches a background job you `await` later. `gather` launches many and waits for all.
- **What replaces `gather` in 3.11+?** `asyncio.TaskGroup` — structured concurrency with automatic cancellation on failure.
- **What is `run_in_executor`?** A bridge that runs a blocking sync function on a background thread (or process) so the loop stays free.
- **When should I NOT use async?** When your work is CPU-bound, when you only have a couple of I/O calls, or when the ecosystem you need (like a DB driver) isn't async-friendly.

---

## Part 14 — Quick reference

```text
# ENTRY POINT
import asyncio
async def main():
    ...
asyncio.run(main())              # call once at the top level

# COROUTINES
async def work():
    await asyncio.sleep(1)       # yield to the loop while waiting
    return "done"

# LAUNCH MANY, WAIT FOR ALL
results = await asyncio.gather(work(), work(), work())
# 3.11+ preferred:
# async with asyncio.TaskGroup() as tg:
#     tg.create_task(work())

# BACKGROUND TASK
t = asyncio.create_task(work())
result = await t

# TIMEOUTS
await asyncio.wait_for(work(), timeout=1.0)          # 3.4+
# async with asyncio.timeout(1.0):                    # 3.11+

# CANCELLATION
t.cancel()
try:
    await t
except asyncio.CancelledError:
    ...

# CONCURRENCY PRIMITIVES
asyncio.Queue()                  # producer/consumer
asyncio.Semaphore(N)             # cap concurrent tasks (VERY common)
asyncio.Event()                  # one-time signal
asyncio.Lock()                   # rarely needed

# BRIDGES
result = await loop.run_in_executor(None, blocking_fn, arg)  # 3.4+
# 3.9+ preferred:
# result = await asyncio.to_thread(blocking_fn, arg)

# LIBRARIES
# HTTP:      aiohttp, httpx (async mode)
# Files:     aiofiles
# Postgres:  asyncpg
# Sqlite:    aiosqlite
# Redis:     redis.asyncio

# THE RULES
# 1. async is for MANY I/O tasks; not for CPU
# 2. never block the loop (no time.sleep, no requests, no big Python loops)
# 3. every network call needs a timeout
# 4. keep references to tasks you create
# 5. re-raise CancelledError after cleanup
```
