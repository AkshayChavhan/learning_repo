# =============================================================
# PYTHON IF / ELIF / ELSE — conditions and decisions
# =============================================================
# Structure:   if <condition>:  ->  elif <condition>:  ->  else:
# The colon and the INDENTATION (4 spaces) are what define the block.
# Only the FIRST matching branch runs — then the whole chain is skipped.
# =============================================================

age = 29
score = 77
name = "Akshay"
items = []


# -------------------------------------------------------------
# 1) THE BASIC FORMS
# -------------------------------------------------------------
print("--- 1) BASIC FORMS ---")

# if alone
if age >= 18:
    print("if            -> adult")

# if / else — exactly one of the two runs
if age >= 60:
    print("if/else       -> senior")
else:
    print("if/else       -> not senior")

# if / elif / else — checked top to bottom, FIRST match wins
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"
print("if/elif/else  -> grade", grade)          # B

# ORDER MATTERS — this chain is broken, everything hits the first branch
if score >= 60:
    wrong = "C"
elif score >= 90:
    wrong = "A"                                  # unreachable for score 95!
else:
    wrong = "F"
print("wrong order   -> grade", wrong, "(always C for anything >= 60)")


# -------------------------------------------------------------
# 2) CONDITIONS ARE JUST TRUTHINESS
# -------------------------------------------------------------
print("\n--- 2) TRUTHINESS ---")
# Falsy: False None 0 0.0 0j "" [] () {} set() range(0)  — everything else True
if items:
    print("truthy        -> has items")
else:
    print("falsy         -> list is empty")      # [] is falsy

if name:
    print("non-empty str -> truthy")

# `if x:` vs `if x is not None:` — NOT the same thing
count = 0
print("if count      ->", bool(count))           # False — 0 is falsy
print("count is not None ->", count is not None)  # True  — it exists
if count is not None:
    print("=> use `is not None` when 0 / '' / [] are valid values")


# -------------------------------------------------------------
# 3) COMPARISON & LOGICAL OPERATORS IN CONDITIONS
# -------------------------------------------------------------
print("\n--- 3) OPERATORS ---")
if 18 <= age < 65:                              # chaining — reads like math
    print("chained       -> working age")

if age > 18 and score > 50:
    print("and           -> both true")
if age < 18 or score > 50:
    print("or            -> at least one true")
if not (age < 18):
    print("not           -> flipped")

# Short-circuit protects the right-hand side
data = None
if data and data["key"]:                         # data is None -> stops, no crash
    print("never runs")
print("short-circuit -> no TypeError on None")

if name in ["Akshay", "Riya"]:
    print("membership    -> found in list")
if "shay" in name:
    print("substring     -> found in string")


# -------------------------------------------------------------
# 4) NESTED IFs vs GUARD CLAUSES
# -------------------------------------------------------------
print("\n--- 4) NESTING ---")
user = {"active": True, "role": "admin"}

# Nested — deep and hard to read
if user:
    if user.get("active"):
        if user.get("role") == "admin":
            print("nested        -> access granted")

# Guard clauses / flat conditions — preferred
if user and user.get("active") and user.get("role") == "admin":
    print("flat          -> access granted")


def check_access(u):
    """Return early on failures — keeps the happy path unindented."""
    if not u:
        return "no user"
    if not u.get("active"):
        return "inactive"
    if u.get("role") != "admin":
        return "not admin"
    return "granted"


print("guard clauses ->", check_access(user), "|", check_access({}))


# -------------------------------------------------------------
# 5) TERNARY (conditional expression)
# -------------------------------------------------------------
print("\n--- 5) TERNARY ---")
#   <value if true>  if  <condition>  else  <value if false>
status = "adult" if age >= 18 else "minor"
print("ternary       ->", status)
print("inline        ->", "even" if age % 2 == 0 else "odd")
print("in f-string   ->", f"You are {'old enough' if age >= 18 else 'too young'}")
print("in a list     ->", ["hi" if n > 1 else "lo" for n in [0, 2, 3]])
print("chained (avoid)->", "A" if score >= 90 else "B" if score >= 75 else "C")
print("default value ->", (name or "guest"))     # `or` as a cheap default


# -------------------------------------------------------------
# 6) pass / empty blocks
# -------------------------------------------------------------
print("\n--- 6) pass ---")
if age > 100:
    pass                                          # placeholder — do nothing (legal)
