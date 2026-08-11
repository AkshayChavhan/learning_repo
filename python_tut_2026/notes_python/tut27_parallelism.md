# Python Parallelism

Making code **actually run on multiple CPU cores at the same instant** so a computation finishes faster. Concurrency is about structure; parallelism is about speed.

```text
                  ┌──────────────────────────┐
                  │       PARALLELISM        │
                  │  many CPUs, same instant │
                  └──────────────────────────┘
                              │
    ┌───────────────────┬─────┴────────────┬─────────────────────┐
    ▼                   ▼                  ▼                     ▼
  PROCESSES         concurrent.futures    Shared memory      Beyond stdlib
  multiprocessing   ProcessPoolExecutor   shared_memory      joblib / dask
  Pool.map          submit + as_completed Value / Array      Ray / cupy
  bypass the GIL    unified pool API      Manager            distributed
```

Rule of thumb:

- **Want CPU speedup on Python code?** — processes, not threads.
- **Same function over many inputs?** — `Pool.map` or `ProcessPoolExecutor.map`.
- **Heterogeneous jobs, stream results as they finish?** — `submit` + `as_completed`.
- **Big arrays shared between workers?** — `shared_memory`.

For the concurrency side — threads, `asyncio`, and *how* the GIL works — see tut26. This chapter is about squeezing real speedup out of your cores.

---

## Concurrency vs Parallelism ★

People mix these up. They are not the same thing.

| Concept       | What it means                                                           | Python tool                            |
|---------------|-------------------------------------------------------------------------|----------------------------------------|
| Concurrency   | Many tasks **in progress** at once — they take turns                    | `threading`, `asyncio` (covered in tut26) |
| Parallelism   | Many tasks **executing at the same instant** on different CPU cores     | `multiprocessing`, `ProcessPoolExecutor` |

A visual:

```text
CONCURRENCY (1 core, taking turns)
core 0:  A A B B A A C C B B A A ...

PARALLELISM (4 cores, at the same instant)
core 0:  A A A A A A A A A ...
core 1:  B B B B B B B B B ...
core 2:  C C C C C C C C C ...
core 3:  D D D D D D D D D ...
```

Concurrency is a **structure** ("I have many things in flight"). Parallelism is a **hardware fact** ("more than one instruction is executing this nanosecond"). You can have concurrency without parallelism (asyncio on one core). You cannot have parallelism without concurrency.

---

## Why Python parallelism is tricky

One-line recap of the GIL: CPython holds a **Global Interpreter Lock**, so only **one thread** executes Python bytecode at a time. Threads therefore do not give you CPU parallelism on pure Python code. Full explanation of *why* — and how I/O-bound threads still help — is in **tut26**.

The takeaway for this chapter: to get real CPU parallelism in Python, you almost always reach for **processes**. Each process has its own interpreter, its own GIL, and its own memory — so N processes really do run on N cores.

The trade-off:

- Processes cost more to start (fork/spawn a whole interpreter).
- They cannot share memory the way threads do — data crosses via **pickle over IPC**.
- Not everything is picklable.

The rest of this chapter is about working with those trade-offs.

---

## Types of parallelism

Three common shapes. You'll see them everywhere.

| Kind                | What it looks like                                            | Python fit                        |
|---------------------|---------------------------------------------------------------|-----------------------------------|
| Task parallelism    | Different workers do **different** jobs                       | `submit` + `as_completed`         |
| Data parallelism    | All workers do the **same** op over **chunks** of the data    | `Pool.map`, `Executor.map`        |
| Pipeline parallelism| Stages pass data forward (producer -> filter -> writer)       | `Process` + `Queue`               |

Data parallelism is the easiest win — it's just "map, but faster". Task parallelism is the most flexible. Pipeline parallelism is the trickiest to balance (one slow stage stalls everything).

---

## Measuring speedup ★

You can't reason about parallelism without measuring. The two things to know: **Amdahl's Law** and `time.perf_counter`.

**Amdahl's Law.** If a fraction **P** of your program can be parallelized and **N** is the number of workers:

```text
speedup = 1 / ((1 - P) + P/N)
```

- P = 1.0 (fully parallel), N = 4  ->  speedup = 4x.
- P = 0.9,                 N = 4   ->  speedup = 1 / (0.1 + 0.225) = ~3.08x.
- P = 0.5,                 N = 4   ->  speedup = 1 / (0.5 + 0.125) = 1.6x.
- P = 0.5,                 N = 1000 ->  speedup approaches 2x. **No matter how many cores you throw at it.**

