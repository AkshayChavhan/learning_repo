# JavaScript Mastery Roadmap
### Crack Top Company Interviews — A Structured Deep-Dive Plan

> **For:** Intermediate developer with MERN/Next.js experience
> **Goal:** Expert-level JS knowledge for top company interviews
> **Duration:** 10–14 weeks (2–3 hours/day)
> **Approach:** Deep dives + Projects + Interview prep (mixed)

---

## Phase 1: Core Engine Internals (Weeks 1–3)

*This is the foundation everything else builds on. Top companies test this heavily.*

### Week 1: Execution Context & Scope

**Deep Dive Topics:**
- Execution Context (Global, Function, Eval)
- Creation Phase vs Execution Phase
- Variable Environment vs Lexical Environment
- Hoisting — what actually happens (memory allocation, not "moving code")
- `var` vs `let` vs `const` — scoping rules, TDZ, global object attachment
- Scope Chain & Lexical Scoping
- Block scope vs Function scope

**Tricky Interview Questions to Master:**
```js
// Q1: What prints and why?
var a = 1;
function foo() {
  console.log(a);  // ???
  var a = 2;
  console.log(a);  // ???
}
foo();

// Q2: What's the difference?
console.log(typeof undeclaredVar);  // ???
console.log(typeof letVar);         // ???
let letVar = 10;

// Q3: Block scoping
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
for (var j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);
}
```

**Resources:**
- [JavaScript Visualizer 9000](https://www.jsv9000.app/) — see execution contexts in real-time
- You Don't Know JS: *Scope & Closures* (Kyle Simpson) — free on GitHub
- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)

---

### Week 2: Closures (Master Level)

**Deep Dive Topics:**
- `[[Environment]]` internal slot — how functions "remember"
- Closure = function + lexical environment reference
- Garbage collection & memory leaks with closures
- Closure in loops (the `var` trap)
- Practical patterns: factories, partial application, currying, memoization, debounce/throttle

**Build These:**
```js
// 1. Implement memoize
function memoize(fn) {
  // Your implementation — should cache results
}

// 2. Implement once (function runs only once)
function once(fn) {
  // Your implementation
}

// 3. Implement curry
function curry(fn) {
  // curry(add)(1)(2)(3) === 6
}

// 4. Implement debounce AND throttle from scratch
function debounce(fn, delay) { /* ... */ }
function throttle(fn, limit) { /* ... */ }
```

**Interview Pattern — Data Privacy:**
```js
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
  };
}
// count is truly private — no way to access it directly
```

---

### Week 3: `this`, Prototypes & Inheritance

**Deep Dive Topics:**
- 5 rules of `this` (default, implicit, explicit, `new`, arrow)
- `call`, `apply`, `bind` — implement each from scratch
- Prototype chain & `__proto__` vs `.prototype`
- `Object.create()`, `Object.getPrototypeOf()`
- ES6 classes — syntactic sugar over prototypes
- Property descriptors & `Object.defineProperty()`
- `instanceof`, `typeof`, `Symbol.hasInstance`

**Implement from Scratch:**
```js
// 1. Polyfill Function.prototype.bind
Function.prototype.myBind = function(context, ...args) {
  // Your implementation
};

// 2. Polyfill Function.prototype.call
Function.prototype.myCall = function(context, ...args) {
  // Your implementation
};

// 3. Implement instanceof
function myInstanceOf(obj, Constructor) {
  // Walk the prototype chain
}

// 4. Implement Object.create
function myObjectCreate(proto) {
  // Your implementation
}
```

**Tricky Questions:**
```js
// Q1: What does `this` refer to in each?
const obj = {
  name: "Akshay",
  greet: function() { console.log(this.name); },
  greetArrow: () => { console.log(this.name); },
  greetNested: function() {
    const inner = function() { console.log(this.name); };
    inner();
  },
};

// Q2: Prototype chain
function Animal(name) { this.name = name; }
Animal.prototype.speak = function() { return `${this.name} makes a sound`; };
function Dog(name) { Animal.call(this, name); }
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
// What's the prototype chain of new Dog("Rex")?
```

---

## Phase 2: Async JavaScript (Weeks 4–6)

*This is where most candidates struggle. Master this and you stand out.*

### Week 4: Event Loop & Microtasks

**Deep Dive Topics:**
- Call Stack, Web APIs, Callback Queue, Microtask Queue
- Event loop algorithm: call stack → microtasks (ALL) → one macrotask → repeat
- `setTimeout` vs `Promise.then` vs `queueMicrotask` ordering
- `requestAnimationFrame` in the event loop
- Starvation: infinite microtasks block rendering

