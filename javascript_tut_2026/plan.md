# JavaScript Learning Plan (Basic → Intermediate → Expert)

> Mark each topic with `[x]` when done. Format: `- [ ]` = pending, `- [x]` = completed.

---

## 🟢 PART 1 — BASICS (Foundations)

### 1. Introduction & Setup
- [x] What is JavaScript? History & where it runs (browser, Node.js)
- [x] How to run JS: browser console, `<script>` tag, Node.js, online editors
- [x] JavaScript engines (V8, SpiderMonkey) — high-level overview
- [x] Statements, expressions & semicolons
- [x] Comments (single-line, multi-line)
- [x] `"use strict"` mode

### 2. Variables & Constants
- [x] `var`, `let`, `const` — differences
- [x] Variable naming rules & conventions
- [x] Hoisting (intro level)
- [x] Scope basics (global vs local)

### 3. Data Types
- [x] Primitive types: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`
- [x] Reference types: `object`, `array`, `function`
- [x] `typeof` operator
- [x] Dynamic typing
- [x] Type coercion (implicit vs explicit)  <!-- covered in §4 Operators (tut04) -->
- [x] Truthy & falsy values

### 4. Operators
- [x] Arithmetic operators (`+`, `-`, `*`, `/`, `%`, `**`)
- [x] Assignment operators (`=`, `+=`, `-=`, etc.)
- [x] Comparison operators (`==` vs `===`, `!=` vs `!==`, `<`, `>`)
- [x] Logical operators (`&&`, `||`, `!`)
- [x] Ternary operator (`? :`)
- [x] Nullish coalescing (`??`)
- [x] Optional chaining (`?.`)
- [x] Operator precedence

### 5. Strings
- [x] String creation (quotes, template literals)
- [x] String concatenation & interpolation
- [x] Common string methods (`length`, `slice`, `substring`, `split`, `replace`, `trim`, `toUpperCase`, etc.)
- [x] Escape characters
- [x] String immutability

### 6. Numbers & Math
- [x] Integers & floats
- [x] `Number` methods & properties (`parseInt`, `parseFloat`, `toFixed`, `isNaN`)
- [x] `Math` object (`round`, `floor`, `ceil`, `random`, `max`, `min`, `pow`, etc.)
- [x] `NaN`, `Infinity`, `-Infinity`
- [x] Floating-point precision issues

### 7. Conditionals
- [x] `if`, `else if`, `else`
- [x] `switch` statement
- [x] Ternary operator usage
- [x] Short-circuit evaluation

### 8. Loops
- [x] `for` loop
- [x] `while` loop
- [x] `do...while` loop
- [x] `for...of` (iterables)
- [x] `for...in` (object keys)
- [x] `break` & `continue`
- [x] Nested loops & labels

### 9. Functions (Basics)
- [x] Function declaration vs expression
- [x] Parameters & arguments
- [x] Return values
- [x] Default parameters
- [x] Arrow functions
- [x] Function scope & block scope

---

## 🟡 PART 2 — INTERMEDIATE

### 10. Arrays (Deep Dive)
- [ ] Creating & accessing arrays
- [ ] Mutating methods (`push`, `pop`, `shift`, `unshift`, `splice`, `sort`, `reverse`)
- [ ] Non-mutating methods (`slice`, `concat`, `join`)
- [ ] Iteration methods (`forEach`, `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`)
- [ ] `includes`, `indexOf`, `flat`, `flatMap`
- [ ] Spread operator with arrays
- [ ] Array destructuring
- [ ] Multidimensional arrays

### 11. Objects (Deep Dive)
- [ ] Object literals
- [ ] Accessing properties (dot vs bracket notation)
- [ ] Adding, updating, deleting properties
- [ ] Nested objects
- [ ] Object methods & `this` keyword
- [ ] `Object.keys`, `Object.values`, `Object.entries`
- [ ] `Object.assign`, `Object.freeze`, `Object.seal`
- [ ] Object destructuring
- [ ] Spread operator with objects
- [ ] Computed property names
- [ ] Shorthand properties & methods
- [ ] Optional chaining with objects

### 12. Functions (Advanced)
- [ ] First-class functions
- [ ] Higher-order functions
- [ ] Callback functions
- [ ] Rest parameters (`...args`)
- [ ] IIFE (Immediately Invoked Function Expression)
- [ ] Closures
- [ ] `call`, `apply`, `bind`
- [ ] `this` keyword in depth (global, object, arrow, event handlers)
- [ ] Pure functions & side effects
- [ ] Recursion

### 13. Scope & Hoisting (Deep Dive)
- [ ] Lexical scope
- [ ] Scope chain
- [ ] Hoisting of `var`, `let`, `const`, functions
- [ ] Temporal Dead Zone (TDZ)
- [ ] Block scope vs function scope

### 14. ES6+ Features
- [ ] Template literals
- [ ] Destructuring (array & object)
- [ ] Default, rest & spread
- [ ] Arrow functions & lexical `this`
- [ ] Enhanced object literals
- [ ] `let` / `const` recap
- [ ] Modules (`import` / `export`)
- [ ] Symbols
- [ ] Iterators & generators
- [ ] Tagged template literals

### 15. The DOM (Document Object Model)
- [ ] What is the DOM
- [ ] Selecting elements (`getElementById`, `querySelector`, `querySelectorAll`)
- [ ] Manipulating content (`textContent`, `innerHTML`, `innerText`)
- [ ] Manipulating attributes & styles
- [ ] Creating & removing elements
- [ ] Traversing the DOM (parent, children, siblings)
- [ ] `classList` API

### 16. Events
- [ ] Event listeners (`addEventListener`)
- [ ] Event object
- [ ] Event bubbling & capturing
- [ ] Event delegation
- [ ] `preventDefault` & `stopPropagation`
- [ ] Common events (click, input, submit, keydown, mouseover, etc.)

### 17. Error Handling
- [ ] `try`, `catch`, `finally`
- [ ] `throw` statement
- [ ] Error objects & types (`Error`, `TypeError`, `RangeError`, etc.)
- [ ] Custom errors
- [ ] Error handling best practices

### 18. Asynchronous JavaScript
- [ ] Synchronous vs asynchronous execution
- [ ] The call stack
- [ ] `setTimeout` & `setInterval`
- [ ] Callbacks & callback hell
- [ ] Promises (`then`, `catch`, `finally`)
- [ ] Promise chaining
- [ ] `Promise.all`, `Promise.race`, `Promise.allSettled`, `Promise.any`
- [ ] `async` / `await`
- [ ] Error handling in async code
- [ ] The event loop, microtasks & macrotasks

### 19. Working with APIs
- [ ] `fetch` API
- [ ] HTTP methods (GET, POST, PUT, DELETE)
- [ ] Working with JSON (`JSON.parse`, `JSON.stringify`)
- [ ] Handling responses & errors
- [ ] `async/await` with fetch
- [ ] `AbortController` & request cancellation

### 20. Storage & Browser APIs
- [ ] `localStorage` & `sessionStorage`
- [ ] Cookies basics
- [ ] `IndexedDB` (intro)
- [ ] `History` API
- [ ] `Location` & `Navigator` objects
- [ ] Geolocation API (intro)

---

## 🔴 PART 3 — ADVANCED / EXPERT

### 21. Object-Oriented JavaScript
- [ ] Constructor functions
- [ ] Prototypes & prototype chain
- [ ] `__proto__` vs `prototype`
- [ ] ES6 Classes
- [ ] Class constructors, methods, getters & setters
- [ ] Inheritance (`extends`, `super`)
- [ ] Static methods & properties
- [ ] Private fields (`#`)
- [ ] `instanceof` operator
- [ ] Mixins
- [ ] `Object.create` & prototypal inheritance patterns

