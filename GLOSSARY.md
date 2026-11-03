# Glossary — cross-cutting terms

Terms that show up across **many** folders (Python, JS, Git, system design, GenAI) and
deserve one clear definition. Add a term here when it appears in more than one topic.

**Index:** [Hashing](#hashing) · [Base62](#base62) · [CDN](#cdn-content-delivery-network) · [API Gateway](#api-gateway)

---

## Hashing

**Hashing** = turning any input (password, file, string) into a **fixed-size** value called a
**hash** using a **one-way** function. Think of it as a **fingerprint**, not storage.

```text
  input ──hash()──►  hash (fingerprint)
  input ◄──✗──────   hash          (cannot go back)
```

### Three properties

| Property | Meaning | Why it matters |
|---|---|---|
| **Deterministic** | same input → same hash, every time | lets you **compare** without the original |
| **One-way** | cannot get input back from hash | safe to store / publish the hash |
| **Avalanche** | 1-char change → completely different hash | tampering is obvious |

### "If it's one-way, how do I get the data back?"

**You don't — you never need to.** You keep the original elsewhere (or the user keeps it in
their head) and use the hash only to **check "is this the same thing?"**

```text
Sign-up:  "mypassword" ──hash──► "a3f9c…"  (store ONLY this)

Login:    "mypassword" ──hash──► "a3f9c…"  ──► matches? ✅ let in
          "wrongpass"  ──hash──► "7b21e…"  ──► matches? ❌ reject
```

Same input → same hash, so a match proves the user knew the input. The server never
recovers the password.

### Hashing vs encryption

| | **Hashing** | **Encryption** |
|---|---|---|
| Direction | one-way | two-way (with a key) |
| Output size | fixed (e.g. SHA-256 = 64 hex chars) | grows with input |
| Purpose | verify / compare / lookup | hide now, **read again later** |
| Examples | passwords, checksums, dict keys | messages, disk encryption |

> **Rule:** hash when you only need to check *"is this the same?"*; encrypt when you need
> the data *back*.

### Where it shows up in this repo

| Place | How hashing is used |
|---|---|
| Python `dict` / `set` → [tut13](python_tut_2026/03_notes_python/tut13_dictionaries.md), [tut12](python_tut_2026/03_notes_python/tut12_sets.md) | key is hashed → O(1) lookup. That's why keys must be **hashable** (immutable) |
| Git internals → [212](python_tut_2026/05_python_genai/13_udemy_learn/01_full_stack_generative_and_agentic_ai_with_python/05_git/212_gitInternalWorkingAndConfigs.md) | every commit id is a **SHA-1** of content + parent hash → history is tamper-evident |
| URL shortener → [system design](system_design/youtube/kodekloud/01_SystemDesignInterviewPrepForBeginners.md) | hash the long URL, take 7 chars → short code; **collisions** are the gotcha |
| File downloads / integrity | site publishes SHA-256; you hash your copy; equal → not tampered |
| Password storage | store `hash(password)`, never the password; leaked DB reveals nothing usable |
| Deduplication | identical content → identical hash → duplicates spotted instantly |

### Gotchas

