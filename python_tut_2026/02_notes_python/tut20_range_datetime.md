# Python `range` & `datetime`

Two built-in tools you'll reach for constantly:

- **`range`** — produce a sequence of integers, cheap and lazy.
- **`datetime`** — work with dates, times, and durations.

---

# Part 1 — `range`

`range` was introduced in tut16 for the `for` loop. Here we look at it as its own **type** — what it really is and what else you can do with it.

## What `range` is

`range(...)` returns a **range object** — a lazy sequence of integers. It doesn't build a list. It computes each value on demand.

```python
r = range(5)
print(r)               # range(0, 5)
print(type(r))         # <class 'range'>
print(list(r))         # [0, 1, 2, 3, 4]
```

```text
range(0, 5)
<class 'range'>
[0, 1, 2, 3, 4]
```

Cheap and memory-friendly:

```python
print(range(10**9))    # works instantly — nothing is computed yet
# print(list(range(10**9)))   # would crash — tries to build a billion-item list
```

---

## The three call forms

```python
range(stop)                  # 0, 1, ..., stop-1
range(start, stop)           # start, start+1, ..., stop-1
range(start, stop, step)     # start, start+step, ..., < stop (or > stop if step < 0)
```

| Call               | Yields              |
|--------------------|---------------------|
| `range(5)`         | `0 1 2 3 4`         |
| `range(2, 6)`      | `2 3 4 5`           |
| `range(0, 10, 2)`  | `0 2 4 6 8`         |
| `range(10, 0, -2)` | `10 8 6 4 2`        |
| `range(5, 5)`      | (empty)             |
| `range(5, 0)`      | (empty — no step)   |

```python
print(list(range(5)))
print(list(range(2, 6)))
print(list(range(0, 10, 2)))
print(list(range(10, 0, -2)))
print(list(range(5, 5)))
print(list(range(5, 0)))
```

```text
[0, 1, 2, 3, 4]
[2, 3, 4, 5]
[0, 2, 4, 6, 8]
[10, 8, 6, 4, 2]
[]
[]
```

`stop` is **exclusive** — `range(5)` does not include `5`.

---

## `range` is a sequence — supports `len`, indexing, slicing, `in`

Most tutorials never mention this. `range` behaves like a tuple of ints.

### Length

```python
print(len(range(10)))           # 10
print(len(range(0, 20, 3)))     # 7  -> 0, 3, 6, 9, 12, 15, 18
```

### Indexing

```python
r = range(10, 20)
print(r[0])     # 10
print(r[5])     # 15
print(r[-1])    # 19
```

### Slicing — gives another `range`

```python
r = range(100)
print(r[10:15])     # range(10, 15)
print(list(r[10:15]))   # [10, 11, 12, 13, 14]
```

### Membership — `in` is fast

```python
print(5 in range(10))            # True
print(99 in range(10))           # False
print(2 in range(0, 100, 3))     # False — 2 is not 0/3/6/...
print(6 in range(0, 100, 3))     # True
```

`in` on a range is O(1) — it's a math check, not a scan.

---

## Common idioms

### Build a list of numbers

```python
print(list(range(5)))            # [0, 1, 2, 3, 4]
print(list(range(1, 6)))         # [1, 2, 3, 4, 5]
```

### Repeat a block N times — use `_`

When you don't need the index:

```python
for _ in range(3):
    print("hello")
```

```text
hello
hello
hello
```

### Reverse a count

```python
for i in range(5, 0, -1):
    print(i)
```

```text
5
4
3
2
1
```

### Use `range` for indices, but prefer `enumerate`

```python
fruits = ["apple", "banana", "cherry"]

# Works but verbose:
for i in range(len(fruits)):
    print(i, fruits[i])

# Better — clearer intent:
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

Reach for `range(len(...))` only when you need to mutate the list by index.

---

## `range` quick reference

```text
range(stop)                # 0 .. stop-1
range(start, stop)         # start .. stop-1
range(start, stop, step)   # in steps; step != 0; can be negative

list(range(...))           # materialize to a list
len(r)                     # length
r[i]                       # indexing
r[a:b]                     # slicing -> another range
x in r                     # O(1) membership

for i in range(n):         # loop n times
for _ in range(n):         # loop n times, ignore the index
```

---

# Part 2 — `datetime`

Python's built-in `datetime` module handles dates, times, durations, and formatting.

Import it once and you get four main classes:

```python
from datetime import date, time, datetime, timedelta, timezone
```

| Class       | Represents                                      |
|-------------|-------------------------------------------------|
| `date`      | A calendar date — year, month, day              |
| `time`      | A time of day — hour, minute, second, microsecond |
| `datetime`  | Both together                                   |
| `timedelta` | A **duration** — difference between two dates/times |
| `timezone`  | A fixed offset from UTC                         |

---

## `date` — just the calendar

```python
from datetime import date

d = date(2026, 6, 3)
print(d)               # 2026-06-03
print(d.year, d.month, d.day)
```

```text
2026-06-03
2026 6 3
```

Today's date:

```python
from datetime import date