### 22. Functional Programming
- [ ] Pure functions & immutability
- [ ] Function composition
- [ ] Currying & partial application
- [ ] Higher-order functions (deep)
- [ ] Point-free style
- [ ] Memoization
- [ ] Recursion & tail-call concepts
- [ ] Declarative vs imperative code

### 23. Iterators, Generators & Symbols
- [ ] Iterator protocol
- [ ] Iterable protocol
- [ ] Custom iterators
- [ ] Generator functions (`function*`, `yield`)
- [ ] Generator delegation (`yield*`)
- [ ] Async generators & `for await...of`
- [ ] Well-known symbols (`Symbol.iterator`, etc.)

### 24. Advanced Async Patterns
- [ ] Event loop in depth (call stack, task queue, microtask queue)
- [ ] Concurrency vs parallelism
- [ ] Debouncing & throttling
- [ ] Web Workers
- [ ] Cancellable promises
- [ ] Async iteration patterns
- [ ] Race conditions & how to avoid them

### 25. Data Structures & Collections
- [ ] `Map` & `WeakMap`
- [ ] `Set` & `WeakSet`
- [ ] When to use Map/Set vs objects/arrays
- [ ] `Array.from`, `Array.of`
- [ ] Typed Arrays & `ArrayBuffer` (intro)
- [ ] Implementing stacks, queues, linked lists in JS

