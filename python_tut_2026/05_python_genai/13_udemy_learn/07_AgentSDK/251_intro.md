# Intro — OpenAI Agents SDK

A section intro, not a technical lecture yet. It names what's coming and why.

---

## Where we are

| Already done in this course | What it taught |
|---|---|
| weather agent with tool calling | an agent = LLM + tools, wired by hand |
| system-prompt JSON loop, memory agents, voice agents | the mechanics underneath |

Hand-wired agents work, but the glue code (prompt format, parsing, call loop) is yours to
write and maintain every time.

---

## What this section adds

**OpenAI Agents SDK**: an official library that does the glue for you.

| It promises | Meaning |
|---|---|
| **simpler** | less boilerplate than the hand-rolled loop |
| **cleaner** | tools, instructions and agents declared, not stitched together |
| **more maintainable** | one standard structure instead of your own conventions |
| **more scalable** | built for multiple agents working together |

> Same agent idea as before. The SDK **abstracts** the parts you've been writing by hand.

---

## Not covered yet

What the SDK's building blocks are, how to install it, how a tool is declared, how agents
hand off to each other. Next lectures.
