# =============================================================
# PYTHON STRINGS — every str method on ONE example sentence
# =============================================================
# Rule to remember: strings are IMMUTABLE.
# No method below changes `s` — each one RETURNS a new string.
# =============================================================

import sys

s = "  python is Fun, and Python is powerful!  "

print("original      ->", repr(s))
print("len           ->", len(s))          # 42  (spaces counted too)
print("s unchanged   ->", repr(s))


# -------------------------------------------------------------
# 1) CASE METHODS
# -------------------------------------------------------------
print("\n--- 1) CASE ---")
print("upper()       ->", s.upper())       # '  PYTHON IS FUN, AND PYTHON IS POWERFUL!  '
print("lower()       ->", s.lower())       # '  python is fun, and python is powerful!  '
print("title()       ->", s.title())       # '  Python Is Fun, And Python Is Powerful!  '
print("capitalize()  ->", s.capitalize())  # only 1st char up, REST forced lower
print("swapcase()    ->", s.swapcase())    # upper <-> lower flipped
print("casefold()    ->", s.casefold())    # aggressive lower() — use for comparisons

# lower() vs casefold(): German 'ß'
print("'ß'.lower()   ->", "ß".lower())     # 'ß'
print("'ß'.casefold()->", "ß".casefold())  # 'ss'  <- correct for matching


# -------------------------------------------------------------
# 2) STRIP / TRIM METHODS
# -------------------------------------------------------------
print("\n--- 2) STRIP ---")
print("strip()       ->", repr(s.strip()))     # both sides
print("lstrip()      ->", repr(s.lstrip()))    # left only
print("rstrip()      ->", repr(s.rstrip()))    # right only

t = s.strip()                                   # clean version reused below
print("t             ->", repr(t))

# strip(chars) removes a SET of characters, not a prefix/suffix string
print("strip(' !')   ->", repr(s.strip(" !")))  # spaces AND '!' stripped
# removeprefix / removesuffix need Python 3.9+  (this machine runs 3.8)
if sys.version_info >= (3, 9):
    print("removeprefix  ->", t.removeprefix("python "))  # 'is Fun, and Python is powerful!'
    print("removesuffix  ->", t.removesuffix("!"))        # drops trailing '!'
    print("no-match keeps->", t.removeprefix("java "))    # unchanged if prefix absent
else:
    print("removeprefix  -> needs Python 3.9+ | 3.8 way:", t[len("python "):])
    print("removesuffix  -> needs Python 3.9+ | 3.8 way:", t[:-1])


# -------------------------------------------------------------
# 3) SEARCH / FIND METHODS
# -------------------------------------------------------------
print("\n--- 3) SEARCH ---")
print("find('is')    ->", t.find("is"))         # 7   -> first index
print("rfind('is')   ->", t.rfind("is"))        # 26  -> last index
print("find('java')  ->", t.find("java"))       # -1  -> NOT found (safe)
print("index('is')   ->", t.index("is"))        # 7   -> same as find
# t.index("java")  ->  raises ValueError  (find returns -1 instead)
print("rindex('is')  ->", t.rindex("is"))       # 26
print("count('is')   ->", t.count("is"))        # 2
print("count('Python')->", t.count("Python"))   # 1  <- case sensitive!
print("count in slice->", t.count("is", 10))    # search from index 10 onward

print("startswith    ->", t.startswith("python"))          # True
print("endswith      ->", t.endswith("!"))                 # True
print("startswith tup->", t.startswith(("java", "python")))# True — tuple = any of
print("'is' in t     ->", "is" in t)                       # True — pythonic membership


# -------------------------------------------------------------
# 4) REPLACE
# -------------------------------------------------------------
print("\n--- 4) REPLACE ---")
print("replace all   ->", t.replace("Python", "Java"))     # only exact-case matches
print("replace count ->", t.replace("is", "IS", 1))        # only FIRST occurrence
print("case-insens.  ->", t.lower().replace("python", "java"))
print("remove char   ->", t.replace(",", ""))              # replace with '' = delete


# -------------------------------------------------------------
# 5) SPLIT / JOIN / PARTITION
# -------------------------------------------------------------
print("\n--- 5) SPLIT & JOIN ---")
print("split()       ->", t.split())            # split on ANY whitespace run
print("split(',')    ->", t.split(","))         # ['python is Fun', ' and Python is powerful!']
print("split maxsplit->", t.split(" ", 2))      # only 2 splits, rest stays whole
print("rsplit maxsp. ->", t.rsplit(" ", 2))     # splits from the RIGHT
print("splitlines()  ->", "line1\nline2\nline3".splitlines())

words = t.split()
print("join with '-' ->", "-".join(words))      # python-is-Fun,-and-Python-is-powerful!
print("join with ' ' ->", " ".join(words))      # back to the sentence
print("join chars    ->", "|".join("abc"))      # 'a|b|c'  — any iterable of strings

# partition: splits into exactly 3 parts (before, separator, after)
print("partition(',')->", t.partition(","))     # ('python is Fun', ',', ' and Python...')
print("rpartition(' ')->", t.rpartition(" "))   # splits at the LAST space
print("partition miss->", t.partition("#"))     # ('whole string', '', '') — never errors


