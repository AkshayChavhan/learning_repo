# =============================================================
# PYTHON range() & datetime
# =============================================================
# range    -> a LAZY sequence of integers. Stores start/stop/step only.
# datetime -> date, time, datetime, timedelta + parsing/formatting.
# =============================================================

import sys
import time
import calendar
from datetime import date, time as dtime, datetime, timedelta, timezone


# =============================================================
# PART A — range()
# =============================================================
print("--- 1) range FORMS ---")
print("range(5)      ->", list(range(5)))            # 0..4  (stop EXCLUDED)
print("range(2, 6)   ->", list(range(2, 6)))         # 2..5
print("range(0,10,2) ->", list(range(0, 10, 2)))     # step 2
print("range(10,0,-1)->", list(range(10, 0, -1)))    # countdown
print("range(0)      ->", list(range(0)))            # [] — empty, no error
print("range(5, 2)   ->", list(range(5, 2)))         # [] — start past stop
print("negative      ->", list(range(-3, 3)))
try:
    range(0, 5, 0)
except ValueError as e:
    print("step 0        -> ValueError:", e)


# -------------------------------------------------------------
# 2) range IS LAZY (and that's the whole point)
# -------------------------------------------------------------
print("\n--- 2) LAZY ---")
r = range(1000000)
print("object        ->", r)
print("size in bytes ->", sys.getsizeof(r), "<- same for range(10) or range(1e9)")
print("list would be ->", sys.getsizeof(list(range(1000))), "bytes for just 1000")
print("start/stop/step->", r.start, r.stop, r.step)


# -------------------------------------------------------------
# 3) range IS A SEQUENCE — index, slice, membership
# -------------------------------------------------------------
print("\n--- 3) SEQUENCE OPS ---")
r = range(0, 20, 3)
print("r             ->", list(r))
print("len(r)        ->", len(r))
print("r[0] / r[-1]  ->", r[0], r[-1])
print("r[2:5]        ->", list(r[2:5]))              # slicing gives a RANGE
print("type of slice ->", type(r[2:5]))
print("9 in r        ->", 9 in r)                    # O(1) — computed, not scanned
print("index(9)      ->", r.index(9))
print("count(9)      ->", r.count(9))
print("reversed      ->", list(reversed(range(5))))
print("== compares values ->", range(0, 3) == range(3))


# -------------------------------------------------------------
# 4) range IN LOOPS
# -------------------------------------------------------------
print("\n--- 4) IN LOOPS ---")
for i in range(3):
    print("  i =", i, end="")
print()
items = ["a", "b", "c"]
for i in range(len(items)):
    print("  by index ->", i, items[i], end="")
print()
print("prefer        -> enumerate(items) over range(len(items))")
print("skip counting ->", [x for _ in range(3) for x in "ab"])
print("step through  ->", [items[i] for i in range(0, len(items), 2)])
print("sum via range ->", sum(range(1, 101)))        # 5050
print("float range?  -> NO. use [i/10 for i in range(0, 10)] ->",
      [i / 10 for i in range(0, 5)])


# =============================================================
# PART B — datetime
# =============================================================
print("\n--- 5) THE 4 CLASSES ---")
d = date(2026, 7, 28)
t = dtime(14, 30, 45)
dt = datetime(2026, 7, 28, 14, 30, 45)
td = timedelta(days=7, hours=3)
print("date          ->", d, type(d).__name__)
print("time          ->", t, type(t).__name__)
print("datetime      ->", dt, type(dt).__name__)
print("timedelta     ->", td, type(td).__name__)


# -------------------------------------------------------------
# 6) GETTING "NOW"
# -------------------------------------------------------------
print("\n--- 6) NOW ---")
now = datetime.now()
print("datetime.now()->", now)
print("date.today()  ->", date.today())
print("utc now       ->", datetime.now(timezone.utc))
print("time.time()   ->", round(time.time(), 2), "<- unix seconds since 1970")
print("from stamp    ->", datetime.fromtimestamp(0))
print("to stamp      ->", int(dt.timestamp()))


