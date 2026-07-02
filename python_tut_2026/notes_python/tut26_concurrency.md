# Python Concurrency

Doing **more than one thing at once**. Python offers three tools, each solving a different problem.

```text
                  ┌──────────────────────────┐
                  │      CONCURRENCY         │
                  │  do many things at once  │
                  └──────────────────────────┘
                            │
    ┌───────────────────┬───┴───────────────┬─────────────────────┐
    ▼                   ▼                   ▼                     ▼
  THREADS           PROCESSES            ASYNCIO             concurrent.futures
  threading         multiprocessing      async def / await   ThreadPoolExecutor
  I/O-bound work    CPU-bound work       many I/O tasks       ProcessPoolExecutor
  (GIL applies)     (bypass GIL)         cooperative loop     unified pool API
```

Rule of thumb (memorize this):

- **I/O-bound?** — threads or asyncio.
- **CPU-bound?** — processes.
- **Many small I/O ops?** — asyncio.

---

## The GIL ★ — the one concept you must know

CPython has a **Global Interpreter Lock**. At any instant, **only one thread** executes Python bytecode. Multiple threads exist, but they take turns.

Consequence:

- **CPU-bound Python code doesn't speed up with threads.** Two threads doing math take the same time as one.
- **I/O-bound code DOES speed up with threads** — while one thread waits on the network/disk, another runs.
- **Multiprocessing bypasses the GIL** — each process has its own interpreter, so CPU work parallelizes across cores.

This is why the tool you pick depends entirely on whether the work is CPU-bound or I/O-bound.

---

# Part 1 — `threading`

Best for **I/O-bound** work: HTTP requests, DB queries, file downloads, waiting on sockets.

## Simple thread

```python
import threading
import time

def worker(name):
    print(f"[{name}] starting")
    time.sleep(1)
    print(f"[{name}] done")

t = threading.Thread(target=worker, args=("A",))
t.start()
t.join()          # wait for it to finish
print("main done")
```

```text
[A] starting
[A] done
main done
```

`start()` launches the thread. `join()` blocks until it finishes.

## Many threads at once

```python
import threading
import time

def worker(name):
    time.sleep(1)
    print(f"[{name}] done")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(f"T{i}",))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("all done")
```

Five threads sleep in parallel — total ≈ **1 second**, not 5. Because sleeping releases the GIL, other threads run.

## Passing kwargs

```python
import threading

def greet(name, greeting="Hi"):
    print(f"{greeting}, {name}!")

t = threading.Thread(target=greet, args=("Akshay",), kwargs={"greeting": "Hello"})
t.start()
t.join()
```

## When threads DON'T help — CPU-bound work

```python
import threading
import time

def cpu_hog(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

N = 20_000_000

# Two threads doing the same CPU work — no speedup
t1 = threading.Thread(target=cpu_hog, args=(N,))
t2 = threading.Thread(target=cpu_hog, args=(N,))

start = time.perf_counter()
t1.start(); t2.start()
t1.join(); t2.join()
print("2 threads:", round(time.perf_counter() - start, 2), "s")
```

You'll see it's roughly the same as running twice in serial. The GIL is why.

## Locks — protecting shared state

If two threads mutate a shared variable, you get races. Use a `Lock`.

```python
import threading

counter = 0
lock = threading.Lock()

def bump(n):
    global counter
    for _ in range(n):
        with lock:                    # acquire + release automatically
            counter += 1

threads = [threading.Thread(target=bump, args=(100_000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)     # 400000 — exactly, thanks to the lock
```

