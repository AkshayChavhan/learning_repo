# What Is MCP? — The Problem It Solves

An LLM alone only predicts the next token. Developers turn it into an **agent** by
attaching **tools** - but everyone wires tools to LLMs their own way. **MCP (Model
Context Protocol)** fixes that: one standard way to connect any tool to any LLM.

---

## 🟢 Beginner — why MCP exists

| Part of an agent | Who controls it | Where MCP fits |
|---|---|---|
| **LLM** (GPT, Claude, Gemini) | the provider - fixed, same for everyone | - |
| **Tools + system prompt** | you | your agent's actual value |
| **How tools connect to the LLM** | before MCP: however you like | **this is what MCP standardizes** |

Without a standard, every team invents its own tool format and its own
calling loop. MCP replaces that with one shared protocol.

---

## 🟡 Intermediate — the USB-C analogy

```text
   iPhone ──┐                               GPT 4.1 ──┐
   MacBook ─┤── USB-C ──► charge / data     Gemini ────┤── MCP ──► Gmail tools
   Android ─┘                               Claude ────┘           X (Twitter) tools
```

One cable charges and transfers data for every device. One protocol
connects every tool to every model - a tool maker builds their tool
**once**, and any MCP-aware agent can plug into it, no custom glue per pairing.

---

## 🔴 Expert — the N × M problem

```text
  WITHOUT MCP                          WITH MCP
  agent A ──custom──► tool 1           agent A ──┐          ┌── tool 1
  agent A ──custom──► tool 2           agent B ──┼── MCP ───┼── tool 2
  agent B ──custom──► tool 1           agent C ──┘          └── tool 3
  agent B ──custom──► tool 2            (N + M)
   (N × M pieces of glue)
```

Without a standard, every agent (N) needs custom glue for every tool
(M) - N × M integrations. With MCP, each side implements the protocol
once - N + M. The tool doesn't care whether GPT, Gemini, or Claude is
calling it.

---

## Gotchas

- **MCP doesn't make the model smarter** - it only standardizes the tool connection.
- **The LLM is a commodity.** Your value is in the tools and the wiring, not the model.
- **Next:** MCP's official architecture - hosts, clients, servers.

> **Interview angle:** *"What problem does MCP solve?"* Every team wires tools to
> LLMs differently, so nothing is reusable. MCP is a standard protocol - like USB-C
> for devices - so a tool maker builds once and any MCP-aware agent can use it.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Agent** | LLM + tools, built for a use case |
| **MCP** | a standard protocol connecting tools to any LLM |
| **USB-C analogy** | one universal plug for every device = one protocol for every tool |
| **N × M → N + M** | the core reason standardization matters |