# -------------------------------------------------------------
# 7) COMPONENTS
# -------------------------------------------------------------
print("\n--- 7) COMPONENTS ---")
print("full          ->", dt)
print("y / m / d     ->", dt.year, dt.month, dt.day)
print("h / mi / s    ->", dt.hour, dt.minute, dt.second)
print("microsecond   ->", dt.microsecond)
print("weekday()     ->", dt.weekday(), "(Mon=0 .. Sun=6)")
print("isoweekday()  ->", dt.isoweekday(), "(Mon=1 .. Sun=7)")
print("day name      ->", calendar.day_name[dt.weekday()])
print("month name    ->", calendar.month_name[dt.month])
print(".date()/.time()->", dt.date(), dt.time())
print("isocalendar   ->", tuple(dt.isocalendar()))   # (year, week, weekday)
print("day of year   ->", dt.timetuple().tm_yday)
print("leap year?    ->", calendar.isleap(dt.year))
print("days in month ->", calendar.monthrange(2026, 7)[1])


# -------------------------------------------------------------
# 8) FORMATTING — strftime (datetime -> string)
# -------------------------------------------------------------
print("\n--- 8) strftime ---")
#   %Y 2026   %y 26     %m 07    %B July   %b Jul
#   %d 28     %A Tuesday %a Tue   %j 209
#   %H 14 (24h)  %I 02 (12h)  %p PM   %M 30   %S 45
print("%Y-%m-%d      ->", dt.strftime("%Y-%m-%d"))
print("%d/%m/%Y      ->", dt.strftime("%d/%m/%Y"))
print("%B %d, %Y     ->", dt.strftime("%B %d, %Y"))
print("%A            ->", dt.strftime("%A"))
print("12-hour       ->", dt.strftime("%I:%M %p"))
print("24-hour       ->", dt.strftime("%H:%M:%S"))
print("full readable ->", dt.strftime("%a, %d %b %Y at %H:%M"))
print("isoformat()   ->", dt.isoformat())
print("f-string fmt  ->", f"{dt:%d-%m-%Y %H:%M}")    # works directly in f-strings
print("str(dt)       ->", str(dt))


# -------------------------------------------------------------
# 9) PARSING — strptime (string -> datetime)
# -------------------------------------------------------------
print("\n--- 9) strptime ---")
print("from Y-m-d    ->", datetime.strptime("2026-07-28", "%Y-%m-%d"))
print("from d/m/Y    ->", datetime.strptime("28/07/2026", "%d/%m/%Y"))
print("with time     ->", datetime.strptime("28-07-2026 14:30", "%d-%m-%Y %H:%M"))
print("month name    ->", datetime.strptime("July 28, 2026", "%B %d, %Y"))
print("fromisoformat ->", datetime.fromisoformat("2026-07-28T14:30:45"))
try:
    datetime.strptime("28-07-2026", "%Y-%m-%d")
except ValueError as e:
    print("wrong pattern -> ValueError:", str(e)[:52])
print("=> the format string must match the input EXACTLY")


# -------------------------------------------------------------
# 10) timedelta — date arithmetic
# -------------------------------------------------------------
print("\n--- 10) timedelta ---")
print("dt + 7 days   ->", dt + timedelta(days=7))
print("dt - 30 days  ->", dt - timedelta(days=30))
print("dt + 5 hours  ->", dt + timedelta(hours=5))
print("mixed units   ->", dt + timedelta(weeks=1, days=2, hours=3, minutes=30))
print("tomorrow      ->", date.today() + timedelta(days=1))
print("last week     ->", date.today() - timedelta(weeks=1))

diff = date(2026, 12, 25) - date(2026, 7, 28)
print("difference    ->", diff, type(diff).__name__)
print(".days         ->", diff.days)
print("total_seconds ->", diff.total_seconds())
gap = datetime(2026, 7, 28, 18, 0) - datetime(2026, 7, 28, 14, 30)
print("hours between ->", gap.total_seconds() / 3600)
print("negative delta->", date(2026, 1, 1) - date(2026, 7, 28))