Serial code is the ceiling. Cut serial fraction before adding cores.

**Real measurement — serial vs 4 processes.**

```python
from concurrent.futures import ProcessPoolExecutor
import time

def count_primes_upto(n):
    # CPU-bound: sieve of Eratosthenes, no I/O
    if n < 2:
        return 0
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return sum(sieve)

inputs = [400_000, 400_000, 400_000, 400_000]

if __name__ == "__main__":
    # Serial
    start = time.perf_counter()
    serial = [count_primes_upto(n) for n in inputs]
    t_serial = time.perf_counter() - start

    # Parallel
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        parallel = list(ex.map(count_primes_upto, inputs))
    t_par = time.perf_counter() - start

    print("serial:  ", round(t_serial, 2), "s")
    print("parallel:", round(t_par, 2), "s")
    print("speedup: ", round(t_serial / t_par, 2), "x")
    print("results equal:", serial == parallel)   # True
```

```text
serial:   1.60 s
parallel: 0.55 s
speedup:  2.91 x
results equal: True
```

On a 4-core machine you'll typically see **2.5x-3.5x**, not the theoretical 4x — pool startup, pickling of arguments and results, and OS scheduling eat some of the win.

**Overhead can make you SLOWER.** For tiny tasks, the cost of shipping arguments and results across processes dominates.

```python
from concurrent.futures import ProcessPoolExecutor
import time

def tiny(n):
    return n * n            # trivial work

inputs = list(range(200_000))

if __name__ == "__main__":
    start = time.perf_counter()
    serial = [tiny(n) for n in inputs]
    print("serial:  ", round(time.perf_counter() - start, 3), "s")

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        parallel = list(ex.map(tiny, inputs))    # chunksize=1 by default
    print("parallel:", round(time.perf_counter() - start, 3), "s")
```

```text
serial:   0.02 s
parallel: 3.50 s
```

Parallel is **~100x slower**. Serialisation cost per item overwhelms the work per item. The fix is either "don't parallelize" or "chunk the work" — covered below.

---

# Part 1 — Data parallelism with `ProcessPoolExecutor.map`

The everyday pattern: **run this CPU-heavy function on this big list of inputs, in parallel**.

```python
from concurrent.futures import ProcessPoolExecutor
import time

def sum_of_squares(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

inputs = [2_000_000, 2_000_000, 2_000_000, 2_000_000,
          2_000_000, 2_000_000, 2_000_000, 2_000_000]

if __name__ == "__main__":
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(sum_of_squares, inputs))
    print("done in", round(time.perf_counter() - start, 2), "s")
    print("first result:", results[0])
```

Why `ProcessPoolExecutor.map` and not `Pool.map`? Same idea, cleaner interface, unified with the thread version. Pick either — they cover the same 95% of cases.

Key properties of `.map`:

- Results come back **in input order**.
- Blocks (via `list(...)`) until every input is processed.
- Same function must handle every input — this is data parallelism, not task parallelism.

---

# Part 2 — `multiprocessing.Pool` — `imap` and `imap_unordered`

`Pool.map` blocks until every result is ready. For long jobs you often want results **as they arrive** — for progress bars, for early stopping, for streaming to disk.

```python
from multiprocessing import Pool
import time

def slow_square(n):
    time.sleep(0.2)         # pretend the work is slow
    return n * n

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        # imap: streams results, IN ORDER
        for result in pool.imap(slow_square, range(8)):
            print("got:", result)
```

`imap` yields results in the **same order** as inputs — but each result is available as soon as it (and every earlier one) is ready.

`imap_unordered` gives them up **as soon as any worker finishes**, regardless of input order — usually the fastest for streaming.

```python
from multiprocessing import Pool
import time, random

def variable_work(n):
    time.sleep(random.random() * 0.5)
    return n

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        for result in pool.imap_unordered(variable_work, range(8)):
            print("finished:", result)
```

You'll see them arrive out of order — 3, 0, 5, 1, ... — but the whole batch finishes faster than `imap` because no result blocks waiting for a slow earlier one.

Rule: **use `imap_unordered` when order doesn't matter; use `imap` when it does; use `map` when you just want the full list.**

---

# Part 3 — Chunking ★ — the `chunksize` you must set

`Pool.map`, `Pool.imap`, and `Executor.map` all take a `chunksize` argument. It controls how many inputs a worker grabs at once from the queue.

- Small `chunksize` -> more IPC, more overhead, better load balancing.
- Large `chunksize` -> less IPC, less overhead, worse load balancing.

For **tiny tasks over large inputs**, the default `chunksize=1` is a disaster.

