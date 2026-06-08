# JavaScript Interview Questions — by Topic

> Curated from multiple 2026 interview sources (GreatFrontEnd, InterviewBit, Frontend
> Interview Handbook, GeeksforGeeks, Toptal, Simplilearn). Organized to match `plan.md` sections.
>
> **Legend:** ★ = very frequently / repeatedly asked &nbsp;|&nbsp; 🔥 = classic "must-know" &nbsp;|&nbsp; 🧩 = predict-the-output
>
> **Workflow:** As we learn each topic, we'll mark questions answered and (when useful) link
> the answer to the topic's note in `notes_javascript/`. Checkbox `- [x]` = you can answer it confidently.

---

## §2–3 Variables, Data Types & Coercion

- [x] ★🔥 What's the difference between `var`, `let`, and `const`? (scope, hoisting, TDZ, re-assign/re-declare) <!-- tut02 -->
- [x] Can you change a `const` object? (yes — locks binding, not contents) <!-- tut02 -->
- [x] ★🔥 Explain `==` vs `===`. When does coercion bite? <!-- tut04 -->
- [x] ★ What are the data types in JavaScript? (primitives vs reference) <!-- tut03 -->
- [x] ★ What's the difference between `null` and `undefined`? <!-- tut03 -->
- [x] Explain implicit type coercion with examples. <!-- tut04 -->
- [x] Is JavaScript statically or dynamically typed? <!-- tut03 -->
- [x] What is `NaN`? Why is `NaN === NaN` false? How to check for it? <!-- tut06 -->
- [x] ★🔥 Why is `0.1 + 0.2 !== 0.3`? How to compare safely? <!-- tut06 -->
- [x] `parseInt` vs `parseFloat` vs `Number()` — differences? Why pass radix? <!-- tut06 -->
- [x] Coercing vs non-coercing checks (`isNaN` vs `Number.isNaN`)? <!-- tut06 -->
- [x] When would you use `BigInt`? (ints beyond 2^53) <!-- tut06 -->
- [x] ★🔥 Pass-by-value vs pass-by-reference — explain with an example. <!-- tut03 -->
- [x] What is `typeof null`? Why? (`"object"` — historical bug) <!-- tut03 -->
- [x] What is strict mode (`"use strict"`) and what does it change? <!-- tut01 -->
- [x] ★ Is JavaScript single-threaded? <!-- tut01 -->
- [x] ★ Is JavaScript compiled or interpreted? (trick: both — JIT) <!-- tut01 -->
- [x] Which engines run JS? (V8, SpiderMonkey, JavaScriptCore) <!-- tut01 -->
- [x] What are the ways to run JS? (console, &lt;script&gt;, Node, online) <!-- tut01 -->
- [x] What are truthy and falsy values? List all falsy values. <!-- tut03 -->
- [x] Why is `[]` / `{}` truthy but `""` falsy? (objects always truthy) <!-- tut03 -->
- [x] 🧩 `1 + "2" + "2"`, `"5" - 2`, `true + true` — predict the output. <!-- tut04 (basic coercion); [] + {} edge cases later -->
- [ ] 🧩 `[] + {}`, `[] + []`, `{}+[]` — deep coercion edge cases.  <!-- revisit after Objects §11 -->

---

## §7 Conditionals & Operators

- [x] What does optional chaining (`?.`) do and where does it short-circuit? <!-- tut04 -->
- [x] What is nullish coalescing (`??`) and how does it differ from `||`? <!-- tut04 -->
- [ ] What are logical assignment operators (`||=`, `&&=`, `??=`)?
- [x] Explain short-circuit evaluation. <!-- tut04 -->
- [ ] 🧩 Ternary / post-increment / operator precedence output puzzles.

---

## §10 Arrays

- [ ] ★ Explain `map()`, `filter()`, and `reduce()` with examples.
- [ ] ★🔥 Difference between `map()` and `forEach()`?
- [ ] What does `Array.prototype.reduce()` do? (and implement it)
- [ ] How do you flatten a nested array?
- [ ] Immutable array methods: `toSorted`, `toReversed`, `toSpliced`, `with`?
- [ ] What does `findLast()` / `findLastIndex()` do?
- [ ] 🧩 `sort()` default behavior puzzle (numbers sorted as strings).
- [ ] 🧩 Why are two arrays with same contents `!==`? (reference equality)

---

## §11 Objects & Equality

- [ ] ★ What are the different ways to create objects in JavaScript?
- [ ] ★🔥 Shallow copy vs deep copy — how to do each?
- [ ] What is `structuredClone()` and how is it different from `JSON.parse(JSON.stringify())`?
- [ ] How do you implement deep equality (deep-equal)?
- [ ] `Object.freeze` vs `Object.seal` — difference?
- [ ] What is `Object.groupBy()` / `Map.groupBy()`?
- [ ] What does `==` do when comparing objects?
- [ ] 🧩 Spread operator / shallow copy mutation puzzles.

