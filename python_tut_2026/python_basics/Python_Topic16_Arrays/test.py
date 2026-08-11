# =============================================================
# PYTHON ARRAYS
# =============================================================
# Python has NO built-in "array" type like C or Java.
# You have three options:
#   1. list          -> the everyday choice (any type, flexible)
#   2. array.array   -> stdlib, ONE numeric type, compact memory
#   3. numpy.ndarray -> 3rd-party, fast math on whole arrays (pip install numpy)
# =============================================================

import sys
from array import array


# -------------------------------------------------------------
# 1) THE LIST AS AN "ARRAY" (what tutorials usually mean)
# -------------------------------------------------------------
print("--- 1) LIST AS ARRAY ---")
cars = ["BMW", "Volvo", "Ford"]
print("cars          ->", cars)
print("cars[0]       ->", cars[0])
print("cars[-1]      ->", cars[-1])
print("len()         ->", len(cars))
cars[0] = "Audi"
print("assign        ->", cars)
cars.append("Tesla")
print("append        ->", cars)
cars.insert(1, "Kia")
print("insert        ->", cars)
cars.pop(1)
print("pop(1)        ->", cars)
cars.remove("Ford")
print("remove        ->", cars)
for c in cars:
    print("  loop ->", c, end="")
print()
print("mixed types OK->", [1, "two", 3.0, [4]])       # a list doesn't care


# -------------------------------------------------------------
# 2) array.array — the real typed array
# -------------------------------------------------------------
print("\n--- 2) array.array ---")
a = array("i", [10, 20, 30, 40])          # 'i' = signed int
print("array         ->", a)
print("type          ->", type(a))
print("typecode      ->", a.typecode)
print("itemsize      ->", a.itemsize, "bytes per item")
print("as a list     ->", a.tolist())

# EVERY item must match the typecode
try:
    a.append("hello")
except TypeError as e:
    print("wrong type    -> TypeError:", e)
try:
    array("i", [1.5])
except TypeError as e:
    print("float into i  -> TypeError:", e)


# -------------------------------------------------------------
# 3) TYPECODES
# -------------------------------------------------------------
print("\n--- 3) TYPECODES ---")
#   'b'/'B'  signed/unsigned char    1 byte
#   'h'/'H'  short                   2 bytes
#   'i'/'I'  int                     2 or 4 bytes
#   'l'/'L'  long                    4 or 8 bytes
#   'q'/'Q'  long long               8 bytes
#   'f'      float                   4 bytes
#   'd'      double                  8 bytes
#   'u'      unicode char            2 or 4 bytes
for code in "bhilqfd":
    sample = array(code, [1])
    print("  '%s' -> %d bytes/item" % (code, sample.itemsize))
print("floats        ->", array("d", [1.5, 2.5]))
print("small ints    ->", array("b", [1, 2, 3]))
try:
    array("b", [200])
except OverflowError as e:
    print("overflow      -> OverflowError:", e)


# -------------------------------------------------------------
# 4) ALL array METHODS
# -------------------------------------------------------------
print("\n--- 4) METHODS ---")
a = array("i", [10, 20, 30])
a.append(40)
print("append(40)    ->", a)
a.extend([50, 60])
print("extend        ->", a)
a.insert(0, 5)
print("insert(0, 5)  ->", a)
print("pop()         ->", a.pop(), "| now:", a)
print("pop(0)        ->", a.pop(0), "| now:", a)
a.remove(20)
print("remove(20)    ->", a)
print("index(30)     ->", a.index(30))
print("count(30)     ->", a.count(30))
a.reverse()
print("reverse()     ->", a)
a.fromlist([70, 80])
print("fromlist      ->", a)
print("tolist()      ->", a.tolist())
print("tobytes()     ->", a.tobytes()[:8], "...")
b2 = array("i")
b2.frombytes(a.tobytes())
print("frombytes     ->", b2)
print("buffer_info   ->", a.buffer_info(), "(memory address, item count)")
print("byteswap      -> flips endianness (used for binary file I/O)")


# -------------------------------------------------------------
# 5) OPERATORS & SLICING (same as lists)
# -------------------------------------------------------------
print("\n--- 5) OPERATORS ---")
x = array("i", [1, 2, 3])
y = array("i", [4, 5])
print("concat +      ->", x + y)
print("repeat *      ->", x * 2)
print("slice         ->", x[1:])
print("in            ->", 2 in x)
print("len/min/max   ->", len(x), min(x), max(x))
print("sum           ->", sum(x))
print("sorted        ->", sorted(array("i", [3, 1, 2])))   # returns a LIST
print("comprehension ->", array("i", [n * 2 for n in x]))
print("== compares   ->", array("i", [1, 2]) == array("i", [1, 2]))
try:
    x + [9]