- **Collision** — two different inputs with the same hash. Rare for SHA-256, common when
  you truncate (URL shortener's 7 chars). Always plan a retry/check.
- **Fast hash ≠ password hash.** SHA-256 is *fast*, which lets attackers guess billions/sec.
  For passwords use a deliberately **slow, salted** hash (bcrypt, argon2).
- **Salt** — random bytes mixed in before hashing so two users with the same password get
  different hashes, and precomputed "rainbow tables" are useless.
- **MD5 / SHA-1 are broken** for security (collisions can be forged). Fine for non-security
  checksums; use SHA-256+ otherwise.

### Python one-liner

```python
import hashlib
print(hashlib.sha256(b"hello").hexdigest())
print(hashlib.sha256(b"hellO").hexdigest())   # one char changed
```

```text
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
04a6f55face2f46be8c23f627d539827615851e10751b63ec59db6d2c706b770   ← totally different
```

---

## Base62

**Base62** = writing a number with **62 symbols** instead of 10. Same idea as base10
(`0–9`) or base2 (`0–1`), just a bigger alphabet.

| Base | Symbols | Count |
|---|---|---|
| base2 | `0 1` | 2 |
| base10 | `0–9` | 10 |
| base16 (hex) | `0–9 a–f` | 16 |
| **base62** | `0–9` + `a–z` + `A–Z` | **62** |
| base64 | base62 + `+ /` (and `=` padding) | 64 |

### Why it matters

Each character packs more information, so a **big number becomes a short string**.

```text
base10:  125,000,000,000   (12 digits)
base62:  2crtgcg           (7 chars)

      0 → 0        61 → Z        62 → 10        1000 → g8
```

| Length | Unique codes (62ⁿ) |
|---|---|
| 6 chars | ≈ 56 billion |
| **7 chars** | **≈ 3.5 trillion** |

### Where it shows up in this repo

| Place | How it's used |
|---|---|
| URL shortener → [system design](system_design/youtube/kodekloud/01_SystemDesignInterviewPrepForBeginners.md) | keep a **counter** (1, 2, 3…), convert each number to base62 → unique short code, **no collisions** (vs [hashing](#hashing) + truncating) |

### Base62 vs base64

- **base62** is chosen for URLs because all 62 chars are **URL-safe**.
- **base64** adds `+`, `/`, `=`, which must be escaped in URLs. Base64 is for encoding
  *bytes* (images, tokens) as text, not for shortening numbers.

### Python one-liner

```python
import string
A = string.digits + string.ascii_lowercase + string.ascii_uppercase   # 62 chars

def to62(n):
    s = ""
    while n:
        n, r = divmod(n, 62)
        s = A[r] + s
    return s or "0"

print(to62(125_000_000_000))
```

```text
2crtgcg
```

---

## CDN (Content Delivery Network)

**CDN** = a network of servers spread around the world that keep **copies of your static
files** (images, CSS, JS, video) **close to users**. Think of it as a **geographic cache**
for HTTP responses.

```text
Without CDN:  user in Mumbai ──── 200 ms ────► your server in Virginia
With CDN:     user in Mumbai ── 20 ms ──► CDN edge in Mumbai (cached copy)
```

### How a request flows

```text
1. user asks for cdn.site.com/logo.png
2. DNS / anycast → nearest edge (Mumbai)
3. edge checks its cache:
     HIT  → serve from SSD, done
     MISS → fetch from origin, store it, serve it
4. next Mumbai user → HIT
```

### What a CDN is made of

```text
                    DNS / Anycast
                   "nearest edge?"
                         │
   user ────────────────►│
                         ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Mumbai  │   │ London  │   │ Tokyo   │   ◄── edge servers (PoPs)
   │  cache  │   │  cache  │   │  cache  │       nginx / Varnish + SSD
   └────┬────┘   └────┬────┘   └────┬────┘
        └─────────────┼─────────────┘
                      ▼  cache MISS only
               ┌─────────────┐
               │   ORIGIN    │   ◄── your real server / S3 bucket
               └─────────────┘
```

| Block | What it is | How it's built |
|---|---|---|
| **Edge servers (PoPs)** | caching reverse proxies in many cities | `nginx proxy_cache` / Varnish, lots of SSD + RAM |
| **Routing** | send user to the **closest** edge | **GeoDNS** (different IP per region) or **Anycast** (same IP announced everywhere, shortest route wins) |
| **Cache rules** | what to cache, how long, under what key | origin's `Cache-Control: max-age=…`, `ETag`; key = hash of URL |
| **Origin** | the single source of truth | your app server / S3. Only sees **misses** |

### Why it's useful

| Benefit | Why |
|---|---|
| **Faster pages** | served from ~20 ms away instead of ~200 ms |
| **Less origin load** | 90%+ of requests never reach your server |
| **Absorbs spikes / DDoS** | hundreds of PoPs share the hit |
| **Cheaper bandwidth** | CDN egress is cheaper than cloud egress |

Examples: Cloudflare, AWS CloudFront, Akamai, Fastly.

### Mini CDN you could build

1. Rent 3 small VMs in 3 regions.
2. nginx on each: `proxy_pass` → origin, `proxy_cache on`.
3. Geo-routed DNS (Route 53 latency-based) pointing at the 3 IPs.
4. Set `Cache-Control` headers on origin.

### Where it shows up in this repo

| Place | How it's used |
|---|---|
| URL shortener read path → [system design](system_design/youtube/kodekloud/01_SystemDesignInterviewPrepForBeginners.md) | cache layers: Redis → in-process → **CDN** for the hot-key redirect |
| Docker orchestration → [243](python_tut_2026/05_python_genai/13_udemy_learn/01_full_stack_generative_and_agentic_ai_with_python/06_docker/243_introToDockerOrchestrationAndWhyItsCrucialForProduction.md) | listed with load balancing as production infra |

### Gotchas

- **Stale content** after you update a file → **purge** the CDN or use **versioned URLs**
  (`app.v2.js`) so the cache key changes.
- **Thundering herd** on a cold file → real CDNs use **request coalescing** (one origin fetch,
  others wait) and **tiered caching** (edge → regional shield → origin).
- **Dynamic / per-user pages** → don't cache, or cache fragments only; edge compute
  (Cloudflare Workers) for logic at the edge.
- **CDN vs Redis**: same *"check cache first, origin on miss"* pattern. Redis caches **data
  objects** near the app; a CDN caches **HTTP responses** near the **user**.

---

## API Gateway

**API gateway** = the **single front door** for your backend. Every request hits it first;
it checks, limits, and routes the request **before** any of your real code runs.

### Mental model: the hotel reception desk

A hotel has many departments (rooms, restaurant, spa, laundry). You don't walk into the
kitchen to order food. You go to **one desk**; the receptionist checks who you are and
passes your request to the right department.

```text
   You (the app on your phone)
          │
          ▼
   ┌──────────────┐
   │  RECEPTION   │   ◄── API gateway: ONE address, api.site.com
   └──────┬───────┘
          │  "who are you? not too many requests? ok, this is an orders question"
          ▼
   rooms   restaurant   spa   laundry    ◄── your services: users, orders, payments, search
```

| Receptionist says… | Gateway does… |
|---|---|
| "Can I see your room key?" | **authentication** (check token / API key) |
| "You've called 10 times this minute, please wait" | **rate limiting** (429) |
| "Food? That's the restaurant, I'll pass it on" | **routing** (`/orders/*` → orders-service) |
| writes every request in the log book | **logging / metrics** |
| same question again? answers from memory | **caching** |
| speaks to guests in English, to staff in shorthand | **TLS termination** (HTTPS outside, plain HTTP inside) |

### Why have one at all?

```text
   WITHOUT:  client must know 4 addresses; each service repeats auth, limits, logging
   WITH:     client knows ONE address; cross-cutting work done once; services only do business logic
```

### Gateway vs load balancer vs reverse proxy

| | **API gateway** | **Load balancer** | **Reverse proxy** |
|---|---|---|---|
| Understands | your **API** (routes, auth, limits) | servers | HTTP |
| Picks | which **service** | which **copy** of a service | forwards / caches |

They overlap (nginx can be all three). Typical chain:

```text
   client ──► API gateway ──► load balancer ──► orders-service × 3 copies
```

**Examples:** AWS API Gateway, Kong, Nginx, Envoy, Traefik, Apigee.

### Where it shows up in this repo

| Place | How it's used |
|---|---|
| Rate limiter → [system design, Problem 2](system_design/youtube/kodekloud/01_SystemDesignInterviewPrepForBeginners.md#where-it-lives-the-front-door) | the counter lives in the gateway: a doomed request dies at the front door, not after travelling half the system |
| Docker orchestration → [243](python_tut_2026/05_python_genai/13_udemy_learn/01_full_stack_generative_and_agentic_ai_with_python/06_docker/243_introToDockerOrchestrationAndWhyItsCrucialForProduction.md) | the thing in front of all the containers that the outside world actually talks to |

### Gotchas

- **Single point of failure** → run several gateway instances behind a load balancer.
- **One extra hop** on every request (usually ~1 ms).
- **Don't let it become a dumping ground.** Auth, routing, limits only; business logic stays
  in the services.

> **One line:** API gateway = the single front door that checks, limits, and routes every
> request before it reaches your real code.
