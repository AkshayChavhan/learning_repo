# Why Voice Can't Just Be "More Tokens" — S2S vs Chained

An LLM's whole job is: take tokens in, predict the next tokens out. Voice
isn't tokens - this is why building a voice agent needs its own
architecture, not just "feed audio into an LLM."

---

## 🟢 Beginner — you can't feed raw voice into an LLM (today)

```text
   text ──► tokens ──► LLM ──► predicted next tokens
                          │
                   this is ALL it does
```

Voice is a continuous waveform, a spectrum - not tokens. There's no clean
way to hand a wave to something built to predict "the next token from a
fixed vocabulary." As of today (not a permanent law, just the current
state of the tech), no model takes raw voice directly into an LLM.

---

## 🟡 Intermediate — the two named patterns

| Pattern | What it is | Status in this course |
|---|---|---|
| **S2S** (Speech-to-Speech) | one way to build a voice agent | named, not yet explained |
| **Chained architecture** | the commonly-used, foundational pattern | "the meat part" - what actually powers conversational AI behind the scenes |

The key relationship: **S2S itself relies on chained architecture
somewhere underneath it.** Chained isn't just "the other option" - it's
the more fundamental one. That's why this course teaches chained first:
once you know chained architecture, S2S and everything else becomes easy.

---

## 🔴 Expert — why voice can't just be "more tokens"

Text works as tokens because language has a natural **discrete
vocabulary** - a finite set of words/subwords, each with a learnable
probability of coming next. Next-token prediction is tractable *because*
the space of possible next-tokens is fixed and small.

Voice has no equivalent discrete vocabulary: different accents, different
pitch (even within one speaker - excited vs serious), different speech
length, different wavelength. That's continuous, essentially unbounded
variation - there's no fixed set of "next possible audio samples" to
assign clean probabilities over, the way there is for the next word in a
sentence. Discrete-and-bounded (text) vs continuous-and-unbounded (voice)
is why this is a genuinely different problem, not just a bigger one.

---

## Not covered yet

The actual mechanics of either pattern - how chained architecture is
built, how S2S works around this limitation. Next lectures' job.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **S2S (Speech-to-Speech)** | a voice agent pattern - not yet explained in depth |
| **Chained architecture** | the foundational pattern behind conversational AI - even S2S relies on it |
| **Why raw voice can't feed an LLM** | text has a discrete vocabulary to predict over; voice is continuous and unbounded |
