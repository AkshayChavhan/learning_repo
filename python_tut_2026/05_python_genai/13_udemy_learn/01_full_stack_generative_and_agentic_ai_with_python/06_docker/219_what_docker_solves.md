# What Problem Docker Solves

No Docker commands yet - this is the pain, told as a story, that Docker
exists to fix. No mechanism explained; that's deliberately next.

---

## The problem, in two layers

**Layer 1 - a second developer joins.** You've got Node 18, Postgres 12,
MongoDB, and Redis installed locally - the app runs fine. A new teammate
clones the repo from GitHub, but that only gets the *code*. To actually
run it, they need the exact same tools, at the exact same versions -
Node 20 instead of 18, and the app breaks. Every new feature that needs
a new tool means telling every teammate, by hand, to install it.

**Layer 2 - going to production.** Even once your team is in sync, the
production server needs the same setup replicated again - and now
there's a third variable: your Mac, your teammate's Windows machine, and
a Linux production server don't behave identically. Code that "works on
my machine" is not guaranteed to work on theirs.

```text
   dev 1 (Mac, Node 18)  ──┐
   dev 2 (Windows, Node 20) ├── all need the SAME environment ──► production (Linux)
   "works on my machine"  ──┘        this is the actual problem
```

---

## The named problem

**"Works on my machine."** The classic syndrome: an environment that's
correct on one machine, for reasons nobody fully tracked, and wrong
everywhere else. This is exactly what Docker exists to solve.

---

## "But I can pin versions in package.json?"

Yes, and that fixes only **one layer**: the npm libraries. Everything
underneath is still whatever your machine happens to have.

| Layer | Pinned by `package.json`? |
|---|---|
| npm packages | ✅ |
| Node.js version | ❌ `engines` is only a warning |
| Postgres / MongoDB / Redis | ❌ not npm packages |
| gcc, ffmpeg, system libs | ❌ |
| operating system | ❌ |

`package.json` solves *same libraries*. Docker solves *same machine*,
pinning every layer in one image. You still use `package.json` (or
`requirements.txt`) **inside** it.

---

## Not covered yet

How Docker actually solves this - and, before that, what *other*
solutions exist besides Docker. The instructor's explicit homework: think
of alternatives first, so the comparison in the next video actually means something.
