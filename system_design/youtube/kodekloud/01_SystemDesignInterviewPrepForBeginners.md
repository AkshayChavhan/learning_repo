# System Design Interview Prep for Beginners (KodeKloud)

A beginner's framework for system design interviews, then four classic problems solved
with it. Nobody expects a perfect system in 45 minutes. Interviewers grade **how you
think**: narrowing a vague problem, explaining trade-offs, communicating, and taking
hints.

> **Status:** transcript covered up to ~59 min (rate limiter, token bucket). The rest of
> the rate limiter, Notification System and News Feed are placeholders at the bottom.

---

## Navigation

| Part | Jump to |
|---|---|
| What interviewers grade | [What interviewers expect](#what-interviewers-expect) |
| The 6-step framework (memorise this) | [The six-step framework](#the-six-step-framework) |
| First 5 minutes: good vs bad questions | [Clarifying questions](#clarifying-questions) |
| Problem 1 | [URL shortener](#problem-1-url-shortener) |
| Problem 2 | [Rate limiter](#problem-2-rate-limiter) |
| Problem 3 | [Notification system](#problem-3-notification-system-pending) |
| Problem 4 | [News feed](#problem-4-news-feed-pending) |
| Patterns to reuse | [Patterns cheat sheet](#patterns-cheat-sheet) |

---

## How to prepare

- The first few problems will feel like you know nothing. **Normal.** Keep going.
- After a few problems the same patterns repeat: cache, queue, counter, fan-out.
- The only real prep: **solve many problems** until you know which component to use and when.
- Interview questions are open-ended: "design Instagram", "design Dropbox".

---

## What interviewers expect

Feedback never says "knows how a load balancer works". It says things like:

- "can work with an ambiguous problem"
- "explained trade-offs clearly"
- "took the hint and adjusted instead of defending"

| Graded on | Meaning |
|---|---|
| **Judgment under ambiguity** | vague problem → something concrete |
| **Technical depth** | "I'll add a cache" → what problem it solves **and** what new problem it creates |
| **Communication** | explain what you're doing while you do it |
| **Collaboration** | ask the right questions, validate assumptions |

**Two ways to fail:**

| Failure | What it looks like |
|---|---|
| jump straight to architecture | no questions, draws boxes, builds the **wrong** system |
| over-engineer | caches, queues, shards, multi-region, runs out of time |

```text
  Candidate 1: grabs marker, draws servers + DBs + arrows → 10 min: impressive diagram of the wrong system
  Candidate 2: asks who/how many, uploads vs feed? → "I'll do photos + home feed, skip search/DMs"
               → 10 min: a smaller problem they can actually finish
```

Same knowledge, very different scores. Be candidate 2. You need a **method**, not talent.

---

## The six-step framework

| Step | Time | Do | Instagram example |
|---|---|---|---|
| **1. Clarify requirements** | 5 min | turn vague into concrete | users post photos, follow users, scroll a feed; feed loads fast |
| **2. Back-of-envelope estimation** | 5 min | numbers that decide scale | 10M daily users, scroll 100 / post 1 per week → **read-heavy** |
| **3. Define the API** | 5 min | the few calls users make | `uploadPhoto`, `followUser`, `getFeed` → tells you what to store |
| **4. High-level design** | 10–15 min | plain boxes that satisfy the requirements | user → app server → DB (users, follows) + photo storage |
| **5. Deep dives** | 10–15 min | the 1–2 genuinely hard parts | celebrity with 1M followers posts: how does it reach 1M feeds? |
| **6. Bottlenecks & scaling** | 5 min | what breaks first, what you'd do | follows DB at 10× traffic → cache in front |
| **Summary** | 30–60 s | recap what you built | |

Confirm numbers with the interviewer **before** building on them.

---

## Clarifying questions

Interviewers ask vague questions on purpose. "Photo sharing" could be Instagram (billions
of small images, fast feed) or Flickr (fewer users, huge uncompressed images).

**The one test for any question:** *will the answer change my design?*
If A → design one way, B → another way: ask. Otherwise state your assumption and move on.

### Bad questions

| Question | Why bad |
|---|---|
| "SQL or NoSQL?" | your decision, from the access pattern. Not the interviewer's |
| "Should it be scalable and highly available?" | "yes" adds no information. Ask **how many users, growing how fast** |
| any of 15 memorised questions in a row | not thinking, reciting |
| asking a good question, then **ignoring the answer** | told 10,000 users, built a massive distributed system anyway |

### Good questions (non-functional)

Functional requirements ("what does it do") are easy: ask, the interviewer describes it.
Non-functional ("how well") needs these four:

1. How many users, and how fast is that growing?
2. Do people **read** more or **write** more?
3. What data can we **not afford to lose**?
4. How **fast** should the important actions feel (latency)?

When asked to pick numbers yourself, **give the reasoning**: *"Consumer photo app, say 10M
daily actives, people scroll a lot but post rarely, so read-heavy. Reasonable?"*

### Worked example: ticket booking (Ticketmaster)

| Question | Decides |
|---|---|
| Only booking, or also organisers creating events? | **scope** |
| How many people show up when a big event goes on sale? (say 10M) | **scale** |
| When one user starts checkout, is that seat locked for others? For how long? | the **hard part**: seat holds, locks, timers |
| Do users search for events, or arrive with a direct link? | **features** |

Four questions → scope, scale, hard part, features.

---

## Problem 1: URL shortener

"Design a URL shortener like bit.ly."

```text
   paste:   https://kodekloud.com/courses/system-design/lesson-12?ref=newsletter
   get:     https://kk.io/g8Zx2Qa            ◄── 7 characters
   click:   kk.io/g8Zx2Qa  ──►  browser lands on the long page
```

Two jobs only: **make** a short code for a long URL, and **redirect** a short code back to
its long URL. Looks too simple, which is why interviewers love it: the difficulty is
hidden in the numbers.

### The whole answer in one picture

Read this first, then the steps below explain how we get here.

```text
  CREATE (rare, ~12/sec)
  user ──long URL──► app server ──next number from counter──► base62 ──► "g8Zx2Qa"
                                 └── save (g8Zx2Qa → long URL) in Postgres

  CLICK (constant, ~11,000/sec)
  user ──kk.io/g8Zx2Qa──► app server ──► Redis has it?  yes ──► 302 redirect (fast)
                                              │ no
                                              ▼
                                           Postgres ──► put in Redis ──► 302 redirect
```

Three ideas carry the whole design: **counter + base62** for codes, **cache** for reads,
**302** for the redirect. Each gets a step below.

### Step 1: clarify (what are we NOT building?)

Ask 3 questions. Each answer removes work.

| Question | If "yes" you'd also need… | Our answer |
|---|---|---|
| Custom short links (`kk.io/my-course`)? | user-chosen names, name clashes | **no** |
| Do links expire? | cleanup job + a date check on every click | **no**, live forever |
| Click analytics? | counting on every redirect (affects Step 5C) | **nice-to-have** |

Say it out loud: *"short link → redirect; no custom links; no expiry; analytics if time
permits."* Now you both know the target.

### Step 2: estimate (find the hard part with arithmetic)

Rough numbers are enough. The point is to discover **which side is heavy**.

| Question | Arithmetic | Result | So what? |
|---|---|---|---|
| New links per day? | 1M ÷ 86,400 sec | **~12 writes/sec** | tiny, any DB copes |
| Clicks per link? | assume ~1,000 | **reads : writes = 1000 : 1** | **read-heavy** system |
| Clicks per day? | 1M × 1,000 = 1B ÷ 86,400 | **~11,000 reads/sec** | one DB is already sweating |
| Links in 10 years? | 1M × 365 × 10 | **~3.6 billion** | code must have ≥ 3.6B combinations |

**Conclusion:** writes are nothing. **All the effort goes into the read (redirect) path.**

### Step 3: API and data model (keep it boring)

| Call | In | Out |
|---|---|---|
| `POST /create` | long URL | short code |
| `GET /{code}` | short code | redirect to long URL |

**Data model:** one table, two columns.

```text
   short_code (indexed) │ long_url
   ───────────────────────────────────────────────
   g8Zx2Qa              │ https://kodekloud.com/courses/...
```

**Which database?** The access pattern is *one key → one value*, no joins, no multi-row
updates. **Postgres with an index on `short_code`** is the strong answer.
*"We need scale, so NoSQL"* is the weak answer: it names a tool without a reason.

### Step 4: high-level design (the version that already works)

```text
   CREATE:  user ──long URL──► app server ──make code, save (code, url)──► Postgres
                               └──short URL──► user

   CLICK:   user ──short URL──► app server ──look up code──► Postgres ──long URL──► redirect
```

Say: *"This simple version works. Now let's find what breaks."* Two things will: how we
**make** the code (5A) and how we **survive 11,000 reads/sec** (5B).

### Step 5A: deep dive, making the short code

The code must be **short** (7 chars) and **never repeat**. Two ways to make it:

| Option | How | Example | Problem |
|---|---|---|---|
| **Hashing** ([glossary](../../../GLOSSARY.md#hashing)) | hash the long URL, keep first 7 chars | `sha256(url)` = `a3f9c1e…` → `a3f9c1e` | **collisions**: two different URLs can share the same 7 chars. Must check DB every time and retry. Gets worse as the table fills |
| **Counter + base62** ([glossary](../../../GLOSSARY.md#base62)) | global counter 1, 2, 3…; write the number in base62 | `1000` → `g8`, `125,000,000,000` → `2crtgcg` | none for uniqueness: 62⁷ ≈ **3.5 trillion** codes, we need 3.6B |

```text
   counter:  … 1000   1001   1002 …
   base62:   …  g8     g9     ga  …     ◄── every number → a different code, by definition
```

**Counter wins.** Now beat the interviewer to its two weaknesses:

| Weakness | Why it's a problem | Fix |
|---|---|---|
| **Guessable** | `g8` → 1000 → +1 → `g9` → I just found someone else's link. I can walk the whole table | **shuffle** the number with a fixed, secret, **reversible** rule before base62 (e.g. rearrange digits + shift). Reversible ⇒ still unique, but looks random |
| **Race condition** | two servers read counter = 1000 at the same instant, both make `g8` | make read → increment → store **one atomic step** (a lock, or Redis `INCR`). See follow-ups |

### Step 5B: deep dive, the read path and the "hot key"

**Normal day:** 11,000 reads/sec, and each one asks a question **whose answer never
changes**. 1,000 people click `g8Zx2Qa`, the DB looks up the same row 1,000 times.
Wasteful.

**Bad day:** a celebrity posts one link. 1M clicks in an hour, maybe 100M in a day, **all
for one code**. That one row is a **hot key**, the classic failure of read-heavy systems.

**Fix: put Redis in front of the DB.**

```text
   click ──► app server ──► Redis has code?  HIT ──► long URL (sub-ms, DB never touched)
                                │ MISS (first time only)
                                ▼
                             Postgres ──► save in Redis ──► long URL
```

The **first** viral click reaches Postgres. The next **million** are answered by Redis.

**Why this is the easiest cache you will ever design:** the usual cache problem is
**staleness** (cache says x=7, DB was updated to x=9). Here a code is written once and
**never changes**, so the cache can never be wrong. Say this sentence: *"I can cache
aggressively because the data is immutable."*

Also mention: Redis memory is finite, it evicts **least recently used** keys, so hot links
stay in and dead links fall out by themselves.

**If even Redis is overloaded**, two more layers, each closer to the user:

| Layer | Where | What |
|---|---|---|
| in-process cache | inside each app server | top few thousand links in local memory, no network hop |
| CDN ([glossary](../../../GLOSSARY.md#cdn-content-delivery-network)) | servers around the world | a user in Tokyo gets the redirect from Tokyo, not Virginia |

### Step 5C: deep dive, 301 vs 302

A redirect is an HTTP status code. There are two, and the choice matters.

```text
   301 "moved permanently"   browser writes a sticky note: "kk.io/g8Zx2Qa = long URL"
                             next click → goes straight there, never asks us again

   302 "found" (temporary)   browser asks us every single time
```

| | **301** permanent | **302** temporary |
|---|---|---|
| load on us | less (browser remembers) | more (every click reaches us) |
| speed for user | slightly faster after first click | one extra hop each time |
| click analytics | ❌ impossible, we never see repeat clicks | ✅ |
| disable a scam link | ❌ browsers already memorised it | ✅ |

Most candidates pick 301 because "permanent sounds right". **Pick 302** if the business
ever wants click data or the power to kill a link. (Exact behaviour varies with headers and
browser settings; the interviewer wants the **reasoning**, not the RFC.)

### Step 6: bottlenecks (what breaks, and does it matter?)

| Question | Answer |
|---|---|
| What breaks first? | **Redis dies** → every read hits Postgres → **slow, but still correct**. Cache refills as people click. *"The cache is a performance layer, not the source of truth."* |
| What can we never lose? | the **mapping table**. One lost row = that link dead forever. Postgres gets **replicas + backups** |
| What must never repeat? | the **counter**, even after a crash. A repeated number = two links, one code |

### Closing summary (say this in 30–60 s)

*A click hits our servers; most answers come from Redis and the user is redirected in
milliseconds with a 302, so we keep visibility and control. The mapping table is
replicated and backed up. New links get a number from a global counter encoded in base62.
Reads scale through caching; writes were never the problem.*

### If you remember only 3 things

1. **Read-heavy → cache.** "Same answer served again and again" should trigger "Redis".
2. **Counter + base62** makes short, unique codes. Hashing collides.
3. **302, not 301**, so you keep analytics and the kill switch.

### Follow-up questions

| Follow-up | Answer |
|---|---|
| Two create requests at the same instant, same code? | No. The counter's read → increment → store is **atomic** (locked). Only one request at a time |
| The counter is one shared thing. If it goes down? | Single point of failure. Hand each app server a **block of 10,000 numbers** at a time (server 1: 1,000,000–1,009,999; server 2: next block…). Servers count locally; the central counter is touched rarely, and a short outage doesn't stop creates |
| Links should expire after some time? | Add an **expiry date** column; on redirect compare with now; expired → 404. Cost: one extra comparison per redirect |

**Lab 1:** run the shortener, create links, fire 200 requests at one and watch each hit the DB.
---

## Problem 2: Rate limiter

"Design a rate limiter."

```text
   rule:  max 100 requests per minute per user

   user:  req 1 ✅  req 2 ✅  …  req 100 ✅  req 101 ❌  429 Too Many Requests, Retry-After: 40
          └──────────────── same 60-second window ────────────────┘
```

**Why it matters:** in the URL shortener, user "Shadow" writes a loop and creates **1M junk
links in an hour**. Nobody was hacked, he just called the API too often, but the DB fills
with garbage and real users get a slow system. A **rate limiter** caps calls per user and
rejects the rest. It sits in front of ChatGPT, Claude, Stripe, and every API gateway.

### The whole answer in one picture

```text
   request ──► API GATEWAY (front door) ──► "has user:42 still got budget this minute?"
                    │                              │
                    │  yes                         │  no
                    ▼                              ▼
             pass to app servers          429 + Retry-After, request never goes deeper
```

Four decisions make the design: **who** to count, **what limit**, **what to do when over**,
and **which counting algorithm** (the deep dive).

### Step 1: clarify (who, how much, then what?)

| Question | Options | Our answer |
|---|---|---|
| **Who** is "one user"? | per **IP**: an office of 300 looks like one noisy user; attackers rotate IPs. Per **API key**: only developers have one. Per **account**: anonymous users have none | **account** when logged in, **IP** when anonymous |
| **What limit?** | pick a number, but say how you'd really choose it: **measure** normal traffic, set the limit comfortably above | 100 req/min |
| **Over the limit, then what?** | **queue** (invites duplicate retries, memory grows) or **reject** | **reject politely**: say you were limited and when to retry |

Scope in one line: *100 req/min per account; extras get a clear 429; users under the limit
never notice the limiter exists.*

### Step 2: estimate (does it fit in memory?)

| Question | Arithmetic | Result | So what? |
|---|---|---|---|
| Storage per user? | one count + one timestamp | **~50 bytes** | 10M users ≈ 500 MB, fits in one machine's RAM |
| Requests per second? | 10M users × 100 req/**day** = 1B/day ÷ 86,400 | **~12,000/sec**, ×3 at peak ≈ **35,000/sec** | the limiter itself must be very fast |

**Two different 100s, don't mix them up:**

```text
   100 per DAY     = what a normal user averages (arrives in short bursts when the app opens)
   100 per MINUTE  = the limit; only abusers get near it
```

That gap is exactly why a per-minute limit catches abuse without touching normal use.

### Step 3: API (one question, two answers)

The limiter answers one question: *is this request allowed?*

| Response | Include | Why |
|---|---|---|
| **rejected** | `429 Too Many Requests` + `Retry-After: 40` | so the client waits instead of hammering us with retries |
| **allowed** | `X-RateLimit-Remaining`, reset time | so well-behaved clients slow themselves down |

### Where it lives: the front door

```text
   ❌ deep inside:   client ──► gateway ──► app ──► service ──► DB ──► "rejected"
                                 (doomed request already travelled half the system)

   ✅ at the gate:   client ──► gateway ──► "rejected"   (nothing else did any work)
```

The **API gateway** is the first server every request passes through. Reject there.

### Step 4 + 5: three algorithms (the deep dive)

All three answer "has this user exceeded 100 in a minute?". They differ in **how they
define "a minute"** and **how much memory** that costs.

#### 1. Fixed window: a counter that resets on the clock

One counter per user per clock-minute. Under 100 → +1 and allow. Minute ends → reset to 0.

```text
   minute 1                    │ minute 2
   ...................100 reqs │ 100 reqs...................
                        ↑      │ ↑
                     0:59      │ 1:00        ◄── 200 requests in 2 seconds, all allowed
```

| Pro | Con |
|---|---|
| simplest possible: `INCR` + `EXPIRE 60` | **sharp edges**: the clock says "two different minutes", so a 2× burst slips through |

#### 2. Sliding window log: count only the last 60 seconds from *now*

Store the **timestamp of every request**. On each new request: drop timestamps older than
60 s, count what's left, reject at 100. The window moves with every request, so there are no
edges.

```text
   now = 1:00:30
   keep timestamps in (0:59:30 … 1:00:30]  ──► count = 100 ──► reject the 101st
```

| Pro | Con |
|---|---|
| **exact**, no edge burst | 100 timestamps per active user ≈ **2.5 KB** instead of 50 B → 10M users ≈ **25 GB**. Cost grows with the limit: at 10,000 req/min it's infeasible |

#### 3. Token bucket: a budget that refills steadily

Each user has a bucket of **100 tokens**. Every request spends one. The bucket refills at
100/min ≈ **1.67 tokens/sec**, capped at 100. Empty bucket → reject.

```text
   bucket (max 100)        ◄── refill: +1.67 tokens every second
   ┌──────────────┐
   │ ●●●●●●●●●●●● │ ──► each request takes 1 token
   └──────────────┘
   empty? → 429
```

| User "Allen" does… | Result |
|---|---|
| spends all 100 tokens in 2 s | allowed, that's a **burst** |
| keeps going | gets ~2 req/sec from now on (the refill rate), never fully locked out |

| Property | Detail |
|---|---|
| burst | allowed, but a **number you chose** (bucket size), not an accident of the clock. Want smaller bursts? bucket = 20, keep the 1.67/sec refill |
| meaning of the limit | not a hard "100 per any 60 s"; it's **burst size + sustained rate** |
| storage | tokens left + last refill time ≈ **50 bytes**, same as fixed window |

#### Compare

| Algorithm | Accuracy | Memory / user | Burst control | Used by |
|---|---|---|---|---|
| fixed window | ❌ 2× at edges | 50 B | none | simple internal tools |
| sliding window log | ✅ exact | ~2.5 KB (grows with limit) | exact | small limits only |
| **token bucket** | ✅ good | 50 B | **tunable** | Stripe, GitHub, most gateways |

### Where the counters live (from our discussion, not yet in the transcript)

There are many gateway servers, but the limit is **per user across all of them**. So the
bucket/counter must sit in one **shared, fast** place: **Redis**.

```text
   gateway 1 ──┐
   gateway 2 ──┼──► Redis: INCR user:42:1:00  →  101 > 100?  →  429
   gateway 3 ──┘          (atomic, so two gateways can't both allow the 100th)
                          EXPIRE 60 makes the window clean itself up
```

### If you remember only 3 things

1. Limit at the **front door** (gateway), not deep inside.
2. **Token bucket**: 50 bytes per user, bursts are a knob you set, nobody gets locked out forever.
3. Reject with **429 + Retry-After**, so clients back off instead of retrying harder.

> **Transcript ends here (~59:19).** Still to add from the video: step 6 bottlenecks,
> follow-up questions, Lab 2.
---

## Problem 3: Notification system (pending)

Transcript not yet provided. Video timestamps: 01:14:15 design, 01:52:12 interview
questions, 01:57:39 lab.

---

## Problem 4: News feed (pending)

Transcript not yet provided. Video timestamps: 01:58:00 design, 02:35:13 interview
questions, 02:45:00 lab (feed fan-out).

---

## Patterns cheat sheet

| You see | Reach for | Seen in |
|---|---|---|
| same answer served over and over | **cache** (Redis), then in-process cache, then CDN | URL shortener |
| one item suddenly accessed by millions | **hot key** → cache | URL shortener |
| need unique short ids | **counter + base62**, shuffled; block allocation for resilience | URL shortener |
| data written once, never updated | cache aggressively, no staleness | URL shortener |
| a shared counter / single point of failure | hand out **blocks** to servers | URL shortener |
| keep analytics / ability to revoke | **302** not 301 | URL shortener |
| one user abusing an API | **rate limiter** at the gateway, 429 + Retry-After | rate limiter |
| limit with controlled bursts, tiny memory | **token bucket** | rate limiter |
| "cache died" | slow, not wrong: performance layer vs source of truth | URL shortener |
| "what can we never lose" | replicas + backups for that table | URL shortener |

> **Interview reflex:** clarify (5) → estimate (5) → API (5) → boxes (10–15) → the one hard
> part (10–15) → what breaks first (5) → 60-second summary. Every question you ask must be
> able to change the design.
