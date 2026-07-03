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
    time.sleep(1)                 # pretend to do something for 1 second
    print(f"[{name}] done")

t = threading.Thread(target=worker, args=("A",))
t.start()
t.join()          # main waits for it to finish
print("main done")
```

```text
[A] starting
[A] done
main done
```

`start()` launches the thread. `join()` blocks until it finishes.

## The mental model

```text
main:  [ create t ] [ start ] --> [ join, waiting... ] [ print "main done" ]
                       |
                       └──> thread A:  [ print "starting" ] [ sleep 1s ] [ print "done" ]
```

Two lanes running side by side. `join` is the "merge back into one lane" line.

## Many threads at once

```python
import threading
import time

def worker(name):
    time.sleep(1)     # pretend to wait for something (network, file, etc.)
    print(f"[{name}] done")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(f"T{i}",))
    t.start()
    threads.append(t)    # save it so we can wait for it later

for t in threads:
    t.join()             # main waits until this thread finishes

print("all done")
```

Each turn of the loop:

1. Creates a thread that will run `worker("T0")`, then `worker("T1")`, etc.
2. `t.start()` — fires it off immediately. The loop does not wait; it moves on.
3. Saves it in the `threads` list.

So after the loop finishes (which takes microseconds), all 5 threads are already running at the same time, each sleeping.

Five threads sleep in parallel — total ≈ **1 second**, not 5. Because sleeping releases the GIL, other threads run.

We loop through the saved threads and `join` each one. Main can't reach "all done" until every thread has finished.

### The output

```text
[T0] done
[T1] done
[T2] done
[T3] done
[T4] done
all done
```

(Order of the 5 lines may vary — they finish roughly at the same instant.)

### The key insight ★

All 5 threads sleep at the same time. Total wall-clock time ≈ **1 second**, not 5.

```text
Serial (no threads):     [sleep 1s][sleep 1s][sleep 1s][sleep 1s][sleep 1s]  → 5 seconds
Threaded:                [sleep 1s]                                          → 1 second
                         [sleep 1s]  ← all running in parallel
                         [sleep 1s]
                         [sleep 1s]
                         [sleep 1s]
```

### Why this is safe (even with the GIL)

**The GIL, in one sentence:**

> In Python, only one thread can run Python code at a time.

That's it. Not "one at a time per second" — one at a time, period. There's a lock (the Global Interpreter Lock) inside Python that only one thread can hold. Whoever holds it, runs.

`time.sleep` releases the GIL — it's basically "I'm not doing Python work, someone else can run." Same for network calls, disk reads, DB queries. That's why threads are perfect for I/O-bound work.

If `worker` were doing math instead of sleeping, all 5 threads would fight for the GIL and take the same total time as running one at a time. That's the whole reason processes exist.

Drawn as a timeline:

```text
                     GIL holder →
time: 0.000s      Thread T0 runs Python.  Reaches time.sleep(1).
                  T0 releases the GIL, goes to sleep.

time: 0.000001s   Thread T1 grabs the GIL, runs.  Reaches time.sleep(1).
                  T1 releases the GIL, goes to sleep.

time: 0.000002s   T2 grabs GIL → sleep → release.
time: 0.000003s   T3 grabs GIL → sleep → release.
time: 0.000004s   T4 grabs GIL → sleep → release.

time: 0.000005s   All 5 threads are sleeping.  Nobody holds the GIL.
                  (Main thread is at the join loop, also mostly waiting.)

time: 1.000s      OS wakes them up.  They queue for the GIL again,
                  print their message one by one (microseconds apart),
                  and finish.
```

Total wall-clock: **~1 second. Not 5.** Because the actual "wait" happened outside Python, in parallel.

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

start = time.perf_counter()   # start stopwatch
t1.start(); t2.start()        # launch both threads
t1.join(); t2.join()          # wait for both to finish
print("2 threads:", round(time.perf_counter() - start, 2), "s")
```

