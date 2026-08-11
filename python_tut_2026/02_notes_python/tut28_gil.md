# Python — The GIL (Global Interpreter Lock)

The single most-asked, most-misunderstood thing about Python. This chapter goes deeper than the intro in tut26 and tut27 — what the GIL actually is, why it exists, when it hurts, when it doesn't, and what's changing in Python 3.13+.

```text
                  ┌──────────────────────────┐
                  │       THE GIL            │
                  │  one lock, one thread    │
                  │  runs Python at a time   │
                  └──────────────────────────┘
                              │
    ┌─────────────────┬───────┴────────┬──────────────────┐
    ▼                 ▼                ▼                  ▼
  WHAT IT IS      WHY IT EXISTS     WHEN IT'S BAD     WHEN IT DOESN'T APPLY
  a mutex on      thread-safe       CPU-bound         I/O syscalls,
  the interpreter reference count   pure-Python code  numpy/C-ext,
                                    threading = no    3.13+ free-threading
                                    speedup
```

Two-line summary:

- The GIL is a **mutex inside CPython** that lets **only one thread execute Python bytecode at a time**.
- It exists to protect Python's memory model (mainly reference counting). Its downside is that pure-Python CPU work can't use multiple cores from within one process.

---

## Part 1 — What the GIL actually is

Every CPython process holds **one** lock called the GIL. To run Python bytecode, a thread must first **acquire** that lock. When it's done (or periodically pauses), it **releases** the lock and another thread can grab it.

```text
    Thread A                 Thread B                 Thread C
      │                         │                        │
      ▼                         ▼                        ▼
    grab GIL 🔒            wait...                    wait...
    run bytecode
    release GIL 🔓
                           grab GIL 🔒                wait...
                           run bytecode
                           release GIL 🔓
                                                     grab GIL 🔒
                                                     run bytecode
```

Only one at a time. The others don't stop existing — they just **wait** for the lock. On a machine with 8 cores, 7 of them can sit idle while one thread runs Python.

### It's a real mutex, not "a special thing"

```python
# You can see the switch interval — how long a thread holds the GIL before
# it's asked to yield:
import sys
print(sys.getswitchinterval())    # 0.005 -> 5 ms, the default
```

Every ~5 ms, the current thread is nudged to release the GIL so someone else can run. That's how threads take turns.

### Reminder — where the GIL sits

```text
┌────────────────────────────────────────────────────┐
│  Your Python process (one interpreter, one GIL)    │
│                                                    │
│    Thread 1        Thread 2        Thread 3        │
│    │               │               │               │
│    └───► Only one holds ────► the GIL at a time    │
│                                                    │
│    All threads share the same memory (objects,     │
│    dicts, imports, globals). That's why they need  │
│    a lock in the first place.                      │
└────────────────────────────────────────────────────┘
```

Multiprocessing works around it because each **process** has its own interpreter and therefore its own GIL. Same code, different lock — see tut27.

---

## Part 2 — Why the GIL exists ★

Not a mistake. A design choice made in the early '90s that's very hard to remove without breaking a lot of things.

### The core reason: reference counting

CPython manages memory with **reference counts**. Every object has a counter — when it hits 0, the object is freed.

```python
import sys
x = [1, 2, 3]
print(sys.getrefcount(x))    # e.g. 2  (x + the arg passed to getrefcount)

y = x                        # bump the count
print(sys.getrefcount(x))    # 3
```

Every time a Python name binds to an object, or a container adds/removes it, a **`+1` or `-1` on the count** happens. Millions of times per second.

Without a lock, two threads could increment or decrement the same count at the same time and one update could get lost — remember the `counter += 1` race in tut26? Same problem, but on **every single object**. Result: memory corruption, crashes, or leaks.

Options the CPython authors had:

| Option                                | Cost                              |
|---------------------------------------|-----------------------------------|
| One lock over the whole interpreter   | Slow for CPU-bound threads. **Chosen.** |
| A fine-grained lock per object        | Massive slowdown for single-threaded code |
| Atomic reference-count instructions   | Complex, platform-specific, still slower on many CPUs |
| Skip reference counting altogether    | Big rewrite; changes GC semantics |

The single big lock was the **simplest** and **fastest for the common case** (most Python is single-threaded).

### Other things the GIL protects

- Import system (avoid duplicate module loading).
- Common built-in types (`list`, `dict`, `set`) — many of their operations are atomic **because** the GIL forbids two threads from stepping on each other mid-operation.
- C extensions written before threading was a concern.

