# =============================================================
# PYTHON while LOOP — repeat while a condition stays True
# =============================================================
#   while <condition>:
#       body            <- runs again and again
#       (something must eventually make the condition False!)
#
# Use `while` when you DON'T know how many rounds you need.
# Use `for`   when you're walking a known sequence.
# =============================================================


# -------------------------------------------------------------
# 1) THE BASIC LOOP
# -------------------------------------------------------------
print("--- 1) BASIC ---")
i = 1
while i <= 5:
    print("  i =", i, end="  |")
    i += 1                       # <- THE most forgotten line = infinite loop
print("\nafter loop    -> i is", i)      # 6 — the value that failed the test

# Counting down
n = 3
while n > 0:
    print("  countdown ->", n)
    n -= 1
print("liftoff!")

# Loop that never runs — the condition was False from the start
while False:
    print("never printed")
print("zero rounds   -> a while loop can run 0 times")


# -------------------------------------------------------------
# 2) ACCUMULATOR PATTERNS
# -------------------------------------------------------------
print("\n--- 2) ACCUMULATORS ---")
total, k = 0, 1
while k <= 10:
    total += k
    k += 1
print("sum 1..10     ->", total)                # 55

fact, m = 1, 5
while m > 1:
    fact *= m
    m -= 1
print("5 factorial   ->", fact)                 # 120

num, digits = 9384, 0
while num > 0:
    num //= 10
    digits += 1
print("digit count   ->", digits)               # 4

rev, src = 0, 1234
while src > 0:
    rev = rev * 10 + src % 10
    src //= 10
print("reverse 1234  ->", rev)                  # 4321


# -------------------------------------------------------------
# 3) break — leave the loop immediately
# -------------------------------------------------------------
print("\n--- 3) break ---")
i = 0
while True:                       # deliberate infinite loop...
    i += 1
    if i == 4:
        break                     # ...with a clear exit
    print("  round", i, end="")
print("\nbroke at      ->", i)

# break only exits the INNERMOST loop
outer = 0
while outer < 3:
    inner = 0
    while inner < 5:
        if inner == 2:
            break                 # exits the inner while only
        inner += 1
    outer += 1
print("nested break  -> outer ran", outer, "times")


# -------------------------------------------------------------
# 4) continue — skip to the next round
# -------------------------------------------------------------
print("\n--- 4) continue ---")
i = 0
while i < 8:
    i += 1                        # increment FIRST — continue would skip it
    if i % 2 == 0:
        continue                  # jump straight back to the condition
    print("  odd ->", i, end="")
print()
# TRAP: putting `i += 1` after `continue` = infinite loop


# -------------------------------------------------------------
# 5) while ... else  (runs only if NO break happened)
# -------------------------------------------------------------
print("\n--- 5) while/else ---")
i = 0
while i < 3:
    i += 1
else:
    print("else ran      -> finished normally, no break")

i = 0
while i < 3:
    i += 1
    if i == 2:
        break
else:
    print("never printed")
print("with break    -> else was SKIPPED")

# Real use: searching
target, found, idx = 7, False, 0
data = [3, 9, 7, 1]
while idx < len(data):
    if data[idx] == target:
        found = True
        break
    idx += 1
else:
    print("search else   -> not found")
print("search        ->", "found at", idx if found else "-")


# -------------------------------------------------------------
# 6) SENTINEL / MENU LOOPS  (classic while use-case)
# -------------------------------------------------------------
print("\n--- 6) SENTINEL ---")
# Real code would use input(); here we replay a scripted list of "typed" values
typed = ["5", "12", "abc", "quit"]
step, running_total = 0, 0
while step < len(typed):
    entry = typed[step]
    step += 1
    if entry == "quit":
        print("  got 'quit' -> stopping")
        break
    if not entry.isdigit():
        print("  '%s' is not a number, ignored" % entry)
        continue
    running_total += int(entry)
print("sentinel total->", running_total)         # 17


