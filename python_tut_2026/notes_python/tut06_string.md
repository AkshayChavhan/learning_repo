# Python Strings

A **string** is text.
Wrap it in quotes — single, double, or triple.

```python
a = "Hello"
b = 'World'
c = """multi-line
string"""

print(a, b)
```

Single and double quotes work the same.
Pick one for consistency.

---

## Quotes inside quotes

If your text has a `'`, wrap it in `"`.
If it has a `"`, wrap it in `'`.

```python
print("It's Monday")
print('She said "hi"')
```

Or escape with a backslash:

```python
print('It\'s Monday')
print("She said \"hi\"")
```

---

## Multi-line strings

Triple quotes (`"""` or `'''`) keep line breaks.

```python
text = """Line 1
Line 2
Line 3"""

print(text)
```

Output:

```text
Line 1
Line 2
Line 3
```

---

## f-strings — insert variables

Put `f` before the quote.
Use `{ }` for variables or expressions.

```python
name = "Akshay"
age = 30

print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")
```

Output:

```text
Name: Akshay, Age: 30
Next year: 31
```

f-strings work with any expression inside `{ }`:

```python
nums = [1, 2, 3]
print(f"Sum is {sum(nums)}")
```

---

## Strings are immutable

You can't change a string in place.
Methods return a **new** string.

```python
s = "hello"
s.upper()
print(s)   # 'hello' — unchanged

s = s.upper()
print(s)   # 'HELLO'  — rebind to the new string
```

---

## Length and indexing

`len()` gives the number of characters.
Indexes start at `0`.

```python
s = "Python"

print(len(s))   # 6
print(s[0])     # 'P'
print(s[1])     # 'y'
print(s[-1])    # 'n'  — last character
print(s[-2])    # 'o'  — second to last
```

---

## Slicing — `[start:stop:step]`

Get a substring.
`stop` is **exclusive**.

```python
s = "Python"

print(s[0:3])    # 'Pyt'
print(s[2:])     # 'thon'   — from index 2 to end
print(s[:4])     # 'Pyth'   — start to index 4
print(s[::-1])   # 'nohtyP' — reverse
print(s[::2])    # 'Pto'    — every 2nd character
```

---

## Concatenation and repetition

`+` joins strings.
`*` repeats them.

```python
print("Hello " + "World")    # 'Hello World'
print("ha" * 3)               # 'hahaha'
print("-" * 20)               # '--------------------'
```

You can't `+` a string and a number directly:

```python
# "Age: " + 30   # TypeError
print("Age: " + str(30))   # works
print(f"Age: {30}")        # cleaner
```

---

## Common string methods

```python
s = "  Hello, World!  "

print(s.upper())         # '  HELLO, WORLD!  '
print(s.lower())         # '  hello, world!  '
print(s.strip())         # 'Hello, World!'  — removes whitespace
print(s.replace("World", "Python"))   # '  Hello, Python!  '
print(s.startswith("  H"))  # True
print(s.endswith("!  "))    # True
print(s.find("World"))      # 9   — index, or -1 if not found
print(s.count("l"))         # 3
```

---

## Split and join

`split()` turns a string into a list.

```python
csv = "apple,banana,mango"
parts = csv.split(",")
print(parts)   # ['apple', 'banana', 'mango']

words = "hello world how are you".split()   # splits on whitespace
print(words)   # ['hello', 'world', 'how', 'are', 'you']
```

`join()` turns a list into a string.

```python
parts = ["apple", "banana", "mango"]
print(",".join(parts))   # 'apple,banana,mango'
print(" - ".join(parts)) # 'apple - banana - mango'
```

---

## Check what's inside a string

```python
s = "Python3"

print(s.isalpha())   # False  — contains '3'
print(s.isdigit())   # False
print(s.isalnum())   # True   — letters + digits
print("123".isdigit())   # True
print("abc".isalpha())   # True
print("hello".islower()) # True
print("HELLO".isupper()) # True
```

---

## `in` — check for substring

```python
s = "Hello, World!"

print("World" in s)        # True
print("python" in s)       # False
print("python" in s.lower())   # False — still no "python"
```