**Master These Ordering Questions:**
```js
// Q1: Predict the exact output order
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
Promise.resolve().then(() => {
  console.log("4");
  setTimeout(() => console.log("5"), 0);
});
console.log("6");
// Answer: 1, 6, 3, 4, 2, 5

// Q2: More complex
async function foo() {
  console.log("A");
  await Promise.resolve();
  console.log("B");
}
console.log("C");
foo();
console.log("D");
// Answer: C, A, D, B

// Q3: Microtask starvation
function flood() {
  Promise.resolve().then(flood);
}
flood();
setTimeout(() => console.log("Will this ever print?"), 0);
// Answer: No — microtask queue never empties
```

**Resources:**
- [Jake Archibald: In The Loop (JSConf talk)](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — MUST watch
- [Loupe](http://latentflip.com/loupe/) — event loop visualizer

---

### Week 5: Promises (Deep)

**Deep Dive Topics:**
- Promise states: pending → fulfilled/rejected (immutable once settled)
- `.then()` chaining — each returns a NEW promise
- Error propagation & `.catch()` placement
- `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any` — know the differences
- Microtask scheduling of `.then` callbacks

**Implement from Scratch (TOP interview question):**
```js
class MyPromise {
  constructor(executor) {
    this.state = 'pending';
    this.value = undefined;
    this.callbacks = [];

    const resolve = (value) => { /* ... */ };
    const reject = (reason) => { /* ... */ };

    try { executor(resolve, reject); }
    catch (err) { reject(err); }
  }

  then(onFulfilled, onRejected) { /* returns new MyPromise */ }
  catch(onRejected) { return this.then(null, onRejected); }
  static resolve(value) { /* ... */ }
  static all(promises) { /* ... */ }
  static race(promises) { /* ... */ }
}
```

**Tricky Patterns:**
```js
// Q1: Sequential vs Parallel execution
// Sequential (one at a time)
async function sequential(urls) {
  for (const url of urls) {
    await fetch(url);  // waits for each
  }
}

// Parallel (all at once)
async function parallel(urls) {
  await Promise.all(urls.map(url => fetch(url)));
}

// Q2: What happens here?
Promise.resolve(1)
  .then(x => { throw new Error("boom"); })
  .then(x => console.log("A:", x))      // skipped
  .catch(e => { console.log("B:", e.message); return 42; })
  .then(x => console.log("C:", x));      // C: 42
```

---

### Week 6: Async/Await, Generators & Iterators

**Deep Dive Topics:**
- `async/await` is syntactic sugar over generators + promises
- Generator functions: `function*`, `yield`, `.next()`, `.return()`, `.throw()`
- Iterators & `Symbol.iterator` protocol
- `for...of` vs `for...in`
- Async iterators & `for await...of`
- Async error handling patterns (try/catch vs .catch)

**Build These:**
```js
// 1. Implement async/await using generators
function asyncRunner(generatorFn) {
  // Should handle generator that yields promises
}

// 2. Build a lazy range iterator
function* range(start, end, step = 1) {
  // yields values lazily
}

// 3. Build an async queue that processes N concurrent tasks
class AsyncQueue {
  constructor(concurrency) { /* ... */ }
  add(task) { /* returns promise */ }
}
```

---

## Phase 3: Performance & Memory (Weeks 7–8)

### Week 7: Performance Optimization

**Deep Dive Topics:**
- V8 engine internals: parsing → AST → bytecode → optimized code
- Hidden classes & inline caching — why object shape matters
- Monomorphic vs polymorphic vs megamorphic calls
- Deoptimization triggers (changing object shapes, `arguments` usage, `try/catch` in hot loops)
- Memory layout: stack vs heap, small integers (SMI) vs heap numbers
- `requestIdleCallback` and task scheduling

**Practical Knowledge:**
```js
// BAD — polymorphic, V8 can't optimize
function process(input) {
  return input.x + input.y;
}
process({ x: 1, y: 2 });         // shape A
process({ y: 2, x: 1 });         // shape B (different order!)
process({ x: 1, y: 2, z: 3 });   // shape C

// GOOD — monomorphic, same shape every time
function process(input) {
  return input.x + input.y;
}
process({ x: 1, y: 2 });
process({ x: 3, y: 4 });
process({ x: 5, y: 6 });
```

**Resources:**
- [V8 Blog](https://v8.dev/blog) — official V8 engine blog
- Mathias Bynens talks on V8 internals

---

### Week 8: Memory Management & Debugging

**Deep Dive Topics:**
- Garbage Collection: Mark-and-sweep, generational GC (young gen, old gen)
- Memory leaks: common causes and detection
- Weak references: `WeakRef`, `WeakMap`, `WeakSet` — when and why
- Performance profiling with Chrome DevTools
- Memory snapshots and heap analysis

**Common Memory Leak Patterns:**
```js
// 1. Forgotten timers
const data = loadHugeDataSet();
setInterval(() => {
  // `data` can never be GC'd — even if you don't need it
  processData(data);
}, 1000);

// 2. Closures holding large scopes
function createHandler() {
  const hugeArray = new Array(1000000);
  return function handler() {
    // Even if handler doesn't USE hugeArray,
    // some engines keep the entire closure scope alive
    console.log("handled");
  };
}

// 3. Detached DOM nodes
const elements = [];
function addElement() {
  const el = document.createElement('div');
  document.body.appendChild(el);
  elements.push(el);  // reference kept even after removal
}

// 4. Event listeners not cleaned up
// In React: missing cleanup in useEffect
useEffect(() => {
  window.addEventListener('resize', handler);
  // Missing: return () => window.removeEventListener('resize', handler);
}, []);
```

---

## Phase 4: Design Patterns & Architecture (Weeks 9–10)

### Week 9: Core Design Patterns in JS

**Patterns to Master:**
| Pattern | Use Case | Example |
|---------|----------|---------|
| Module | Encapsulation, private state | Closures, ES modules |
| Observer/PubSub | Event systems, state management | EventEmitter, Redux |
| Factory | Object creation without `new` | React.createElement |
| Singleton | Single instance (DB connections) | Module-level instance |
| Strategy | Swappable algorithms | Validation rules, sorting |
| Proxy/Decorator | Intercept operations | ES6 Proxy, HOCs in React |
| Iterator | Sequential access | Generators, `Symbol.iterator` |
| Command | Undo/redo, action queuing | Editor commands |

**Build These:**
```js
// 1. EventEmitter (asked at Google, Meta)
class EventEmitter {
  on(event, listener) { }
  off(event, listener) { }
  emit(event, ...args) { }
  once(event, listener) { }
}

// 2. Observable (RxJS-lite)
class Observable {
  constructor(subscribeFn) { }
  subscribe(observer) { }
  pipe(...operators) { }
  static from(iterable) { }
}

// 3. Middleware pattern (Express-style)
class App {
  use(middleware) { }
  handle(req, res) { } // chain middlewares
}
```

---

### Week 10: Metaprogramming & Advanced Patterns

**Deep Dive Topics:**
- ES6 Proxy & Reflect — intercept any object operation
- `Symbol` — well-known symbols (`Symbol.iterator`, `Symbol.toPrimitive`, etc.)
- `Object.defineProperty` — getters/setters, non-enumerable properties
- Tagged template literals
- Decorators (Stage 3 proposal)

**Build These:**
```js
// 1. Reactive system (Vue-style) using Proxy
function reactive(obj) {
  // Returns proxy that tracks dependencies and auto-updates
}

// 2. Deep clone that handles circular references
function deepClone(obj, seen = new WeakMap()) {
  // Handle Date, RegExp, Map, Set, circular refs
}

// 3. Type-checking proxy
function createTyped(schema) {
  // proxy that validates property types on set
}

// 4. Implement JSON.stringify from scratch
function myStringify(value) {
  // Handle: primitives, arrays, objects, null, undefined, nested
}
```

---

## Phase 5: Interview-Specific Prep (Weeks 11–14)

### Week 11–12: Coding Challenges (JS-Specific)

**Must-Implement List (these come up repeatedly):**

| # | Problem | Key Concept |
|---|---------|-------------|
| 1 | `Array.prototype.map/filter/reduce` polyfill | Prototype, callbacks |
| 2 | `Promise.all / allSettled / race` | Async patterns |
| 3 | `Function.prototype.bind` polyfill | `this`, closures |
| 4 | Deep equality check | Recursion, type checking |
| 5 | `debounce` and `throttle` | Closures, timers |
| 6 | `flatten(arr, depth)` | Recursion |
| 7 | `EventEmitter` class | Observer pattern |
| 8 | `curry(fn)` implementation | Closures, recursion |
| 9 | `Promise` from scratch | Microtasks, state machine |
| 10 | DOM: `getElementsByClassName` polyfill | Tree traversal |
| 11 | `JSON.parse` / `JSON.stringify` | Recursion, type handling |
| 12 | `setInterval` using `setTimeout` | Closures, recursion |
| 13 | Implement `pipe` and `compose` | Functional programming |
| 14 | `cloneDeep` with circular ref handling | WeakMap, recursion |
| 15 | Rate limiter / retry with backoff | Async, closures |

**Practice Platforms:**
- [GreatFrontEnd](https://www.greatfrontend.com/) — JS-specific interview questions
- [BFE.dev](https://bigfrontend.dev/) — frontend interview coding challenges
- [LeetCode JavaScript track](https://leetcode.com/problemset/javascript/)

---

### Week 13: System Design (Frontend)

**Common Questions:**
- Design an autocomplete/typeahead
- Design an infinite scroll feed
- Design a real-time collaborative editor
- Design a chat application
- Design a virtual list (render 10K items efficiently)
- Design a state management library (mini-Redux)

**Key Concepts to Know:**
- Rendering strategies: SSR, CSR, SSG, ISR (you know this from Next.js!)
- Web Workers for heavy computation
- Service Workers & caching strategies
- WebSocket vs SSE vs Long Polling
- Virtual DOM & reconciliation
- Bundle splitting & lazy loading
- Web Vitals: LCP, FID, CLS

---

### Week 14: Behavioral + Final Review

**Review Checklist — Can You Explain These?**
- [ ] Two-phase execution (creation + execution)
- [ ] Scope chain traversal
- [ ] Closure = function + `[[Environment]]`
- [ ] 5 rules of `this` binding
- [ ] Prototype chain lookup
- [ ] Event loop: call stack → microtasks → macrotask
- [ ] Promise states & chaining
- [ ] `async/await` desugaring to generators
- [ ] V8 hidden classes & optimization
- [ ] GC: mark-and-sweep, generational
- [ ] WeakMap/WeakRef for memory management
- [ ] Proxy/Reflect for metaprogramming
- [ ] Common design patterns in JS context
- [ ] Frontend system design principles

---

## Daily Practice Routine

| Time | Activity |
|------|----------|
| **30 min** | Read/study the week's topic (book, article, or video) |
| **60 min** | Implement from scratch (polyfills, patterns, utilities) |
| **30 min** | Solve 1–2 JS coding challenges (BFE.dev or GreatFrontEnd) |
| **30 min** | Review: explain concepts out loud or write a blog post |

---

## Top Resources (Ranked)

### Books
1. **You Don't Know JS** (Kyle Simpson) — free on GitHub, covers everything deeply
2. **JavaScript: The Definitive Guide** (David Flanagan) — comprehensive reference
3. **Eloquent JavaScript** — free online, great for filling gaps

### Video
1. **Namaste JavaScript** (Akshay Saini on YouTube) — excellent for engine internals
2. **Jake Archibald: In The Loop** — best event loop explanation ever
3. **Fun Fun Function** — great for functional patterns

### Practice
1. **BFE.dev** — best for JS-specific interview coding
2. **GreatFrontEnd** — structured frontend interview prep
3. **LeetCode 30 Days of JS** — quick daily practice

### Blogs
1. **V8 Blog** (v8.dev/blog) — engine internals
2. **MDN Web Docs** — the definitive reference
3. **javascript.info** — modern tutorial, excellently structured

---

## Progress Tracker

| Week | Topic | Status |
|------|-------|--------|
| 1 | Execution Context & Scope | ⬜ |
| 2 | Closures (Master Level) | ⬜ |
| 3 | `this`, Prototypes & Inheritance | ⬜ |
| 4 | Event Loop & Microtasks | ⬜ |
| 5 | Promises (Deep) | ⬜ |
| 6 | Async/Await, Generators & Iterators | ⬜ |
| 7 | Performance Optimization | ⬜ |
| 8 | Memory Management & Debugging | ⬜ |
| 9 | Design Patterns in JS | ⬜ |
| 10 | Metaprogramming & Advanced Patterns | ⬜ |
| 11–12 | Coding Challenges (JS-Specific) | ⬜ |
| 13 | Frontend System Design | ⬜ |
| 14 | Behavioral + Final Review | ⬜ |

---

*Tip: For each topic, don't just read — implement from scratch, explain it to someone, and then solve related interview questions. The "explain out loud" step is what separates people who understand from people who can demonstrate understanding in interviews.*