You'll see it's roughly the same as running twice in serial. The GIL is why.

### What you'd naively expect

"Two workers → half the time!" If `cpu_hog(N)` takes 2 seconds alone, then two of them running at the same time should take… 2 seconds. Right?

### What actually happens

They take **the same time** as running them one after the other. Roughly:

```text
1 thread:   ~2.0 s
2 threads:  ~2.0 s   (same!)  ← the surprise
```

Sometimes even a hair slower, because the GIL switches back and forth between the two threads and that switching costs a little time.

### Why? Back to the GIL rule

> Only one thread can run Python code at a time.

Both threads want to run pure Python math. Both need the GIL. So they take turns:

```text
time 0.000s   T1 runs Python.  Does some multiplies.
time 0.005s   Python says "5 ms is up, next!"  T1 releases GIL.
time 0.005s   T2 grabs GIL.  Does some multiplies.
time 0.010s   T2 releases.  T1 grabs it back.  And so on.
...
time 2.000s   All 20M+20M multiplies done.
```

At any single instant, only one thread is actually computing. Even though there are 2 CPU cores available, they're wasted. The GIL forces them to sit in a queue.

### Compare to the sleep example

| Code            | What worker does | GIL held?               | 2 threads speedup?       |
|-----------------|------------------|-------------------------|--------------------------|
| `time.sleep(1)` | Waiting on OS    | Released while sleeping | ✅ finishes together     |
| `cpu_hog(N)`    | Doing math       | Held the whole time     | ❌ same as serial        |

That's the whole lesson.

### The fix

If you actually want 2 CPU cores working at the same time on Python math, use **processes**, not threads:

```python
from multiprocessing import Process

p1 = Process(target=cpu_hog, args=(N,))
p2 = Process(target=cpu_hog, args=(N,))
p1.start(); p2.start()
p1.join(); p2.join()
```

Each process has its own Python interpreter with its own GIL, so they don't fight each other. On your 8-core box, that would finish in roughly half the time. That's Part 2 of the file (`multiprocessing`).



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

This one is about the danger of sharing data between threads, and how a `Lock` fixes it. We build it up in two steps: **why we need a lock**, then **how the code uses one**.

### Step 1 — Why we need a lock

Imagine you deleted the `with lock:` line. What could go wrong with a simple `counter += 1`?

Here's the hidden truth: `counter += 1` is **not one action**. Python actually does three tiny steps:

```text
1. READ counter's current value  →  say it's 42
2. ADD 1                          →  compute 43
3. WRITE 43 back into counter
```

Threads take turns. Python can pause a thread **between any two of these steps** and let another thread run. Watch this disaster:

```text
counter = 42

Thread A: READ counter → sees 42
Thread A: ADD 1        → computed 43 (still in A's head)
                        ← Python switches to Thread B
Thread B: READ counter → sees 42 (!)  because A didn't write back yet
Thread B: ADD 1        → computed 43
Thread B: WRITE 43
                        ← Python switches back to Thread A
Thread A: WRITE 43

counter = 43   ← two bumps happened, but the counter only went up by 1!
```

One increment was lost. This is called a **race condition**. Do this millions of times across 4 threads and the final number is unpredictable and always less than expected.

### Step 2 — What a Lock does

A `Lock` is like a **key to a room**. Only one thread can hold the key. If another thread wants it, it must **wait**.

```python
lock = threading.Lock()   # one key, shared by everyone
```

Then:

```python
with lock:                # "grab the key, or wait until you can"
    counter += 1          # only one thread is in here at a time
                          # "drop the key" happens automatically when the block ends
```

While one thread is inside the `with lock:` block, no other thread can enter its own `with lock:` block. They queue up. The earlier scenario becomes:

```text
Thread A: grabs lock 🔑
Thread A: READ counter → 42
Thread A: ADD 1        → 43
Thread A: WRITE 43
Thread A: drops lock

Thread B: grabs lock 🔑
Thread B: READ counter → 43
Thread B: ADD 1        → 44
Thread B: WRITE 44
Thread B: drops lock

counter = 44   ← perfect. no lost increments.
```

### Step 3 — Walking through the code

```python
counter = 0
lock = threading.Lock()
```

One shared counter, one shared lock.

```python
def bump(n):
    global counter               # tell Python we mean the outside counter
    for _ in range(n):           # do this n times
        with lock:               # grab the key
            counter += 1         # safe increment
                                 # key released automatically here
```

Each thread bumps the counter `n` times.

```python
threads = [threading.Thread(target=bump, args=(100_000,)) for _ in range(4)]
for t in threads: t.start()      # launch all 4
for t in threads: t.join()       # wait for all 4
print(counter)                   # 400000 — exactly, thanks to the lock
```

Total = 4 threads × 100,000 bumps = **400,000**. Every single time. Exact. Remove the `with lock:` and you'd see something like `372,451` or `389,102` — different every run, always less than 400,000, because increments got lost to the race.

### Two mental pictures

With the lock — one bathroom, everyone lines up:

```text
🔒
Thread A ─→ [in the room, bumping] ─→ 🔓
Thread B ─→ waiting ────────────→ [in the room] ─→ 🔓
Thread C ─→ waiting ─────────────────────────→ [in the room] ─→ 🔓
Thread D ─→ waiting ──────────────────────────────────────→ [in the room]
```

Without the lock — everyone piles into the room at once and steps on each other's math.

### The rule ★

> If two or more threads read AND write the same variable, you need a lock.

- If threads only **read** shared data (never modify it), no lock needed.
- If each thread has its **own** local variable, no lock needed.
- It's the combination of **shared + modified** that causes the bug.

### Cost — locks are slow

Every `with lock:` costs a little time (acquire → run → release). If you put a lock inside a tight loop, your "parallel" code can be **slower than serial**. The trick is to grab the lock as briefly as possible — do the shared bit inside the `with`, everything else outside it.

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

```text
tick
tick
tick
main exiting — daemon dies with me
```

### What "daemon" means

A **daemon thread** is a background helper. Two rules:

- The main program does **not** wait for daemon threads to finish.
- When main exits, all daemon threads are **killed instantly**, mid-work.

A non-daemon thread is the opposite — the program keeps running until every non-daemon thread has finished, even if `main()` has nothing left to do.

### Walking through the code

```python
def background():
    while True:              # infinite loop — would run forever
        print("tick")
        time.sleep(1)
```

An endless "tick" loop. If this were a **regular** thread, `main` could never exit — it would wait forever.

```python
t = threading.Thread(target=background, daemon=True)   # ← the important flag
t.start()

time.sleep(2.5)              # main does its own thing for 2.5 seconds
print("main exiting — daemon dies with me")
```

`daemon=True` tells Python: "don't wait for me." Main sleeps 2.5 seconds, prints, then exits. The background thread — even though it's still in its infinite loop — is killed on the spot.

### When to use `daemon=True`

Good fit:

- Auto-refreshing a cache.
- Heartbeats / status pings.
- Anything that's fine to lose if the program exits.

Bad fit:

- Writing to a file (can leave it half-written).
- Committing a database transaction.
- Anything with cleanup that must run.

### The rule ★

> Use `daemon=True` for background helpers that don't need to finish. Otherwise, leave `daemon=False` (the default) so main waits for them.

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

```text
[A] starting
[A] done
main done
```

**The `if __name__ == "__main__":` guard is not optional** on Windows/macOS — child processes re-import the script, and without the guard they'd spawn their own children, forever.

### Threads vs processes — how they look side by side

The API is almost identical:

| Threads                          | Processes                             |
|----------------------------------|---------------------------------------|
| `from threading import Thread`   | `from multiprocessing import Process` |
| `Thread(target=fn, args=(...,))` | `Process(target=fn, args=(...,))`     |
| `t.start()` / `t.join()`         | `p.start()` / `p.join()`              |
| Share memory (global vars) ✅    | Each has its own memory ❌            |
| One GIL for everyone             | One GIL **per process**               |

That last row is the whole point: N processes → N GILs → real CPU parallelism.

### Why the `if __name__ == "__main__":` guard

On Windows/macOS, a new process is created by **starting a fresh Python and re-importing your script**. If your process-creation code sits at the top level, the child re-runs it → spawns its own children → those children spawn more children → fork bomb.

Wrap all `Process(...)` and `.start()` calls inside `if __name__ == "__main__":` and the child imports the module but skips that block, because for the child `__name__` is not `"__main__"`.

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

### What "actually parallelizes" means, next to threads

Same `cpu_hog` function, same 4 workers. Two very different outcomes:

| Setup                | 1 worker | 4 workers | Speedup |
|----------------------|----------|-----------|---------|
| 4 threads            | ~2 s     | ~2 s      | ❌ 1×   |
| 4 processes          | ~2 s     | ~0.6 s    | ✅ ~3×  |

Not exactly 4× — starting a process and shipping args across processes has overhead — but it's close, and that's what people mean by "parallelism".

### The trade-off

