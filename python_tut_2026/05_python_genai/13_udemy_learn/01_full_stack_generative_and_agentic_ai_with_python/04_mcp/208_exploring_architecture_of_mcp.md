# MCP — Model Context Protocol

MCP is an open standard, from Anthropic, that lets an AI model connect to
live data sources and tools through one common interface - instead of a
custom integration for every data source.

---

## 🟢 Beginner — the USB-C analogy

> "Think of MCP like a USB-C port for AI applications. Just as USB-C
> provides a standardized way to connect devices to peripherals, MCP
> provides a standardized way to connect AI models to different data
> sources." - MCP's own documentation

| | |
|---|---|
| Created by | Anthropic (the company behind Claude) |
| Announced | November 25, 2024 - open-sourced the spec, Python/TypeScript SDKs, and prebuilt servers |
| Current status | donated to the **Agentic AI Foundation** under the Linux Foundation (December 2025) - no longer Anthropic-owned alone |

---

## 🟡 Intermediate — the problem it actually solves

Models are trained once, on a fixed snapshot of data. New data sources
show up constantly - a new database, a new API, a new tool - and you
can't retrain a model every time one appears. Before MCP, connecting a
model to each new source meant a **custom, one-off integration** per
source. That doesn't scale.

MCP fixes this by giving every data source the *same* kind of connector:

```text
   LLM ──MCP──► Postgres
   LLM ──MCP──► MongoDB
   LLM ──MCP──► Google Search
   LLM ──MCP──► Snowflake
   LLM ──MCP──► GitHub
```

One protocol, many sources - the model gains access to whatever the MCP
server exposes (query a database, search the web, read GitHub issues)
without a bespoke integration for each one. In practice, most major
platforms now expose their own MCP server: GitHub, Hugging Face, Figma,
Playwright, Notion, Linear, and more.

---

## 🔴 Expert — the three-part architecture

| Component | What it is | Example |
|---|---|---|
| **MCP Host** | the AI application itself | your IDE, Claude Desktop, any agent app |
| **MCP Client** | lives *inside* the host, maintains a **1:1 connection** to one server | the IDE's built-in "Add MCP Server" feature |
| **MCP Server** | exposes a specific data source or tool | a GitHub MCP server, a Postgres MCP server, a filesystem MCP server |

```text
                    MCP HOST  (your AI application)
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    MCP Client 1   MCP Client 2   MCP Client 3
          │              │              │
          ▼              ▼              ▼
    MCP Server      MCP Server      MCP Server
    (filesystem)     (database)      (GitHub)
```

**One host can run many clients. Each client talks to exactly one
server.** Browsing an IDE's "MCP servers" list (GitHub, Hugging Face,
Figma, Playwright...) and installing one is literally registering a new
client → server connection - install the GitHub MCP server, and the
agent running in that host now has access to your pull requests and
issues, with no custom integration code written.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **MCP** | an open standard for connecting AI models to data sources/tools, one common interface |
| **MCP Host** | the AI application (e.g. an IDE, Claude Desktop) |
| **MCP Client** | lives inside the host, one connection per server |
| **MCP Server** | exposes one specific data source or tool (DB, GitHub, filesystem, etc.) |

---

## Sources

- [History of the Model Context Protocol (MCP)](https://www.taskade.com/blog/mcp-protocol-history)
