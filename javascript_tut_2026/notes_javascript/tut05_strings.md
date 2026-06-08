# JavaScript — Strings

A **string** is text. Wrap it in `'…'`, `"…"`, or `` `…` ``.
Strings are **immutable** — every "modification" returns a new string.

```text
                  ┌──────────────────────────┐
                  │       STRINGS            │
                  │ immutable text in JS     │
                  └──────────────────────────┘
                            │
        ┌───────────┬───────┴───────┬──────────────┐
        ▼           ▼               ▼              ▼
     CREATE       INDEX           SLICE          BUILD
   "x" 'x' `x`    s[0]            slice          template
                  s.length        substring      `${var}`
                                                  + concat
        ▼           ▼               ▼              ▼
              METHODS (search, transform, split, trim, …)
```

---

## Creating strings

Three quote styles, all giving the **same** type.

```js
let a = "Hello";        // double
let b = 'World';        // single
let c = `Backtick`;     // template literal
console.log(typeof a);  // 'string'
```

| Quote | Best for                                 |
|-------|------------------------------------------|
| `"…"` | most text                                |
| `'…'` | text containing `"`                      |
| `` `…` `` | interpolation, multi-line, embedded expressions |

### Escape characters

```js
"It's \"OK\""           // It's "OK"
"line1\nline2"          // newline
"col1\tcol2"            // tab
"\\path\\to\\file"      // \path\to\file
"❤"                // ❤ (unicode)
```

| Sequence | Means |
|---------|-------|
| `\n` | newline |
| `\t` | tab |
| `\\` | backslash |
| `\'` `\"` `` \` `` | escape that quote |
| `\u{1F600}` | unicode codepoint |

---

## Template literals ★ (`` `…` ``)

The modern way to build strings.

```js
const name = "Akshay";
const age  = 30;

`Hello, ${name}! Next year: ${age + 1}`
// "Hello, Akshay! Next year: 31"
```

What they give you:

- **Interpolation** — `${ any expression }` inside the backticks.
- **Multi-line** — line breaks are preserved.

```js
const msg = `Line 1
Line 2
Line 3`;
```

```js
const sum = `2 + 3 = ${2 + 3}`;   // expressions, calls, ternaries — anything
```

Prefer template literals to `"a" + b + "c"` — easier to read, fewer string-vs-number bugs.

---

## Length & indexing

```js
const s = "JavaScript";

s.length      // 10
s[0]          // 'J'
s[s.length-1] // 't'
s.at(-1)      // 't'    — modern: negative index
```

`at(i)` (ES2022) supports negative indices like Python's `s[-1]`.
`s[i]` does **not** — it returns `undefined`.

```js
"abc"[-1]     // undefined
"abc".at(-1)  // 'c'
```

---

## Strings are immutable ★

You **cannot** mutate a character.

```js
let s = "hello";
s[0] = "H";          // silently ignored in non-strict; TypeError in strict
console.log(s);      // 'hello'

s = "H" + s.slice(1);
console.log(s);      // 'Hello'   ← rebound, new string
```

Every "string method" returns a **new** string. The original is unchanged.

---

## Concatenation

```js
"foo" + "bar"           // "foobar"
"score: " + 5           // "score: 5"   ← + with a string ⇒ stringified
1 + 2 + "x"             // "3x"
"x" + 1 + 2             // "x12"   (left-to-right)
```

Prefer template literals over `+` for readability.

```js
const user = "Akshay";
const html = `<h1>Hi, ${user}</h1>`;
```

---

## Slicing — `slice`, `substring`, `substr` ★

Three methods, only two worth using.

| Method | Form | Negative? |
|--------|------|-----------|
| `slice(start, end)` | end is **exclusive** | ✅ yes |
| `substring(start, end)` | end is **exclusive**, no negatives | ❌ |
| `substr(start, length)` | **deprecated** — don't use | — |

```js
const s = "JavaScript";

s.slice(0, 4)     // 'Java'
s.slice(4)        // 'Script'
s.slice(-6)       // 'Script'     ← negative = from end
s.slice(-6, -3)   // 'Scr'

s.substring(0, 4) // 'Java'       ← same as slice for positives
s.substring(-2)   // 'JavaScript' ← negatives become 0 (weird)
```

**Rule:** use `slice`. It's the most predictable.

---

## Common methods — search

```js
const s = "Hello, world";

s.includes("world")     // true
s.startsWith("Hello")   // true
s.endsWith("ld")        // true
s.indexOf("o")          // 4   (first), -1 if not found
s.lastIndexOf("o")      // 8   (last)
```

`includes` is the cleanest "is this substring there?" check.

---

## Common methods — transform (return a NEW string)

```js
"  Hi  ".trim()           // 'Hi'
"  Hi  ".trimStart()      // 'Hi  '
"  Hi  ".trimEnd()        // '  Hi'

"hello".toUpperCase()     // 'HELLO'
"HI".toLowerCase()        // 'hi'

"abc".repeat(3)           // 'abcabcabc'

"5".padStart(3, "0")      // '005'
"5".padEnd(3, ".")        // '5..'

