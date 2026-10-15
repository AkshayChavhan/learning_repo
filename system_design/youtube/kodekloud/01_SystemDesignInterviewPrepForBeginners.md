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

"Design a URL shortener like bit.ly." Paste a long link, get a short one; clicking the
short one redirects to the long one. Looks too simple, which is why interviewers love it.

### Step 1: clarify

| Question | Why it changes the design | Answer (assumed) |
|---|---|---|
| Custom short links (e.g. branded `kodekloud`)? | changes how codes are generated | no |
| Do links expire? | expiry = cleanup + a check on every click | no, live forever |
| Analytics (click counts)? | affects redirect choice later | nice-to-have |

Restate the scope out loud: *short link → redirect; no custom links; no expiry; analytics
if time permits.*

### Step 2: estimate

| Number | Estimate | What it tells you |
|---|---|---|
| new links per day | 1M → ~12 writes/sec | any DB handles this |
| clicks per link | ~1,000 | **read-heavy, 1000:1**. Focus on the read path |
| links stored over 10 years | 1M × 365 × 10 ≈ **3.6 billion** | code length must cover this |
| redirects per day | 1M × 1,000 = 1B → **~11,000 reads/sec** | one DB is already working hard |

### Step 3: API and data model

| Call | In | Out |
|---|---|---|
| create | long URL | short code |
| redirect | short code (from the browser) | send browser to long URL |

Data model: **one table**, `short_code → long_url`.

**Database choice, the strong answer:** access pattern is one key → one value, no joins,
no multi-row operations. Plain **Postgres with an index on short_code** is fine. Weak
answer: "we need scale, so NoSQL".

### Step 4: high-level design

```text
   CREATE:  user ──long URL──► app server ──generates code, stores (code, url)──► Postgres
                               └──short URL──► user

   CLICK:   user ──short URL──► app server ──lookup code──► Postgres ──long URL──► redirect user
```

Say it: *"This simple version already works. Now let's find the hard part."*

### Step 5: deep dive A, generating the code

Constraints: **short** and **never repeats**.

| Option | How | Problem |
|---|---|---|
| **Hashing** | hash the long URL, take first 7 chars | **collisions**: two URLs can share 7 chars. Must check DB each time, retry with a salt. Collisions grow as the table fills, so creates get slower |
| **Counter + base62** | global counter 1, 2, 3…; encode in base62 (0-9, a-z, A-Z = 62 symbols) | none for uniqueness: 62⁷ ≈ **3.5 trillion** codes, we need 3.6B. No collisions, no retries |

**Counter wins.** State its two weaknesses before the interviewer does:

| Weakness | Fix |
|---|---|
| **guessable**: decode a code → number → +1 → encode → someone else's link. Walk the whole table | **shuffle** the number with a fixed, secret, **reversible** rule before encoding (e.g. rearrange digits + shift). Reversible ⇒ still unique, looks random |
| **concurrent reads**: two requests read the counter at once, both get the same number | lock: read → increment → store as one atomic step (see follow-ups) |

### Step 5: deep dive B, the read path and the hot key

Normal day: 11,000 reads/sec, and every read asks a question **whose answer never
changes**. 1,000 queries for the same code = DB answering the same thing 1,000 times.
Wasteful.

Celebrity posts a link: 1M clicks in an hour, maybe 100M in a day, **all for one code**.
This is a **hot key**, the signature failure of read-heavy systems.

**Fix: a cache (Redis).**

```text
   click ──► app server ──► Redis?  hit  ──► long URL (sub-millisecond, DB never touched)
                              │ miss
                              ▼
                           Postgres (once) ──► store in Redis ──► long URL
```

First viral click hits the DB; the next million are served from the cache.

**Why this is a dream case for caching:** the usual cache headache is **staleness** (cache
has x=7, DB updated to x=9). Here a code always maps to the same URL, written once, never
updated. *"I can cache this aggressively because the data never changes."* Say that
sentence. Also mention: cache memory is finite, Redis evicts least-recently-used entries,
so popular links stay and dead links go.

**Two more upgrades if even the cache is overloaded:**

| Upgrade | What |
|---|---|
| in-process cache | each app server keeps the top few thousand links in its own memory |
| CDN | servers across countries; a user in Tokyo gets the answer from Tokyo, not Virginia |

### Step 5: deep dive C, 301 vs 302

| | 301 Moved Permanently | 302 Found (temporary) |
|---|---|---|
| browser behaviour | **remembers** the answer; next click goes straight to the destination, never asks us | asks us **every time** |
| load / speed | less load, faster | more load |
| analytics | ❌ impossible, clicks never reach us | ✅ |
| kill a bad link (scam page) | ❌ browsers already memorised it | ✅ |

Most candidates pick 301 because "permanent sounds right". **Pick 302** if the business
ever wants click data or the power to disable a link. Exact behaviour depends on headers
and browser config; the interviewer wants the **reasoning**.

### Step 6: bottlenecks

| Question | Answer |
|---|---|
| What breaks first? | Redis crashes → every read lands on the DB → **slow, but not wrong**. Cache refills as queries come. *"The cache is a performance layer, not the source of truth."* |
| What can we never lose? | the **mapping table**. One lost row = that link dead forever. Postgres needs **replicas + backups** |
| What must never repeat? | the **counter**, even after a crash. A repeat = two links, one code |

