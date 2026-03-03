"""
PYTHON MATH MODULE - COMPLETE GUIDE
====================================

The math module is part of Python's standard library (stdlib) and provides
access to mathematical functions defined by the C standard. It is always
available — no installation needed.

Key Characteristics:
- Works exclusively with real numbers (float/int)
- For complex numbers, use the 'cmath' module
- For arrays and vectorized operations, use NumPy

Common Uses:
- Trigonometric calculations (angles, circles, physics)
- Logarithmic and exponential functions
- Combinatorics (factorials, combinations, permutations)
- Working with mathematical constants (π, e, τ)
- Checking for special float values (NaN, Inf)
- High-precision floating point operations
"""

import math


def main():

    print("=== PYTHON MATH MODULE - COMPLETE GUIDE ===\n")

    # ------------------------------------------------------------------
    # 1. IMPORTING
    # ------------------------------------------------------------------
    print("1. IMPORTING:")
    print("-" * 70)
    print("import math                     # recommended — keeps namespace clean")
    print("from math import sqrt, pi       # import specific functions")
    print("from math import *              # NOT recommended — pollutes namespace")
    print()
    print("💡 Always use 'import math' and access via 'math.function()'")
    print("   This makes it clear where each function comes from.")
    print()


    # ------------------------------------------------------------------
    # 2. CONSTANTS
    # ------------------------------------------------------------------
    print("2. CONSTANTS:")
    print("-" * 70)

    print(f"math.pi  = {math.pi}")     # 3.141592653589793
    print(f"math.e   = {math.e}")      # 2.718281828459045
    print(f"math.tau = {math.tau}")    # 6.283185307179586  (τ = 2π)
    print(f"math.inf = {math.inf}")    # inf
    print(f"-math.inf= {-math.inf}")   # -inf
    print(f"math.nan = {math.nan}")    # nan

    print()
    print("💡 math.tau = 2 * math.pi   →  useful for full-circle calculations")
    print("💡 math.inf is equivalent to float('inf')")
    print("💡 NaN ≠ NaN   →  any comparison with nan is always False!")
    print()

    # Practical example
    radius = 5
    area      = math.pi * radius ** 2
    perimeter = math.tau * radius          # 2π × r

    print(f"Circle (r=5):  area = {area:.4f},  perimeter = {perimeter:.4f}")
    print()


    # ------------------------------------------------------------------
    # 3. ROUNDING FUNCTIONS
    # ------------------------------------------------------------------
    print("3. ROUNDING FUNCTIONS:")
    print("-" * 70)

    x = 4.7
    y = -4.7

    print(f"Value:          x = {x},  y = {y}")
    print(f"math.floor(x) = {math.floor(x)}   → always rounds DOWN (toward -∞)")
    print(f"math.floor(y) = {math.floor(y)}  → -5, NOT -4! (more negative)")
    print(f"math.ceil(x)  = {math.ceil(x)}   → always rounds UP (toward +∞)")
    print(f"math.ceil(y)  = {math.ceil(y)}   → -4, NOT -5! (less negative)")
    print(f"math.trunc(x) = {math.trunc(x)}   → removes decimal part (toward 0)")
    print(f"math.trunc(y) = {math.trunc(y)}   → -4, NOT -5! (always toward 0)")
    print(f"round(x)      = {round(x)}   → Python builtin (banker's rounding)")

    print()
    print("⚠️  floor(-4.7) = -5, NOT -4!")
    print("   'Down' means toward -∞, not toward zero.")
    print("   Use math.trunc() if you want truncation toward zero.")
    print()

    # Quick comparison table
    print("  Value  | floor | ceil | trunc | round")
    print("  -------|-------|------|-------|------")
    for val in [4.2, 4.5, 4.7, -4.2, -4.5, -4.7]:
        print(f"  {val:5.1f}  |  {math.floor(val):3d}  |  {math.ceil(val):3d} |  {math.trunc(val):3d}  |  {round(val):3d}")
    print()


    # ------------------------------------------------------------------
    # 4. POWERS AND ROOTS
    # ------------------------------------------------------------------
    print("4. POWERS AND ROOTS:")
    print("-" * 70)

    print("--- Square root ---")
    print(f"math.sqrt(25) = {math.sqrt(25)}")         # 5.0
    print(f"math.sqrt(2)  = {math.sqrt(2)}")          # 1.4142...

    print()
    print("--- Power: math.pow() vs ** operator ---")
    print(f"math.pow(2, 8) = {math.pow(2, 8)}     → always returns float")
    print(f"2 ** 8         = {2 ** 8}           → returns int (faster)")

    print()
    print("--- Arbitrary roots using pow ---")
    print(f"Cube root of 27:  math.pow(27, 1/3) = {math.pow(27, 1/3):.6f}")
    print(f"4th root of 16:   math.pow(16, 0.25) = {math.pow(16, 0.25)}")

    print()
    print("--- Exponential: e^x ---")
    print(f"math.exp(0) = {math.exp(0)}")             # 1.0
    print(f"math.exp(1) = {math.exp(1):.6f}")         # e
    print(f"math.exp(2) = {math.exp(2):.6f}")         # e²

    print()
    print("💡 math.pow() always returns float; use ** when you need an int.")
    print()


    # ------------------------------------------------------------------
    # 5. LOGARITHMS
    # ------------------------------------------------------------------
    print("5. LOGARITHMS:")
    print("-" * 70)

    print("--- Natural log (base e) ---")
    print(f"math.log(1)        = {math.log(1)}")          # 0.0
    print(f"math.log(math.e)   = {math.log(math.e)}")     # 1.0
    print(f"math.log(math.e**3)= {math.log(math.e**3)}")  # 3.0

    print()
    print("--- Log with specific base ---")
    print(f"math.log(100, 10)  = {math.log(100, 10)}")    # 2.0
    print(f"math.log(8, 2)     = {math.log(8, 2)}")       # 3.0

    print()
    print("--- Shortcuts for common bases (more precise!) ---")
    print(f"math.log10(1000)   = {math.log10(1000)}")     # 3.0
    print(f"math.log2(1024)    = {math.log2(1024)}")      # 10.0

    print()
    print("--- log1p(x) = log(1 + x) — more accurate when x ≈ 0 ---")
    print(f"math.log1p(0.0001) = {math.log1p(0.0001)}")
    print(f"math.log(1.0001)   = {math.log(1.0001)}")

    print()
    print("💡 Prefer math.log10() and math.log2() over math.log(x, 10/2)")
    print("   They are both faster and more numerically precise.")
    print()


    # ------------------------------------------------------------------
    # 6. TRIGONOMETRY
    # ------------------------------------------------------------------
    print("6. TRIGONOMETRY:")
    print("-" * 70)

    print("⚠️  ALL trig functions use RADIANS, not degrees!")
    print()

    print("--- Conversion ---")
    print(f"math.radians(180) = {math.radians(180):.6f}   → π")
    print(f"math.radians(90)  = {math.radians(90):.6f}   → π/2")
    print(f"math.degrees(math.pi)     = {math.degrees(math.pi)}")
    print(f"math.degrees(math.pi/2)   = {math.degrees(math.pi/2)}")

    print()
    print("--- Basic trig functions (argument in radians) ---")
    print(f"math.sin(math.pi/2) = {math.sin(math.pi/2)}")    # 1.0
    print(f"math.cos(0)         = {math.cos(0)}")            # 1.0
    print(f"math.tan(math.pi/4) = {math.tan(math.pi/4):.6f}")  # ≈ 1.0

    print()
    print("--- Inverse trig functions (return radians) ---")
    print(f"math.asin(1)        = {math.asin(1):.6f}  → π/2 = 90°")
    print(f"math.acos(1)        = {math.acos(1)}")           # 0.0
    print(f"math.atan(1)        = {math.atan(1):.6f}  → π/4 = 45°")

    print()
    print("--- atan2(y, x) — handles all quadrants correctly ---")
    print(f"math.atan2(1, 1)    = {math.degrees(math.atan2(1, 1)):.1f}°  →  45°")
    print(f"math.atan2(1, -1)   = {math.degrees(math.atan2(1, -1)):.1f}° →  135°")
    print(f"math.atan2(-1, -1)  = {math.degrees(math.atan2(-1, -1)):.1f}° → -135°")

    print()
    print("💡 Use math.atan2(y, x) instead of math.atan(y/x)")
    print("   atan2 handles all quadrants and avoids division by zero when x=0.")

    print()
    print("--- Hyperbolic functions ---")
    print(f"math.sinh(1) = {math.sinh(1):.6f}")
    print(f"math.cosh(1) = {math.cosh(1):.6f}")
    print(f"math.tanh(1) = {math.tanh(1):.6f}")
    print()

    # Practical: create degree-based wrappers
    def sind(degrees): return math.sin(math.radians(degrees))
    def cosd(degrees): return math.cos(math.radians(degrees))

    print("--- Practical wrapper functions ---")
    print("def sind(degrees): return math.sin(math.radians(degrees))")
    print(f"sind(30) = {sind(30):.1f},  cosd(60) = {cosd(60):.1f}")
    print()


    # ------------------------------------------------------------------
    # 7. COMBINATORICS
    # ------------------------------------------------------------------
    print("7. COMBINATORICS:")
    print("-" * 70)

    print("--- Factorial: n! = n × (n-1) × ... × 1 ---")
    print(f"math.factorial(0)  = {math.factorial(0)}")
    print(f"math.factorial(5)  = {math.factorial(5)}")     # 120
    print(f"math.factorial(10) = {math.factorial(10)}")    # 3628800

    print()
    print("--- Combinations C(n,k): 'choose k from n, order doesn't matter' ---")
    print(f"math.comb(5, 2)    = {math.comb(5, 2)}")      # 10
    print(f"math.comb(10, 3)   = {math.comb(10, 3)}")     # 120
    print(f"math.comb(52, 5)   = {math.comb(52, 5)}  → 5-card poker hands")

    print()
    print("--- Permutations P(n,k): 'arrange k from n, order matters' ---")
    print(f"math.perm(5, 2)    = {math.perm(5, 2)}")      # 20
    print(f"math.perm(10, 3)   = {math.perm(10, 3)}")     # 720

    print()
    n, k = 8, 3
    print(f"Relationship: perm(n,k) = comb(n,k) × k!")
    print(f"  perm({n},{k}) = {math.perm(n, k)}")
    print(f"  comb({n},{k}) × {k}! = {math.comb(n,k)} × {math.factorial(k)} = {math.comb(n,k) * math.factorial(k)}")

    print()
    print("--- GCD and LCM ---")
    print(f"math.gcd(48, 36)        = {math.gcd(48, 36)}")       # 12
    print(f"math.gcd(12, 8, 4)      = {math.gcd(12, 8, 4)}")    # 4  (Python 3.9+)
    print(f"math.lcm(4, 6)          = {math.lcm(4, 6)}")         # 12
    print(f"math.lcm(3, 4, 5)       = {math.lcm(3, 4, 5)}")     # 60 (Python 3.9+)

    print()
    print("💡 comb and perm require Python 3.8+")
    print("💡 Multi-argument gcd and lcm require Python 3.9+")
    print()


    # ------------------------------------------------------------------
    # 8. FLOATING POINT PRECISION
    # ------------------------------------------------------------------
    print("8. FLOATING POINT PRECISION:")
    print("-" * 70)

    print("--- The classic float problem ---")
    print(f"0.1 + 0.2              = {0.1 + 0.2}")          # 0.30000000000000004
    print(f"0.1 + 0.2 == 0.3       = {0.1 + 0.2 == 0.3}")  # False!

    print()
    print("--- Solution: math.isclose() ---")
    print(f"math.isclose(0.1+0.2, 0.3)                = {math.isclose(0.1+0.2, 0.3)}")
    print(f"math.isclose(0.1+0.2, 0.3, rel_tol=1e-9) = {math.isclose(0.1+0.2, 0.3, rel_tol=1e-9)}")
    print(f"math.isclose(1.0, 1.0000001, abs_tol=1e-5)= {math.isclose(1.0, 1.0000001, abs_tol=1e-5)}")

    print()
    print("--- math.fsum() — high-precision summation ---")
    numbers = [0.1] * 10
    print(f"sum([0.1] * 10)        = {sum(numbers)}")        # 0.9999999999999999
    print(f"math.fsum([0.1] * 10)  = {math.fsum(numbers)}")  # 1.0  ✅

    print()
    print("⚠️  NEVER compare floats with ==   →   always use math.isclose()")
    print("💡 math.fsum() avoids rounding errors when summing many floats.")
    print()


    # ------------------------------------------------------------------
    # 9. SPECIAL VALUES (NaN, Infinity)
    # ------------------------------------------------------------------
    print("9. SPECIAL VALUES (NaN, Infinity):")
    print("-" * 70)

    print("--- Infinity ---")
    inf = math.inf
    print(f"math.isinf(math.inf)    = {math.isinf(inf)}")
    print(f"math.isinf(-math.inf)   = {math.isinf(-inf)}")
    print(f"math.isinf(1e308 * 10)  = {math.isinf(1e308 * 10)}")  # overflow

    print()
    print("--- NaN: Not a Number ---")
    nan = float('nan')
    print(f"math.isnan(nan)         = {math.isnan(nan)}")
    print(f"nan == nan              = {nan == nan}")   # False — NaN is never equal to itself!
    print(f"nan != nan              = {nan != nan}")   # True
    result = 0 * float('inf')
    print(f"0 * float('inf')        = {result}  → produces NaN")
    print(f"math.isnan(0 * inf)     = {math.isnan(result)}")

    print()
    print("--- math.isfinite() — check if normal finite number ---")
    print(f"math.isfinite(42)       = {math.isfinite(42)}")
    print(f"math.isfinite(math.inf) = {math.isfinite(math.inf)}")
    print(f"math.isfinite(math.nan) = {math.isfinite(math.nan)}")

    print()
    print("💡 Always validate before computing: use math.isfinite() defensively.")
    print()

    def safe_sqrt(x):
        if not math.isfinite(x) or x < 0:
            return None
        return math.sqrt(x)

    print("--- Defensive computation example ---")
    print(f"safe_sqrt(25)        = {safe_sqrt(25)}")
    print(f"safe_sqrt(-1)        = {safe_sqrt(-1)}")
    print(f"safe_sqrt(math.inf)  = {safe_sqrt(math.inf)}")
    print()


    # ------------------------------------------------------------------
    # 10. PRACTICAL EXAMPLES
    # ------------------------------------------------------------------
    print("10. PRACTICAL EXAMPLES:")
    print("-" * 70)

    # Example 1: Geometry
    print("--- Example 1: Circle geometry ---")

    class Circle:
        def __init__(self, radius):
            self.radius = radius

        def area(self):
            return math.pi * self.radius ** 2

        def perimeter(self):
            return math.tau * self.radius  # tau = 2π

        def arc_length(self, angle_degrees):
            return self.radius * math.radians(angle_degrees)

    c = Circle(5)
    print(f"  Area:         {c.area():.4f}")
    print(f"  Perimeter:    {c.perimeter():.4f}")
    print(f"  Arc (90°):    {c.arc_length(90):.4f}")
    print()

    # Example 2: Compound interest
    print("--- Example 2: Compound interest (continuous) ---")
    print("  Formula: M = C × e^(r × t)")

    def compound_interest(capital, annual_rate, years):
        return capital * math.exp(annual_rate * years)

    def years_to_double(rate):
        return math.log(2) / rate  # Rule of 70 (exact version)

    capital = 10_000
    rate    = 0.05

    for years in [1, 5, 10, 20]:
        amount = compound_interest(capital, rate, years)
        print(f"  After {years:2d} years: €{amount:10,.2f}")

    print(f"  Years to double at 5%: {years_to_double(0.05):.1f}")
    print()

    # Example 3: Combinatorics — lottery probability
    print("--- Example 3: Lottery probability ---")
    combos = math.comb(50, 5) * math.comb(12, 2)
    print(f"  EuroMillions combinations: {combos:,}")
    print(f"  Probability: 1 in {combos:,}")
    print()

    # Example 4: Sigmoid function (machine learning)
    print("--- Example 4: Sigmoid activation function ---")

    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    for val in [-5, -1, 0, 1, 5]:
        print(f"  sigmoid({val:+2d}) = {sigmoid(val):.4f}")
    print()


    # ------------------------------------------------------------------
    # 11. COMMON MISTAKES
    # ------------------------------------------------------------------
    print("11. COMMON MISTAKES:")
    print("-" * 70)

    print("--- Mistake 1: Degrees vs Radians ---")
    print(f"  math.sin(90)              = {math.sin(90):.4f}  ← WRONG (expects radians!)")
    print(f"  math.sin(math.radians(90))= {math.sin(math.radians(90)):.1f}    ← CORRECT")

    print()
    print("--- Mistake 2: Comparing floats with == ---")
    result = math.sqrt(2) ** 2
    print(f"  math.sqrt(2) ** 2         = {result}")
    print(f"  math.sqrt(2)**2 == 2      = {result == 2}  ← WRONG approach")
    print(f"  math.isclose(result, 2)   = {math.isclose(result, 2)}  ← CORRECT")

    print()
    print("--- Mistake 3: math.log(0) raises ValueError ---")
    print("  math.log(0)    → ValueError: math domain error")
    print("  math.sqrt(-1)  → ValueError: math domain error")
    print("  math.log(-1)   → ValueError: math domain error")
    print("  → Always validate inputs before computing!")

    print()
    print("--- Mistake 4: math doesn't work with complex numbers ---")
    print("  math.sqrt(-1)  → ValueError!")
    print("  Use cmath.sqrt(-1) instead  →  1j")
    print()


    # ------------------------------------------------------------------
    # 12. math vs. Python BUILTINS
    # ------------------------------------------------------------------
    print("12. math vs. PYTHON BUILTINS:")
    print("-" * 70)
    print()
    print(f"  {'Operation':<20} {'Builtin':<25} {'math module':<30} {'Note'}")
    print(f"  {'-'*20} {'-'*25} {'-'*30} {'-'*35}")
    print(f"  {'Power':<20} {'2**10 → 1024 (int)':<25} {'math.pow(2,10) → 1024.0':<30} ** gives int; math.pow gives float")
    print(f"  {'Absolute value':<20} {'abs(-5) → 5':<25} {'math.fabs(-5) → 5.0':<30} abs works on complex; fabs only float")
    print(f"  {'Rounding':<20} {'round(4.5) → 4':<25} {'math.floor(4.5) → 4':<30} round uses banker's rounding")
    print(f"  {'Sum':<20} {'sum([0.1]*10)':<25} {'math.fsum([0.1]*10)':<30} fsum avoids float rounding errors")
    print()


    # ------------------------------------------------------------------
    # 13. QUICK REFERENCE TABLE
    # ------------------------------------------------------------------
    print("13. QUICK REFERENCE TABLE:")
    print("-" * 70)
    print()
    print(f"  {'Function':<28} {'Description':<38} {'Example'}")
    print(f"  {'-'*28} {'-'*38} {'-'*30}")

    ref = [
        # Constants
        ("math.pi",              "π = 3.14159...",                   "math.pi → 3.14159..."),
        ("math.e",               "Euler's number = 2.71828...",       "math.e  → 2.71828..."),
        ("math.tau",             "τ = 2π",                            "math.tau → 6.28318..."),
        ("math.inf",             "Positive infinity",                 "math.inf → inf"),
        ("math.nan",             "Not a Number",                      "math.nan → nan"),
        # Rounding
        ("math.floor(x)",        "Round down (toward -∞)",            "floor(4.7) → 4"),
        ("math.ceil(x)",         "Round up (toward +∞)",              "ceil(4.2)  → 5"),
        ("math.trunc(x)",        "Truncate toward zero",              "trunc(-4.9) → -4"),
        # Power & Roots
        ("math.sqrt(x)",         "Square root",                       "sqrt(25) → 5.0"),
        ("math.pow(x, y)",       "Power x^y (returns float)",         "pow(2, 10) → 1024.0"),
        ("math.exp(x)",          "e raised to x",                     "exp(1) → 2.71828..."),
        # Logarithms
        ("math.log(x[, base])",  "Natural log or log in base",        "log(100, 10) → 2.0"),
        ("math.log10(x)",        "Base-10 logarithm",                 "log10(1000) → 3.0"),
        ("math.log2(x)",         "Base-2 logarithm",                  "log2(8) → 3.0"),
        ("math.log1p(x)",        "log(1+x), precise near 0",          "log1p(0.0001) → 9.99...e-5"),
        # Trigonometry
        ("math.sin/cos/tan(x)",  "Trig functions (x in radians)",     "sin(pi/2) → 1.0"),
        ("math.asin/acos/atan(x)","Inverse trig (returns radians)",   "asin(1) → 1.5707..."),
        ("math.atan2(y, x)",     "Angle from (x,y) — all quadrants",  "atan2(1,1) → 0.7853..."),
        ("math.radians(x)",      "Degrees → radians",                 "radians(180) → 3.14159"),
        ("math.degrees(x)",      "Radians → degrees",                 "degrees(pi) → 180.0"),
        # Combinatorics
        ("math.factorial(n)",    "n! (n must be integer ≥ 0)",        "factorial(5) → 120"),
        ("math.comb(n, k)",      "Combinations C(n,k)  [Py 3.8+]",    "comb(5, 2) → 10"),
        ("math.perm(n, k)",      "Permutations P(n,k)  [Py 3.8+]",    "perm(5, 2) → 20"),
        ("math.gcd(*args)",      "Greatest Common Divisor",           "gcd(48, 36) → 12"),
        ("math.lcm(*args)",      "Least Common Multiple  [Py 3.9+]",  "lcm(4, 6) → 12"),
        # Precision & Specials
        ("math.fsum(iterable)",  "High-precision sum",                "fsum([0.1]*10) → 1.0"),
        ("math.fabs(x)",         "Absolute value (float)",            "fabs(-5) → 5.0"),
        ("math.isclose(a, b)",   "Compare floats with tolerance",     "isclose(0.1+0.2, 0.3) → True"),
        ("math.isnan(x)",        "Check if NaN",                      "isnan(float('nan')) → True"),
        ("math.isinf(x)",        "Check if infinite",                 "isinf(math.inf) → True"),
        ("math.isfinite(x)",     "Check if normal finite number",     "isfinite(42) → True"),
    ]

    for func, desc, example in ref:
        print(f"  {func:<28} {desc:<38} {example}")

    print()


    # ------------------------------------------------------------------
    # 14. RELATED MODULES
    # ------------------------------------------------------------------
    print("14. RELATED MODULES:")
    print("-" * 70)
    print()
    print("  math     → real numbers (float)     → import math")
    print("  cmath    → complex numbers           → import cmath")
    print("  random   → random numbers            → import random")
    print("  decimal  → exact decimal arithmetic  → from decimal import Decimal")
    print("  fractions→ exact fractions           → from fractions import Fraction")
    print("  numpy    → arrays & vectorized ops   → import numpy as np   (3rd party)")
    print("  scipy    → scientific computing      → import scipy         (3rd party)")
    print()
    print("  💡 numpy replaces math for working with arrays and large datasets.")
    print("  💡 Use decimal.Decimal when exact decimal precision is required (e.g. money).")
    print()