"hi hi".replace("hi", "yo")     // 'yo hi'      ← only first
"hi hi".replaceAll("hi", "yo")  // 'yo yo'      ← ES2021
```

`replace` only replaces the **first** match by default. Use `replaceAll` or a regex with `/g`.

```js
"hi hi".replace(/hi/g, "yo")    // 'yo yo'
```

---

## Common methods — split & join

```js
"a,b,c".split(",")         // ['a', 'b', 'c']
"hello".split("")          // ['h', 'e', 'l', 'l', 'o']
"hello world".split(" ")   // ['hello', 'world']

["a", "b", "c"].join("-")  // 'a-b-c'
```

`split` returns an array — useful for parsing.
`join` is the reverse, called on the array.

---

## Iterating a string

A string is iterable, so all of these work:

```js
const s = "abc";

for (const ch of s) console.log(ch);

[...s]                 // ['a', 'b', 'c']
Array.from(s)          // ['a', 'b', 'c']
```

Each step yields a **code point**, not a raw byte — emoji and multi-byte chars work correctly.

```js
[..."🙂a"]             // ['🙂', 'a']
"🙂".length            // 2   ← length counts UTF-16 code units!
```

**Gotcha:** `length` is in UTF-16 units, not characters. For visible-character length:

```js
[..."🙂"].length       // 1   ← use spread
```

---

## Comparison

```js
"abc" === "abc"   // true
"abc" === "ABC"   // false (case-sensitive)
"a" < "b"         // true   (lexicographic, char codes)
"10" < "9"        // true   (!) — string compare, "1" < "9"
```

For case-insensitive compare, normalize first:

```js
"Apple".toLowerCase() === "apple".toLowerCase()  // true
```

For human-friendly compare (locale, numbers, accents), use `localeCompare`:

```js
"a".localeCompare("b")    // -1 (a comes first)
"10".localeCompare("9", undefined, { numeric: true })  // 1
```

---

## String → number / number → string

```js
Number("42")          // 42
Number("3.14")        // 3.14
Number("abc")         // NaN
parseInt("42px", 10)  // 42       (stops at first non-digit)
parseFloat("3.14abc") // 3.14
+"42"                 // 42       (unary plus — concise)

String(42)            // '42'
(42).toString()       // '42'
(255).toString(16)    // 'ff'     (hex)
(3.14159).toFixed(2)  // '3.14'
```

---

## Useful one-liners

```js
// Reverse
[..."hello"].reverse().join("")          // 'olleh'

// Count occurrences
"banana".split("a").length - 1           // 3

// First N chars
"JavaScript".slice(0, 4)                 // 'Java'

// Last N chars
"JavaScript".slice(-6)                   // 'Script'

// Capitalize first letter
const cap = s => s[0].toUpperCase() + s.slice(1);
cap("hello")                             // 'Hello'

// Pad a number with leading zeros
String(7).padStart(3, "0")               // '007'
```

---

## Pitfalls ★

| Pitfall | Demo | Why |
|---------|------|-----|
| `+` mixes types | `1 + "2"` → `"12"` | `+` with any string ⇒ string |
| Lexicographic compare | `"10" < "9"` → `true` | char codes, not numbers |
| Negative index with `[]` | `"abc"[-1]` → `undefined` | use `.at(-1)` |
| `length` counts UTF-16 units | `"🙂".length === 2` | use `[..."🙂"].length` |
| `replace` only does the first | `"hi hi".replace("hi","yo")` → `"yo hi"` | use `replaceAll` or `/g` |
| `substring` swaps negatives | `"abc".substring(-2)` → `"abc"` | prefer `slice` |
| Mutating fails silently | `s[0] = "X"` does nothing | rebind with a new string |

---

## Interview angle

- **Why are strings immutable?** Predictability, hashing/interning, thread/event-loop safety, and identity-style optimizations (engine can share the same buffer).
- **`slice` vs `substring`?** `slice` accepts negatives, `substring` clamps and swaps. Use `slice`.
- **`==` vs `===` with strings?** Always use `===`. `"5" == 5` is `true` (coercion), `"5" === 5` is `false`.
- **Memory of `+` in a loop?** Each `+=` builds a new string. For tight loops, push to an array and `.join("")` at the end.
- **Why `"🙂".length === 2`?** UTF-16 surrogate pair. The character is one code point but two code units.

---

## Quick reference

```text
LITERAL          "x"  'x'  `x`             (prefer ` for interpolation)
TEMPLATE         `Hi ${name}, ${1+1}`
LENGTH           s.length
ACCESS           s[i]    s.at(-1)
SLICE            s.slice(start, end)       (end exclusive, neg ok)
INCLUDES         s.includes(x)
INDEX            s.indexOf(x)              -1 if missing
TRIM             s.trim() / trimStart / trimEnd
CASE             s.toUpperCase() / toLowerCase()
REPEAT/PAD       s.repeat(n)  s.padStart(n,'0')
REPLACE          s.replace(a,b)  s.replaceAll(a,b)  s.replace(/a/g,b)
SPLIT            s.split(sep)
JOIN (arr→str)   arr.join(sep)
ITERATE          for (const ch of s)  [...s]
COMPARE          ===   s.toLowerCase()    a.localeCompare(b)
PARSE NUM        Number(s)  parseInt(s,10)  parseFloat(s)  +s
TO STRING        String(n)  n.toString()  n.toFixed(2)
```