```python
from concurrent.futures import ProcessPoolExecutor
import time

def tiny(n):
    return n * n

inputs = list(range(500_000))

if __name__ == "__main__":
    # BAD — 500,000 tiny messages across processes
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        list(ex.map(tiny, inputs, chunksize=1))
    print("chunksize=1:    ", round(time.perf_counter() - start, 2), "s")

    # GOOD — a few thousand messages, each carrying 1000 items
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        list(ex.map(tiny, inputs, chunksize=1000))
    print("chunksize=1000: ", round(time.perf_counter() - start, 2), "s")
```

```text
chunksize=1:     8.42 s
chunksize=1000:  0.18 s
```

A ~50x difference for the same computation. Always tune `chunksize` when inputs are numerous and per-item work is small.

Reasonable starting point: `chunksize = len(inputs) // (workers * 4)`.

---

# Part 4 — Task parallelism with `submit` + `as_completed`

When jobs are **heterogeneous** — different functions, different args, different durations — `map` doesn't fit. Use `submit`.

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

def compress(name, level):
    time.sleep(0.2 * level)      # imagine gzip
    return f"{name} compressed@{level}"

def hash_file(name):
    time.sleep(0.1)
    return f"{name} hashed"

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        futures = [
            ex.submit(compress, "a.txt", 3),
            ex.submit(compress, "b.txt", 1),
            ex.submit(hash_file, "c.txt"),
            ex.submit(hash_file, "d.txt"),
        ]
        # Stream results as each one finishes
        for fut in as_completed(futures):
            print(fut.result())
```

Each `submit` returns a `Future`. `as_completed` yields futures in **completion order**, so you can start reacting to the fast ones before the slow ones are done. Perfect for building a progress bar, or for "return the first N successes and cancel the rest".

Cancel a pending future with `fut.cancel()`. Get exceptions with `fut.exception()` instead of `.result()` (which would re-raise).

---

# Part 5 — Sharing data between processes ★

The hardest part of process-based parallelism. Threads share memory for free; processes do not.

## Return values — the default path

Return the answer from your function. Under the hood it's **pickled**, shipped through a pipe, and unpickled in the parent. Simple and correct for reasonably sized results.

```python
from concurrent.futures import ProcessPoolExecutor

def work(x):
    return {"input": x, "square": x * x}

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(work, range(4)))
    print(results)
    # [{'input': 0, 'square': 0}, {'input': 1, 'square': 1},
    #  {'input': 2, 'square': 4}, {'input': 3, 'square': 9}]
```

## `Manager` — shared dict / list (slow, but easy)

```python
from multiprocessing import Process, Manager

def add(shared, key, value):
    shared[key] = value

if __name__ == "__main__":
    with Manager() as m:
        shared = m.dict()
        procs = [Process(target=add, args=(shared, i, i * i)) for i in range(4)]
        for p in procs: p.start()
        for p in procs: p.join()
        print(dict(shared))     # {0: 0, 1: 1, 2: 4, 3: 9}
```

`Manager` runs a **server process** that holds the object. Every read/write is an IPC round-trip — do not use it in hot loops.

## `Value` / `Array` — shared primitives

For a single number or a fixed-size array of primitives, `Value` and `Array` share **real memory**, guarded by a lock. Much faster than `Manager`.

```python
from multiprocessing import Process, Value