else:
    print("pass          -> a block can never be empty; use pass")


# -------------------------------------------------------------
# 7) COMMON MISTAKES
# -------------------------------------------------------------
print("\n--- 7) MISTAKES ---")
# 1. = vs ==      ->  `if x = 5:` is a SyntaxError (Python protects you here)
print("assignment in if -> SyntaxError (use == to compare)")

# 2. is vs ==     ->  `is` compares IDENTITY, `==` compares VALUE
n1 = int("1000")
n2 = int("1000")
print("n1 == n2      ->", n1 == n2)              # True  — same value
print("n1 is n2      ->", n1 is n2)              # False — different objects
print("=> use `is` ONLY for None / True / False")

# 3. float equality
print("0.1+0.2 == 0.3->", 0.1 + 0.2 == 0.3)      # False!
print("use isclose   ->", abs((0.1 + 0.2) - 0.3) < 1e-9)

# 4. checking many values
day = "sat"
print("long or chain ->", day == "sat" or day == "sun")
print("better: in    ->", day in ("sat", "sun"))     # cleaner and faster

# 5. comparing different types
print("'5' == 5      ->", "5" == 5)              # False — no auto conversion
print("int('5') == 5 ->", int("5") == 5)         # True


# -------------------------------------------------------------
# 8) if INSIDE OTHER CONSTRUCTS
# -------------------------------------------------------------
print("\n--- 8) IF ELSEWHERE ---")
nums = [1, 2, 3, 4, 5, 6]
print("comp filter   ->", [n for n in nums if n % 2 == 0])
print("comp ternary  ->", ["even" if n % 2 == 0 else "odd" for n in nums[:3]])
print("both          ->", [n * 10 if n > 3 else n for n in nums if n != 1])
print("dict comp     ->", {n: "big" for n in nums if n > 4})
print("filter()      ->", list(filter(lambda n: n > 4, nums)))
print("any/all       ->", any(n > 5 for n in nums), all(n > 0 for n in nums))

# while ... else / for ... else run when the loop finished WITHOUT break
for n in nums:
    if n > 99:
        break
else:
    print("for/else      -> loop finished, nothing broke out")


# -------------------------------------------------------------
# 9) REPLACING LONG if/elif CHAINS
# -------------------------------------------------------------
print("\n--- 9) ALTERNATIVES ---")
# dict dispatch — O(1) instead of scanning every branch
grades = {"A": 90, "B": 75, "C": 60}
print("dict lookup   ->", grades.get("B", "unknown"))

handlers = {"add": lambda p, q: p + q, "mul": lambda p, q: p * q}
print("dispatch      ->", handlers["mul"](3, 4))

# Range-based tables
def grade_of(mark):
    for cutoff, letter in [(90, "A"), (75, "B"), (60, "C")]:
        if mark >= cutoff:
            return letter
    return "F"


print("table lookup  ->", [grade_of(m) for m in (95, 80, 65, 20)])

# Python 3.10+ also has structural pattern matching:
#     match command:
#         case "start": ...
#         case _:       ...
print("match/case    -> Python 3.10+ feature (this machine runs %d.%d)"
      % (__import__("sys").version_info[0], __import__("sys").version_info[1]))


# -------------------------------------------------------------
# 10) WALRUS := IN CONDITIONS  (3.8+)
# -------------------------------------------------------------
print("\n--- 10) WALRUS ---")
values = [1, 2, 3, 4]
if (total := sum(values)) > 5:
    print("walrus        -> total is", total)    # computed once, reused

text = "hello world"
if (found := text.find("world")) != -1:
    print("find + walrus -> index", found)


# -------------------------------------------------------------
# 11) CHEAT SHEET
# -------------------------------------------------------------
#   if / elif / else  -> first match wins, rest skipped
#   indentation       -> 4 spaces, defines the block (no braces)
#   truthiness        -> empty things are False, everything else True
#   ternary           -> value_if_true if cond else value_if_false
#   guard clause      -> return early, keep the happy path flat
#   `is` -> only for None/True/False.  `==` -> for values.
#   `in` -> beats long `or` chains.    dict -> beats long elif chains.
print("\n--- 11) DONE ---")
print("final grade   ->", grade, "| status:", status)
