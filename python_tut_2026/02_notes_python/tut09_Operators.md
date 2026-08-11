# Python Operators

Operators are symbols that perform an action on one or more values.
Python groups them into **7 categories**.

| Category       | Examples                  |
|----------------|---------------------------|
| Arithmetic     | `+  -  *  /  //  %  **`   |
| Assignment     | `=  +=  -=  *=  …`        |
| Comparison     | `==  !=  >  <  >=  <=`    |
| Logical        | `and  or  not`            |
| Identity       | `is  is not`              |
| Membership     | `in  not in`              |
| Bitwise        | `&  |  ^  ~  <<  >>`      |

---

## Arithmetic operators

Do math on numbers.

| Operator | Name           | Example  | Result |
|----------|----------------|----------|--------|
| `+`      | Addition       | `7 + 2`  | `9`    |
| `-`      | Subtraction    | `7 - 2`  | `5`    |
| `*`      | Multiplication | `7 * 2`  | `14`   |
| `/`      | True division  | `7 / 2`  | `3.5`  |
| `//`     | Floor division | `7 // 2` | `3`    |
| `%`      | Modulo         | `7 % 2`  | `1`    |
| `**`     | Power          | `2 ** 8` | `256`  |

```python
print(7 + 2)    # 9
print(7 / 2)    # 3.5    — always float
print(7 // 2)   # 3      — drops the decimal
print(7 % 2)    # 1      — remainder
print(2 ** 10)  # 1024   — 2 to the power 10
```

---

## Assignment operators

`=` binds a value to a name.
The others combine arithmetic with assignment.

| Operator | Same as       | Example     |
|----------|---------------|-------------|
| `=`      | —             | `x = 5`     |
| `+=`     | `x = x + 3`   | `x += 3`    |
| `-=`     | `x = x - 3`   | `x -= 3`    |
| `*=`     | `x = x * 3`   | `x *= 3`    |
| `/=`     | `x = x / 3`   | `x /= 3`    |
| `//=`    | `x = x // 3`  | `x //= 3`   |
| `%=`     | `x = x % 3`   | `x %= 3`    |
| `**=`    | `x = x ** 3`  | `x **= 3`   |

```python
x = 10
x += 5      # x is now 15
x *= 2      # x is now 30
x //= 4     # x is now 7
print(x)
```

### The walrus operator `:=` (Python 3.8+)

The walrus operator **assigns a value to a variable inside an expression**.
It's called "walrus" because `:=` looks like a walrus's eyes and tusks.

Normally `=` is a **statement** — you can't use it inside an `if` or `while`.
`:=` is an **expression** — it both assigns and returns the value.

```python
# Without walrus — you call len() twice or use an extra line:
data = "hello world"
n = len(data)
if n > 5:
    print(f"{data} has {n} chars")

# With walrus — assign and check in one line:
if (n := len(data)) > 5:
    print(f"{data} has {n} chars")
```

### Where it's actually useful

**1. Avoid computing the same thing twice.**

```python
import math

# Without walrus — sqrt is computed twice
if math.sqrt(n) > 10:
    print(math.sqrt(n))

# With walrus — computed once
if (root := math.sqrt(n)) > 10:
    print(root)
```

**2. Read input in a loop until a sentinel.**

```python
# Pre-3.8 — repeat the input() call
line = input("> ")
while line != "quit":
    print("you typed:", line)
    line = input("> ")

# With walrus — one input() in the loop condition
while (line := input("> ")) != "quit":
    print("you typed:", line)
```

**3. Reuse a value in a comprehension.**

```python
data = [1, 4, 9, 16, 25]

# Without walrus — sqrt computed twice per item
result = [math.sqrt(x) for x in data if math.sqrt(x) > 2]

# With walrus — sqrt computed once per item
result = [r for x in data if (r := math.sqrt(x)) > 2]
print(result)   # [3.0, 4.0, 5.0]
```

### Rules to remember

- **Always wrap it in parentheses** inside an `if` or `while`.
  `if n := len(s) > 5:` is **wrong** (the `>` binds first).
  `if (n := len(s)) > 5:` is correct.

- **Use it when you'd otherwise repeat a calculation** or need to capture a value just before using it.

- **Don't overuse it.** If a normal `n = ...` line on its own is clearer, prefer that. Walrus is for cases where the assignment is genuinely part of the condition.

- **Only Python 3.8 and newer.** Older versions raise a `SyntaxError`.

---

## Comparison operators

Return `True` or `False`.