### 26. Modules & Tooling
- [ ] ES Modules vs CommonJS
- [ ] Dynamic imports
- [ ] Module bundlers (Webpack, Vite, Rollup) — concepts
- [ ] Transpilers (Babel) — concepts
- [ ] `package.json` & npm/yarn/pnpm
- [ ] Semantic versioning
- [ ] Tree shaking
- [ ] Linters & formatters (ESLint, Prettier)

### 27. Memory Management & Performance
- [ ] How JS manages memory
- [ ] Garbage collection (mark-and-sweep)
- [ ] Memory leaks & how to detect them
- [ ] Performance optimization techniques
- [ ] Reflow & repaint (browser rendering)
- [ ] Lazy loading & code splitting
- [ ] Profiling with DevTools

### 28. Metaprogramming
- [ ] `Proxy` object
- [ ] `Reflect` API
- [ ] Property descriptors (`Object.defineProperty`)
- [ ] Getters & setters (deep)
- [ ] `Symbol` for metaprogramming

### 29. Regular Expressions
- [ ] RegEx syntax & patterns
- [ ] Character classes, quantifiers, anchors
- [ ] Groups & capturing
- [ ] Flags (`g`, `i`, `m`, `s`, `u`, `y`)
- [ ] Lookahead & lookbehind
- [ ] String methods with RegEx (`match`, `replace`, `matchAll`, `test`)

### 30. Testing
- [ ] Why testing matters
- [ ] Unit testing (Jest / Vitest)
- [ ] Test structure (describe, it, expect)
- [ ] Mocking & spies
- [ ] Integration testing (intro)
- [ ] End-to-end testing (Cypress / Playwright — concepts)
- [ ] Test-driven development (TDD)

### 31. Security
- [ ] XSS (Cross-Site Scripting)
- [ ] CSRF (Cross-Site Request Forgery)
- [ ] CORS (Cross-Origin Resource Sharing)
- [ ] Content Security Policy (CSP)
- [ ] Safe handling of user input
- [ ] Secure storage of tokens

### 32. Modern JS & Ecosystem
- [ ] Latest ECMAScript features (yearly updates)
- [ ] TypeScript (intro & why)
- [ ] Node.js fundamentals (intro)
- [ ] Frameworks overview (React, Vue, Angular, Svelte)
- [ ] State management concepts
- [ ] SSR vs CSR vs SSG (concepts)
- [ ] Progressive Web Apps (PWA — intro)

### 33. Design Patterns & Architecture
- [ ] Module pattern
- [ ] Singleton pattern
- [ ] Factory pattern
- [ ] Observer / Pub-Sub pattern
- [ ] Strategy pattern
- [ ] MVC / MVVM concepts
- [ ] SOLID principles in JS
- [ ] Clean code practices

### 34. Expert Internals
- [ ] How the JS engine works (parsing, compilation, JIT)
- [ ] Execution context & lexical environment (deep)
- [ ] Scope chain & closures (engine level)
- [ ] `this` binding rules (all 4 rules)
- [ ] Hoisting at engine level
- [ ] Microtask vs macrotask queue (deep)
- [ ] Tail call optimization

---

## 🚀 PART 4 — PRACTICE & PROJECTS
- [ ] Small projects (calculator, to-do list, quiz app)
- [ ] DOM-heavy projects (image slider, modal, form validation)
- [ ] API projects (weather app, GitHub user finder)
- [ ] Async/data projects (infinite scroll, debounced search)
- [ ] Build a small library/utility from scratch
- [ ] Algorithm & data structure challenges
- [ ] Code refactoring exercises

---

## 🎯 PART 5 — INTERVIEW PREP (turn knowledge into performance)

> Parts 1–4 teach you the language. This part is what interviews *actually* test:
> implement-from-scratch, predict-the-output, and build-a-feature-live.
> Don't just read these — **code them by hand without looking**, then explain out loud.

### 35. Polyfills & Implement-From-Scratch (the #1 advanced round)
- [ ] `Array.prototype.map` / `filter` / `reduce` / `forEach` from scratch
- [ ] `Function.prototype.bind` (and `call` / `apply`) from scratch
- [ ] `Promise` from scratch (then/catch, states, resolve/reject)
- [ ] `Promise.all` / `Promise.race` / `Promise.allSettled` / `Promise.any` from scratch
- [ ] `debounce` (with leading/trailing options)
- [ ] `throttle` (timestamp & timer variants)
- [ ] Deep clone (`structuredClone`, recursive, handling cycles)
- [ ] Shallow vs deep copy — spread/Object.assign limits, JSON pitfalls
- [ ] `curry` / partial application implementation
- [ ] `flatten` an array (recursive + iterative, with depth)
- [ ] `memoize` (with custom cache key)
- [ ] Event emitter / pub-sub (`on`, `off`, `emit`, `once`)
- [ ] LRU cache (Map-based)
- [ ] `retry` with exponential backoff
- [ ] `pipe` / `compose`
- [ ] `JSON.stringify` (simplified) from scratch
- [ ] `getElementsByClassName` / DOM tree traversal by hand
- [ ] Promisify a callback-based function

