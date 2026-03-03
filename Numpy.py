"""
NUMPY - COMPLETE GUIDE
========================

NumPy (Numerical Python) is the foundational library for scientific computing
in Python. It provides a powerful N-dimensional array object and tools for
working with these arrays efficiently.

Key Characteristics:
- Arrays are stored in contiguous memory → much faster than Python lists
- Operations are vectorized → no need for explicit loops
- Broadcasting allows operations on arrays of different shapes
- Foundation for Pandas, Matplotlib, Scikit-learn, TensorFlow, and more

Installation:
  pip install numpy

Common Uses:
- Array and matrix operations
- Linear algebra (dot products, matrix inversion, eigenvalues)
- Statistical analysis (mean, std, percentiles)
- Data preprocessing for Machine Learning
- Random number generation
- Fourier transforms and signal processing
"""

import numpy as np


def main():

    print("=== NUMPY - COMPLETE GUIDE ===\n")


    # ------------------------------------------------------------------
    # 1. IMPORTING
    # ------------------------------------------------------------------
    print("1. IMPORTING:")
    print("-" * 70)
    print("import numpy as np          # standard alias — always use 'np'")
    print()
    print(f"NumPy version: {np.__version__}")
    print()


    # ------------------------------------------------------------------
    # 2. CREATING ARRAYS
    # ------------------------------------------------------------------
    print("2. CREATING ARRAYS:")
    print("-" * 70)

    print("--- From Python lists ---")
    a1 = np.array([1, 2, 3, 4, 5])
    a2 = np.array([[1, 2, 3],
                   [4, 5, 6]])
    a3 = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])

    print(f"1D array:  {a1}")
    print(f"2D array:\n{a2}")
    print(f"3D array shape: {a3.shape}")

    print()
    print("--- Specifying dtype ---")
    int_arr   = np.array([1, 2, 3], dtype=np.int32)
    float_arr = np.array([1, 2, 3], dtype=np.float64)
    bool_arr  = np.array([0, 1, 1, 0], dtype=bool)
    print(f"int32:   {int_arr}    dtype: {int_arr.dtype}")
    print(f"float64: {float_arr}  dtype: {float_arr.dtype}")
    print(f"bool:    {bool_arr}   dtype: {bool_arr.dtype}")

    print()
    print("--- Built-in array constructors ---")
    print(f"np.zeros((2, 3)):\n{np.zeros((2, 3))}")
    print(f"np.ones((2, 3)):\n{np.ones((2, 3))}")
    print(f"np.full((2, 3), 7):\n{np.full((2, 3), 7)}")
    print(f"np.eye(3):\n{np.eye(3)}")
    print(f"np.arange(0, 10, 2):    {np.arange(0, 10, 2)}")
    print(f"np.linspace(0, 1, 5):   {np.linspace(0, 1, 5)}")
    print(f"np.logspace(0, 3, 4):   {np.logspace(0, 3, 4)}")
    print(f"np.empty((2, 2)):       (uninitialized — fast allocation)")

    print()
    print("💡 np.arange(start, stop, step)  →  like range(), but returns array")
    print("💡 np.linspace(start, stop, n)   →  n evenly spaced points (inclusive)")
    print()


    # ------------------------------------------------------------------
    # 3. ARRAY ATTRIBUTES
    # ------------------------------------------------------------------
    print("3. ARRAY ATTRIBUTES:")
    print("-" * 70)

    arr = np.array([[1, 2, 3],
                    [4, 5, 6]])

    print(f"Array:\n{arr}")
    print(f"  arr.shape   = {arr.shape}      → (rows, cols)")
    print(f"  arr.ndim    = {arr.ndim}           → number of dimensions")
    print(f"  arr.size    = {arr.size}           → total number of elements")
    print(f"  arr.dtype   = {arr.dtype}       → data type of elements")
    print(f"  arr.itemsize= {arr.itemsize}           → bytes per element")
    print(f"  arr.nbytes  = {arr.nbytes}          → total bytes in memory")
    print()
    print("💡 Understanding shape is critical:")
    print("   (3,)      → 1D array with 3 elements")
    print("   (3, 1)    → 2D column vector: 3 rows, 1 col")
    print("   (1, 3)    → 2D row vector: 1 row, 3 cols")
    print("   (3, 4, 5) → 3D array: 3 'blocks' of 4×5 matrices")
    print()


    # ------------------------------------------------------------------
    # 4. DATA TYPES (dtype)
    # ------------------------------------------------------------------
    print("4. DATA TYPES (dtype):")
    print("-" * 70)

    print(f"  {'dtype':<15} {'Description':<35} {'Range / Precision'}")
    print(f"  {'-'*15} {'-'*35} {'-'*30}")
    print(f"  {'np.int8':<15} {'8-bit signed integer':<35} -128 to 127")
    print(f"  {'np.int16':<15} {'16-bit signed integer':<35} -32768 to 32767")
    print(f"  {'np.int32':<15} {'32-bit signed integer':<35} -2.1B to 2.1B")
    print(f"  {'np.int64':<15} {'64-bit signed integer (default)':<35} very large range")
    print(f"  {'np.uint8':<15} {'8-bit unsigned integer':<35} 0 to 255  (images!)")
    print(f"  {'np.float32':<15} {'32-bit float':<35} ~7 decimal digits")
    print(f"  {'np.float64':<15} {'64-bit float (default)':<35} ~15 decimal digits")
    print(f"  {'np.complex128':<15} {'128-bit complex':<35} real + imaginary")
    print(f"  {'np.bool_':<15} {'Boolean':<35} True / False")

    print()
    print("--- Type conversion ---")
    arr = np.array([1.7, 2.3, 3.9])
    print(f"Original (float64): {arr}")
    print(f"As int32:           {arr.astype(np.int32)}  ← truncates, doesn't round!")
    print(f"As bool:            {arr.astype(bool)}")

    print()
    print("💡 Use float32 instead of float64 in ML to halve memory usage.")
    print("💡 Use uint8 for image pixel data (0-255).")
    print()


    # ------------------------------------------------------------------
    # 5. INDEXING AND SLICING
    # ------------------------------------------------------------------
    print("5. INDEXING AND SLICING:")
    print("-" * 70)

    arr = np.array([10, 20, 30, 40, 50, 60])

    print("--- 1D Indexing ---")
    print(f"arr = {arr}")
    print(f"arr[0]   = {arr[0]}    → first element")
    print(f"arr[-1]  = {arr[-1]}    → last element")
    print(f"arr[1:4] = {arr[1:4]}  → slice [start:stop) (stop excluded)")
    print(f"arr[::2] = {arr[::2]}  → every 2nd element")
    print(f"arr[::-1]= {arr[::-1]}  → reversed")

    print()
    print("--- 2D Indexing ---")
    m = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    print(f"Matrix:\n{m}")
    print(f"m[0, 1]  = {m[0, 1]}   → row 0, col 1")
    print(f"m[1, :]  = {m[1, :]}  → entire row 1")
    print(f"m[:, 2]  = {m[:, 2]}  → entire col 2")
    print(f"m[0:2, 1:3]:\n{m[0:2, 1:3]}  → submatrix")

    print()
    print("--- Boolean Indexing (very important for data filtering!) ---")
    arr = np.array([10, 25, 3, 47, 8, 36])
    mask = arr > 20
    print(f"arr         = {arr}")
    print(f"arr > 20    = {mask}")
    print(f"arr[arr>20] = {arr[arr > 20]}  → filter: only values > 20")
    print(f"arr[(arr>10) & (arr<40)] = {arr[(arr > 10) & (arr < 40)]}")

    print()
    print("--- Fancy Indexing ---")
    arr = np.array([10, 20, 30, 40, 50])
    indices = [0, 2, 4]
    print(f"arr[[0, 2, 4]] = {arr[indices]}  → select by index list")

    print()
    print("⚠️  NumPy slices are VIEWS, not copies!")
    print("   Modifying a slice modifies the original array.")
    print("   Use arr[1:3].copy() to get an independent copy.")
    print()

    # Demonstrate view vs copy
    original = np.array([1, 2, 3, 4, 5])
    view     = original[1:3]         # view — shares memory
    copy     = original[1:3].copy()  # independent copy
    view[0]  = 99
    print(f"After modifying view[0] = 99:")
    print(f"  original = {original}  ← also changed!")
    print(f"  copy     = {copy}        ← unchanged")
    print()


    # ------------------------------------------------------------------
    # 6. RESHAPING AND MANIPULATION
    # ------------------------------------------------------------------
    print("6. RESHAPING AND MANIPULATION:")
    print("-" * 70)

    arr = np.arange(12)
    print(f"Original: {arr}  shape={arr.shape}")

    print()
    print("--- reshape ---")
    r1 = arr.reshape(3, 4)
    r2 = arr.reshape(2, 2, 3)
    print(f"reshape(3, 4):\n{r1}")
    print(f"reshape(2, 2, 3) shape: {r2.shape}")
    print(f"reshape(3, -1):  shape: {arr.reshape(3, -1).shape}  ← -1 means 'figure it out'")

    print()
    print("--- flatten vs ravel ---")
    m = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"flatten(): {m.flatten()}    ← always returns a copy")
    print(f"ravel():   {m.ravel()}    ← returns a view when possible (faster)")

    print()
    print("--- transpose ---")
    m = np.array([[1, 2, 3],
                  [4, 5, 6]])
    print(f"Original shape: {m.shape}")
    print(f"Transposed:\n{m.T}  shape: {m.T.shape}")

    print()
    print("--- squeeze and expand_dims ---")
    a = np.array([[[1, 2, 3]]])  # shape (1, 1, 3)
    print(f"Original shape: {a.shape}")
    print(f"np.squeeze(a) shape: {np.squeeze(a).shape}  ← removes dimensions of size 1")
    b = np.array([1, 2, 3])      # shape (3,)
    print(f"np.expand_dims(b, 0) shape: {np.expand_dims(b, 0).shape}  ← adds dimension at axis 0")
    print(f"np.expand_dims(b, 1) shape: {np.expand_dims(b, 1).shape}  ← adds dimension at axis 1")

    print()
    print("--- Stacking and splitting ---")
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    print(f"np.concatenate([a, b]): {np.concatenate([a, b])}")
    print(f"np.vstack([a, b]):\n{np.vstack([a, b])}")
    print(f"np.hstack([a, b]):  {np.hstack([a, b])}")

    m = np.arange(12).reshape(3, 4)
    parts = np.split(m, 3, axis=0)
    print(f"np.split(m, 3, axis=0) → {len(parts)} arrays of shape {parts[0].shape}")
    print()


    # ------------------------------------------------------------------
    # 7. VECTORIZED OPERATIONS
    # ------------------------------------------------------------------
    print("7. VECTORIZED OPERATIONS (Element-wise):")
    print("-" * 70)

    a = np.array([1, 2, 3, 4])
    b = np.array([10, 20, 30, 40])

    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print(f"a + b    = {a + b}          → element-wise addition")
    print(f"a - b    = {a - b}       → element-wise subtraction")
    print(f"a * b    = {a * b}      → element-wise multiplication")
    print(f"a / b    = {a / b}  → element-wise division")
    print(f"a ** 2   = {a ** 2}           → element-wise power")
    print(f"a % 3    = {a % 3}           → element-wise modulo")
    print(f"a // 3   = {a // 3}           → element-wise floor division")

    print()
    print("--- Scalar operations (broadcast automatically) ---")
    print(f"a + 100  = {a + 100}")
    print(f"a * 2    = {a * 2}")
    print(f"a > 2    = {a > 2}")

    print()
    print("--- Comparison operators ---")
    print(f"a == b   = {a == b}")
    print(f"a < 3    = {a < 3}")
    print(f"np.array_equal(a, a) = {np.array_equal(a, a)}")

    print()
    print("--- Universal functions (ufuncs) ---")
    arr = np.array([1.0, 4.0, 9.0, 16.0])
    print(f"np.sqrt(arr)  = {np.sqrt(arr)}")
    print(f"np.abs([-1,-2,3]) = {np.abs([-1,-2,3])}")
    print(f"np.exp([0,1,2])   = {np.exp([0,1,2]).round(4)}")
    print(f"np.log([1,np.e])  = {np.log([1, np.e])}")
    print(f"np.sin(np.linspace(0, np.pi, 4)).round(4) = {np.sin(np.linspace(0, np.pi, 4)).round(4)}")

    print()
    print("💡 Vectorized operations are 10x-100x faster than Python for-loops.")
    print("   Always prefer arr * 2 over [x * 2 for x in arr]")
    print()


    # ------------------------------------------------------------------
    # 8. BROADCASTING
    # ------------------------------------------------------------------
    print("8. BROADCASTING:")
    print("-" * 70)

    print("Broadcasting allows operations between arrays of different shapes.")
    print()

    # Example 1
    m = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    row = np.array([10, 20, 30])
    print(f"Matrix (3x3) + row (3,):")
    print(f"  {row}  is broadcast across each row")
    print(f"  Result:\n{m + row}")

    print()
    # Example 2
    col = np.array([[10], [20], [30]])  # shape (3, 1)
    print(f"Matrix (3x3) + column (3,1):")
    print(f"  Result:\n{m + col}")

    print()
    print("Broadcasting rules:")
    print("  1. If arrays have different ndim, prepend 1s to the smaller shape")
    print("     (3,)  →  (1, 3)")
    print("  2. Dimensions with size 1 are stretched to match the other array")
    print("     (1, 3) + (3, 1)  →  both become (3, 3)")
    print("  3. If neither dimension is 1 and they differ → ERROR")
    print()
    print("  (3, 4) + (4,)    →  OK  →  (3, 4)")
    print("  (3, 4) + (3, 1)  →  OK  →  (3, 4)")
    print("  (3, 4) + (3,)    →  ERROR: shapes (3,4) and (3,) are incompatible")
    print()


    # ------------------------------------------------------------------
    # 9. AGGREGATE FUNCTIONS
    # ------------------------------------------------------------------
    print("9. AGGREGATE FUNCTIONS:")
    print("-" * 70)

    m = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

    print(f"Matrix:\n{m}\n")
    print(f"np.sum(m)          = {np.sum(m)}         → sum of ALL elements")
    print(f"np.sum(m, axis=0)  = {np.sum(m, axis=0)}  → sum along columns (collapse rows)")
    print(f"np.sum(m, axis=1)  = {np.sum(m, axis=1)}  → sum along rows (collapse cols)")
    print()
    print(f"np.mean(m)         = {np.mean(m)}")
    print(f"np.median(m)       = {np.median(m)}")
    print(f"np.std(m)          = {np.std(m):.4f}")
    print(f"np.var(m)          = {np.var(m):.4f}")
    print(f"np.min(m)          = {np.min(m)}")
    print(f"np.max(m)          = {np.max(m)}")
    print(f"np.argmin(m)       = {np.argmin(m)}         → flat index of min element")
    print(f"np.argmax(m)       = {np.argmax(m)}         → flat index of max element")
    print(f"np.cumsum(m.flatten()) = {np.cumsum(m.flatten())}")
    print(f"np.prod([1,2,3,4]) = {np.prod([1,2,3,4])}")

    print()
    print("💡 axis=0 collapses ROWS   → result has shape of one row")
    print("   axis=1 collapses COLS   → result has shape of one column")
    print("   axis=None (default)     → operates on ALL elements")
    print()


    # ------------------------------------------------------------------
    # 10. LINEAR ALGEBRA
    # ------------------------------------------------------------------
    print("10. LINEAR ALGEBRA (np.linalg):")
    print("-" * 70)

    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])

    print(f"A:\n{A}")
    print(f"B:\n{B}")
    print()

    print("--- Matrix multiplication ---")
    print(f"A @ B  (matrix product):\n{A @ B}")
    print(f"np.dot(A, B):\n{np.dot(A, B)}")
    print(f"A * B  (element-wise — NOT matrix multiply):\n{A * B}")

    print()
    print("--- Common linalg operations ---")
    print(f"np.linalg.det(A)       = {np.linalg.det(A):.1f}         → determinant")
    print(f"np.linalg.inv(A):\n{np.linalg.inv(A)}  → inverse matrix")
    print(f"np.linalg.matrix_rank(A) = {np.linalg.matrix_rank(A)}")

    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"np.linalg.eig(A):")
    print(f"  eigenvalues:  {eigenvalues.round(4)}")
    print(f"  eigenvectors:\n{eigenvectors.round(4)}")

    print()
    print("--- Solving linear systems ---")
    # Solve: Ax = b
    A_sys = np.array([[2, 1], [1, 3]], dtype=float)
    b_sys = np.array([5, 10], dtype=float)
    x = np.linalg.solve(A_sys, b_sys)
    print(f"Solve: 2x + y = 5, x + 3y = 10")
    print(f"  Solution x = {x}")
    print(f"  Verification A @ x = {A_sys @ x}  (should be {b_sys})")

    print()
    print("--- Norms ---")
    v = np.array([3.0, 4.0])
    print(f"Vector: {v}")
    print(f"L2 norm (Euclidean): {np.linalg.norm(v)}")       # 5.0
    print(f"L1 norm (Manhattan): {np.linalg.norm(v, ord=1)}")  # 7.0

    print()
    print("--- SVD (Singular Value Decomposition) ---")
    print("U, S, Vt = np.linalg.svd(A)  → used in PCA, recommender systems")
    U, S, Vt = np.linalg.svd(A)
    print(f"  Singular values: {S.round(4)}")
    print()

    print("⚠️  A @ B is matrix multiplication;  A * B is element-wise!")
    print("💡 np.linalg.solve(A, b) is more stable than np.dot(inv(A), b)")
    print()


    # ------------------------------------------------------------------
    # 11. RANDOM MODULE
    # ------------------------------------------------------------------
    print("11. RANDOM MODULE (np.random):")
    print("-" * 70)

    rng = np.random.default_rng(seed=42)   # modern, reproducible way

    print("--- Recommended: use np.random.default_rng(seed) ---")
    print(f"rng = np.random.default_rng(seed=42)  ← always set seed for reproducibility")
    print()

    print("--- Generating random arrays ---")
    print(f"rng.random((2,3)):         uniform [0,1)\n{rng.random((2,3)).round(4)}")
    print(f"rng.integers(0,10,(2,3)):  random ints [0,10)\n{rng.integers(0,10,(2,3))}")
    print(f"rng.normal(0, 1, (2,3)):   standard normal (μ=0, σ=1)\n{rng.normal(0,1,(2,3)).round(4)}")
    print(f"rng.uniform(5, 10, 4):     uniform [5,10): {rng.uniform(5,10,4).round(4)}")
    print(f"rng.choice([10,20,30,40], 3): {rng.choice([10,20,30,40], 3)}")

    print()
    print("--- Shuffling ---")
    arr = np.array([1, 2, 3, 4, 5])
    rng.shuffle(arr)
    print(f"After shuffle: {arr}")

    print()
    print("--- Legacy API (still widely used) ---")
    print("np.random.seed(42)           ← set global seed")
    print("np.random.rand(2, 3)         ← uniform [0,1)")
    print("np.random.randn(2, 3)        ← standard normal")
    print("np.random.randint(0, 10, 5)  ← random integers")

    print()
    print("💡 Always set a seed when reproducibility matters (ML experiments, tests).")
    print("💡 Prefer np.random.default_rng() over legacy np.random.seed() in new code.")
    print()


    # ------------------------------------------------------------------
    # 12. SORTING AND SEARCHING
    # ------------------------------------------------------------------
    print("12. SORTING AND SEARCHING:")
    print("-" * 70)

    arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

    print(f"arr = {arr}")
    print(f"np.sort(arr)         = {np.sort(arr)}  ← returns sorted copy")
    print(f"np.argsort(arr)      = {np.argsort(arr)}  ← indices that would sort arr")
    print(f"np.sort(arr)[::-1]   = {np.sort(arr)[::-1]}  ← descending order")

    print()
    print("--- Searching ---")
    arr2 = np.array([10, 25, 3, 47, 8, 36])
    print(f"arr2 = {arr2}")
    print(f"np.where(arr2 > 20)         = {np.where(arr2 > 20)}  ← indices where condition is True")
    print(f"np.where(arr2>20, 'big','small') = {np.where(arr2>20, 'big', 'small')}")
    print(f"np.searchsorted([1,3,5,7], 4) = {np.searchsorted([1,3,5,7], 4)}  ← insertion point")

    print()
    print("--- Min/Max positions ---")
    print(f"np.argmin(arr2) = {np.argmin(arr2)}  → index of minimum value ({arr2[np.argmin(arr2)]})")
    print(f"np.argmax(arr2) = {np.argmax(arr2)}  → index of maximum value ({arr2[np.argmax(arr2)]})")

    print()
    print("--- 2D sorting ---")
    m = np.array([[3, 1, 2], [6, 4, 5]])
    print(f"Matrix:\n{m}")
    print(f"np.sort(m, axis=1):\n{np.sort(m, axis=1)}  ← sort each row")
    print(f"np.sort(m, axis=0):\n{np.sort(m, axis=0)}  ← sort each column")
    print()


    # ------------------------------------------------------------------
    # 13. SET OPERATIONS
    # ------------------------------------------------------------------
    print("13. SET OPERATIONS:")
    print("-" * 70)

    a = np.array([1, 2, 3, 4, 5, 3, 2])
    b = np.array([3, 4, 5, 6, 7])

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"np.unique(a)            = {np.unique(a)}      ← sorted unique values")
    print(f"np.union1d(a, b)        = {np.union1d(a, b)}")
    print(f"np.intersect1d(a, b)    = {np.intersect1d(a, b)}")
    print(f"np.setdiff1d(a, b)      = {np.setdiff1d(a, b)}      ← in a but not b")
    print(f"np.isin(a, b)           = {np.isin(a, b)}  ← element-wise membership")
    print()

    # Unique with counts
    vals, counts = np.unique(a, return_counts=True)
    print(f"np.unique(a, return_counts=True):")
    for v, c in zip(vals, counts):
        print(f"  value {v}: appears {c} time(s)")
    print()


    # ------------------------------------------------------------------
    # 14. MISSING VALUES AND NaN
    # ------------------------------------------------------------------
    print("14. MISSING VALUES AND NaN:")
    print("-" * 70)

    arr = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])
    print(f"arr = {arr}")
    print(f"np.isnan(arr)           = {np.isnan(arr)}")
    print(f"np.sum(np.isnan(arr))   = {int(np.sum(np.isnan(arr)))}   → count NaNs")
    print(f"arr[~np.isnan(arr)]     = {arr[~np.isnan(arr)]}   → remove NaNs")

    print()
    print("--- NaN-safe aggregate functions ---")
    print(f"np.mean(arr)            = {np.mean(arr)}    ← NaN propagates!")
    print(f"np.nanmean(arr)         = {np.nanmean(arr)}    ← ignores NaN ✅")
    print(f"np.nansum(arr)          = {np.nansum(arr)}")
    print(f"np.nanstd(arr)          = {np.nanstd(arr):.4f}")
    print(f"np.nanmin(arr)          = {np.nanmin(arr)}")
    print(f"np.nanmax(arr)          = {np.nanmax(arr)}")

    print()
    print("--- Replacing NaN ---")
    arr_filled = np.where(np.isnan(arr), 0, arr)
    print(f"Replace NaN with 0: {arr_filled}")
    arr_filled_mean = np.where(np.isnan(arr), np.nanmean(arr), arr)
    print(f"Replace NaN with mean ({np.nanmean(arr)}): {arr_filled_mean}")

    print()
    print("💡 Always use nan-safe functions (nanmean, nansum, etc.) when data")
    print("   may contain missing values — regular mean()/sum() return NaN.")
    print()


    # ------------------------------------------------------------------
    # 15. PRACTICAL EXAMPLES FOR DATA & ML
    # ------------------------------------------------------------------
    print("15. PRACTICAL EXAMPLES FOR DATA & ML:")
    print("-" * 70)

    print("--- Example 1: Feature Normalization (Min-Max Scaling) ---")
    data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    normalized = (data - data.min()) / (data.max() - data.min())
    print(f"  Original:   {data}")
    print(f"  Normalized: {normalized}  → range [0, 1]")

    print()
    print("--- Example 2: Standardization (Z-score Scaling) ---")
    standardized = (data - data.mean()) / data.std()
    print(f"  Original:      {data}")
    print(f"  Standardized:  {standardized.round(4)}")
    print(f"  Mean: {standardized.mean():.10f}  (≈ 0)")
    print(f"  Std:  {standardized.std():.1f}  (= 1)")

    print()
    print("--- Example 3: Euclidean Distance (used in KNN, clustering) ---")
    point_a = np.array([1.0, 2.0, 3.0])
    point_b = np.array([4.0, 6.0, 3.0])
    distance = np.linalg.norm(point_a - point_b)
    print(f"  Point A: {point_a}")
    print(f"  Point B: {point_b}")
    print(f"  Distance: {distance:.4f}")

    print()
    print("--- Example 4: One-Hot Encoding ---")
    labels = np.array([0, 2, 1, 2, 0])
    n_classes = 3
    one_hot = np.zeros((len(labels), n_classes), dtype=int)
    one_hot[np.arange(len(labels)), labels] = 1
    print(f"  Labels:  {labels}")
    print(f"  One-Hot:\n{one_hot}")

    print()
    print("--- Example 5: Cosine Similarity (text/ML) ---")
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    v1 = np.array([1.0, 0.0, 1.0])
    v2 = np.array([1.0, 1.0, 0.0])
    v3 = np.array([1.0, 0.0, 1.0])
    print(f"  v1 vs v2 (different): {cosine_similarity(v1, v2):.4f}")
    print(f"  v1 vs v3 (identical): {cosine_similarity(v1, v3):.4f}")

    print()
    print("--- Example 6: Confusion Matrix Stats ---")
    y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0])
    y_pred = np.array([1, 0, 1, 0, 0, 1, 1, 0])

    TP = np.sum((y_true == 1) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))

    accuracy  = (TP + TN) / len(y_true)
    precision = TP / (TP + FP)
    recall    = TP / (TP + FN)
    f1        = 2 * (precision * recall) / (precision + recall)

    print(f"  TP={TP}  TN={TN}  FP={FP}  FN={FN}")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print()


    # ------------------------------------------------------------------
    # 16. SAVING AND LOADING DATA
    # ------------------------------------------------------------------
    print("16. SAVING AND LOADING DATA:")
    print("-" * 70)

    arr = np.array([[1, 2, 3], [4, 5, 6]])

    print("--- Binary format (fast, preserves dtype) ---")
    print("np.save('data.npy', arr)              ← single array")
    print("np.load('data.npy')                   ← load it back")
    print("np.savez('data.npz', a=arr, b=arr)    ← multiple arrays")
    print("data = np.load('data.npz')            ← load: data['a'], data['b']")

    print()
    print("--- Text format (human-readable, slower) ---")
    print("np.savetxt('data.csv', arr, delimiter=',', fmt='%d')")
    print("np.loadtxt('data.csv', delimiter=',')")

    print()
    print("💡 Use .npy/.npz for speed and dtype preservation.")
    print("💡 Use .csv when interoperability with other tools is needed.")
    print()


    # ------------------------------------------------------------------
    # 17. PERFORMANCE TIPS
    # ------------------------------------------------------------------
    print("17. PERFORMANCE TIPS:")
    print("-" * 70)

    print("✅ DO — NumPy way (fast):")
    print("   arr = np.arange(1_000_000)")
    print("   result = arr * 2                    ← vectorized, ~100x faster")
    print("   result = np.sum(arr)                ← C-level loop internally")
    print("   result = arr[arr > 500_000]         ← boolean indexing")

    print()
    print("❌ AVOID — Python way (slow):")
    print("   result = [x * 2 for x in arr]      ← Python loop, slow")
    print("   result = sum(arr)                   ← Python sum, slow")

    print()
    print("--- Memory layout tips ---")
    print("  C-contiguous (row-major, default):  arr = np.array(data, order='C')")
    print("  F-contiguous (col-major, Fortran):  arr = np.array(data, order='F')")
    print("  Check: arr.flags['C_CONTIGUOUS']")
    print("  Use np.ascontiguousarray(arr) if passing to C extensions.")

    print()
    print("--- Use views instead of copies ---")
    print("  arr.reshape(-1)    →  view  (fast)")
    print("  arr.flatten()      →  copy  (slower, but always independent)")
    print("  arr.ravel()        →  view when possible (preferred)")

    print()
    print("--- dtype matters for performance ---")
    print("  float32 uses half the memory of float64 → faster in ML training")
    print("  int8/int16 for categorical data or image masks")
    print()


    # ------------------------------------------------------------------
    # 18. COMMON MISTAKES
    # ------------------------------------------------------------------
    print("18. COMMON MISTAKES:")
    print("-" * 70)

    print("--- Mistake 1: Mutable default (view vs copy) ---")
    a = np.array([1, 2, 3])
    b = a          # b is just another name for a — NOT a copy
    b[0] = 99
    print(f"  After b[0]=99:  a={a}  ← changed!")
    print(f"  Fix: b = a.copy()")

    print()
    print("--- Mistake 2: Shape mismatch in matrix ops ---")
    print("  np.dot(A, B) requires A.shape[1] == B.shape[0]")
    print("  (3,4) @ (4,5) → (3,5)  ✅")
    print("  (3,4) @ (5,4) → ERROR  ❌")

    print()
    print("--- Mistake 3: Integer division truncation in dtype ---")
    arr = np.array([1, 2, 3], dtype=np.int32)
    print(f"  int32 array / 2: {arr / 2}    ← float64, OK")
    print(f"  int32 array // 2: {arr // 2}      ← stays int, truncates")

    print()
    print("--- Mistake 4: NaN comparisons ---")
    arr = np.array([1.0, np.nan, 3.0])
    print(f"  arr == np.nan:         {arr == np.nan}  ← always False!")
    print(f"  np.isnan(arr):         {np.isnan(arr)}  ← correct!")

    print()
    print("--- Mistake 5: Forgetting axis in aggregates ---")
    m = np.array([[1, 2], [3, 4]])
    print(f"  np.sum(m)        = {np.sum(m)}   ← sums EVERYTHING")
    print(f"  np.sum(m, axis=0)= {np.sum(m, axis=0)} ← sums per COLUMN")
    print(f"  np.sum(m, axis=1)= {np.sum(m, axis=1)} ← sums per ROW")
    print()


    # ------------------------------------------------------------------
    # 19. QUICK REFERENCE TABLE
    # ------------------------------------------------------------------
    print("19. QUICK REFERENCE TABLE:")
    print("-" * 70)
    print()
    print(f"  {'Function':<35} {'Description'}")
    print(f"  {'-'*35} {'-'*40}")

    ref = [
        # Creation
        ("CREATION", ""),
        ("np.array([1,2,3])",                "Create array from list"),
        ("np.zeros((m, n))",                 "Array of zeros, shape (m,n)"),
        ("np.ones((m, n))",                  "Array of ones, shape (m,n)"),
        ("np.full((m,n), val)",              "Array filled with val"),
        ("np.eye(n)",                        "Identity matrix n×n"),
        ("np.arange(start, stop, step)",     "Range array (like range())"),
        ("np.linspace(start, stop, n)",      "n evenly spaced points"),
        ("np.random.default_rng(seed)",      "Create reproducible RNG"),
        # Shape
        ("SHAPE", ""),
        ("arr.shape",                        "Tuple of dimensions"),
        ("arr.ndim",                         "Number of dimensions"),
        ("arr.size",                         "Total number of elements"),
        ("arr.reshape(m, n)",                "Change shape (same data)"),
        ("arr.flatten()",                    "Flatten to 1D (copy)"),
        ("arr.ravel()",                      "Flatten to 1D (view if possible)"),
        ("arr.T",                            "Transpose"),
        ("np.squeeze(arr)",                  "Remove dimensions of size 1"),
        ("np.expand_dims(arr, axis)",        "Add a dimension"),
        # Indexing
        ("INDEXING", ""),
        ("arr[i]",                           "Element at index i"),
        ("arr[i, j]",                        "Element at row i, col j"),
        ("arr[1:4]",                         "Slice (stop excluded)"),
        ("arr[arr > 5]",                     "Boolean indexing (filter)"),
        ("arr[[0, 2, 4]]",                   "Fancy indexing"),
        ("np.where(condition, a, b)",        "Conditional element selection"),
        # Math
        ("MATH", ""),
        ("arr + / - / * / **",               "Element-wise arithmetic"),
        ("A @ B",                            "Matrix multiplication"),
        ("np.dot(a, b)",                     "Dot / matrix product"),
        ("np.sqrt / exp / log / abs",        "Element-wise ufuncs"),
        # Aggregates
        ("AGGREGATES", ""),
        ("np.sum/mean/std/var(arr, axis=)",  "Aggregates (axis optional)"),
        ("np.min/max/argmin/argmax(arr)",    "Min/max and their indices"),
        ("np.cumsum(arr)",                   "Cumulative sum"),
        ("np.nanmean/nansum/nanstd(arr)",    "NaN-safe aggregates"),
        # Linear Algebra
        ("LINEAR ALGEBRA", ""),
        ("np.linalg.det(A)",                 "Determinant"),
        ("np.linalg.inv(A)",                 "Inverse matrix"),
        ("np.linalg.solve(A, b)",            "Solve Ax = b"),
        ("np.linalg.eig(A)",                 "Eigenvalues and eigenvectors"),
        ("np.linalg.norm(v)",                "Vector/matrix norm"),
        ("np.linalg.svd(A)",                 "Singular Value Decomposition"),
        # Sort & Search
        ("SORT & SEARCH", ""),
        ("np.sort(arr)",                     "Sorted copy"),
        ("np.argsort(arr)",                  "Indices that sort arr"),
        ("np.unique(arr)",                   "Unique values (sorted)"),
        ("np.where(condition)",              "Indices where condition True"),
        # NaN
        ("NaN HANDLING", ""),
        ("np.isnan(arr)",                    "Boolean mask of NaN positions"),
        ("np.nan",                           "NaN constant"),
        ("arr[~np.isnan(arr)]",              "Remove NaNs"),
        # Save/Load
        ("SAVE / LOAD", ""),
        ("np.save('f.npy', arr)",            "Save single array (binary)"),
        ("np.load('f.npy')",                 "Load .npy file"),
        ("np.savetxt('f.csv', arr)",         "Save as text/CSV"),
        ("np.loadtxt('f.csv', delimiter=',')","Load from text/CSV"),
    ]

    for func, desc in ref:
        if desc == "":
            print(f"\n  ── {func} {'─'*(65-len(func))}")
        else:
            print(f"  {func:<35} {desc}")

    print()