# -------------------------------------------------------------
# 7) WALRUS := IN A while  (3.8+ — the tidiest read-until-done)
# -------------------------------------------------------------
print("\n--- 7) WALRUS ---")
queue = [3, 2, 1]
while (item := queue.pop() if queue else None) is not None:
    print("  popped ->", item, end="")
print("\nqueue empty   ->", queue)

# Same idea for consuming a stream / chunked file
chunks = iter(["aa", "bb", ""])
while (chunk := next(chunks)) != "":
    print("  chunk ->", chunk, end="")
print("\nread until empty string")


# -------------------------------------------------------------
# 8) do-while EMULATION  (Python has no do/while)
# -------------------------------------------------------------
print("\n--- 8) do-while ---")
# Guarantee the body runs at least once:  while True + break at the end
attempts = 0
while True:
    attempts += 1
    print("  body ran, attempt", attempts)
    if attempts >= 2:
        break
print("do-while      -> ran", attempts, "times (at least once guaranteed)")


# -------------------------------------------------------------
# 9) ALGORITHMS THAT NEED while
# -------------------------------------------------------------
print("\n--- 9) ALGORITHMS ---")

# Binary search — the range shrinks unpredictably, so `for` doesn't fit
def binary_search(sorted_list, want):
    low, high = 0, len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == want:
            return mid
        if sorted_list[mid] < want:
            low = mid + 1
        else:
            high = mid - 1
    return -1


sorted_data = [1, 3, 5, 7, 9, 11]
print("binary search ->", binary_search(sorted_data, 9), binary_search(sorted_data, 4))


# Euclid's GCD
def gcd(p, q):
    while q:                       # loops until q becomes 0 (falsy)
        p, q = q, p % q
    return p


print("gcd(48, 18)   ->", gcd(48, 18))           # 6


# Collatz — nobody knows the trip count in advance
steps, x = 0, 27
while x != 1:
    x = x // 2 if x % 2 == 0 else 3 * x + 1
    steps += 1
print("collatz(27)   ->", steps, "steps")        # 111


# Convergence loop — stop when the change is tiny enough
guess, target_val = 1.0, 2.0
while abs(guess * guess - target_val) > 1e-10:
    guess = (guess + target_val / guess) / 2      # Newton's method
print("sqrt(2)       ->", round(guess, 8))


# -------------------------------------------------------------
# 10) INFINITE-LOOP TRAPS
# -------------------------------------------------------------
print("\n--- 10) TRAPS ---")
print("1. forgetting i += 1               -> runs forever")
print("2. `continue` before the increment -> runs forever")
print("3. changing the wrong variable     -> runs forever")
print("4. float equality as the condition -> may never hit exactly")
f = 0.0
guard = 0
while f != 1.0 and guard < 100:      # `f != 1.0` alone would never end
    f += 0.1
    guard += 1
print("   float guard ->", guard, "rounds, f =", round(f, 2))
print("5. always add a safety counter when the exit isn't obvious")


# -------------------------------------------------------------
# 11) while vs for
# -------------------------------------------------------------
#   while -> unknown count: user input, retries, convergence, game loops,
#            binary search, reading until EOF, "until it's valid"
#   for   -> known sequence: lists, strings, dicts, range(n), files
print("\n--- 11) while vs for ---")
i, out = 0, []
while i < 5:
    out.append(i)
    i += 1
print("while version ->", out)
print("for version   ->", [i for i in range(5)], "<- shorter, prefer this")


# -------------------------------------------------------------
# 12) CHEAT SHEET
# -------------------------------------------------------------
#   while cond:        repeat while cond is truthy (may run 0 times)
#   break              exit the loop now
#   continue           skip to the next condition check
#   else:              runs ONLY if the loop ended without break
#   while True: ...    infinite loop — must contain a break
#   := walrus          assign + test in one condition (3.8+)
print("\n--- 12) DONE ---")
print("everything above finished — no infinite loops left running")