Removing the GIL isn't just about locks — it's about making decades of C code, extensions, and semantic assumptions all thread-safe.

---

## Part 3 — What the GIL does NOT prevent ★

Beginners often assume "GIL means threads are useless." Not true.

### Threads run in parallel while waiting on I/O

The GIL is released whenever a thread is **waiting on something outside Python**:

- `time.sleep`
- Reading/writing files
- Network requests
- Database queries
- `input()`
- Blocking `queue.get()`

While a thread is blocked in a syscall, it doesn't need to hold the GIL — so **other threads run in parallel**.

```python
import threading, time

def wait_and_report():
    time.sleep(1)                 # GIL released while sleeping
    print("done")

t1 = threading.Thread(target=wait_and_report)
t2 = threading.Thread(target=wait_and_report)
t3 = threading.Thread(target=wait_and_report)
t1.start(); t2.start(); t3.start()
t1.join(); t2.join(); t3.join()
# All three finish in ~1 second, not 3.
```

### C extensions can release the GIL

Compiled C code that doesn't touch Python objects can drop the GIL and run in parallel.

- `numpy` matrix ops release the GIL for the heavy math.
- `hashlib`, `zlib`, `bcrypt`, image codecs, `cryptography` — all release the GIL for their C paths.
- `pandas` on wide numeric ops (via numpy).
- Blocking I/O syscalls (`socket.recv`, `open().read()`).

So `numpy.dot(A, B)` on two big arrays across 4 threads **can** hit 4 cores — because numpy releases the GIL before entering C.

### Rule of thumb ★

> The GIL blocks **Python bytecode** from running in parallel. It does not block **native code** or **waiting**.

That's why pure-Python CPU loops don't scale with threads, but numpy math and network I/O do.

---

## Part 4 — Prove it yourself ★ (real timings)

You don't have to take my word for it. Two threads, two very different outcomes.

### Pure-Python CPU: threads DON'T help

```python
import threading, time

def cpu_hog(n):
    total = 0
    for i in range(n):
        total += i * i

N = 20_000_000

# --- Serial ---
start = time.perf_counter()
cpu_hog(N)
cpu_hog(N)
print("serial:", round(time.perf_counter() - start, 2), "s")

# --- 2 threads ---
start = time.perf_counter()
t1 = threading.Thread(target=cpu_hog, args=(N,))
t2 = threading.Thread(target=cpu_hog, args=(N,))
t1.start(); t2.start()
t1.join(); t2.join()
print("2 threads:", round(time.perf_counter() - start, 2), "s")
```

Typical output (varies by machine and Python version):

```text
serial:    2.10 s
2 threads: 2.12 s     ← same (best case)
```

or, worse:

```text
serial:    1.00 s
2 threads: 1.91 s     ← nearly 2x SLOWER (real case on Python 3.8)
```

Two threads never *win* on pure Python. In practice they often **lose** — the OS keeps switching, the CPU caches thrash, and the GIL churn adds pure overhead. Either way, you're not gaining anything by using threads for CPU-bound Python.

### Sleep-heavy work: threads DO help

```python
import threading, time

def waiter():
    time.sleep(1)

start = time.perf_counter()
threads = [threading.Thread(target=waiter) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("4 sleeping threads:", round(time.perf_counter() - start, 2), "s")
```

```text
4 sleeping threads: 1.00 s
```

`time.sleep` releases the GIL → all four sleep concurrently → total ≈ 1 s, not 4.

### Numpy CPU: threads DO help

```python
# Requires: pip install numpy
import numpy as np
import threading, time

def matmul():
    A = np.random.random((1000, 1000))
    B = np.random.random((1000, 1000))
    A @ B                           # C code, releases the GIL

# --- Serial ---
start = time.perf_counter()
matmul(); matmul()
print("serial numpy:", round(time.perf_counter() - start, 2), "s")

# --- 2 threads ---
start = time.perf_counter()
t1 = threading.Thread(target=matmul)
t2 = threading.Thread(target=matmul)
t1.start(); t2.start()
t1.join(); t2.join()
print("2 threads:", round(time.perf_counter() - start, 2), "s")
```

Numpy releases the GIL for the matmul → 2 threads roughly **half the time**.

### The result table

