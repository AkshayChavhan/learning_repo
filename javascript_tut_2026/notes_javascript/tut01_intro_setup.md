# JavaScript — Introduction & Setup

```text
JavaScript (JS) is the programming language that gives websites behavior. Like clicks, updates, and interactions. When you open a site, the server sends JavaScript to your browser. Your browser runs that JavaScript on the main thread, parsed, interpreted, and sped up by JIT. The server runs its own code separately on its own processors, and they talk over the internet. Threads are the paths of execution. JavaScript is usually single-threaded on the page, but you can add web workers for extra threads so the page stays smooth.

Parse checks your code's structure and syntax. Interpret runs your code step by step. JIT turns hot spots into fast machine code while your program runs.
```



---

## How to run JS

| Where               | How                         | Use for                    |
| ------------------- | --------------------------- | -------------------------- |
| **Browser console** | `F12` → Console → type code | Quick experiments          |
| `<script>` **tag**  | JS inside an HTML file      | Web pages                  |
| **Node.js**         | `node file.js` in terminal  | Servers, scripts, learning |
| **Online editor**   | CodePen, JSFiddle           | Zero setup                 |

First program — `console.log` prints to the screen (your main debugging tool):

```js
console.log("Hello, JavaScript!");
```

```text
Hello, JavaScript!
```

---

## Engines (the program that runs JS)

| Engine | Used by |
|--------|---------|
| **V8** | Chrome, Edge, **Node.js** |
| **SpiderMonkey** | Firefox |
| **JavaScriptCore** | Safari |

---

## Syntax basics

```js
let x = 5;          // a statement, ended with ;  (; mostly optional but recommended)
console.log(x);

// single-line comment
/* multi-line
   comment */
```

- **Statement** = one instruction.
- **Comments** are ignored by the engine.

---

## Single-threaded (key concept)

JS uses **ONE thread** — one task list, one step at a time — **no matter how many CPU cores** you have.

| Term | What it is | Level |
|------|-----------|-------|
| **Core** | A physical worker on the CPU (octa-core = 8) | Hardware |
| **Thread** | One sequence of steps being executed | Software |

```text
   8-core CPU            JS uses
   [1][2][3][4]          [1]  ← just one core; the rest idle for your JS
   [5][6][7][8]
```

```js
console.log("first");   // step 1
console.log("second");  // step 2 — waits for step 1
```

```text
first
second
```

> **Chef analogy:** one chef (1 thread) chops one thing at a time, but puts a pot on the
> stove (hands slow work to the browser/Node) and comes back when it whistles. That hand-off
> is the **event loop** (Topic 18). Extra cores in JS = **Web Workers** (Topic 24), opt-in only.

---

## Interpreted + JIT (how JS runs fast)

The CPU only understands **machine code**; your `.js` is text, so it must be translated.

| | **Interpreted** | **Compiled** |
|---|----------------|--------------|
| How | Translate & run line-by-line, live | Translate whole program first, then run |
| Start | ⚡ Instant | 🐢 Slow |
| Run | 🐢 Slower | ⚡ Fast |

**JIT (Just-In-Time) = best of both:** start interpreting instantly, watch which code runs
a lot ("hot"), then compile *that* to fast machine code **while running**.

```text
 ① INTERPRET every line          ← instant start
 ② WATCH: "this loop ran 10,000×!" ← find hot code
 ③ COMPILE hot code → machine code ← "just in time"
 ④ Run the FAST version next time
```

> **Interview trick:** "Is JS compiled or interpreted?" → **Both** — it's JIT. (V8 = Ignition
> interpreter + TurboFan compiler.)

---

## `"use strict"`

Opts into safer rules — turns silent bugs into errors.

```js
"use strict";
undeclaredVar = 10;   // ❌ ReferenceError
                      // without strict: silently creates a global (bug!)
```

---

## Key takeaways

- ++***JS runs in browsers and Node.js, via an engine (V8 most common).***++
- ++***JS is single-threaded — one thing at a time, regardless of CPU cores.***++
- ++***JS is interpreted + JIT-compiled → fast start and fast execution.***++
- `"use strict"` ++***catches silent mistakes.***++

---

### Interview angle

- ++***★ "Is JavaScript single-threaded?" → Yes (one call stack); concurrency comes from the
event loop + browser/Node APIs, not extra JS threads.***++
- ++***★ "Compiled or interpreted?" → Both — modern engines use JIT.***++
- "What is `'use strict'`?" → safer mode; undeclared assignments and other silent errors throw.