def bump(counter, n):
    for _ in range(n):
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    counter = Value("i", 0)       # signed int
    procs = [Process(target=bump, args=(counter, 10_000)) for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(counter.value)          # 40000
```

Type codes: `"i"` int, `"d"` double, `"b"` byte, etc. — same as `array.array`.

## `shared_memory` ★ — big blocks, near-zero copy

New in Python 3.8. Lets multiple processes see the **same bytes** in RAM without pickling. Perfect for large numeric buffers (numpy arrays, image buffers).

```python
from multiprocessing import Process
from multiprocessing import shared_memory

def writer(shm_name):
    shm = shared_memory.SharedMemory(name=shm_name)
    shm.buf[0:5] = b"HELLO"
    shm.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(create=True, size=16)
    try:
        p = Process(target=writer, args=(shm.name,))
        p.start()
        p.join()
        print(bytes(shm.buf[0:5]))      # b'HELLO'
    finally:
        shm.close()
        shm.unlink()                    # free the OS-level segment
```

Rules for `shared_memory`:

- The **creator** must eventually `unlink()` it — otherwise it leaks at the OS level.
- Every process that opens it must `close()` its own view.
- With numpy: create a `SharedMemory`, then wrap `shm.buf` as an `ndarray` with the same dtype/shape in every process. No copy.

## The rule

**Prefer functional patterns.** Input goes in, output comes back. No shared mutable state. Code stays testable, no locks, no server processes, no leaks.

Reach for shared memory only when the data really is too large to copy per call.

---

# Part 6 — Pickle limits ★ — what can and cannot cross a process boundary

Everything you send to a worker (arguments, closures, the function itself in `spawn` mode) and everything you get back (return values, exceptions) is **pickled**.

**Fine to pickle:**

- Built-in types: `int`, `float`, `str`, `bytes`, `list`, `dict`, `tuple`, `set`.
- Module-level functions and classes.
- `dataclasses`, most simple objects.
- `numpy` arrays.

**Not picklable (typical `TypeError` / `PicklingError`):**

```python
# BAD — lambdas can't be pickled
with ProcessPoolExecutor() as ex:
    ex.map(lambda x: x * x, range(10))    # PicklingError

# BAD — local (nested) function
def make_worker():
    def inner(x): return x * x            # local, not module-level
    return inner
```

- Lambdas.
- Local (nested) functions.
- Open file handles, sockets, database connections.
- `threading.Lock` (use `multiprocessing.Lock` if you need one).
- Generators, iterators over external state.

**Fix:** define worker functions at **module top level**.

```python
# GOOD — module-level function
def square(x):
    return x * x

if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:
        print(list(ex.map(square, range(10))))
```

---

# Part 7 — Spawn methods — `fork`, `spawn`, `forkserver`

How Python creates worker processes.

| Method       | How                                            | Where it's default            |
|--------------|------------------------------------------------|-------------------------------|
| `fork`       | Clone the parent process (fast, copy-on-write) | Linux (Python <= 3.13)        |
| `spawn`      | Start a fresh Python, re-import your module    | Windows, macOS (3.8+)         |
| `forkserver` | Fork from a small clean helper server          | Available on Unix; opt-in     |

Practical implications:

- With **`spawn`**, each worker **re-imports your script** to find the worker function. Any top-level code runs again. That's why the **`if __name__ == "__main__":` guard is mandatory** — without it, each new worker starts more workers, endlessly.
- With **`fork`**, the workers inherit parent state (file handles, threads, memory). Fast, but subtly dangerous — if the parent had threads or locks, the child inherits them in a possibly broken state.
- You can override the default:

```python
import multiprocessing as mp

if __name__ == "__main__":
    mp.set_start_method("spawn")     # or "fork", "forkserver"
    # ... rest of program
```

Set once, at the start of `__main__`. Changing later raises `RuntimeError`.

---

# Part 8 — Beyond the standard library

The stdlib covers most jobs. When you outgrow it:

| Library                | What it's for                                                    |
|------------------------|------------------------------------------------------------------|
| **`joblib`**           | `Parallel(n_jobs=-1)(delayed(fn)(x) for x in xs)`. Popular in ML — simple syntax, memory-mapped numpy arrays. |
| **`dask`**             | Lazy parallel numpy / pandas / bag / delayed graphs; scales from laptop to cluster. |
| **`ray`**              | Distributed-first, actor model (`@ray.remote`); good fit for RL, ML serving, agentic systems. |
| **`cupy` / `torch`**   | GPU parallelism — thousands of tiny cores; different mental model, but massive speedup for array math. |

Rough guidance: stdlib for one machine, joblib for scikit-learn workflows, dask for larger-than-RAM data, ray for many-machine, GPU for array math.

---

# Part 9 — When NOT to parallelize

Adding parallelism has real costs. Skip it when:

- **Inputs are tiny or few.** Pool startup alone can be 100ms+ — that dwarfs the work.
- **Work is I/O-bound.** Use `threading` or `asyncio` (tut26). Processes are heavy overkill.
- **Tight communication loops.** If workers must constantly talk to each other, IPC will kill your speedup.
- **State is unpicklable.** Database connections, sockets, running threads — cannot cross processes.
- **You already fit in one core comfortably.** Don't optimize what isn't slow.
- **Correctness matters and code isn't tested serially.** Debug serial first; parallelize second.

Measure first. Parallelize second. Ship third.

---

## Common pitfalls

### 1. No `if __name__ == "__main__":` guard

```python
# BAD — on Windows/macOS, workers re-import this script
from multiprocessing import Process
p = Process(target=work)
p.start()
```

Fix: wrap **all** process creation in `if __name__ == "__main__":`.

### 2. Lambdas can't be pickled

```python
# BAD
with ProcessPoolExecutor() as ex:
    ex.map(lambda x: x * 2, range(10))
```

Fix: define the function at module top level, or use `functools.partial` on a real function.

### 3. Global mutable state doesn't propagate

```python
count = 0
def bump():
    global count
    count += 1
```

Each process has its **own** `count`. The parent never sees the child's changes. Fix: return the value, or use `Value` / `Manager`.

### 4. IPC serialization is expensive for large args

Sending a 500MB numpy array to each of 8 workers means **4 GB of pickling and copying**. Fix: use `shared_memory`, or memory-map a file, or write the data once and pass the filename.

### 5. Too many workers past CPU count

```python
# BAD on a 4-core box
with ProcessPoolExecutor(max_workers=64) as ex:
    ...
```

For CPU work, more processes than cores fight for the same CPUs and slow each other down. Fix: `max_workers = os.cpu_count()` (or a bit less if the box has other jobs).

### 6. `ProcessPoolExecutor` for I/O work

```python
# BAD — process pool for HTTP calls
with ProcessPoolExecutor() as ex:
    ex.map(requests.get, urls)
```

Processes are overkill for network calls. Fix: `ThreadPoolExecutor` or `asyncio` (tut26).

### 7. Sharing a `threading.Lock` across processes

```python
# BAD — this Lock lives in one process only
import threading
lock = threading.Lock()
```

Fix: `from multiprocessing import Lock` if you truly need a cross-process lock. Better: avoid shared state entirely.

### 8. Passing huge numpy arrays via IPC

Every call round-trips a copy through pickle. Fix: `multiprocessing.shared_memory` (Python 3.8+), or memory-mapped files (`numpy.memmap`), or pass a filename and load in the worker.

---

## Interview angle

- **What is Amdahl's Law?** `speedup = 1 / ((1 - P) + P/N)`. The serial fraction caps your speedup regardless of core count. Cut serial work before adding cores.
- **Why don't Python threads give CPU parallelism?** The GIL — only one thread runs Python bytecode at a time. Threads help I/O work (they release the GIL while blocked), not CPU work.
- **When does the GIL NOT apply?** Inside C extensions that release it — most `numpy` bulk ops, `zlib`, `hashlib`, blocking I/O syscalls. That's why numpy math on a single thread often beats a "parallel" Python loop.
- **How do you measure speedup properly?** `time.perf_counter` around the exact region of interest, warm up first, average multiple runs, compare serial to parallel with the same input. Watch for pool startup being included.
- **What role does pickle play in `multiprocessing`?** Every argument going into a worker and every result coming out is pickled/unpickled. That's why lambdas fail, why huge args are slow, and why `shared_memory` exists.

---

## Quick reference

```text
# CHOOSING
#   CPU-bound, big inputs, same op       -> ProcessPoolExecutor.map / Pool.map
#   CPU-bound, mixed jobs                -> submit + as_completed
#   CPU-bound, huge shared buffer        -> shared_memory + processes
#   I/O-bound                            -> threading / asyncio  (see tut26)
#   Tiny inputs                          -> don't parallelize

# DATA PARALLELISM (the everyday pattern)
from concurrent.futures import ProcessPoolExecutor
if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(fn, inputs, chunksize=1000))

