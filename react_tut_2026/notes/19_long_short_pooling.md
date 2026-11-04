# 19: Polling & WebSockets

> The client needs **fresh data** from the server. There are three ways to get it:
>
> - **Short polling:** ask on a fixed timer.
> - **Long polling:** ask, and the server replies only when it has news.
> - **WebSocket:** open one two-way connection, and messages flow both ways.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Polling** | The client repeatedly requests updates from the server |
| **Short polling** | Request, get an answer right away, wait a fixed time, repeat |
| **Long polling** | Request, the server holds it open until data arrives or a timeout, then the client immediately re-requests |
| **WebSocket** | One persistent, two-way connection. Either side can send at any time |

---

## 🟢 Beginner: the three approaches

```text
Short polling:   client ──req──► server ──res──►  wait 5s  ──req──► server ──res──► ...
Long polling:    client ──req──► server  (holds)  ...news!──res──► client ──req──► ...
WebSocket:       client ◄═════ one open connection ═════► server   (messages both ways)
```

| | Short polling | Long polling | WebSocket |
|---|---|---|---|
| Connection | New request each time | New request after each reply | **One** connection, kept open |
| Who starts a message? | Client only | Client, but the server replies when ready | **Either side** |
| Latency | Up to the polling interval | Near instant | Near instant |
| Wasted requests | Many, when nothing changed | Few | None |
| Complexity | Simplest | Medium | Most setup |

---

## 🟡 Intermediate: short and long polling

### Short polling

The client asks every few seconds, whether or not anything changed.

```javascript
// Client
const id = setInterval(async () => {
  const res = await fetch("/api/status");
  const data = await res.json();
  console.log(data);
}, 5000);

// Server
app.get("/api/status", (req, res) => {
  res.json({ status: getCurrentStatus() });   // answers immediately
});
```

- **Simple** to build.
- **Wasteful** when nothing has changed: most requests return the same data.
- Stop it with `clearInterval(id)`. In React, return it from `useEffect`:

```jsx
useEffect(() => {
  const id = setInterval(async () => {
    const res = await fetch("/api/status");
    setStatus(await res.json());
  }, 5000);

  return () => clearInterval(id);   // stop on unmount
}, []);
```

### Long polling

The server **holds** the request open until it has new data or a timeout passes.

```javascript
// Server
app.get("/api/updates", async (req, res) => {
  const update = await waitForNewData(30000);   // waits up to 30 seconds
  res.json(update);
});
```

```jsx
// Client (React)
useEffect(() => {
  let active = true;

  async function listen() {
    while (active) {
      try {
        const res = await fetch("/api/updates");
        const data = await res.json();
        if (active) console.log(data);
      } catch (error) {
        await new Promise(r => setTimeout(r, 2000));   // back off before retrying
      }
    }
  }

  listen();
  return () => { active = false; };   // stops the loop after the current request
}, []);
```

> **Why the `try/catch` and delay?** If the server is down, `fetch` fails immediately, and the loop would spin and flood the server. A short pause prevents that.

### Long polling vs short polling

| Situation | Better choice |
|---|---|
| Updates every few minutes | Short polling is fine |
| Updates should arrive within seconds | Long polling |
| Many clients, very frequent changes | WebSocket |

---

## 🔴 Expert: WebSockets

### The client

```javascript
const socket = new WebSocket("wss://example.com/chat");

socket.onopen = () => {
  socket.send("hello server");          // safe only after the connection is open
};

socket.onmessage = (event) => {
  console.log("Server says:", event.data);
};

socket.onclose = () => console.log("Disconnected");
```

> **Common bug:** calling `socket.send()` right after `new WebSocket(...)` fails, because the connection is still opening. Send inside `onopen`.

### The server (Node.js with the `ws` library)

```javascript
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", (socket) => {          // one call per client
  socket.on("message", (msg) => {
    socket.send(`You said: ${msg.toString()}`);   // reply on the same connection
  });
});
```

- Each client gets its own `socket` object.
- The server can also send messages at any time, not only in reply.

### Using a WebSocket in React

```jsx
useEffect(() => {
  const socket = new WebSocket("wss://example.com/chat");

  socket.onmessage = (event) => setMessages(prev => [...prev, event.data]);

  return () => socket.close();        // close when the component unmounts
}, []);
```

> Close the socket in the cleanup, or it stays open after the component is gone.

### Choosing a method

| Need | Use |
|---|---|
| Check something occasionally | Short polling |
| Get news quickly, server → client only | Long polling, or Server-Sent Events (see note 20) |
| Two-way, real-time messages (chat, games, collaboration) | WebSocket |

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Polling interval with no cleanup in React | Return `clearInterval` from `useEffect` |
| Long-polling loop with no error handling | `try/catch` with a delay before retrying |
| Long-polling loop that never stops | Use an `active` flag, and set it false in cleanup |
| `socket.send()` before the connection opens | Send inside `socket.onopen` |
| Socket never closed on unmount | `socket.close()` in the cleanup |
| Polling every second for slow-changing data | Increase the interval, or use a push method |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is polling? | The client repeatedly asks the server for updates. |
| Short vs long polling? | Short polling replies right away, and the client asks on a timer. Long polling holds the request until there is news, then the client re-requests at once. |
| What is a WebSocket? | One persistent, two-way connection. Either side can send messages at any time. |
| WebSocket vs HTTP polling? | WebSockets avoid repeated requests and deliver messages instantly in both directions. |
| Why does long polling still use HTTP? | It works with standard HTTP, but each update still costs a new request. |
| Why close the socket on unmount? | Otherwise the connection stays open and leaks, and the component may receive messages after it's gone. |

---

## ✅ Key Takeaways

- **Short polling** = simple, but wasteful.
- **Long polling** = near-instant updates over normal HTTP, but still one request per update.
- **WebSocket** = a single two-way connection, best for real-time apps.
- Always **clean up** timers, loops, and sockets when the component unmounts.
