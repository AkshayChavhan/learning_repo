## Interview cheat sheet: what to remember from this doc

### How interviewers grade you

| They reward | They punish |
|---|---|
| handling an ambiguous problem | jumping straight to boxes, building the wrong system |
| explaining **both halves** of a trade-off (what it solves, what it breaks) | over-engineering: caches, shards, multi-region, out of time |
| talking while designing | silently drawing |
| taking a hint and adjusting | defending |

**Six steps, timed:** clarify (5) → estimate (5) → API (5) → high-level boxes (10–15) →
1–2 deep dives (10–15) → bottlenecks (5) → 60-second summary.

### Clarifying questions

- **One test for any question:** *will the answer change my design?* Yes → ask. No → state the assumption, move on.
- **The four non-functional questions:** how many users and growing how fast · read-heavy or write-heavy · what can we never lose · how fast must the key action feel.
- **Never ask:** "SQL or NoSQL?" (your call, from the access pattern) · "should it be scalable?" (useless "yes") · a question you then ignore.
- **Ticketmaster pattern:** one question each for **scope, scale, the hard part, features**.
- Every "yes" must **remove or add work** you can name (custom links → name clashes; expiry → cleanup job + date check per click).
- Pick numbers with reasoning out loud, then **confirm before building on them**.

### Estimation habits

- per-day ÷ 86,400 = per-second · ×3 for peak.
- Every number ends with a **"so what"**: *"12 writes/sec, tiny"* · *"11,000 reads/sec, one DB is sweating"*.
- The point of estimation is to find **which side is heavy**, that's where the deep dive goes.

### URL shortener

| Topic | The answer | Why |
|---|---|---|
| numbers | 1M links/day = **12 writes/s**; ×1,000 clicks = **11,000 reads/s**; 10 yrs = **3.6B** links | read-heavy, all effort on redirect path |
| DB | **Postgres + index on short_code**, one table, two columns | key → value, no joins. "NoSQL for scale" names a tool without a reason |
| code generation | **counter + base62** (62⁷ ≈ 3.5T) | hashing collides, needs DB check + retry, gets worse as table fills |
| guessable codes | secret **reversible shuffle** before base62 | reversible ⇒ still unique, looks random |
| race on counter | read → increment → store is **atomic** (lock / Redis `INCR`) | two servers must not both get 1000 |
| counter is a SPOF | hand each server a **block of 10,000** numbers | central counter touched rarely, survives short outage |
| hot key | **Redis in front of Postgres**; first click misses, next million hit | one viral link = same row a million times |
| why cache is safe | *"I can cache aggressively because the data is immutable"* | no staleness, the usual cache problem doesn't exist |
| beyond Redis | in-process cache → CDN; LRU evicts dead links by itself | each layer closer to the user |
| redirect | **302**, not 301 | 301 lets browsers memorise it: no analytics, can't kill a scam link |
| Redis dies | **slow, not wrong** | *"cache is a performance layer, not the source of truth"* |
| never lose | the mapping table → replicas + backups; the counter must never repeat after a crash | one lost row = dead link; repeated number = two links, one code |
| expiry follow-up | expiry column, compare on redirect, 404 if past | one extra comparison per click |

**Pivot sentence after high-level design:** *"This simple version works. Now let's find what breaks."*

**30-second summary:** click hits our servers → mostly answered by Redis → 302 in ms, we keep
visibility and control → mapping table replicated and backed up → codes from a global counter in
base62 → reads scale through caching, writes were never the problem.

### Rate limiter

| Topic | The answer | Why |
|---|---|---|
| why it exists | one user loops and creates 1M junk links/hour; nobody hacked, just called too often | protects real users, not only security. Sits in front of Stripe, GitHub, every gateway |
| who is a user | **account** when logged in, **IP** when anonymous | per-IP: office of 300 = one abuser, attackers rotate IPs; API keys only devs have |
| what limit | **measure** normal traffic, set comfortably above | normal user ≈ 100/**day** in bursts, limit = 100/**min**, only abusers get near |
| over the limit | **reject**, don't queue | queue invites duplicate retries, memory grows |
| response | `429` + `Retry-After` on reject; `X-RateLimit-Remaining` + reset on allow | clients back off instead of retrying harder |
| where | **API gateway**, the front door | a doomed request shouldn't travel half the system |
| memory | count + timestamp ≈ **50 B** → 10M users ≈ 500 MB, one machine | justify the in-memory choice with arithmetic |
| counters live in | **Redis**, shared by all gateways, atomic `INCR`, `EXPIRE 60` | limit is per user across every gateway |

| Algorithm | Accuracy | Memory / user | Burst control | Used by |
|---|---|---|---|---|
| fixed window (`INCR` + `EXPIRE 60`) | ❌ 2× at window edges | 50 B | none | simple internal tools |
| sliding window log (store every timestamp) | ✅ exact | ~2.5 KB, **grows with the limit** (10M users ≈ 25 GB) | exact | small limits only |
| **token bucket** | ✅ good | 50 B | **tunable** (bucket = burst, refill = sustained rate) | Stripe, GitHub, most gateways |

Token bucket maths: 100/min = **1.67 tokens/s**. Drain it in 2 s → still get ~2 req/s after,
never locked out forever. Smaller bursts? bucket = 20, same refill.

### Patterns: symptom → component

| You hear | Reach for |
|---|---|
| same answer served over and over | cache (Redis) → in-process → CDN |
| one item hit by millions | hot key → cache |
| unique short IDs | counter + base62, shuffled; block allocation |
| written once, never updated | cache aggressively, no staleness |
| shared counter / single point of failure | hand out blocks |
| keep analytics / revoke links | 302 not 301 |
| one user abusing an API | rate limiter at the gateway, 429 + Retry-After |
| bursts allowed, tiny memory | token bucket |
| "cache died" | slow, not wrong |
| "what can we never lose" | replicas + backups for that table |

### Sentences to say verbatim

- "Will the answer change my design?"
- "I can cache aggressively because the data is immutable."
- "The cache is a performance layer, not the source of truth."
- "Reject at the gate, so nothing else does any work."
- "Writes were never the problem; reads scale through caching."
- "This simple version works. Now let's find what breaks."