except TypeError as e:
    print("array + list  -> TypeError:", e)


# -------------------------------------------------------------
# 6) WHY BOTHER? — MEMORY
# -------------------------------------------------------------
print("\n--- 6) MEMORY ---")
n = 10000
py_list = list(range(n))
py_array = array("i", range(n))
print("list  bytes   ->", sys.getsizeof(py_list), "(+ each int object separately!)")
print("array bytes   ->", sys.getsizeof(py_array))
print("array stores raw values; a list stores POINTERS to int objects")
print("ratio         -> roughly %.1fx smaller" %
      (sys.getsizeof(py_list) / sys.getsizeof(py_array)))
print("=> use array only for large, homogeneous numeric data or binary I/O")


# -------------------------------------------------------------
# 7) 2D "ARRAYS" WITH LISTS
# -------------------------------------------------------------
print("\n--- 7) 2D ---")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("matrix        ->", matrix)
print("matrix[1][2]  ->", matrix[1][2])
print("row 0         ->", matrix[0])
print("column 1      ->", [row[1] for row in matrix])
print("transpose     ->", [list(t) for t in zip(*matrix)])
print("flatten       ->", [v for row in matrix for v in row])
print("diagonal      ->", [matrix[i][i] for i in range(3)])
print("row sums      ->", [sum(row) for row in matrix])
print("total         ->", sum(sum(row) for row in matrix))

# THE TRAP — * copies the reference to the SAME row
bad = [[0] * 3] * 3
bad[0][0] = 99
print("bad init      ->", bad, "<- all rows changed!")
good = [[0] * 3 for _ in range(3)]
good[0][0] = 99
print("good init     ->", good)


# -------------------------------------------------------------
# 8) COMMON ARRAY ALGORITHMS
# -------------------------------------------------------------
print("\n--- 8) ALGORITHMS ---")
data = [64, 25, 12, 22, 11]
print("data          ->", data)
print("max / min     ->", max(data), min(data))
print("sum / avg     ->", sum(data), round(sum(data) / len(data), 2))
print("sorted        ->", sorted(data))
print("reverse       ->", data[::-1])
print("2nd largest   ->", sorted(data)[-2])
print("search        ->", data.index(22) if 22 in data else -1)
print("evens         ->", [v for v in data if v % 2 == 0])
print("doubled       ->", [v * 2 for v in data])
print("running sum   ->", [sum(data[:i + 1]) for i in range(len(data))])
print("rotate left 2 ->", data[2:] + data[:2])
print("dedupe        ->", list(dict.fromkeys([1, 2, 2, 3, 1])))
print("pairs summing ->", [(p, q) for i, p in enumerate(data)
                          for q in data[i + 1:] if p + q == 36])
print("chunks of 2   ->", [data[i:i + 2] for i in range(0, len(data), 2)])


# -------------------------------------------------------------
# 9) list vs array vs numpy
# -------------------------------------------------------------
print("\n--- 9) COMPARISON ---")
#                 list              array.array          numpy.ndarray
#   import        built-in          from array import    pip install numpy
#   types         any, mixed        one numeric type     one dtype
#   memory        large             compact              compact
#   math on all   loops needed      loops needed         VECTORISED (a * 2)
#   multi-dim     nested lists      no                   native
#   use it for    everything        binary I/O, memory   real numeric work
print("list        -> default choice, flexible, what 99% of code uses")
print("array.array -> compact numeric buffer, binary files, no math speedup")
print("numpy       -> vectorised math:  arr * 2  works on the WHOLE array")
print("plain list  -> [v * 2 for v in data] =", [v * 2 for v in data])


# -------------------------------------------------------------
# 10) CHEAT SHEET
# -------------------------------------------------------------
#   list          [1, 2, 3]                 any type, all list methods
#   array('i',[]) typed, compact            append/extend/insert/pop/remove/
#                                           index/count/reverse/tolist/fromlist/
#                                           tobytes/frombytes/buffer_info/byteswap
#   2D            [[0]*c for _ in range(r)] NEVER [[0]*c]*r
#   transpose     zip(*matrix)
#   flatten       [v for row in m for v in row]
print("\n--- 10) DONE ---")
print("final array   ->", a)
print("final matrix  ->", matrix)