| Work                    | Serial | 2 threads | Speedup? | Why                     |
|-------------------------|--------|-----------|----------|-------------------------|
| Pure-Python math        | 1.00s  | 1.91s     | ❌ often SLOWER | GIL contention + cache thrash |
| `time.sleep(1)` × 4     | 4.00s  | 1.00s     | ✅       | GIL released while sleeping |
| Numpy matmul            | 1.20s  | 0.65s     | ✅       | C code releases GIL     |
| HTTP requests × 5       | 5.00s  | ~1.00s    | ✅       | Blocking socket = no GIL |

---

## Part 5 — Atomic operations and the "GIL as a lock" trap ★

Because only one thread runs Python bytecode at a time, **some** operations look atomic — you can't tell they were interrupted.

**Usually atomic** (in CPython, for built-in types):

```python
d[key] = value         # a single dict-set is atomic
lst.append(x)          # append is atomic
lst[i] = x             # index-assign is atomic
```

**NOT atomic — needs a lock**:

```python
counter += 1           # read + add + write → 3 bytecodes → RACE
```

The trap ★: **relying on "the GIL makes it safe"** is a bad idea, because:

- The set of atomic operations isn't documented.
- Python 3.13+ has a **free-threaded build** where the GIL is optional (see Part 8).
- Other implementations (Jython, IronPython) don't have a GIL.
- Even inside CPython, a well-intentioned change can shift the atomicity.

**Rule:** if two threads read AND write the same variable, use a `threading.Lock`, `queue.Queue`, or an `atomic` counter from `itertools.count` / `threading.local`. Don't count on the GIL as your synchronization.

---

## Part 6 — Escaping the GIL

Four ways, ordered from most common to most exotic.

### 1. Use processes instead of threads

Each process has its own interpreter and its own GIL. Real CPU parallelism.

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_hog(n):
    total = 0
    for i in range(n):
        total += i * i

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        list(ex.map(cpu_hog, [20_000_000] * 4))
```

Trade-off: slower startup, higher memory, args must pickle. See tut27 for the deep dive.

### 2. Use libraries that release the GIL

Numpy, pandas, scipy, torch, hashlib, zlib, cryptography — a huge fraction of "hot" workloads happen in C code that releases the GIL. You get thread-based parallelism **for free** if your bottleneck is in one of these libraries.

### 3. Use asyncio for I/O-bound scale

For thousands of simultaneous network calls, `asyncio` beats threads on memory and switching cost. Same rule though — the GIL still applies to your Python code between `await`s.

### 4. Free-threaded Python (3.13+, experimental)

Since Python 3.13, there is an official **free-threaded build** — a CPython that runs without the GIL. It's opt-in (build flag `--disable-gil`), still experimental in 3.13, and expected to stabilize over 3.14–3.15.

On a free-threaded interpreter, pure-Python threads **do** scale to multiple cores. But:

- Single-threaded code can be ~10–15% slower (fine-grained locking overhead).
- Many C extensions have to be updated to work correctly.
- Not the default. On Python 3.13 the standard build still has the GIL.

If you're on 3.8 (which you are), the free-threaded build doesn't exist for you — but it's the direction the language is going.

---

## Part 7 — When the GIL is NOT the reason you're slow

Programmers blame the GIL for a lot of things it's innocent of. Rule out these first:

| Symptom                                  | Likely cause                                        |
|------------------------------------------|-----------------------------------------------------|
| One thread already 100% CPU              | Your algorithm is O(n²); optimize the algorithm     |
| Slow I/O                                 | Waiting on network/disk; not a CPU issue at all     |
| High memory                              | Data structures too big; unrelated to the GIL       |
| Threads seem fine on one machine, slow on another | Different core counts, thermal throttling  |
| `time.sleep` "makes things faster"       | Congestion; hitting a rate-limited API              |

Measure first (`time.perf_counter`, `cProfile`, `py-spy`). Only *then* decide the GIL is the bottleneck.

---

## Part 8 — Free-threaded Python (3.13+) preview

A one-page preview since you asked for a modern chapter.

### What is it

A build of CPython where the GIL is **removed** — replaced by fine-grained locks inside individual objects and a new garbage collector that no longer relies on the GIL for safety.

### How to try it

```bash
# Requires Python 3.13+
./configure --disable-gil
make
# Or on Python.org's Windows/macOS installers, tick the "free-threaded" option.
```

Check at runtime:

```python
import sys
print(sys._is_gil_enabled())    # False on the free-threaded build
```

(On your Python 3.8, `sys._is_gil_enabled` doesn't exist yet — that's fine.)

### What changes

- **Pure-Python threads scale.** A tight-loop CPU function across 4 threads uses 4 cores.
- **Single-thread perf** dips ~10–15% because every ref-count now uses atomic instructions.
- **C extensions** must opt in. Anything not updated may crash or corrupt data. Numpy, hashlib, and most stdlib have been updated. Third-party libs are catching up.
- **Atomicity guarantees weaken.** Things you could get away with under the GIL (like `d[k] = v` across threads) now genuinely need locks in some cases.

### What to actually do today

- If you're on 3.8–3.12, ignore this — the GIL is still there.
- If you're starting a new project on 3.13+, still target the default (GIL) build. Test on free-threaded once your deps support it.
- **Write your code as if the GIL were gone** — use locks, queues, and shared_memory. Then you're ready either way.

---

## Part 9 — Common pitfalls

### 1. "Threads will speed up my CPU work"

```python
threading.Thread(target=heavy_math_in_python).start()
threading.Thread(target=heavy_math_in_python).start()
```

Fix: use processes. Or a library that releases the GIL (numpy).

### 2. Relying on the GIL as a synchronization tool

```python
counter = 0