main()


"""
SUMMARY — NUMPY
=======================================================

CORE CONCEPT:
  NumPy arrays store data in contiguous memory with a fixed dtype.
  This enables C-speed vectorized operations — no Python loops needed.

ARRAY CREATION:
  np.array([...])            →  from list
  np.zeros/ones/full/eye()   →  filled arrays
  np.arange()                →  like range()
  np.linspace()              →  evenly spaced floats

KEY ATTRIBUTES:
  arr.shape, arr.ndim, arr.size, arr.dtype

INDEXING:
  arr[i]          →  element
  arr[i, j]       →  2D element
  arr[1:4]        →  slice (view!)
  arr[arr > 5]    →  boolean filter
  arr[[0,2,4]]    →  fancy indexing

RESHAPING:
  reshape, flatten, ravel, T, squeeze, expand_dims

VECTORIZED OPS:
  +  -  *  /  **  %  //    →  element-wise
  A @ B                    →  matrix multiply
  np.sqrt/exp/log/abs()    →  ufuncs

AGGREGATES (use axis= for direction):
  sum, mean, std, var, min, max, argmin, argmax, cumsum
  nan-safe: nanmean, nansum, nanstd, nanmin, nanmax

LINEAR ALGEBRA:
  np.linalg.det, inv, solve, eig, norm, svd

RANDOM:
  rng = np.random.default_rng(seed)   ← always set seed!
  rng.random, rng.integers, rng.normal, rng.choice, rng.shuffle

NaN HANDLING:
  np.isnan(arr)           →  find NaN
  np.nanmean/nansum()     →  ignore NaN
  arr[~np.isnan(arr)]     →  remove NaN

ML PATTERNS:
  Min-Max scaling:    (arr - arr.min()) / (arr.max() - arr.min())
  Z-score scaling:    (arr - arr.mean()) / arr.std()
  Euclidean dist:     np.linalg.norm(a - b)
  Cosine similarity:  np.dot(a,b) / (norm(a) * norm(b))
  One-hot encoding:   np.eye(n_classes)[labels]

COMMON PITFALLS:
  • Slices are VIEWS — use .copy() for independence
  • A * B is element-wise; A @ B is matrix multiply
  • NaN != NaN — always use np.isnan(), never ==
  • Set seed for reproducibility: np.random.default_rng(42)
  • Use nanmean/nansum when data may contain NaN

REMEMBER:
  "NumPy is the foundation — Pandas, Matplotlib, Scikit-learn,
   and TensorFlow all operate on NumPy arrays under the hood."
"""