- **Fast:** each process really uses a core.
- **Slow to start:** a process is a whole new Python interpreter. Milliseconds, not microseconds.
- **No shared memory:** everything you pass in and get back travels via **pickle** (Python's serialization). Lambdas and local functions can't be pickled — always define worker functions at module top level.

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

```text
got: 0
got: 1
got: 4
got: 9
got: 16
```

### The pattern in plain words

Processes don't share variables — so instead they use a **mailbox** they can both see.

- **`q.put(x)`** — drop an item into the mailbox.
- **`q.get()`** — take the next item out (blocks until something arrives).
- **Sentinel `None`** — a "we're done" marker so the consumer knows when to stop.

### The two roles

| Role       | What it does                                              |
|------------|-----------------------------------------------------------|
| `producer` | Puts items into the queue, then puts a `None` sentinel.   |
| `consumer` | Pulls items in a loop; stops when it sees `None`.         |

### Why the sentinel?

`q.get()` **blocks forever** if the queue is empty. Without a "we're done" signal, the consumer would sit there waiting for something that never comes. The `None` at the end says "no more items — you can exit."

### When to reach for a Queue

- Producer/consumer patterns (one process makes work, another does it).
- Streaming results from a worker back to main.
- Pipelines: stage A → stage B → stage C, each in its own process.

For "run the same function over a big list", jump to `Pool` in the next section — it's a cleaner API for that.

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

### How to read `Pool.map`

```python
Pool(processes=4).map(fn, inputs)
#     ^^^^^^^^^^      ^^  ^^^^^^
#     4 workers       │   list of items
#                     │
#                     runs fn(x) for every x, in parallel across 4 workers
```

The result is a plain list — same order as the inputs, no need to reassemble.

### Regular `map()` vs `Pool.map`

```python
# Regular (serial)
list(map(square, range(10)))            # runs 10 times in one process

# Pool (parallel)
with Pool(4) as pool:
    pool.map(square, range(10))         # runs 10 times, spread across 4 processes
```

Both give the same list. `Pool.map` uses more CPU and finishes faster when `square` is heavy.

### The mental model

```text
  inputs  ->  [ Pool of 4 workers ]  ->  results
  0 → worker 0 ─→ 0
  1 → worker 1 ─→ 1
  2 → worker 2 ─→ 4
  3 → worker 3 ─→ 9
  4 → worker 0 ─→ 16   (worker 0 free again, grabs the next input)
  ...
```

Workers grab the next input as soon as they're free. `map` gathers the results back **in input order**, so you don't need to sort.

### When it's worth using

- Same function, applied to a big list of inputs — YES.
- CPU-heavy work per item — YES.
- Trivial work per item — often **slower** than serial because of the startup + pickling cost. Rule: if each item takes less than a millisecond, don't parallelize.

## Pitfalls with processes

- Arguments and return values must be **picklable** (most things are; lambdas and local functions are NOT).
- Startup is slower than threads.
- Data isn't shared — copy semantics via IPC.
- On Windows/macOS, the `if __name__ == "__main__":` guard is mandatory.

### What "picklable" means, quickly

Every argument you send into a worker, and every value you return, is **pickled** (serialized to bytes), shipped across the process boundary, and unpickled on the other side. Anything that can't be pickled will fail with a `PicklingError`.

Common non-picklables:

- **Lambdas** — `Pool().map(lambda x: x*x, ...)` → error.
- **Local (nested) functions.**
- **Open sockets, database connections, file handles.**
- **`threading.Lock`** — use `multiprocessing.Lock` instead.

**Fix:** define worker functions at **module top level** (a plain `def square(x): return x * x` in your file).

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

### Two new words: `async` and `await`

- **`async def name():`** — this function can **pause**.
- **`await something`** — pause here, come back when `something` is ready.

Regular `def` runs top to bottom without ever pausing. `async def` runs, but any time it hits `await`, it says to the event loop: "I'm waiting on this — go run someone else in the meantime."

### `asyncio.run(coro)` — the entry point

`asyncio.run(hello())` starts a hidden manager called the **event loop**, runs your coroutine on it, and shuts the loop down when done. You call `asyncio.run` **once**, at the top level of your script.

### The trap 90% of beginners hit

```python
async def hello():
    print("hi")

hello()                # ← nothing prints!
```

Calling an `async def` function does **not** run it. It returns an unstarted coroutine object. You must:

- Wrap the top-level call in `asyncio.run(hello())`, or
- `await hello()` from inside another `async` function, or
- `asyncio.create_task(hello())` to schedule it in the background.

Get used to that — it's the #1 gotcha in asyncio.

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

```text
[A] downloading...
[B] downloading...
[C] downloading...
took: 1.0 s
['A content', 'B content', 'C content']
```

Three "downloads" of 1 second each — total ≈ **1 second**, not 3. All three await concurrently.

### How `gather` works

Pass several coroutines to `asyncio.gather(...)` and it runs them **all at the same time** on the same event loop. The single `await` at the front waits until **every one** has finished.

- Results come back **in the order you passed them** (not the order they finished).
- If any of them raises an exception, the whole `gather` raises.
- The loop still runs **on one thread** — it's not parallel; it's cooperative multitasking.

### Threads vs asyncio for this exact job

Both would finish in ~1 second. Difference:

| Threads                          | asyncio                              |
|----------------------------------|--------------------------------------|
| Each thread is ~1 MB of memory   | Each coroutine is a few hundred bytes|
| OS switches between threads      | You control the switch (`await`)     |
| Fine for dozens                  | Fine for **thousands** of tasks      |
| Any Python function works        | Only async-compatible libs work      |

Rule: for a chat server, web scraper, or anything with **many** simultaneous connections — asyncio wins.

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

```text
started
A done B done
```

`create_task` schedules a coroutine to run in the background. `await` on it gets the result.

### `create_task` vs `gather` — when to use which

| You want to…                                     | Use            |
|--------------------------------------------------|----------------|
| Launch N things and wait for all at once         | `gather`       |
| Start something in the background, do other stuff, then wait | `create_task` |
| Cancel a running task                            | `create_task` (then `t.cancel()`) |

Think of `create_task` as **"fire it off now, I'll deal with it later."** Between the `create_task` call and the `await`, both tasks are already running.

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

### Why it's so bad

Asyncio runs on **one thread**. All coroutines take turns sharing that thread. Every `await` is where they hand off control. A blocking call has no `await` — so no hand-off happens. The whole loop is stuck until the blocking call returns.

Analogy: everyone in a classroom is sharing one microphone. `await` is politely handing the mic to the next person. `time.sleep` is holding the mic and standing motionless for a minute. No one can talk.

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

```text
slept 1
```

### Why this fixes the problem

`run_in_executor(None, blocking, 1)` moves `blocking(1)` **onto a separate thread** — one from asyncio's default thread pool. The event loop stays free the whole time.

You keep the async style in your code, but let the blocking function run in a thread where it can hold up nobody but itself. When it returns, the event loop picks the result up and hands it to your `await`.

Use this for any old-school blocking library you can't get rid of — `requests`, database drivers without async support, `PIL`, etc.

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

### How `wait_for` works

`asyncio.wait_for(coro, timeout=1.0)` runs your coroutine, but sets an internal timer. If the coroutine hasn't finished in that many seconds, it's **cancelled** and `TimeoutError` is raised — which you catch with a normal `try/except`.

Use it any time you're calling something that could hang: a slow HTTP endpoint, a database query, waiting on a socket.

Rule ★: **every network call in production should have a timeout.** Otherwise a single dead server can freeze your program forever.

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

```text
['https://site.com/0 OK', 'https://site.com/1 OK', 'https://site.com/2 OK',
 'https://site.com/3 OK', 'https://site.com/4 OK']
```

Five fake fetches in ≈1 second, not 5. Same benefit as raw threads, cleaner API.

### Why prefer this to raw `threading.Thread`

The manual pattern was: create Thread objects, `start()` each, `join()` each, collect results somewhere. Lots of bookkeeping.

`ThreadPoolExecutor` does all of that for you:

- **Pool** — reuses a fixed number of worker threads instead of creating a new one for every task.
- **`.map(fn, inputs)`** — runs `fn` on every input in parallel and returns results **in order**.
- **`with`** — waits for every task to finish and cleans up the threads.

Fewer lines, no `.start()` / `.join()` / results-list-append juggling.

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

```text
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

Drop-in for `ThreadPoolExecutor` but uses processes — real CPU parallelism.

### One line, huge difference

Change `ThreadPoolExecutor` to `ProcessPoolExecutor` and:

- Every worker is a **separate process** with its own GIL.
- CPU-heavy Python code **actually parallelizes** across cores.
- Every argument and return value is pickled — so worker functions must be at module top level.
- You need the `if __name__ == "__main__":` guard.

Same API. Different engine underneath. Pick `Thread` for I/O, `Process` for CPU.

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

Sample output (order varies per run because `random`):

```text
task 3 done
task 0 done
task 5 done
task 1 done
task 2 done
task 4 done
```

`submit` starts a task, returns a `Future`. `as_completed` yields futures in the order they finish — great for streaming results as they arrive.

### `map` vs `submit + as_completed`

| Use `map`                       | Use `submit + as_completed`                        |
|---------------------------------|----------------------------------------------------|
| Same function, list of inputs   | Different functions or different-shaped args       |
| You need results **in order**   | You want results **as soon as** each one finishes  |
| Fixed workload                  | Progress bar, early stopping, streaming to disk    |

### What's a `Future`?

A **Future** is a placeholder object that will contain the result **later**. You get it from `ex.submit(...)`. You interact with it like this:

| Call                     | Does what                                    |
|--------------------------|----------------------------------------------|
| `fut.result()`           | Waits for the task, returns the value        |
| `fut.result(timeout=5)`  | Same, but raises `TimeoutError` after 5 s    |
| `fut.exception()`        | Returns the exception, if any (no re-raise)  |
| `fut.done()`             | True if finished                             |
| `fut.cancel()`           | Try to cancel (only if not yet running)      |

`as_completed(futures)` **yields futures** in the order they finish — so `next(as_completed(...))` gives you the fastest one first.

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