main()


"""
SUMMARY — PYTHON math MODULE
=======================================================

CONSTANTS:
  math.pi     →  π = 3.141592653589793
  math.e      →  e = 2.718281828459045
  math.tau    →  τ = 2π = 6.283...
  math.inf    →  ∞ (positive infinity)
  math.nan    →  Not a Number

ROUNDING:
  math.floor(x)   →  round down (toward -∞)
  math.ceil(x)    →  round up (toward +∞)
  math.trunc(x)   →  truncate toward zero

POWERS / ROOTS / EXP:
  math.sqrt(x)        →  square root
  math.pow(x, y)      →  x^y as float (use ** for int)
  math.exp(x)         →  e^x

LOGARITHMS:
  math.log(x)         →  natural log
  math.log(x, base)   →  log in any base
  math.log10(x)       →  log base 10 (prefer over log(x,10))
  math.log2(x)        →  log base 2  (prefer over log(x,2))
  math.log1p(x)       →  log(1+x), precise for small x

TRIGONOMETRY (all in radians!):
  math.sin/cos/tan(x)       →  basic functions
  math.asin/acos/atan(x)    →  inverse functions
  math.atan2(y, x)          →  angle handling all quadrants
  math.radians(d)           →  degrees to radians
  math.degrees(r)           →  radians to degrees
  math.sinh/cosh/tanh(x)    →  hyperbolic functions

COMBINATORICS:
  math.factorial(n)   →  n!
  math.comb(n, k)     →  C(n,k)  [Python 3.8+]
  math.perm(n, k)     →  P(n,k)  [Python 3.8+]
  math.gcd(*args)     →  Greatest Common Divisor
  math.lcm(*args)     →  Least Common Multiple  [Python 3.9+]

PRECISION & SPECIALS:
  math.fsum(iter)     →  precise float sum
  math.fabs(x)        →  absolute value as float
  math.isclose(a, b)  →  compare floats with tolerance  ← ALWAYS use instead of ==
  math.isnan(x)       →  check for NaN
  math.isinf(x)       →  check for infinity
  math.isfinite(x)    →  check for normal finite number

COMMON PATTERNS:
  Check even:          (n % 2 == 0)
  Float comparison:    math.isclose(a, b)
  Precise sum:         math.fsum(values)
  Degrees to radians:  math.radians(angle)
  All quadrant angle:  math.atan2(y, x)

REMEMBER:
  "math works on real numbers only — use cmath for complex,
   numpy for arrays, decimal for exact decimal arithmetic."
"""