print("age in days   ->", (date.today() - date(1996, 5, 20)).days)
years = (date.today() - date(1996, 5, 20)).days // 365
print("rough age     ->", years, "years")

# timedelta CANNOT do months/years — they aren't fixed lengths
print("no months arg -> use  dateutil.relativedelta  or day arithmetic")


# -------------------------------------------------------------
# 11) COMPARING & SORTING DATES
# -------------------------------------------------------------
print("\n--- 11) COMPARE & SORT ---")
d1, d2 = date(2026, 1, 1), date(2026, 7, 28)
print("d1 < d2       ->", d1 < d2)
print("== / !=       ->", d1 == d2, d1 != d2)
print("max / min     ->", max(d1, d2), min(d1, d2))
dates = [date(2026, 5, 1), date(2025, 1, 9), date(2026, 1, 1)]
print("sorted        ->", sorted(dates))
print("newest        ->", max(dates))
print("in a range    ->", d1 <= date(2026, 3, 1) <= d2)
print("is past?      ->", d1 < date.today())
# Careful: you cannot compare a date with a datetime
try:
    date(2026, 1, 1) < datetime(2026, 1, 2)
except TypeError as e:
    print("date vs dt    -> TypeError:", e)


# -------------------------------------------------------------
# 12) replace / combine / timezones
# -------------------------------------------------------------
print("\n--- 12) MORE OPS ---")
print("replace year  ->", dt.replace(year=2030))
print("start of day  ->", dt.replace(hour=0, minute=0, second=0))
print("first of month->", d.replace(day=1))
print("combine       ->", datetime.combine(d, t))
print("naive (no tz) ->", dt.tzinfo)
aware = dt.replace(tzinfo=timezone.utc)
print("aware (utc)   ->", aware, "|", aware.tzinfo)
ist = aware.astimezone(timezone(timedelta(hours=5, minutes=30)))
print("to IST        ->", ist)
print("=> never mix naive and aware datetimes in comparisons")


# -------------------------------------------------------------
# 13) PRACTICAL SNIPPETS
# -------------------------------------------------------------
print("\n--- 13) PRACTICAL ---")
print("timestamp file->", datetime.now().strftime("backup_%Y%m%d_%H%M%S.zip"))
print("days till NY  ->", (date(2027, 1, 1) - date.today()).days)
print("is weekend?   ->", date(2026, 8, 1).weekday() >= 5)

start_of_week = d - timedelta(days=d.weekday())
print("week Mon-Sun  ->", start_of_week, "to", start_of_week + timedelta(days=6))

last_day = calendar.monthrange(d.year, d.month)[1]
print("month range   ->", d.replace(day=1), "to", d.replace(day=last_day))

week_dates = [d + timedelta(days=i) for i in range(5)]
print("next 5 days   ->", [x.strftime("%d %a") for x in week_dates])

t0 = time.perf_counter()
sum(range(100000))
print("elapsed ms    ->", round((time.perf_counter() - t0) * 1000, 3))


# -------------------------------------------------------------
# 14) CHEAT SHEET
# -------------------------------------------------------------
#   range(start, stop, step)   lazy int sequence; stop is EXCLUDED
#   date / time / datetime / timedelta   the four classes
#   datetime.now() / date.today()        current moment
#   dt.strftime(fmt)  -> string    |  datetime.strptime(s, fmt) -> datetime
#   dt + timedelta(days=n)         |  d2 - d1 -> timedelta (.days)
#   dt.weekday() Mon=0             |  dt.isoformat()  ->  2026-07-28T14:30:45
#   f"{dt:%d-%m-%Y}"               |  fromisoformat / fromtimestamp
print("\n--- 14) DONE ---")
print("range         ->", range(0, 10, 2))
print("dt            ->", dt)