Without the `with lock:`, you'd sometimes see a smaller number because `counter += 1` isn't atomic (it's a read + increment + write).

## Daemon threads — die with the main thread

```python
import threading, time

def background():
    while True:
        print("tick")
        time.sleep(1)

t = threading.Thread(target=background, daemon=True)
t.start()

time.sleep(2.5)
print("main exiting — daemon dies with me")
```

Daemon threads don't block program exit. Non-daemon threads do — the program waits.

---

# Part 2 — `multiprocessing`

Best for **CPU-bound** work: heavy computation, image processing, ML preprocessing, data crunching. Each process has its own Python interpreter, so the GIL doesn't apply.

## Simple process

```python
from multiprocessing import Process
import time

def worker(name):
    print(f"[{name}] starting")
    time.sleep(1)
    print(f"[{name}] done")

if __name__ == "__main__":     # <-- required on Windows / macOS spawn
    p = Process(target=worker, args=("A",))
    p.start()
    p.join()
    print("main done")
```

**The `if __name__ == "__main__":` guard is not optional** on Windows/macOS — child processes re-import the script, and without the guard they'd spawn their own children, forever.

## CPU-bound parallelism that ACTUALLY parallelizes

```python
from multiprocessing import Process
import time

def cpu_hog(n):
    total = 0
    for i in range(n):
        total += i * i

N = 20_000_000

if __name__ == "__main__":
    procs = [Process(target=cpu_hog, args=(N,)) for _ in range(4)]

    start = time.perf_counter()
    for p in procs: p.start()
    for p in procs: p.join()
    print("4 processes:", round(time.perf_counter() - start, 2), "s")
```

On a 4-core machine, 4 processes finish in roughly the time of 1 — real parallelism.

## Passing data — Queue, Pipe

Processes don't share memory. Send data via `Queue`.

```python
from multiprocessing import Process, Queue

def producer(q):
    for i in range(5):
        q.put(i * i)
    q.put(None)                # sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            return
        print("got:", item)

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start(); p2.start()
    p1.join(); p2.join()
```

## `Pool` — parallel `map`

For "run this function on many inputs", `Pool` is the cleanest API.

```python
from multiprocessing import Pool

def square(n):
    return n * n

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        results = pool.map(square, range(10))
    print(results)     # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

`Pool.map` is a **parallel** replacement for the built-in `map()`. Perfect for CPU-bound batch work.

## Pitfalls with processes

- Arguments and return values must be **picklable** (most things are; lambdas and local functions are NOT).
- Startup is slower than threads.
- Data isn't shared — copy semantics via IPC.
- On Windows/macOS, the `if __name__ == "__main__":` guard is mandatory.

---

# Part 3 — `asyncio`

Best for **many small I/O operations**: hundreds of HTTP requests, thousands of open sockets, chat servers, web scrapers.

One thread, one process, but many **coroutines** cooperatively pausing while waiting on I/O.

## Coroutines — `async def` + `await`

```python
import asyncio

async def hello():
    print("start")
    await asyncio.sleep(1)     # yields control to the loop
    print("end")

asyncio.run(hello())
```

```text
start
end
```

`async def` defines a **coroutine function**. Calling it returns a **coroutine object** — nothing runs until you hand it to `asyncio.run(...)` or `await` it.

## Running many coroutines concurrently

`asyncio.gather` runs several coroutines at once and waits for all.

```python
import asyncio
import time

async def fake_download(name, seconds):
    print(f"[{name}] downloading...")
    await asyncio.sleep(seconds)
    return f"{name} content"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(
        fake_download("A", 1),
        fake_download("B", 1),
        fake_download("C", 1),
    )
    print("took:", round(time.perf_counter() - start, 2), "s")
    print(results)

asyncio.run(main())
```

Three "downloads" of 1 second each — total ≈ **1 second**, not 3. All three await concurrently.

## `create_task` — fire off, join later

```python
import asyncio

async def work(name, s):
    await asyncio.sleep(s)
    return f"{name} done"

async def main():
    t1 = asyncio.create_task(work("A", 1))
    t2 = asyncio.create_task(work("B", 2))

    # do other stuff here — the tasks are already running
    print("started")

    result1 = await t1
    result2 = await t2
    print(result1, result2)

asyncio.run(main())
```

`create_task` schedules a coroutine to run in the background. `await` on it gets the result.

## The rule that catches everyone ★

**Never call blocking code inside an async function.**

```python
import asyncio
import time

# BAD — time.sleep blocks the whole event loop
async def bad():
    time.sleep(1)           # <-- blocks!

# GOOD — asyncio.sleep releases control
async def good():
    await asyncio.sleep(1)
```

`time.sleep`, `requests.get`, `open(...).read()`, `input(...)` — all blocking. Inside a coroutine, they freeze **every** other coroutine on the loop.

Solutions:

- Use async-native libraries (`httpx`, `aiofiles`, `asyncpg`).
- Or delegate to a thread pool (see `run_in_executor` below, and `asyncio.to_thread` in 3.9+).

## Running blocking code from asyncio

```python
import asyncio, time

def blocking(n):
    time.sleep(n)          # a synchronous, blocking function
    return f"slept {n}"

async def main():
    loop = asyncio.get_running_loop()
    # Run blocking() in a thread pool without freezing the event loop
    result = await loop.run_in_executor(None, blocking, 1)
    print(result)

asyncio.run(main())
```

On Python 3.9+, `asyncio.to_thread(blocking, 1)` is the shorter form.

## Timeouts

```python
import asyncio

async def slow():
    await asyncio.sleep(5)
    return "done"

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

---

# Part 4 — `concurrent.futures` — the unified interface

Same API for threads OR processes. Often the cleanest choice.

## `ThreadPoolExecutor` — for I/O-bound tasks

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch(url):
    time.sleep(1)           # pretend to hit the network
    return f"{url} OK"

urls = [f"https://site.com/{i}" for i in range(5)]

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(fetch, urls))

print(results)
```

Five fake fetches in ≈1 second, not 5. Same benefit as raw threads, cleaner API.

## `ProcessPoolExecutor` — for CPU-bound tasks

```python
from concurrent.futures import ProcessPoolExecutor