### Closing summary (30–60 s)

*A click hits our servers; most answers come from the cache and the user is redirected in
milliseconds with a 302 so we keep visibility and control. The mapping table is replicated
and backed up. New links come from a global counter encoded in base62. Reads scale through
caching; writes were never the problem.*

### Key takeaways

1. Read-heavy → **caching**. Serving the same thing repeatedly should trigger "cache".
2. Unique short codes: **counter + base62** (vs hashing and its collisions).
3. **301 vs 302**, and why 302 keeps control.

### Follow-up questions

| Follow-up | Answer |
|---|---|
| Two create requests at the same instant, same code? | No. **Lock** the counter: only one request may read → increment → store at a time |
| The counter is one shared thing. If it goes down? | It's a single point of failure. Give each app server a **block of 10,000 numbers** per call (server 1: 1,000,000–1,010,000; server 2: next block…). Servers allocate locally; the counter is touched rarely and a short outage doesn't stop creates |
| Links should expire after some time? | Add an **expiry date** column; on redirect compare with now; expired → 404. Trade-off: one extra comparison per redirect |

**Lab 1:** run the shortener, create links, fire 200 requests at one and watch each hit the DB.

---

## Problem 2: Rate limiter

Why it matters: in the URL shortener, user "Shadow" writes a loop and creates **1M junk
links in an hour**. The DB fills with garbage, real users see a slow system. Nobody was
hacked; he just called the API too often. A **rate limiter** caps calls per user and
rejects the rest. Core component of ChatGPT, Claude, every API gateway.

### Step 1: clarify

| Question | Options / answer |
|---|---|
| **Who** is making the call? | per **IP** (office of 300 looks like one noisy user; attackers rotate IPs), per **API key** (only developers have them), per **account** (not-logged-in users have none). **Answer:** account for logged-in, IP for anonymous |
| **What limit?** | 100 requests/minute. Don't invent confidently: in reality, measure normal traffic and set the limit comfortably above it |
| **What happens over the limit?** | queue or reject? Queued requests invite duplicate retries. **Reject, politely**: tell the user they were limited and when to retry |

Scope: 100 req/min per user; count by account; extras rejected with a clear message; users
under the limit never notice the limiter exists.

### Step 2: estimate

| Number | Estimate |
|---|---|
| storage per user (simple counter) | one count + one timestamp ≈ **50 bytes** → 10M users ≈ 500 MB, fits in one machine's memory |
| request rate | 10M users × 100 req/**day** = 1B/day ≈ **12,000 req/sec**, ×3 at peak ≈ **35,000/sec** |

Don't confuse the two 100s: **100/day** is the average a normal user makes; **100/minute**
is the limit, which only heavy users approach. A day's 100 arrive in short bursts when the
app is opened, which is exactly why a per-minute limit catches abuse without touching
normal use.

### Step 3: API

One check: *is this request allowed?*

| Response | Include |
|---|---|
| rejected | **429 Too Many Requests** + `Retry-After: 40` so the client doesn't hammer us retrying |
| allowed | remaining requests + reset time, so well-behaved clients slow themselves down |

### Where it lives

At the **front door**: the **API gateway**, the first server every request passes through.
Rejecting deep inside (next to the DB) means a doomed request already travelled half the
system.

### Step 4 + 5: three algorithms

**Fixed window** (the simple version that already works):

One counter per user per clock-minute. Under 100 → +1 and allow. Minute ends → reset to 0.

| Problem | **sharp edges**: 100 requests in the last second of minute 1, 100 in the first second of minute 2. 200 requests in 2 seconds, all allowed, because the clock says two different minutes |
|---|---|

**Sliding window log** (accurate):

Store the **timestamp of every request**. On each new request, drop timestamps older than
60 s, count the rest, reject at 100. The window slides with every request.

| Cost | 100 timestamps per active user ≈ **2.5 KB** instead of 50 bytes → 10M users ≈ **25 GB**. Cost scales with the limit: at 10,000 req/min it's infeasible |
|---|---|

**Token bucket** (what Stripe, GitHub and most gateways use):

Each user has a bucket of **100 tokens**. Every request takes one. The bucket refills at
100/min ≈ **1.67 tokens/sec**, capped at 100. Empty bucket → reject.

| Allen's behaviour | Result |
|---|---|
| drains 100 tokens in 2 s | allowed (burst) |
| keeps going | ~2 requests/sec from now on, never fully locked out |

| Property | |
|---|---|
| burst | allowed, but a **number you chose** (bucket size), not an accident of clock edges. Want smaller bursts? bucket = 20, keep the 1.67/sec refill |
| not a hard "100 per any 60 s" | it's burst + sustained rate |
| storage | tokens left + last refill time ≈ **50 bytes** again |

| Algorithm | Accuracy | Memory / user | Burst control |
|---|---|---|---|
| fixed window | ❌ 2× at edges | 50 B | none |
| sliding window log | ✅ exact | ~2.5 KB (scales with limit) | exact |
| **token bucket** | ✅ good | 50 B | tunable |

> **Transcript ends here (~59:19).** Still to add from the video: where the counters live
> when there are many gateway servers (shared Redis), step 6 bottlenecks, follow-up
> questions, Lab 2.

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