# STREAMING RESULTS
from multiprocessing import Pool
if __name__ == "__main__":
    with Pool(4) as pool:
        for r in pool.imap_unordered(fn, inputs):
            print(r)             # arrives as workers finish

# TASK PARALLELISM
from concurrent.futures import ProcessPoolExecutor, as_completed
if __name__ == "__main__":
    with ProcessPoolExecutor(4) as ex:
        futs = [ex.submit(fn, x) for x in inputs]
        for f in as_completed(futs):
            print(f.result())

# SHARING DATA
from multiprocessing import Value, Array, Manager
from multiprocessing import shared_memory
#   Value("i", 0)                        # shared int
#   Array("d", [0.0]*100)                # shared float array
#   Manager().dict() / .list()           # slow but flexible
#   shared_memory.SharedMemory(create=True, size=N)   # big buffers

# AMDAHL'S LAW
#   speedup = 1 / ((1 - P) + P/N)
#   P = parallelizable fraction, N = workers.
#   Serial fraction is the ceiling.

# ALWAYS
#   - if __name__ == "__main__":         # required on Windows/macOS
#   - worker fns at module top level     # no lambdas/local fns
#   - tune chunksize for small tasks
#   - measure with time.perf_counter
#   - max_workers ~ os.cpu_count() for CPU work
```