---

## §12 Functions, `this`, call/apply/bind

- [ ] ★🔥 Explain the `this` keyword. How is its value determined? (all binding rules)
- [ ] ★🔥 What is a closure? Give a real use case. (data privacy, counters)
- [ ] ★ Explain `call()`, `apply()`, and `bind()`. Differences?
- [ ] 🔥 How does `Function.prototype.bind` work? (implement it)
- [ ] ★ What are higher-order functions?
- [ ] What is currying? (implement curry)
- [ ] What is an IIFE (Immediately Invoked Function Expression)?
- [ ] What are callbacks? Why use them? What is callback hell?
- [ ] What is recursion? What is memoization? (implement memoize)
- [ ] Function declaration vs function expression (and hoisting difference)?
- [ ] What are arrow functions? How does `this` differ in them?
- [ ] Rest parameters vs spread operator?
- [ ] 🧩 Closures-in-loops: `var` + `setTimeout` in a `for` loop — predict output.
- [ ] 🧩 `this` puzzle: method extracted into a variable, then called.

---

## §13 Scope & Hoisting

- [ ] ★🔥 What is hoisting? What gets hoisted (var/let/const/functions)?
- [ ] 🔥 What is the Temporal Dead Zone (TDZ)?
- [ ] What is lexical scope and the scope chain?
- [ ] Block scope vs function scope?
- [ ] 🧩 Access a `let`/`const` before declaration — what happens?

---

## §14 ES6+ Features

- [ ] What are template literals and tagged templates?
- [ ] What is object/array destructuring?
- [ ] What are ES modules? Default vs named exports?
- [ ] What are private class fields (`#field`)?
- [ ] What are Symbols and where are they used?
- [ ] What are the new Set methods (`union`, `intersection`, `difference`)?

---

## §15–16 DOM & Events

- [ ] ★🔥 What is event delegation and why does it matter?
- [ ] ★ Explain event bubbling vs capturing.
- [ ] What's the difference: `preventDefault()` vs `stopPropagation()`?
- [ ] How does `this` work in event handlers?
- [ ] How do `mouseenter` and `mouseover` differ?
- [ ] What is the DOM? What is the BOM?
- [ ] Difference between `innerHTML`, `innerText`, and `textContent`?
- [ ] How to select DOM elements (and implement `getElementsByClassName`)?

---

## §17 Error Handling

- [ ] How do you handle errors? (`try`/`catch`/`finally`, custom errors)
- [ ] What are the types of errors in JavaScript?
- [ ] What is `error.cause` and why is it useful?
- [ ] How do you handle errors in async/await code?

---

## §18 Asynchronous JavaScript ★ (heavily tested)

- [ ] ★🔥 How does the JavaScript event loop work?
- [ ] ★🔥 Explain microtasks vs macrotasks with a real example.
- [ ] ★🔥 How do `async`/`await` work? How do you handle errors?
- [ ] ★ What are Promises? Why use them? (states, then/catch/finally)
- [ ] 🔥 Understanding `Promise.all()` (and implement it).
- [ ] How does `Promise.allSettled()` differ from `Promise.all()`?
- [ ] What is `Promise.any()` / `Promise.race()` and how do they handle rejection?
- [ ] Async/await vs generators to achieve the same result?
- [ ] What is a callback vs promise vs async/await (evolution)?
- [ ] 🧩🔥 Output ordering: `console.log` + `setTimeout(…,0)` + `Promise.then` + sync code.
- [ ] 🧩 `async` function return value & `await` ordering puzzle.

---

## §19 APIs / Network

- [ ] How do you cancel a `fetch` request with `AbortController`?
- [ ] What's the difference between `async/await` and raw Promises with fetch?
- [ ] What are deferred (`defer`) and `async` scripts?
- [ ] Explain `JSON.parse` / `JSON.stringify` (and edge cases).

---

## §20 Storage

- [ ] ★ Difference between `localStorage`, `sessionStorage`, and cookies?
- [ ] When would you use `IndexedDB`?

---

## §21 OOP & Prototypes

- [ ] ★🔥 How does prototypal inheritance work? (prototype chain)
- [ ] ★ Prototypal vs classical inheritance — difference?
- [ ] What are object prototypes? `__proto__` vs `prototype`?
- [ ] How do ES2015 classes differ from ES5 constructor functions?
- [ ] How does inheritance work in ES2015 classes (`extends`, `super`)?
- [ ] What is the prototype design pattern?
- [ ] What is the use of a constructor function?
- [ ] 🧩 Prototype chain lookup / shadowing puzzle.

---

## §22 Functional Programming

- [ ] What is a pure function? What are side effects?
- [ ] What is function composition (`pipe`/`compose`)?
- [ ] Currying & partial application (implement).
- [ ] Declarative vs imperative code?