# -------------------------------------------------------------
# 6) ALIGN / PAD METHODS
# -------------------------------------------------------------
print("\n--- 6) ALIGN & PAD ---")
w = "Python"
print("center(20,'*')->", w.center(20, "*"))    # *******Python*******
print("ljust(20,'.') ->", w.ljust(20, "."))     # Python..............
print("rjust(20,'.') ->", w.rjust(20, "."))     # ..............Python
print("zfill(10)     ->", w.zfill(10))          # 0000Python
print("zfill on num  ->", "-42".zfill(8))       # -0000042  <- sign stays in front
print("expandtabs(4) ->", "a\tb\tc".expandtabs(4))  # tabs -> spaces


# -------------------------------------------------------------
# 7) is* VALIDATION METHODS  (all return True/False)
# -------------------------------------------------------------
print("\n--- 7) is* CHECKS ---")
print("t.isalpha()   ->", t.isalpha())          # False — has spaces/punctuation
print("'Python'.isalpha()  ->", "Python".isalpha())     # True
print("'Python3'.isalnum() ->", "Python3".isalnum())    # True — letters+digits
print("'12345'.isdigit()   ->", "12345".isdigit())      # True
print("'12345'.isdecimal() ->", "12345".isdecimal())    # True — strictest
print("'½'.isnumeric()     ->", "½".isnumeric())        # True — loosest
print("'²'.isdigit()       ->", "²".isdigit(), "| isdecimal ->", "²".isdecimal())
print("t.islower()   ->", t.islower())          # False — has 'F' and 'P'
print("t.isupper()   ->", t.isupper())          # False
print("t.istitle()   ->", t.istitle())          # False
print("title istitle ->", t.title().istitle())  # True
print("'   '.isspace()     ->", "   ".isspace())        # True
print("t.isascii()   ->", t.isascii())          # True — no unicode beyond ASCII
print("t.isprintable()->", t.isprintable())     # True — no \n, \t etc.
print("'my_var'.isidentifier() ->", "my_var".isidentifier())  # True — valid var name
print("'2var'.isidentifier()   ->", "2var".isidentifier())    # False


# -------------------------------------------------------------
# 8) TRANSLATE / MAKETRANS
# -------------------------------------------------------------
print("\n--- 8) TRANSLATE ---")
table = str.maketrans("aeiou", "AEIOU")         # 1-to-1 char mapping
print("vowels upper  ->", t.translate(table))

drop = str.maketrans("", "", ",!")              # 3rd arg = chars to DELETE
print("drop punct    ->", t.translate(drop))

multi = str.maketrans({"P": "J", "p": "j"})     # dict form also works
print("dict maketrans->", t.translate(multi))


# -------------------------------------------------------------
# 9) FORMATTING
# -------------------------------------------------------------
print("\n--- 9) FORMAT ---")
lang, score = "Python", 9.5
print("f-string      ->", f"{lang} scores {score}/10")          # preferred
print("f-string align->", f"|{lang:>10}|{lang:^10}|{lang:<10}|")
print("f-string round->", f"{score:.2f} and {1234567:,}")
print("f-string debug->", f"{score = }")                        # score = 9.5

print("format()      ->", "{} is {}".format(lang, "Fun"))
print("format index  ->", "{1} then {0}".format("second", "first"))
print("format named  ->", "{l} v{v}".format(l=lang, v=3.12))

data = {"l": "Python", "v": 3.12}
print("format_map()  ->", "{l} v{v}".format_map(data))          # takes a dict directly

print("% old style   ->", "%s is %.1f" % (lang, score))         # legacy, avoid


# -------------------------------------------------------------
# 10) ENCODE  (str -> bytes)
# -------------------------------------------------------------
print("\n--- 10) ENCODE ---")
b = t.encode("utf-8")
print("encode()      ->", b[:20], "...")        # b'python is Fun, and P' ...
print("type          ->", type(b))              # <class 'bytes'>
print("decode() back ->", b.decode("utf-8") == t)   # True — round trip
print("unicode bytes ->", "café".encode("utf-8"), "| len", len("café".encode("utf-8")))


# -------------------------------------------------------------
# 11) BONUS — indexing, slicing, operators (not methods, but daily use)
# -------------------------------------------------------------
print("\n--- 11) SLICING & OPERATORS ---")
print("t[0]          ->", t[0])                 # 'p'   first char
print("t[-1]         ->", t[-1])                # '!'   last char
print("t[0:6]        ->", t[0:6])               # 'python'
print("t[:6]         ->", t[:6])                # same — start defaults to 0
print("t[-9:]        ->", t[-9:])               # 'powerful!'
print("t[::2]        ->", t[::2])               # every 2nd char
print("t[::-1]       ->", t[::-1])              # reversed string
print("concat  +     ->", "Py" + "thon")        # 'Python'
print("repeat  *     ->", "-" * 20)             # '--------------------'
print("iterate       ->", [c for c in "abc"])   # ['a', 'b', 'c']


# -------------------------------------------------------------
# 12) IMMUTABILITY PROOF
# -------------------------------------------------------------
print("\n--- 12) IMMUTABLE ---")
print("after ALL calls, s is untouched ->", repr(s))
# t[0] = "P"   ->  TypeError: 'str' object does not support item assignment
print("rebind needed ->", "P" + t[1:])          # build a NEW string instead
