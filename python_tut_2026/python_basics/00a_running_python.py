"""
tut00.1 — Running Python & the REPL.

Run from the repo root:
    python "python_tut_2026/python_basics/00a_running_python.py"

This file shows what's different about Python *as a runtime*:
indentation, print(), comments, docstrings. Open the REPL alongside
to compare interactive vs script behavior.
"""

# ─────────────────────────────────────────────────────────────
# 1. print() is a function — parentheses required.
# ─────────────────────────────────────────────────────────────
print("─── 1. print() ───")
print("Hello, Python!")
print("Multiple", "args", "are", "joined", "by", "spaces")
print("end='' suppresses the newline → ", end="")
print("see, no newline before this.")


# ─────────────────────────────────────────────────────────────
# 2. Expressions in a script produce no output on their own.
#    Uncomment the line below — it runs but you'll see nothing.
# ─────────────────────────────────────────────────────────────
print("\n─── 2. Bare expressions are silent in a script ───")
2 + 2                  # evaluated, result discarded, nothing printed
print("Result of 2+2 if we actually print it:", 2 + 2)


# ─────────────────────────────────────────────────────────────
# 3. Indentation is syntax. The block under `if` must be indented.
# ─────────────────────────────────────────────────────────────
print("\n─── 3. Indentation defines blocks ───")
x = 10
if x > 5:
    print("x is greater than 5")        # indented → inside the if
    print("still inside the if-block")  # same indent → same block
print("this line is outside the if")    # back to top level


# ─────────────────────────────────────────────────────────────
# 4. Comments and docstrings.
# ─────────────────────────────────────────────────────────────
print("\n─── 4. Comments and docstrings ───")

def greet(name):
    """Return a friendly greeting. This is a docstring."""   # docstring
    # The line above is special: it's stored in greet.__doc__
    return f"Hi, {name}!"

print(greet("Akshay"))
print("greet.__doc__ =", greet.__doc__)


# ─────────────────────────────────────────────────────────────
# 5. The "main" idiom — preview of sub-topic 0.8.
#    Top-level code runs automatically. There's no main() requirement.
#    But this idiom lets a file be both runnable AND importable.
# ─────────────────────────────────────────────────────────────
print("\n─── 5. The if __name__ == '__main__' idiom (preview) ───")

def main():
    print("main() ran because we called it explicitly.")

if __name__ == "__main__":
    # This block runs only when the file is executed directly,
    # NOT when another file does `import 00a_running_python`.
    main()


# ─────────────────────────────────────────────────────────────
# 6. Common first-week errors — read, don't run.
# ─────────────────────────────────────────────────────────────
# Uncomment any line below to see the error it produces:

# print "hello"          # SyntaxError: missing parens (Python 2 style)

# if True:
# print("unindented")    # IndentationError: expected an indented block

# x = 1
#     y = 2              # IndentationError: unexpected indent

# x =                    # SyntaxError: invalid syntax (incomplete statement)

print("\nAll examples ran. Now try opening the REPL with just: python")