print(date.today())
```

```text
2026-06-03
```

The day of the week — `weekday()` returns Monday=0 ... Sunday=6:

```python
from datetime import date

d = date(2026, 6, 3)
print(d.weekday())     # 0 = Monday ... 6 = Sunday
print(d.isoweekday())  # 1 = Monday ... 7 = Sunday
```

---

## `time` — just the clock

```python
from datetime import time

t = time(14, 30, 0)
print(t)               # 14:30:00
print(t.hour, t.minute, t.second)
```

```text
14:30:00
14 30 0
```

`time` on its own is rare — usually you want the full `datetime`.

---

## `datetime` — date + time together

```python
from datetime import datetime

dt = datetime(2026, 6, 3, 14, 30, 15)
print(dt)               # 2026-06-03 14:30:15
print(dt.date())        # 2026-06-03
print(dt.time())        # 14:30:15
```

```text
2026-06-03 14:30:15
2026-06-03
14:30:15
```

Now and today:

```python
from datetime import datetime

print(datetime.now())       # local now
print(datetime.utcnow())    # UTC now (no timezone info attached — see "timezones" below)
```

---

## Formatting — `strftime` (datetime → string)

`strftime` ("string format time") turns a datetime into a string using format codes.

```python
from datetime import datetime

dt = datetime(2026, 6, 3, 14, 30, 15)

print(dt.strftime("%Y-%m-%d"))           # 2026-06-03
print(dt.strftime("%d/%m/%Y"))           # 03/06/2026
print(dt.strftime("%H:%M:%S"))           # 14:30:15
print(dt.strftime("%A, %d %B %Y"))       # Wednesday, 03 June 2026
print(dt.strftime("%I:%M %p"))           # 02:30 PM
```

```text
2026-06-03
03/06/2026
14:30:15
Wednesday, 03 June 2026
02:30 PM
```

### Common format codes

| Code | Meaning                       | Example  |
|------|-------------------------------|----------|
| `%Y` | 4-digit year                  | `2026`   |
| `%y` | 2-digit year                  | `26`     |
| `%m` | Month (01–12)                 | `06`     |
| `%B` | Full month name               | `June`   |
| `%b` | Short month name              | `Jun`    |
| `%d` | Day of month (01–31)          | `03`     |
| `%A` | Full weekday name             | `Wednesday` |
| `%a` | Short weekday name            | `Wed`    |
| `%H` | Hour 24h (00–23)              | `14`     |
| `%I` | Hour 12h (01–12)              | `02`     |
| `%M` | Minute (00–59)                | `30`     |
| `%S` | Second (00–59)                | `15`     |
| `%p` | AM / PM                       | `PM`     |
| `%j` | Day of year (001–366)         | `154`    |

---

## Parsing — `strptime` (string → datetime)

The reverse direction. You must give the **exact** format that matches the string.

```python
from datetime import datetime

s = "2026-06-03 14:30:15"
dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
print(dt)
print(type(dt).__name__)
```

```text
2026-06-03 14:30:15
datetime
```

If the format doesn't match exactly, you get `ValueError`:

```python
from datetime import datetime
# datetime.strptime("03/06/2026", "%Y-%m-%d")
# ValueError: time data '03/06/2026' does not match format '%Y-%m-%d'
```

### ISO 8601 — shortcut

`fromisoformat` parses the standard `YYYY-MM-DD[THH:MM:SS]` form without a format string.

```python
from datetime import datetime, date

print(date.fromisoformat("2026-06-03"))
print(datetime.fromisoformat("2026-06-03T14:30:15"))
```

```text
2026-06-03
2026-06-03 14:30:15
```

---

## `timedelta` — durations and arithmetic

`timedelta` is a **difference** between two dates/times. You add or subtract it from a `date`/`datetime`.

```python
from datetime import datetime, timedelta

now = datetime(2026, 6, 3, 14, 30)

tomorrow = now + timedelta(days=1)
print(tomorrow)

one_hour_ago = now - timedelta(hours=1)
print(one_hour_ago)

next_week = now + timedelta(weeks=1)
print(next_week)
```

```text
2026-06-04 14:30:00
2026-06-03 13:30:00
2026-06-10 14:30:00
```

`timedelta` accepts:

```text
days, seconds, microseconds, milliseconds, minutes, hours, weeks
```

Subtracting two `datetime`s gives a `timedelta`:

```python
from datetime import datetime

a = datetime(2026, 6, 3, 14, 30)
b = datetime(2026, 1, 1, 0, 0)
diff = a - b

print(diff)              # 153 days, 14:30:00
print(diff.days)         # 153
print(diff.total_seconds())   # full duration in seconds
```

```text
153 days, 14:30:00
153
13283400.0
```

---

## Comparisons

`date` and `datetime` support `<`, `<=`, `==`, etc. — chronological order.

```python
from datetime import date

