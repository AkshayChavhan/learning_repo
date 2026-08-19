# Sync RAG vs Async RAG

**Sync RAG (Synchronous):** Processes one query at a time — retrieve documents, wait for LLM response, then handle the next query. Simple to code but slow under load (blocking calls, one user blocks others).

**Async RAG (Asynchronous):** Processes multiple queries concurrently on one thread — while waiting for one LLM response, handles other users' requests. No callback delays, scales to thousands of requests without more servers.

**When to use:** Sync RAG for development/testing (easy to debug). Async RAG for production with many users, APIs, or real-time chat where speed matters — trade-off is code complexity (async/await, queues, event loops).

**Real impact:** Sync RAG on 1 CPU takes 10s/query × 100 users = 16 minutes total. Async RAG on same CPU handles all 100 concurrently in ~10s by switching between waiting tasks — 96× faster without extra hardware.

**Key tools:** Sync uses simple `requests` library. Async uses `asyncio`, `aiohttp`, `queue.Queue` for producer-consumer patterns, and distributed workers (Celery, RabbitMQ) for multi-machine scaling.



# Queue system design for Async Setup

A **queue** is a waiting room for work. It sits between *accepting* a request and *doing* it, so
your API can answer in milliseconds while the slow LLM work happens in the background.

**The core trick:** don't make the user wait. Accept the job, hand back a `job_id` instantly, and
let workers chew through the queue. The user polls for the answer when it's ready.

---

## Why you need one

Without a queue, a traffic spike has only two outcomes — both bad:

```text
  NO QUEUE                             WITH QUEUE
  100 requests arrive at once          100 requests arrive at once
        │                                    │
        ▼                                    ▼
  ┌───────────────┐                    ┌───────────────┐
  │   server      │                    │  queue holds  │  ← buffer absorbs the spike
  │  tries all    │                    │   all 100     │
  │  100 at once  │                    └───────┬───────┘
  └───────────────┘                            │ drains steadily
        │                                      ▼
   OOM / crash / timeouts              3 workers, ~1 job each per 2s
```

A queue turns a **spike** into a **steady stream**. Your workers stay at a load they can survive.

---

## The 4 pieces

```text
   USER              PRODUCER              QUEUE              CONSUMERS
   POST /ask   ──►   FastAPI        ──►  [j5][j4][j3]  ──►   worker-1  ──► LLM
   gets job_id       puts job in           waiting          worker-2  ──► LLM
   in ~5ms           returns instantly      room             worker-3  ──► LLM
                                                                  │
   GET /jobs/7  ◄─────────  result store (dict / Redis / DB)  ◄────┘
```

| Piece | Role | In a RAG app |
|---|---|---|
| **Producer** | accepts work, drops it in the queue | FastAPI `POST /ask` → returns `job_id` |
| **Queue** | holds jobs until someone is free | `asyncio.Queue` (dev) or Redis (prod) |
| **Consumer** (worker) | pulls a job, does the slow part | retrieve chunks → call the LLM |
| **Result store** | where the answer waits for pickup | a dict (dev) or Redis/Postgres (prod) |

---

## Beginner example — `asyncio.Queue`

No Redis, no Docker, no install. 5 questions, 3 workers, each job takes 2 seconds.

```python
import asyncio, time

async def worker(name, queue, results):
    while True:
        job_id, question = await queue.get()
        print(f"[{time.time()-T0:4.1f}s] {name} picked up job {job_id}")
        await asyncio.sleep(2)                 # pretend: retrieve + call the LLM
        results[job_id] = f"answer to {question!r}"
        print(f"[{time.time()-T0:4.1f}s] {name} finished job {job_id}")
        queue.task_done()                      # tell the queue this job is done

async def main():
    queue = asyncio.Queue()
    results = {}

    for i, q in enumerate(["What is RAG?", "Why async?", "What is a queue?",
                           "What is a worker?", "What is Celery?"], start=1):
        queue.put_nowait((i, q))               # producer fills the queue
    print(f"[{time.time()-T0:4.1f}s] producer queued {queue.qsize()} jobs\n")

    workers = [asyncio.create_task(worker(f"worker-{n}", queue, results))
               for n in range(1, 4)]           # 3 consumers, running concurrently

    await queue.join()                         # wait until every job is done
    for w in workers:
        w.cancel()                             # workers loop forever - stop them
    print(f"\n[{time.time()-T0:4.1f}s] all {len(results)} jobs done")

T0 = time.time()
asyncio.run(main())
```