def square(n):
    return n * n

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(square, range(10)))
    print(results)
```

Drop-in for `ThreadPoolExecutor` but uses processes — real CPU parallelism.

## `submit` + `as_completed` — flexible dispatch

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random

def work(n):
    time.sleep(random.random())
    return f"task {n} done"

with ThreadPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(work, i) for i in range(6)]
    for fut in as_completed(futures):
        print(fut.result())
```

`submit` starts a task, returns a `Future`. `as_completed` yields futures in the order they finish — great for streaming results as they arrive.

---

## Picking the right tool

| Situation                                  | Best tool                                           |
|--------------------------------------------|-----------------------------------------------------|
| Many CPU-heavy tasks                       | `multiprocessing` / `ProcessPoolExecutor`           |
| Many blocking I/O calls (few dozen)        | `threading` / `ThreadPoolExecutor`                  |
| Thousands of concurrent I/O connections    | `asyncio`                                           |
| Simple parallel `map` over data            | `Pool.map` (procs) or `ex.map` (threads or procs)   |
| Real-time streaming / server               | `asyncio` with an async framework                   |
| Mixing async and blocking libraries        | `asyncio` + `run_in_executor` (or `to_thread` 3.9+) |

---

## Common pitfalls

### 1. Using threads for CPU work

```python
# Doesn't speed up — GIL
threading.Thread(target=heavy_math).start()
threading.Thread(target=heavy_math).start()
```

Fix: use `multiprocessing` or `ProcessPoolExecutor`.

### 2. Sharing mutable state across threads without a lock

```python
counter = 0
def bump():
    global counter
    for _ in range(100_000):
        counter += 1          # race! not atomic
```

Fix: `with lock:` around the mutation.

### 3. Blocking calls inside an async function

```python
async def bad():
    time.sleep(1)             # freezes the entire event loop
```

Fix: use `await asyncio.sleep(1)`, or `run_in_executor` for third-party blocking libs.

### 4. Forgetting `if __name__ == "__main__":` with multiprocessing

Without the guard on Windows/macOS, child processes re-import the script and spawn more children. Infinite explosion.

### 5. Passing unpicklable data to a process

Lambdas, local functions, open sockets — none can be pickled. `TypeError`.

### 6. Daemon threads killing needed work

If your worker needs to finish before exit, don't make it a daemon.

### 7. Awaiting a coroutine you didn't schedule

```python
async def main():
    my_coro = do_work()       # just an object — nothing runs
    # await my_coro             ← runs it now
```

Calling an async function doesn't start it. You must `await` it (or `create_task`).

### 8. Too many workers

Threads have overhead. Processes have MORE overhead (memory, IPC). More workers ≠ faster past your core count for CPU work, or past your I/O saturation point for I/O work.

---

## Interview angle

- **Why can't Python threads use multiple cores for CPU work?** The GIL — only one thread runs Python bytecode at a time.
- **Threads vs processes?** Threads share memory (fast comm, but need locks). Processes are isolated (safe, but pickle everything through IPC).
- **When to use `asyncio` over threads?** When you have **many** simultaneous I/O ops (thousands of sockets). Threads cost ~1MB each; coroutines cost bytes.
- **What's a "coroutine"?** A function that can pause (`await`) and resume, letting others run in between.
- **Why do async libraries exist (`httpx`, `aiofiles`)?** So you can `await` I/O instead of blocking. Standard libraries like `requests` and `open()` do NOT return awaitables.

---

## Quick reference

```text
# THREADING — I/O-bound work
from threading import Thread, Lock
t = Thread(target=fn, args=(...,), daemon=False)
t.start(); t.join()
lock = Lock()
with lock: shared += 1

# MULTIPROCESSING — CPU-bound work
from multiprocessing import Process, Pool, Queue
if __name__ == "__main__":               # required guard
    p = Process(target=fn, args=(...,))
    p.start(); p.join()

    with Pool(4) as pool:
        results = pool.map(fn, inputs)   # parallel map

# ASYNCIO — many I/O ops in one thread
import asyncio
async def work(): await asyncio.sleep(1); return "x"

asyncio.run(work())                       # entry point
await asyncio.gather(a(), b(), c())       # concurrent
t = asyncio.create_task(work())           # fire & join later
await asyncio.wait_for(work(), timeout=1) # timeout

# CONCURRENT.FUTURES — unified pool API
from concurrent.futures import (
    ThreadPoolExecutor, ProcessPoolExecutor, as_completed
)
with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fn, inputs))
    futures = [ex.submit(fn, x) for x in inputs]
    for f in as_completed(futures):
        print(f.result())

# CHOOSING:
#   CPU-bound  -> ProcessPoolExecutor / multiprocessing
#   I/O-bound  -> ThreadPoolExecutor / threading / asyncio
#   Many I/Os  -> asyncio
```