a = date(2026, 6, 3)
b = date(2026, 12, 25)

print(a < b)      # True
print(a == b)     # False
print(min(a, b))  # 2026-06-03
```

---

## Timezones — naive vs aware

A `datetime` with **no** timezone is **naive** — it's just numbers, no real-world meaning.
A `datetime` with a `tzinfo` attached is **aware**.

```python
from datetime import datetime, timezone, timedelta

naive = datetime(2026, 6, 3, 14, 30)
print(naive.tzinfo)        # None

aware = datetime(2026, 6, 3, 14, 30, tzinfo=timezone.utc)
print(aware.tzinfo)        # UTC
print(aware)               # 2026-06-03 14:30:00+00:00

# A non-UTC fixed offset (e.g. India = +5:30)
ist = timezone(timedelta(hours=5, minutes=30))
local = datetime(2026, 6, 3, 20, 0, tzinfo=ist)
print(local)               # 2026-06-03 20:00:00+05:30
```

```text
None
UTC
2026-06-03 14:30:00+00:00
2026-06-03 20:00:00+05:30
```

For real timezone names (`"Asia/Kolkata"`, `"Europe/London"`), use `zoneinfo` (Python 3.9+) or the `pytz` package on 3.8.

```python
# Python 3.9+ only:
# from zoneinfo import ZoneInfo
# dt = datetime(2026, 6, 3, 20, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
```

Don't compare or subtract a naive and an aware datetime — Python raises `TypeError`.

---

## Common patterns

### "5 days ago" / "in 30 minutes"

```python
from datetime import datetime, timedelta

now = datetime.now()
print(now - timedelta(days=5))
print(now + timedelta(minutes=30))
```

### Age in years (rough)

```python
from datetime import date

born = date(1995, 4, 12)
today = date.today()
age_days = (today - born).days
age_years = age_days // 365      # approximate
print(age_years)
```

### Number of days between two dates

```python
from datetime import date

a = date(2026, 1, 1)
b = date(2026, 12, 31)
print((b - a).days)              # 364
```

### Loop over a date range

```python
from datetime import date, timedelta

start = date(2026, 6, 1)
end = date(2026, 6, 5)

d = start
while d <= end:
    print(d)
    d += timedelta(days=1)
```

```text
2026-06-01
2026-06-02
2026-06-03
2026-06-04
2026-06-05
```

---

## Common pitfalls

### 1. Confusing `strftime` and `strptime`

- `strftime` — **format** a datetime into a string. (`f` for "format".)
- `strptime` — **parse** a string into a datetime. (`p` for "parse".)

```python
from datetime import datetime

# format -> string
s = datetime.now().strftime("%Y-%m-%d")

# parse -> datetime
dt = datetime.strptime("2026-06-03", "%Y-%m-%d")
```

### 2. Naive vs aware datetimes can't mix

```python
from datetime import datetime, timezone
naive = datetime(2026, 6, 3)
aware = datetime(2026, 6, 3, tzinfo=timezone.utc)
# naive < aware   # TypeError: can't compare offset-naive and offset-aware datetimes
```

Fix: make them both aware (attach `tzinfo`) or both naive.

### 3. `utcnow()` returns a **naive** datetime

`datetime.utcnow()` gives the UTC time but **does not** attach `tzinfo`. That's surprising and a frequent bug.

```python
from datetime import datetime, timezone

# Avoid:
bad = datetime.utcnow()              # naive — pretends to be UTC

# Better:
good = datetime.now(timezone.utc)    # aware UTC datetime
print(good)
```

### 4. Month/day order in `strptime`

`strptime("03/06/2026", "%m/%d/%Y")` parses June 3rd.
`strptime("03/06/2026", "%d/%m/%Y")` parses March 6th.
The format string decides — be explicit.

### 5. `timedelta` doesn't know about months or years

You can't write `timedelta(months=1)` — months have variable length. Use `dateutil.relativedelta` from the `python-dateutil` package for month/year arithmetic.

---

## `datetime` quick reference

```text
from datetime import date, time, datetime, timedelta, timezone

date(y, m, d)              date.today()
time(h, m, s)
datetime(y, m, d, h, m, s)
datetime.now()             local now
datetime.now(timezone.utc) UTC now (aware)

dt.strftime("%Y-%m-%d")    format -> string
datetime.strptime(s, fmt)  parse -> datetime
date.fromisoformat(s)      ISO shortcut: "2026-06-03"
datetime.fromisoformat(s)  ISO shortcut: "2026-06-03T14:30:15"

dt + timedelta(days=1)     arithmetic
dt - timedelta(hours=2)
b - a                      timedelta
diff.days, diff.total_seconds()

a < b, a == b              comparisons (same kind only)
weekday() / isoweekday()   0..6 (Mon=0)  /  1..7 (Mon=1)

timezone.utc               built-in UTC
timezone(timedelta(...))   fixed-offset zone
ZoneInfo("Asia/Kolkata")   named zone (3.9+)
```