---

## Escape characters

An **escape character** is a backslash `\` followed by another character.
Together they mean something special — a character you can't easily type, or one that has another job (like a quote).

### Why escapes exist

You can't put a `"` inside a `"..."` string directly:

```python
# print("She said "hi"")   # SyntaxError
print("She said \"hi\"")   # OK — escaped
```

### Common escape sequences

| Escape | Meaning            | What it does                                  |
|--------|--------------------|-----------------------------------------------|
| `\n`   | Newline            | Moves text to the next line                   |
| `\t`   | Tab                | Inserts a tab space (usually 4 or 8 columns)  |
| `\\`   | Backslash          | Prints a single `\`                            |
| `\'`   | Single quote       | Lets you put `'` inside `'...'`                |
| `\"`   | Double quote       | Lets you put `"` inside `"..."`                |
| `\r`   | Carriage return    | Moves cursor to start of the line (overwrites)|
| `\b`   | Backspace          | Removes the previous character                |
| `\0`   | Null character     | The zero byte — used in low-level code        |
| `\a`   | Bell / alert       | Beeps in some terminals                       |
| `\f`   | Form feed          | Page break in printers (very rare today)      |
| `\v`   | Vertical tab       | Vertical tab character (very rare today)      |

### `\n` — newline

```python
print("Line 1\nLine 2\nLine 3")
```

Output:

```text
Line 1
Line 2
Line 3
```

### `\t` — tab

```python
print("Name\tAge\tCity")
print("Akshay\t30\tMumbai")
```

Output:

```text
Name    Age     City
Akshay  30      Mumbai
```

### `\\` — backslash

You need two backslashes to print one.
`\` alone tries to start an escape.

```python
print("path: C:\\Users\\Akshay")
```

Output:

```text
path: C:\Users\Akshay
```

### `\'` and `\"` — escape the quote

You only need to escape the quote that matches your wrapper.

```python
print('It\'s Monday')        # ' inside '...'
print("She said \"hi\"")     # " inside "..."

# Or just switch quote style — usually cleaner:
print("It's Monday")
print('She said "hi"')
```

### `\r` — carriage return (rarely useful)

`\r` moves the cursor to the start of the line, overwriting what's there.

```python
print("Loading...\rDone!")
```

Output (in a real terminal):

```text
Done!...
```

### Raw strings — turn off escapes

Put `r` before the quote.
Backslashes become regular characters.

```python
print(r"C:\Users\Akshay\n")
```

Output:

```text
C:\Users\Akshay\n
```

Useful for:

- Windows file paths
- Regular expressions (regex uses `\` heavily)

```python
import re

pattern = r"\d+"            # without `r`, you'd need "\\d+"
print(re.findall(pattern, "abc 42 xyz 7"))   # ['42', '7']
```

### Unicode escapes

You can write any Unicode character with `\u` (4 hex digits) or `\U` (8):

```python
print("♥")    # ♥
print("π")    # π
print("Café") # Café
```

---

## f-string formatting tricks

```python
price = 59
txt = f"The price is {price} dollars"
print(txt)
```

```python
n = 3.14159

print(f"{n:.2f}")     # '3.14'   — 2 decimal places
print(f"{n:10.2f}")   # '      3.14'  — width 10, padded with spaces
print(f"{n:<10.2f}")  # '3.14      '  — left-aligned
print(f"{n:^10.2f}")  # '   3.14   '  — centered

big = 1_000_000
print(f"{big:,}")     # '1,000,000'  — thousands separator
```

---

## Quick reference

```text
len(s)              length
s[i]                character at index i
s[a:b]              slice from a to b (exclusive)
s + t               concatenation
s * n               repeat
s.upper() / .lower()
s.strip()           remove surrounding whitespace
s.replace(a, b)
s.split(sep)        string → list
sep.join(list)      list → string
s.startswith(x)
s.endswith(x)
s.find(x)           index or -1
"x" in s            True if substring present
f"{var}"            insert variable
f"{n:.2f}"          format number
```
