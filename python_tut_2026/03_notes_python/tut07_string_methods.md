# Python String Methods

All 45 public string methods in Python 3.
Plus `removeprefix` and `removesuffix` (added in 3.9) — your Python 3.8 won't have those yet.
Sorted **top = most useful, bottom = least useful** in everyday code.

Strings are **immutable** — every method below returns a **new** string. The original is unchanged.

> `len(s)` is a built-in function, not a `str` method.
> It's included at the top because it's used constantly with strings.

---

## Reference table

| Method            | Use case                                            | Example                                                  |
|-------------------|-----------------------------------------------------|----------------------------------------------------------|
| `len(s)`          | Get the length of the string (built-in, not a method) | `len("hello")` → `5`                                  |
| `s.strip()`       | Remove whitespace from both ends                    | `"  hi  ".strip()` → `"hi"`                              |
| `s.lower()`       | Convert to lowercase                                | `"Hello".lower()` → `"hello"`                            |
| `s.upper()`       | Convert to uppercase                                | `"hi".upper()` → `"HI"`                                  |
| `s.split(sep)`    | Break string into a list                            | `"a,b,c".split(",")` → `["a", "b", "c"]`                 |
| `sep.join(list)`  | Join list of strings into one string                | `",".join(["a", "b"])` → `"a,b"`                         |
| `s.replace(a, b)` | Replace all `a` with `b`                            | `"hi hi".replace("hi", "yo")` → `"yo yo"`                |
| `s.startswith(x)` | True if string starts with `x`                      | `"hello".startswith("he")` → `True`                      |
| `s.endswith(x)`   | True if string ends with `x`                        | `"file.txt".endswith(".txt")` → `True`                   |
| `s.find(x)`       | Index of first `x`, or `-1` if missing              | `"hello".find("l")` → `2`                                |
| `s.count(x)`      | Count how many times `x` appears                    | `"banana".count("a")` → `3`                              |
| `s.format(...)`   | Old-style formatting (use f-strings now)            | `"Hi {}".format("Ak")` → `"Hi Ak"`                       |
| `s.isdigit()`     | True if all characters are digits                   | `"123".isdigit()` → `True`                               |
| `s.isalpha()`     | True if all characters are letters                  | `"abc".isalpha()` → `True`                               |
| `s.isalnum()`     | True if letters or digits only                      | `"abc123".isalnum()` → `True`                            |
| `s.isspace()`     | True if all characters are whitespace               | `"   ".isspace()` → `True`                               |
| `s.title()`       | Capitalize first letter of every word               | `"hello world".title()` → `"Hello World"`                |
| `s.capitalize()`  | Capitalize first letter only                        | `"hello world".capitalize()` → `"Hello world"`           |
| `s.lstrip()`      | Strip whitespace from the **left** side only        | `"  hi  ".lstrip()` → `"hi  "`                           |
| `s.rstrip()`      | Strip whitespace from the **right** side only       | `"  hi  ".rstrip()` → `"  hi"`                           |
| `s.zfill(n)`      | Pad with zeros on the left to length `n`            | `"7".zfill(3)` → `"007"`                                 |
| `s.center(n)`     | Center text in a field of width `n`                 | `"hi".center(6)` → `"  hi  "`                            |
| `s.ljust(n)`      | Left-align in a field of width `n`                  | `"hi".ljust(5)` → `"hi   "`                              |
| `s.rjust(n)`      | Right-align in a field of width `n`                 | `"hi".rjust(5)` → `"   hi"`                              |
| `s.index(x)`      | Like `find()` but raises `ValueError` if missing    | `"hello".index("l")` → `2`                               |
| `s.rfind(x)`      | Find from the **right** side                        | `"hello".rfind("l")` → `3`                               |
| `s.rindex(x)`     | Like `rfind()` but raises `ValueError` if missing   | `"hello".rindex("l")` → `3`                              |
| `s.splitlines()`  | Split on line breaks (`\n`, `\r\n`)                  | `"a\nb".splitlines()` → `["a", "b"]`                     |
| `s.rsplit(sep)`   | Like `split()` but starts from the right            | `"a,b,c".rsplit(",", 1)` → `["a,b", "c"]`                |
| `s.partition(x)`  | Split into (before, sep, after)                     | `"a=1".partition("=")` → `("a", "=", "1")`               |
| `s.rpartition(x)` | Like `partition()` but searches from the right      | `"a=b=c".rpartition("=")` → `("a=b", "=", "c")`          |
| `s.removeprefix(x)` | Remove `x` from the start (Python 3.9+)            | `"unwanted_name".removeprefix("unwanted_")` → `"name"`   |
| `s.removesuffix(x)` | Remove `x` from the end (Python 3.9+)              | `"file.txt".removesuffix(".txt")` → `"file"`             |
| `s.islower()`     | True if all letters are lowercase                   | `"hello".islower()` → `True`                             |
| `s.isupper()`     | True if all letters are uppercase                   | `"HI".isupper()` → `True`                                |
| `s.istitle()`     | True if string is in Title Case                     | `"Hello World".istitle()` → `True`                       |
| `s.swapcase()`    | Flip case of every letter                           | `"Hi".swapcase()` → `"hI"`                               |
| `s.encode()`      | Convert string to bytes                             | `"hi".encode()` → `b"hi"`                                |
| `s.expandtabs(n)` | Replace tabs with `n` spaces                         | `"a\tb".expandtabs(4)` → `"a   b"`                       |
| `s.maketrans()`   | Build a translation table for `translate()`         | `str.maketrans("ab", "12")` → `{97: 49, 98: 50}`         |
| `s.translate(t)`  | Replace characters using a translation table        | `"abc".translate(str.maketrans("ab", "12"))` → `"12c"`   |
| `s.isidentifier()`| True if string is a valid Python identifier         | `"my_var".isidentifier()` → `True`                       |
| `s.isnumeric()`   | True if all characters are numeric (incl. ½, ², …)  | `"½".isnumeric()` → `True`                               |
| `s.isdecimal()`   | True if all characters are decimal digits           | `"123".isdecimal()` → `True`                             |
| `s.isprintable()` | True if all characters are printable                | `"hi\n".isprintable()` → `False`                         |
| `s.isascii()`     | True if all characters are ASCII (Python 3.7+)      | `"hello".isascii()` → `True`                             |
| `s.casefold()`    | Aggressive lowercase for case-insensitive compare   | `"ß".casefold()` → `"ss"`                                |
| `s.format_map(d)` | Like `.format()` but takes a dict directly          | `"Hi {name}".format_map({"name": "Ak"})` → `"Hi Ak"`     |

---

## How to use this table

- The **top ~10 rows** cover 90% of real-world string work.
- Use **f-strings** (`f"{x}"`) instead of `.format()`.
- For checking what's in a string, prefer `in` over `.find()` when you only need True/False:

```python
"py" in "python"   # True — cleaner than .find()
```

---

## Quick example combining the top methods

```python
raw = "  Hello, World!  "

# Clean it up
clean = raw.strip().lower()
print(clean)              # 'hello, world!'

# Split into words
words = clean.replace(",", "").split()
print(words)              # ['hello', 'world!']

# Check something
print(clean.startswith("hello"))   # True
print(clean.count("l"))            # 3
```