| Operator | Meaning            | Example       | Result |
|----------|--------------------|---------------|--------|
| `==`     | Equal              | `5 == 5`      | `True` |
| `!=`     | Not equal          | `5 != 3`      | `True` |
| `>`      | Greater than       | `5 > 3`       | `True` |
| `<`      | Less than          | `5 < 3`       | `False`|
| `>=`     | Greater or equal   | `5 >= 5`      | `True` |
| `<=`     | Less or equal      | `4 <= 5`      | `True` |

```python
print(5 == 5)     # True
print("a" == "A") # False — case-sensitive
print(10 != 5)    # True
```

### Chained comparisons

Python allows natural chains.

```python
age = 25

if 18 <= age < 65:
    print("working age")
```

Equivalent to `18 <= age and age < 65`.

---

## Logical operators

Combine boolean expressions.

| Operator | Meaning                            |
|----------|------------------------------------|
| `and`    | True if **both** sides are True    |
| `or`     | True if **either** side is True    |
| `not`    | Flips True ↔ False                 |

```python
a = True
b = False

print(a and b)   # False
print(a or b)    # True
print(not a)     # False
```

### Short-circuit evaluation

`and` / `or` stop as soon as the answer is known.

```python
user = None
if user and user.is_active:    # safe — short-circuits on None
    print("active")
```

`or` returns the **first truthy value** — handy for defaults:

```python
name = ""
display = name or "Guest"
print(display)   # 'Guest'
```

---

## Identity operators

Check if two names point to the **same object** in memory.
Different from `==` (which checks values).

| Operator | Meaning                                        |
|----------|------------------------------------------------|
| `is`     | True if both refer to the same object          |
| `is not` | True if they refer to different objects        |

```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a is b)     # True   — same object
print(a is c)     # False  — different objects, same content
print(a == c)     # True   — values are equal

print(a is not c) # True
```

**Use `is` only for** `None`, `True`, `False`:

```python
if x is None:
    print("no value")
```

Don't use `is` to compare numbers or strings — use `==`.

---

## Membership operators

Check if an item is inside a sequence.

| Operator | Meaning                            |
|----------|------------------------------------|
| `in`     | True if value is in the sequence   |
| `not in` | True if it's not in the sequence   |

```python
fruits = ["apple", "banana", "mango"]

print("apple" in fruits)        # True
print("grape" in fruits)        # False
print("grape" not in fruits)    # True

# Works on strings too
print("py" in "python")         # True

# And dictionaries (checks keys)
user = {"name": "Akshay", "age": 30}
print("name" in user)           # True
print("Akshay" in user)         # False — values aren't checked
```

---

## Bitwise operators

Work on the binary representation of integers.
Used in flags, masks, low-level code.

| Operator | Name         | Example      | Result |
|----------|--------------|--------------|--------|
| `&`      | AND          | `6 & 3`      | `2`    |
| `\|`     | OR           | `6 \| 3`     | `7`    |
| `^`      | XOR          | `6 ^ 3`      | `5`    |
| `~`      | NOT          | `~5`         | `-6`   |
| `<<`     | Left shift   | `2 << 3`     | `16`   |
| `>>`     | Right shift  | `16 >> 2`    | `4`    |

```python
print(6 & 3)    # 2   →  110 & 011 = 010
print(6 | 3)    # 7   →  110 | 011 = 111
print(6 ^ 3)    # 5   →  110 ^ 011 = 101
print(2 << 3)   # 16  →  2 * 2^3
print(16 >> 2)  # 4   →  16 / 2^2
```

You won't need these often.
Useful when working with low-level data, flags, or hashing.

---

## Operator precedence

When an expression mixes operators, Python applies them in this order
(top = highest priority, bottom = lowest):

```text
**                  Power
+x  -x  ~x          Unary plus / minus / bitwise NOT
*  /  //  %         Multiplication, division, modulo
+  -                Addition, subtraction
<<  >>              Bit shifts
&                   Bitwise AND
^                   Bitwise XOR
|                   Bitwise OR
==  !=  <  >  <=  >=  is  is not  in  not in
not                 Logical NOT
and                 Logical AND
or                  Logical OR
```

When in doubt, use **parentheses** to make intent obvious:

```python
print((5 + 3) * 2)   # 16  — parentheses first
print(5 + 3 * 2)     # 11  — * before +
```

---

## Quick reference

```text
Arithmetic   +  -  *  /  //  %  **
Assignment   =  +=  -=  *=  /=  //=  %=  **=
Comparison   ==  !=  >  <  >=  <=
Logical      and  or  not
Identity     is  is not
Membership   in  not in
Bitwise      &  |  ^  ~  <<  >>
```