---

## §23 Iterators & Generators

- [ ] What are generator functions? (`function*`, `yield`)
- [ ] What is the iterator/iterable protocol?
- [ ] Async/await vs generators?

---

## §24 Advanced Async Patterns

- [ ] ★🔥 What are debouncing and throttling? (implement debounce & throttle)
- [ ] How would you design a concurrency limiter for async tasks?
- [ ] Implement promise retry with exponential backoff.
- [ ] What is a race condition and how do you avoid it?
- [ ] What are Web Workers?

---

## §25 Data Structures & Collections

- [ ] Map vs plain object — differences and when to use each?
- [ ] `Map`/`Set` vs `WeakMap`/`WeakSet` — differences?
- [ ] Explain `WeakSet` and `WeakMap`.
- [ ] What are TypedArrays and when would you use them?

---

## §26 Modules & Tooling

- [ ] ES Modules vs CommonJS?
- [ ] What is tree shaking?
- [ ] What do bundlers / transpilers do (Webpack/Vite, Babel)?

---

## §27 Memory & Performance ★ (senior)

- [ ] ★ What causes memory leaks? How do you detect them?
- [ ] What is garbage collection in V8 (mark-and-sweep)?
- [ ] How do you prevent expensive reflows and repaints?
- [ ] What are "deopts" and what causes them?
- [ ] How does the JS engine optimize code at a high level?
- [ ] Lazy loading & code splitting — what and why?

---

## §28 Metaprogramming

- [ ] What is a `Proxy`? Use cases?
- [ ] What is the `Reflect` API?
- [ ] What is `Object.defineProperty` / property descriptors?

---

## §29 RegEx

- [ ] Difference between `exec()` and `test()` methods?
- [ ] What do the flags `g`, `i`, `m`, `s`, `u`, `y` do?
- [ ] Lookahead vs lookbehind?

---

## §31 Security

- [ ] What is XSS and how do you prevent it?
- [ ] What is CSRF? What is CORS?
- [ ] How do you safely store auth tokens?

---

## §33 Design Patterns

- [ ] What JavaScript design patterns do you know?
- [ ] Explain the module / singleton / observer (pub-sub) pattern.
- [ ] How do SOLID principles apply in JS?

---

## §35 Polyfills / Implement-From-Scratch ★ (the #1 coding round)

> Be able to **code these by hand in <20 min**, then explain edge cases.

- [ ] ★🔥 Implement `debounce` (with leading/trailing).
- [ ] ★🔥 Implement `throttle`.
- [ ] ★🔥 Implement `Promise.all` (preserve order, handle empty input, reject on first failure).
- [ ] 🔥 Implement `Array.prototype.map` / `filter` / `reduce`.
- [ ] 🔥 Implement `Function.prototype.bind` (and `call` / `apply`).
- [ ] Implement deep clone (handle nested + cycles).
- [ ] Implement `curry`.
- [ ] Implement `flatten` (recursive + iterative, with depth).
- [ ] Implement `memoize`.
- [ ] Implement an event emitter / pub-sub (`on`, `off`, `emit`, `once`).
- [ ] Implement an LRU cache.
- [ ] Implement `retry` with exponential backoff.
- [ ] Implement `pipe` / `compose`.
- [ ] Implement a Promise from scratch.

---

## §37 Machine Coding (live build)

- [ ] Autocomplete / typeahead (debounce + cancel + cache).
- [ ] Infinite scroll.
- [ ] A small state store / observable (`getState`, `setState`, `subscribe`).
- [ ] Accordion / tabs / modal / star rating (vanilla).
- [ ] Rate limiter.

---

## §38 Frontend System Design (senior)

- [ ] CSR vs SSR vs SSG vs ISR — trade-offs?
- [ ] Data fetching & caching strategy (stale-while-revalidate, dedup)?
- [ ] State management at scale?
- [ ] Core Web Vitals (LCP / CLS / INP) — what and how to improve?
- [ ] Real-time updates: polling vs SSE vs WebSockets?

---

## Sources
- [GreatFrontEnd — 50 must-know JS questions by ex-interviewers](https://www.greatfrontend.com/blog/50-must-know-javascript-interview-questions-by-ex-interviewers)
- [InterviewBit — 60+ JavaScript interview questions](https://www.interviewbit.com/javascript-interview-questions/)
- [Frontend Interview Handbook — JS quiz](https://www.frontendinterviewhandbook.com/javascript-questions)
- [GeeksforGeeks — JS output-based questions](https://www.geeksforgeeks.org/javascript/javascript-output-based-interview-questions/)
- [GreatFrontEnd — JS machine coding / utility functions](https://www.frontendinterviewhandbook.com/coding/javascript-utility-function)
- [Toptal — Top 37 technical JS questions](https://www.toptal.com/developers/javascript/interview-questions)