### 36. Output Prediction & "Gotcha" Questions (predict-the-output)
- [ ] Event loop ordering: `setTimeout` vs `Promise.then` vs `async/await` vs sync
- [ ] Microtask vs macrotask ordering puzzles
- [ ] Closures in loops (`var` vs `let` with `setTimeout`)
- [ ] Hoisting & TDZ traps (access before declaration)
- [ ] `this` binding puzzles (method extracted, arrow vs regular, `setTimeout` callbacks)
- [ ] Coercion gotchas: `[] == ![]`, `[] + {}`, `{} + []`, `null == undefined`
- [ ] `==` algorithm (ToPrimitive / ToNumber) step by step
- [ ] `==` vs `===` vs `Object.is` (NaN, `+0`/`-0`)
- [ ] Pass-by-value vs pass-by-reference (mutation surprises)
- [ ] `typeof` quirks (`typeof null`, `typeof NaN`, `typeof function`)
- [ ] Floating point gotchas (`0.1 + 0.2 !== 0.3`)
- [ ] Array holes & `length` manipulation surprises
- [ ] Object key ordering & key coercion (numeric vs string keys)
- [ ] Reference equality vs value equality

### 37. Machine Coding / Live Feature Building
- [ ] Autocomplete / typeahead (debounce + request cancel + cache)
- [ ] Infinite scroll (IntersectionObserver / scroll listener)
- [ ] Star rating / accordion / tabs / modal from scratch (vanilla JS)
- [ ] Carousel / image slider
- [ ] Form validation engine (rules, async validation)
- [ ] A small state store / observable (`getState`, `setState`, `subscribe`)
- [ ] Event bus across components
- [ ] Rate limiter
- [ ] Polling with backoff & stop conditions
- [ ] Virtualized list (windowing) — concept + basic build
- [ ] Drag and drop (vanilla)
- [ ] Toast/notification queue

### 38. Frontend System Design (senior rounds)
- [ ] Rendering patterns: CSR vs SSR vs SSG vs ISR (trade-offs)
- [ ] Data fetching & caching strategies (stale-while-revalidate, dedup)
- [ ] State management at scale (local vs global, normalization)
- [ ] Component/API design & reusability
- [ ] Performance budgets (bundle size, Core Web Vitals: LCP/CLS/INP)
- [ ] Optimistic UI & error/rollback handling
- [ ] Pagination vs infinite scroll vs cursor-based
- [ ] Designing a design system / component library (concepts)
- [ ] Accessibility considerations in design (a11y basics)
- [ ] Real-time updates: polling vs SSE vs WebSockets

### 39. "Explain It Out Loud" (verbal/theory rounds)
- [ ] Explain the event loop with a whiteboard example
- [ ] Explain closures with a real use case (and a memory-leak risk)
- [ ] Explain prototypal inheritance vs classical
- [ ] Explain `this` — all binding rules with examples
- [ ] Explain hoisting & TDZ precisely
- [ ] Explain how `async/await` desugars to promises
- [ ] Explain garbage collection & common memory leaks
- [ ] Explain `var` vs `let` vs `const` (scope, hoisting, TDZ)
- [ ] Explain debounce vs throttle (when to use which)
- [ ] Explain deep vs shallow copy & immutability
- [ ] Explain CORS, XSS, CSRF in one minute each
- [ ] Explain `==` vs `===` and when coercion bites

### 40. Mock Interview Practice
- [ ] Timed polyfill: implement under 20 min, no references
- [ ] Timed output-prediction set (10 snippets)
- [ ] Timed machine-coding: build a feature in 45 min
- [ ] Explain a past project's tricky bug (STAR format)
- [ ] Rubber-duck a hard concept to a non-expert
- [ ] Solve, then optimize (time/space) and discuss trade-offs

---

**Progress Tip:** Work top-to-bottom for *learning* (Parts 1–4). For *interview prep*, run Part 5 in parallel once you've reached Part 2/3 — the muscle memory takes weeks to build. After finishing a topic, change its `- [ ]` to `- [x]` and (optionally) note the date or commit it.

**Interview-priority order (if time-constrained):** §35 Polyfills → §36 Output Prediction → §12/§18/§21 (closures, async, OOP) → §37 Machine Coding → §39 Explain Out Loud → §38 System Design (senior only).