def bump():
    global counter
    for _ in range(1_000_000):
        counter += 1        # RACE — not atomic
```

Fix: use `threading.Lock`, `Queue`, or store per-thread and merge at the end.

### 3. Assuming numpy always releases the GIL

Only the **heavy C paths** release it. Element-wise Python loops over numpy arrays hold the GIL. Vectorize.

### 4. Forgetting `daemon=False` when threads must finish

The GIL doesn't kill your threads at shutdown — daemon settings do. See tut26 for the details.

### 5. Confusing the GIL with `asyncio`

`asyncio` is single-threaded regardless of the GIL. Removing the GIL wouldn't parallelize an asyncio loop. Different problem.

### 6. Blaming the GIL when the code just hasn't been profiled

`cProfile` first. Then decide.

---

## Part 10 — Interview angle ★

Common questions and one-line answers.

- **What is the GIL?** A mutex in CPython that allows only one thread to execute Python bytecode at a time.
- **Why does it exist?** To make reference counting (and the whole memory model) thread-safe without a lock on every object.
- **Does it affect I/O-bound programs?** No — the GIL is released while a thread is blocked on I/O.
- **Does it apply to multiprocessing?** No — each process has its own interpreter and its own GIL.
- **Does numpy help?** Yes — numpy releases the GIL around C bulk ops, so threads over numpy math **do** scale.
- **Is Python removing the GIL?** Yes — 3.13+ has an experimental free-threaded build. It's opt-in and still stabilizing.
- **Can I make my Python program faster without processes?** Sometimes: vectorize with numpy, use async for I/O, offload hot loops to C/Cython/PyO3.
- **How do I know if the GIL is the bottleneck?** Profile. If one core is at 100% and the others are idle in a threaded CPU program → yes.
- **Why do dict operations "seem" thread-safe?** Because the GIL prevents interleaving of a single bytecode. It's an implementation detail, not a guarantee. Don't rely on it.

---

## Part 11 — Quick reference

```text
# WHAT THE GIL IS
# - one mutex per interpreter
# - only one thread runs Python bytecode at a time
# - other threads wait

# WHY IT EXISTS
# - thread-safe reference counting
# - single-threaded speed
# - simple C-extension model

# THE GIL IS RELEASED WHEN
# - time.sleep, blocking I/O
# - socket recv/send, file read/write
# - most numpy C ops
# - hashlib / zlib / cryptography C paths
# - asyncio await points (they yield to the loop; GIL is separate)

# WHERE IT HURTS
# - pure-Python CPU-bound loops on multiple threads
# - only ONE core will be busy

# WHERE IT DOESN'T HURT
# - I/O-bound threading
# - numpy / pandas / torch heavy math
# - multiprocessing (each process has its own GIL)

# THE RULES
# 1. threads for I/O, processes for CPU
# 2. don't rely on the GIL for correctness — use locks
# 3. profile before you blame the GIL

# INTROSPECTION
import sys
sys.getswitchinterval()          # default ~0.005s (5 ms)
sys.setswitchinterval(0.01)      # threads hold the GIL longer
# sys._is_gil_enabled()          # 3.13+ only: False on free-threaded build

# ESCAPE ROUTES
# 1. multiprocessing / ProcessPoolExecutor
# 2. numpy / C-extension libraries
# 3. asyncio (for I/O-bound scale)
# 4. free-threaded Python 3.13+ (experimental)
```