```text
[ 0.0s] producer queued 5 jobs

[ 0.0s] worker-1 picked up job 1
[ 0.0s] worker-2 picked up job 2
[ 0.0s] worker-3 picked up job 3
[ 2.0s] worker-1 finished job 1
[ 2.0s] worker-1 picked up job 4
[ 2.0s] worker-2 finished job 2
[ 2.0s] worker-2 picked up job 5
[ 2.0s] worker-3 finished job 3
[ 4.0s] worker-1 finished job 4
[ 4.0s] worker-2 finished job 5

[ 4.0s] all 5 jobs done
```

**Read the timestamps — that's the whole lesson.** Sequential would be 5 × 2s = **10s**. Three
workers did it in **4s**: jobs 1–3 ran together, then the free workers immediately grabbed 4 and 5.
Worker-3 finished at 2.0s and found an empty queue, so it idled — that's what "more workers than
work" looks like.

| Method | What it does |
|---|---|
| `queue.put_nowait(x)` | add a job, never blocks |
| `await queue.get()` | take a job, **waits** if the queue is empty |
| `queue.task_done()` | mark the job complete — forget this and `join()` hangs forever |
| `await queue.join()` | block until every job has a matching `task_done()` |

---

## Picking a queue technology

| Queue | Survives restart? | Multi-machine? | Use it when |
|---|---|---|---|
| `asyncio.Queue` | ❌ in-memory only | ❌ one process | learning, single-server side jobs |
| **Redis** (list / stream) | ✅ | ✅ | the default production choice — fast and simple |
| **RabbitMQ** | ✅ | ✅ | you need routing, priorities, strong delivery guarantees |
| **Celery** (on Redis/Rabbit) | ✅ | ✅ | you want retries, scheduling, monitoring for free |

**Rule of thumb:** start with `asyncio.Queue`. The moment you need the jobs to **survive a restart**
or run on **more than one machine**, move to Redis. Reach for Celery when you're rewriting retry
logic for the third time.

---

## Concepts that bite beginners

| Concept | What it means | What to do |
|---|---|---|
| **Backpressure** | queue grows faster than workers drain it → memory blows up | `asyncio.Queue(maxsize=100)` — `put` then waits instead of hoarding |
| **At-least-once delivery** | a crashed worker's job gets re-run, so it can run **twice** | make handlers **idempotent** — same input, same result, no double charge |
| **Dead letter queue** | a "poison" job that fails every time blocks the pipeline | after N retries, move it to a separate DLQ and alert |
| **Worker count** | too few = backlog, too many = thrashing | I/O-bound (LLM calls): start high. CPU-bound: ≈ number of cores |
| **Job status** | the user still needs their answer | `GET /jobs/{id}` returns `pending` / `running` / `done` / `failed` |

The typical API shape:

```text
POST /ask       ──►  {"job_id": 7, "status": "pending"}      ~5ms
GET  /jobs/7    ──►  {"status": "running"}                   while a worker has it
GET  /jobs/7    ──►  {"status": "done", "answer": "RAG is…"} once finished
```

---

## Fishbone — why a queue system breaks

```text
                   PRODUCER                    QUEUE
                       \                         /
   no maxsize ──────────\      lost on restart ─/
   blocking put ─────────\     no persistence  /
   no job_id returned ────\                   /
                           \                 /
                            ►  QUEUE SYSTEM FAILS ◄
                           /                 \
   missing task_done() ───/     no status API \
   worker crashes ───────/      results never  \
   no retry limit ──────/       collected       \
                    WORKERS                   RESULTS
```

---

## Gotchas & best practices

| Gotcha | Do this |
|---|---|
| `await queue.join()` hangs forever | you forgot `queue.task_done()` in the worker |
| Worker dies silently on an exception | wrap the body in `try/except`, log it, still call `task_done()` |
| Jobs vanish when the server restarts | `asyncio.Queue` is in-memory — move to Redis |
| Queue grows without limit | set `maxsize` to apply backpressure |
| Same job processed twice | expected under at-least-once — make the handler idempotent |
| Cancelling workers throws noise | `task.cancel()` then `await asyncio.gather(*workers, return_exceptions=True)` |

**Next step — distributed workers.** Everything above still runs in **one process**. Swap
`asyncio.Queue` for **Redis** and the same producer/consumer design spreads across many machines:
FastAPI on one box, a pool of **Celery** workers on others, all sharing one queue. The design
doesn't change — only where the queue lives.

