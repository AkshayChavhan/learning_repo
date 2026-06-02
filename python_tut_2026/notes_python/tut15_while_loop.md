# Python `while` Loop

A **`while` loop** repeats a block as long as a condition is `True`.
You decide when to stop by changing the condition.

```python
count = 1

while count <= 3:
    print(count)
    count += 1
```

Output:

```text
1
2
3
```

Four key facts:

- The condition is checked **before** every iteration.
- The body must change something the condition depends on — otherwise it loops forever.
- The body must be **indented** (4 spaces).
- Use `break` to exit early and `continue` to skip to the next iteration.

---

## When to use `while` vs `for`

| Use `for`   | Use `while`                              |
|-------------|------------------------------------------|
| You're iterating over a known collection | You don't know how many iterations yet |
| Number of iterations is known            | Stop when some condition becomes False |
| Looping a fixed number of times          | Polling, waiting, reading input        |

Rule of thumb: if you can write it with `for`, prefer `for`.

---

## The simplest form

```python
n = 0

while n < 5:
    print(n)
    n += 1
```

Output:

```text
0
1
2
3
4
```

The loop checks `n < 5`, runs the body, then checks again.
When `n` reaches `5`, the condition becomes `False` and the loop ends.

---

## Infinite loops

If the condition never becomes `False`, the loop runs forever.

```python
while True:
    print("forever!")
```

Stop a runaway loop in the terminal with **Ctrl + C**.

Infinite loops are useful with an explicit `break` inside.

```python
while True:
    answer = input("> ")
    if answer == "quit":
        break
    print("you said:", answer)
```

---

## `break` — exit early

`break` jumps out of the loop immediately.

```python
n = 0

while n < 100:
    if n == 5:
        break
    print(n)
    n += 1

print("done")
```

Output:

```text
0
1
2
3
4
done
```

The loop stopped at `n == 5` even though the condition `n < 100` was still true.

---

## `continue` — skip to next iteration

`continue` jumps back to the condition check, skipping the rest of the body.

```python
n = 0

while n < 6:
    n += 1
    if n % 2 == 0:
        continue
    print(n)
```

Output:

```text
1
3
5
```

Even numbers are skipped because `continue` jumps over the `print` call.

---

## `else` on a `while`

A `while` can have an `else` block.
It runs **only if the loop ends normally** (condition became `False`) — not if you `break` out.

```python
n = 1

while n < 4:
    print(n)
    n += 1
else:
    print("finished normally")
```

Output:

```text
1
2
3
finished normally
```

With `break`, the `else` is skipped:

```python
n = 1

while n < 10:
    if n == 3:
        break
    print(n)
    n += 1
else:
    print("won't print")
```

Output:

```text
1
2
```

Use `while...else` mostly for search-style loops: "did we find it?"

---

## The walrus operator in `while`

`:=` lets you assign **inside** the condition — useful for reading input.

```python
# Without walrus — input() in two places
line = input("> ")
while line != "quit":
    print("you said:", line)
    line = input("> ")

# With walrus — input() only once
while (line := input("> ")) != "quit":
    print("you said:", line)
```

Python 3.8+ only.

---

## Common patterns

### Countdown

```python
n = 5

while n > 0:
    print(n)
    n -= 1

print("Go!")
```

### Wait for valid input

```python
while True:
    answer = input("Enter a number: ")
    if answer.isdigit():
        n = int(answer)
        break
    print("Not a number, try again.")
```

### Sum until a target

```python
total = 0
n = 1

while total < 100:
    total += n
    n += 1

print(total)   # first total >= 100
```

### Process a queue

```python
queue = [1, 2, 3, 4, 5]

while queue:
    item = queue.pop(0)
    print("processing", item)
```

When `queue` becomes `[]` (falsy), the loop ends.

---

## Common pitfalls

**1. Forgetting to update the variable** — infinite loop.

```python
n = 0
while n < 5:
    print(n)   # n never changes → infinite loop
```

Fix: include `n += 1` (or similar) inside the body.

**2. Wrong condition direction.**

```python
n = 0
while n > 5:    # never enters — 0 is not > 5
    print(n)
```

Fix: check whether you meant `<` or `>`.

**3. `break` placement** — if you break before changing the variable, the next iteration may behave oddly.

**4. Mixing up `while` and `for`.**
If you have a collection (list, range, etc.), `for` is almost always cleaner.

---

## `while` vs `for` — same thing, two ways

```python
# while
n = 0
while n < 5:
    print(n)
    n += 1

# for — cleaner for fixed counts
for n in range(5):
    print(n)
```

Reach for `while` when the count isn't known upfront.

---

## Quick reference

```text
while condition:
    body
else:                    # optional — runs if loop ends normally
    body

break                    # exit the loop immediately
continue                 # skip to next condition check

while True:              # infinite loop — needs break to exit
    ...
    if done:
        break

while (x := next_val()) is not None:   # walrus (3.8+)
    ...
```
