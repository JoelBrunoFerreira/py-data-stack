"""
SCIPY - COMPLETE GUIDE
========================

SciPy (Scientific Python) is a library built on top of NumPy that provides
algorithms and mathematical tools for scientific and engineering computing.
While NumPy focuses on array operations, SciPy provides higher-level routines
for statistics, linear algebra, optimization, integration, and more.

Key Characteristics:
- Organized into submodules — import only what you need
- Builds directly on NumPy arrays
- Peer-reviewed, numerically stable implementations
- Foundation for many ML and scientific Python libraries

Installation:
  pip install scipy

Submodules covered in this reference:
  scipy.stats        → probability distributions, statistical tests
  scipy.linalg       → advanced linear algebra (extends numpy.linalg)
  scipy.optimize     → minimization, root finding, curve fitting
  scipy.integrate    → numerical integration, ODEs
  scipy.special      → special mathematical functions

Relationship to the stack:
  NumPy   → arrays, basic linear algebra, random numbers
  SciPy   → scientific algorithms on top of NumPy arrays
  Pandas  → tabular data, uses SciPy for statistical tests
  Sklearn → ML models, uses SciPy under the hood
"""

import numpy as np
import scipy
from scipy import stats, linalg, optimize, integrate, special
from typing import Callable, Any
import warnings
warnings.filterwarnings('ignore')

np.set_printoptions(precision=4, suppress=True)


def section(title):
    print(f"\n{title}")
    print("-" * 70)


def main():

    print("=== SCIPY - COMPLETE GUIDE ===\n")
    print(f"SciPy  version: {scipy.__version__}")
    print(f"NumPy  version: {np.__version__}")

    print("""
  IMPORT PATTERN:
    from scipy import stats, linalg, optimize, integrate, special

    Never:   import scipy  then  scipy.stats.norm(...)  ← slow, cluttered
    Always:  from scipy import stats  then  stats.norm(...)  ← clean ✅
    """)


    # ══════════════════════════════════════════════════════════════════
    # PART 1 — SCIPY.STATS
    # ══════════════════════════════════════════════════════════════════

    print("\n" + "═" * 70)
    print("PART 1 — scipy.stats  (Statistics)")
    print("═" * 70)


    # ------------------------------------------------------------------
    # 1. PROBABILITY DISTRIBUTIONS
    # ------------------------------------------------------------------
    section("1. PROBABILITY DISTRIBUTIONS")

    print("""
  Every SciPy distribution is an object with the same interface:

    dist = stats.norm(loc=0, scale=1)   ← create frozen distribution
      dist.pdf(x)   → Probability Density Function
      dist.cdf(x)   → Cumulative Distribution Function  P(X ≤ x)
      dist.ppf(q)   → Percent Point Function (inverse CDF / quantile)
      dist.sf(x)    → Survival Function  1 - CDF  =  P(X > x)
      dist.rvs(n)   → Random Variates Sample (random samples)
      dist.mean()   → theoretical mean
      dist.std()    → theoretical std
      dist.interval(0.95) → 95% equal-tailed interval
    """)

    print("--- Normal distribution ---")
    norm = stats.norm(loc=0, scale=1)   # standard normal

    print(f"  P(X ≤ 1.96)       = {norm.cdf(1.96):.4f}  (should be ~0.975)")
    print(f"  P(X > 1.96)       = {norm.sf(1.96):.4f}   (should be ~0.025)")
    print(f"  P(-1.96 ≤ X ≤ 1.96) = {norm.cdf(1.96) - norm.cdf(-1.96):.4f}  (~0.95)")
    print(f"  95th percentile   = {norm.ppf(0.95):.4f}  (z = 1.6449)")
    print(f"  97.5th percentile = {norm.ppf(0.975):.4f} (z = 1.96)")
    print(f"  95% CI interval   = {norm.interval(0.95)}")

    rng = np.random.default_rng(42)
    samples = norm.rvs(size=1000, random_state=42)
    print(f"  1000 samples: mean={samples.mean():.4f}  std={samples.std():.4f}")

    print()
    print("--- t distribution (small samples) ---")
    t10 = stats.t(df=10)   # 10 degrees of freedom
    t30 = stats.t(df=30)
    print(f"  t(df=10) 97.5th pct = {t10.ppf(0.975):.4f}  (wider than normal)")
    print(f"  t(df=30) 97.5th pct = {t30.ppf(0.975):.4f}")
    print(f"  norm     97.5th pct = {norm.ppf(0.975):.4f}  (t → normal as df → ∞)")

    print()
    print("--- Other key distributions ---")

    # Uniform
    u = stats.uniform(loc=0, scale=10)  # Uniform[0, 10]
    print(f"  Uniform[0,10]: mean={u.mean():.1f}  std={u.std():.4f}")

    # Chi-squared
    chi2 = stats.chi2(df=5)
    print(f"  Chi²(df=5):  mean={chi2.mean():.1f}  "
          f"95th pct={chi2.ppf(0.95):.4f}")

    # F distribution
    f_dist = stats.f(dfn=3, dfd=20)
    print(f"  F(3,20):     95th pct={f_dist.ppf(0.95):.4f}")

    # Binomial
    binom = stats.binom(n=20, p=0.3)
    print(f"  Binom(n=20,p=0.3): mean={binom.mean():.1f}  "
          f"P(X=6)={binom.pmf(6):.4f}")

    # Poisson
    poisson = stats.poisson(mu=3.5)
    print(f"  Poisson(μ=3.5): P(X=3)={poisson.pmf(3):.4f}  "
          f"P(X≤5)={poisson.cdf(5):.4f}")

    # Exponential
    exp = stats.expon(scale=2)   # scale = 1/lambda = mean
    print(f"  Expon(mean=2): P(X≤1)={exp.cdf(1):.4f}  "
          f"median={exp.ppf(0.5):.4f}")

    print()
    print("--- Fitting a distribution to data ---")
    rng_data = np.random.default_rng(0)
    data = rng_data.normal(loc=5, scale=2, size=500)

    # Fit normal distribution to data (MLE)
    mu_hat, sigma_hat = stats.norm.fit(data)
    print(f"  True:    μ=5.0     σ=2.0")
    print(f"  MLE fit: μ={mu_hat:.4f}  σ={sigma_hat:.4f}")

    # Goodness-of-fit test
    ks_stat, ks_p = stats.kstest(data, 'norm', args=(mu_hat, sigma_hat))
    print(f"  KS test: statistic={ks_stat:.4f}  p-value={ks_p:.4f}")
    print(f"  → {'Fits well (fail to reject H₀)' if ks_p > 0.05 else 'Poor fit (reject H₀)'}")

    print()
    print("  KEY DISTRIBUTIONS:")
    print(f"  {'stats.norm(loc, scale)':<35} Normal (Gaussian)")
    print(f"  {'stats.t(df)':<35} Student's t")
    print(f"  {'stats.chi2(df)':<35} Chi-squared")
    print(f"  {'stats.f(dfn, dfd)':<35} F distribution")
    print(f"  {'stats.uniform(loc, scale)':<35} Uniform")
    print(f"  {'stats.expon(scale)':<35} Exponential")
    print(f"  {'stats.binom(n, p)':<35} Binomial (discrete)")
    print(f"  {'stats.poisson(mu)':<35} Poisson (discrete)")
    print(f"  {'stats.beta(a, b)':<35} Beta [0,1]")
    print(f"  {'stats.gamma(a, scale)':<35} Gamma")
    print(f"  {'stats.lognorm(s, scale)':<35} Log-normal")
    print(f"  {'stats.multivariate_normal(mean, cov)':<35} Multivariate Normal")


    # ------------------------------------------------------------------
    # 2. DESCRIPTIVE STATISTICS
    # ------------------------------------------------------------------
    section("2. DESCRIPTIVE STATISTICS")

    rng = np.random.default_rng(42)
    data = rng.normal(50, 15, 200)
    data_skewed = rng.exponential(scale=10, size=200)

    print("--- Central tendency and spread ---")
    print(f"  data (n={len(data)}):")
    print(f"  mean        = {np.mean(data):.4f}")
    print(f"  median      = {np.median(data):.4f}")
    print(f"  mode        = {stats.mode(data.round(0)).mode:.1f}")
    print(f"  std         = {np.std(data, ddof=1):.4f}  (ddof=1 → sample std)")
    print(f"  variance    = {np.var(data, ddof=1):.4f}")
    print(f"  sem         = {stats.sem(data):.4f}  (standard error of mean)")
    print(f"  IQR         = {stats.iqr(data):.4f}")
    print(f"  range       = {np.ptp(data):.4f}")

    print()
    print("--- Shape statistics ---")
    print(f"  skewness    = {stats.skew(data):.4f}  (0=symmetric)")
    print(f"  kurtosis    = {stats.kurtosis(data):.4f}  (0=normal, >0=heavy tails)")
    print(f"  skewness (skewed data) = {stats.skew(data_skewed):.4f}")
    print(f"  kurtosis (skewed data) = {stats.kurtosis(data_skewed):.4f}")

    print()
    print("--- Percentiles and quantiles ---")
    pcts = [10, 25, 50, 75, 90, 95, 99]
    vals = np.percentile(data, pcts)
    for p, v in zip(pcts, vals):
        print(f"  P{p:2d}  = {v:.2f}")

    print()
    print("--- stats.describe() — full summary in one call ---")
    desc = stats.describe(data)
    print(f"  n        = {desc.nobs}")
    print(f"  min, max = {desc.minmax[0]:.4f}, {desc.minmax[1]:.4f}")
    print(f"  mean     = {desc.mean:.4f}")
    print(f"  variance = {desc.variance:.4f}")
    print(f"  skewness = {desc.skewness:.4f}")
    print(f"  kurtosis = {desc.kurtosis:.4f}")


    # ------------------------------------------------------------------
    # 3. HYPOTHESIS TESTING
    # ------------------------------------------------------------------
    section("3. HYPOTHESIS TESTING")

    print("""
  INTERPRETING p-values:
    p ≤ 0.05 → reject H₀ at 5% significance level (significant result)
    p > 0.05 → fail to reject H₀ (insufficient evidence against H₀)

  RESULT OBJECT:
    result = stats.ttest_ind(a, b)
    result.statistic  → test statistic
    result.pvalue     → p-value
    result.df         → degrees of freedom (some tests)
    """)

    rng  = np.random.default_rng(42)
    grpA = rng.normal(100, 15, 50)   # group A: mean=100, sd=15
    grpB = rng.normal(108, 15, 50)   # group B: mean=108, sd=15

    print("--- One-sample t-test: is mean = 100? ---")
    t_stat, p_val = stats.ttest_1samp(grpA, popmean=100)
    print(f"  H₀: μ = 100   H₁: μ ≠ 100")
    print(f"  t = {t_stat:.4f}   p = {p_val:.4f}")
    print(f"  → {'Reject H₀' if p_val < 0.05 else 'Fail to reject H₀'} (α=0.05)")

    print()
    print("--- Two-sample t-test: do groups differ? ---")
    t_stat, p_val = stats.ttest_ind(grpA, grpB, equal_var=True)
    print(f"  H₀: μA = μB   H₁: μA ≠ μB")
    print(f"  t = {t_stat:.4f}   p = {p_val:.4f}")
    print(f"  → {'Reject H₀' if p_val < 0.05 else 'Fail to reject H₀'} (α=0.05)")
    print(f"  True difference: {grpB.mean() - grpA.mean():.2f}")

    print()
    print("--- Welch's t-test: unequal variances (more robust) ---")
    t_stat, p_val = stats.ttest_ind(grpA, grpB, equal_var=False)
    print(f"  t = {t_stat:.4f}   p = {p_val:.4f}")

    print()
    print("--- Paired t-test: before vs after ---")
    before = rng.normal(80, 10, 30)
    after  = before + rng.normal(5, 3, 30)   # improvement of ~5
    t_stat, p_val = stats.ttest_rel(before, after)
    print(f"  H₀: μ_diff = 0   H₁: μ_diff ≠ 0")
    print(f"  Mean before={before.mean():.2f}  after={after.mean():.2f}  "
          f"diff={after.mean()-before.mean():.2f}")
    print(f"  t = {t_stat:.4f}   p = {p_val:.4f}")
    print(f"  → {'Reject H₀' if p_val < 0.05 else 'Fail to reject H₀'} (α=0.05)")

    print()
    print("--- One-way ANOVA: multiple groups ---")
    g1 = rng.normal(100, 10, 40)
    g2 = rng.normal(105, 10, 40)
    g3 = rng.normal(115, 10, 40)
    f_stat, p_val = stats.f_oneway(g1, g2, g3)
    print(f"  H₀: μ1=μ2=μ3   H₁: at least one differs")
    print(f"  F = {f_stat:.4f}   p = {p_val:.4f}")
    print(f"  → {'Reject H₀' if p_val < 0.05 else 'Fail to reject H₀'} (α=0.05)")
    print(f"  True means: g1={g1.mean():.2f}  g2={g2.mean():.2f}  g3={g3.mean():.2f}")

    print()
    print("--- Chi-squared test: independence of categorical variables ---")
    # Contingency table: Product × Region purchase counts
    observed = np.array([[45, 30, 25, 20],
                          [20, 35, 30, 15],
                          [15, 20, 40, 25]])
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(observed)
    print(f"  Contingency table (3 products × 4 regions):")
    print(f"  χ² = {chi2_stat:.4f}   p = {p_val:.4f}   dof = {dof}")
    print(f"  → {'Reject H₀' if p_val < 0.05 else 'Fail to reject H₀'} "
          f"(product and region are "
          f"{'dependent' if p_val < 0.05 else 'independent'})")

    print()
    print("--- Normality tests ---")
    data_normal = rng.normal(0, 1, 200)
    data_skewed = rng.exponential(1, 200)

    # Shapiro-Wilk (best for n < 5000)
    stat, p = stats.shapiro(data_normal)
    print(f"  Shapiro-Wilk (normal data):  W={stat:.4f}  p={p:.4f}  "
          f"→ {'Normal' if p > 0.05 else 'Not normal'}")
    stat, p = stats.shapiro(data_skewed)
    print(f"  Shapiro-Wilk (skewed data):  W={stat:.4f}  p={p:.4f}  "
          f"→ {'Normal' if p > 0.05 else 'Not normal'}")

    # D'Agostino-Pearson (good for larger samples)
    stat, p = stats.normaltest(data_normal)
    print(f"  D'Agostino (normal data):    stat={stat:.4f}  p={p:.4f}  "
          f"→ {'Normal' if p > 0.05 else 'Not normal'}")

    print()
    print("--- Non-parametric tests (when normality fails) ---")
    # Mann-Whitney U (non-parametric alternative to t-test)
    stat, p = stats.mannwhitneyu(grpA, grpB, alternative='two-sided')
    print(f"  Mann-Whitney U (non-param t-test):  U={stat:.1f}  p={p:.4f}")

    # Wilcoxon signed-rank (non-parametric paired t-test)
    stat, p = stats.wilcoxon(before, after)
    print(f"  Wilcoxon signed-rank (non-param paired): stat={stat:.1f}  p={p:.4f}")

    # Kruskal-Wallis (non-parametric ANOVA)
    stat, p = stats.kruskal(g1, g2, g3)
    print(f"  Kruskal-Wallis (non-param ANOVA): H={stat:.4f}  p={p:.4f}")

    print()
    print("--- Correlation tests ---")
    x = rng.normal(0, 1, 100)
    y = 2 * x + rng.normal(0, 0.5, 100)

    r, p = stats.pearsonr(x, y)
    print(f"  Pearson r   = {r:.4f}  p = {p:.4e}  (linear correlation)")

    rho, p = stats.spearmanr(x, y)
    print(f"  Spearman ρ  = {rho:.4f}  p = {p:.4e}  (rank correlation)")

    tau, p = stats.kendalltau(x, y)
    print(f"  Kendall τ   = {tau:.4f}  p = {p:.4e}  (concordance)")

    print()
    print("--- Effect size (beyond p-values) ---")
    # Cohen's d — standardized mean difference
    def cohens_d(a, b):
        pooled_std = np.sqrt((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2)
        return (np.mean(b) - np.mean(a)) / pooled_std

    d = cohens_d(grpA, grpB)
    print(f"  Cohen's d (grpA vs grpB) = {d:.4f}")
    print(f"  Interpretation: "
          f"{'small' if abs(d)<0.5 else 'medium' if abs(d)<0.8 else 'large'} effect "
          f"(small<0.5, medium<0.8, large≥0.8)")

    print()
    print("  HYPOTHESIS TEST CHEAT SHEET:")
    print(f"  {'Test':<35} {'Use when'}")
    print(f"  {'-'*35} {'-'*40}")
    tests = [
        ("stats.ttest_1samp(a, μ₀)",        "Compare sample mean to known value"),
        ("stats.ttest_ind(a, b)",            "Compare means of 2 independent groups"),
        ("stats.ttest_rel(a, b)",            "Compare means of 2 paired samples"),
        ("stats.f_oneway(g1, g2, g3, ...)",  "Compare means of 3+ groups (ANOVA)"),
        ("stats.chi2_contingency(table)",    "Independence of 2 categorical vars"),
        ("stats.shapiro(data)",              "Test normality (n < 5000)"),
        ("stats.normaltest(data)",           "Test normality (larger n)"),
        ("stats.mannwhitneyu(a, b)",         "Non-param: 2 independent groups"),
        ("stats.wilcoxon(a, b)",             "Non-param: 2 paired samples"),
        ("stats.kruskal(g1, g2, ...)",       "Non-param: 3+ groups"),
        ("stats.pearsonr(x, y)",             "Linear correlation"),
        ("stats.spearmanr(x, y)",            "Monotonic (rank) correlation"),
        ("stats.kstest(data, 'norm')",       "Compare data to a distribution"),
    ]
    for t, desc in tests:
        print(f"  {t:<35} {desc}")


    # ------------------------------------------------------------------
    # 4. CONFIDENCE INTERVALS AND BOOTSTRAP
    # ------------------------------------------------------------------
    section("4. CONFIDENCE INTERVALS AND BOOTSTRAP")

    rng  = np.random.default_rng(42)
    data = rng.normal(50, 15, 100)

    print("--- t-interval for the mean ---")
    ci = stats.t.interval(confidence=0.95,
                           df=len(data) - 1,
                           loc=data.mean(),
                           scale=stats.sem(data))
    print(f"  Data: mean={data.mean():.4f}  sem={stats.sem(data):.4f}")
    print(f"  95% CI for mean: ({ci[0]:.4f}, {ci[1]:.4f})")
    print(f"  Width: {ci[1]-ci[0]:.4f}")

    print()
    print("--- Bootstrap confidence interval (distribution-free) ---")
    def bootstrap_ci(data, statistic: Callable = np.mean, n_boot=2000,
                     ci=0.95, seed=42):
        rng_b = np.random.default_rng(seed)
        boot_stats = [
            statistic(rng_b.choice(data, size=len(data), replace=True))
            for _ in range(n_boot)
        ]
        alpha = (1 - ci) / 2
        return np.percentile(boot_stats, [alpha*100, (1-alpha)*100])

    boot_mean   = bootstrap_ci(data, np.mean)
    boot_median = bootstrap_ci(data, np.median)
    boot_std    = bootstrap_ci(data, np.std)

    print(f"  Bootstrap 95% CI for mean:   ({boot_mean[0]:.4f}, {boot_mean[1]:.4f})")
    print(f"  Bootstrap 95% CI for median: ({boot_median[0]:.4f}, {boot_median[1]:.4f})")
    print(f"  Bootstrap 95% CI for std:    ({boot_std[0]:.4f}, {boot_std[1]:.4f})")

    print()
    print("--- scipy.stats.bootstrap (built-in, Python 3.9+ / SciPy 1.7+) ---")
    boot_result = stats.bootstrap(
        (data,),
        statistic=np.mean,
        n_resamples=2000,
        confidence_level=0.95,
        random_state=42
    )
    print(f"  scipy bootstrap CI for mean: "
          f"({boot_result.confidence_interval.low:.4f}, "
          f"{boot_result.confidence_interval.high:.4f})")

    print()
    print("💡 Use t-interval when data is approximately normal.")
    print("   Use bootstrap when: non-normal data, unusual statistics")
    print("   (median, std, correlation), or small samples.")


    # ══════════════════════════════════════════════════════════════════
    # PART 2 — SCIPY.LINALG
    # ══════════════════════════════════════════════════════════════════

    print("\n" + "═" * 70)
    print("PART 2 — scipy.linalg  (Advanced Linear Algebra)")
    print("═" * 70)


    # ------------------------------------------------------------------
    # 5. SCIPY.LINALG vs NUMPY.LINALG
    # ------------------------------------------------------------------
    section("5. SCIPY.LINALG vs NUMPY.LINALG")

    print("""
  scipy.linalg includes everything in numpy.linalg PLUS:
    - More decompositions (LU, Cholesky, QR, Schur, Polar)
    - More solvers (banded, triangular, block)
    - Matrix functions (expm, logm, sqrtm, funm)
    - More numerically stable implementations
    - Better error messages

  💡 Prefer scipy.linalg over numpy.linalg for serious numerical work.

  COMMON IMPORT:
    from scipy import linalg
    """)


    # ------------------------------------------------------------------
    # 6. MATRIX DECOMPOSITIONS
    # ------------------------------------------------------------------
    section("6. MATRIX DECOMPOSITIONS")

    rng = np.random.default_rng(42)
    A   = np.array([[4, 3, 2],
                    [3, 5, 1],
                    [2, 1, 6]], dtype=float)
    B   = np.array([[1, 2, 1],
                    [2, 3, 0],
                    [1, 0, 4]], dtype=float)

    print("Matrix A:")
    print(A)

    print()
    print("--- LU Decomposition: A = P @ L @ U ---")
    P, L, U = linalg.lu(A)
    print(f"  P (permutation):\n{P}")
    print(f"  L (lower triangular):\n{L.round(4)}")
    print(f"  U (upper triangular):\n{U.round(4)}")
    print(f"  Verify P@L@U = A: {np.allclose(P @ L @ U, A)}")
    print("""
  Use case: solving Ax=b efficiently for multiple b vectors.
  lu, piv = linalg.lu_factor(A)
  x = linalg.lu_solve((lu, piv), b)
    """)

    print("--- Cholesky Decomposition: A = L @ L.T  (symmetric positive definite) ---")
    # Need a symmetric positive definite matrix
    S = A.T @ A   # A.T @ A is always SPD
    L_chol = linalg.cholesky(S, lower=True)
    print(f"  L:\n{L_chol.round(4)}")
    print(f"  Verify L@L.T = S: {np.allclose(L_chol @ L_chol.T, S)}")
    print("  Use case: Gaussian processes, MVN sampling, solving SPD systems faster.")

    print()
    print("--- QR Decomposition: A = Q @ R ---")
    Q, R = linalg.qr(A)
    print(f"  Q (orthogonal):\n{Q.round(4)}")
    print(f"  R (upper triangular):\n{R.round(4)}")
    print(f"  Verify Q@R = A: {np.allclose(Q @ R, A)}")
    print(f"  Q is orthogonal: Q.T@Q = I: {np.allclose(Q.T @ Q, np.eye(3))}")
    print("  Use case: least squares, Gram-Schmidt, numerical stability.")

    print()
    print("--- Singular Value Decomposition: A = U @ Σ @ V.T ---")
    U_svd, s, Vt = linalg.svd(A)
    S_mat = np.diag(s)
    print(f"  Singular values: {s.round(4)}")
    print(f"  Verify U@Σ@Vt = A: {np.allclose(U_svd @ S_mat @ Vt, A)}")
    print("""
  Use cases:
    - PCA (principal component analysis)
    - Low-rank matrix approximation
    - Pseudoinverse (Moore-Penrose)
    - Recommender systems

  Rank-k approximation (keep top k singular values):
    A_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    """)

    print("--- Eigenvalue Decomposition: A @ v = λ @ v ---")
    eigenvalues, eigenvectors = linalg.eig(A)
    print(f"  Eigenvalues:  {eigenvalues.real.round(4)}")
    print(f"  Eigenvectors:\n{eigenvectors.real.round(4)}")

    # eigh: optimized for symmetric/Hermitian matrices
    eigenvalues_s, eigenvectors_s = linalg.eigh(A)   # symmetric A
    print(f"  eigh eigenvalues (symmetric): {eigenvalues_s.round(4)}")
    print("  💡 Use eigh() for symmetric matrices — faster and always real.")

    print()
    print("--- Schur Decomposition: A = Z @ T @ Z.T ---")
    T_schur, Z = linalg.schur(A)
    print(f"  T (quasi-upper triangular):\n{T_schur.round(4)}")
    print(f"  Verify Z@T@Z.T = A: {np.allclose(Z @ T_schur @ Z.T, A)}")


    # ------------------------------------------------------------------
    # 7. SOLVING LINEAR SYSTEMS
    # ------------------------------------------------------------------
    section("7. SOLVING LINEAR SYSTEMS")

    print("--- Standard solve: Ax = b ---")
    A_sys = np.array([[3, 1, -1],
                       [2, 4,  1],
                       [-1, 2,  5]], dtype=float)
    b_sys = np.array([4, 1, 1], dtype=float)

    x = linalg.solve(A_sys, b_sys)
    print(f"  A:\n{A_sys}")
    print(f"  b: {b_sys}")
    print(f"  Solution x: {x.round(4)}")
    print(f"  Verify A@x = b: {np.allclose(A_sys @ x, b_sys)}")

    print()
    print("--- Least squares: solve overdetermined Ax ≈ b ---")
    # More equations than unknowns
    A_over = rng.normal(0, 1, (10, 3))
    b_over = rng.normal(0, 1, 10)
    x_ls, res, rank, sv = linalg.lstsq(A_over, b_over)
    print(f"  A shape: {A_over.shape}  (overdetermined: 10 equations, 3 unknowns)")
    print(f"  Least squares solution: {x_ls.round(4)}")
    print(f"  Rank: {rank}")
    print(f"  Residual norm²: {np.sum((A_over @ x_ls - b_over)**2):.4f}")

    print()
    print("--- Matrix inverse and pseudoinverse ---")
    A_sq = np.array([[2, 1], [5, 3]], dtype=float)
    A_inv   = linalg.inv(A_sq)
    A_pinv  = linalg.pinv(A_sq)   # Moore-Penrose pseudoinverse

    print(f"  A:\n{A_sq}")
    print(f"  inv(A):\n{A_inv.round(4)}")
    print(f"  Verify A @ inv(A) = I: {np.allclose(A_sq @ A_inv, np.eye(2))}")
    print()
    print("  ⚠️  Never use inv(A) to solve Ax=b!")
    print("      linalg.solve(A, b) is faster, more stable, and preferred.")

    print()
    print("--- Determinant, rank, norm, condition number ---")
    print(f"  det(A):        {linalg.det(A_sys):.4f}")
    print(f"  matrix_rank:   {np.linalg.matrix_rank(A_sys)}")
    print(f"  norm (Frobenius): {linalg.norm(A_sys, 'fro'):.4f}")
    print(f"  norm (2-norm):    {linalg.norm(A_sys, 2):.4f}")
    print(f"  cond number:   {np.linalg.cond(A_sys):.4f}")
    print("  💡 Condition number >> 1 → matrix is ill-conditioned (sensitive to errors)")


    # ------------------------------------------------------------------
    # 8. MATRIX FUNCTIONS
    # ------------------------------------------------------------------
    section("8. MATRIX FUNCTIONS")

    A_small = np.array([[1, 2],
                         [0, 1]], dtype=float)

    print("--- Matrix exponential: e^A ---")
    expA = linalg.expm(A_small)
    print(f"  A:\n{A_small}")
    print(f"  expm(A):\n{expA.round(4)}")
    print("  Use case: solving systems of ODEs  dx/dt = Ax → x(t) = expm(A*t) @ x0")

    print()
    print("--- Matrix logarithm, square root ---")
    A_pos = np.array([[4, 2], [1, 3]], dtype=float)
    print(f"  logm(A):\n{linalg.logm(A_pos).round(4)}")
    sqrtA = linalg.sqrtm(A_pos)
    print(f"  sqrtm(A):\n{sqrtA.real.round(4)}")
    print(f"  Verify sqrtm(A) @ sqrtm(A) = A: "
          f"{np.allclose(sqrtA.real @ sqrtA.real, A_pos)}")

    print()
    print("--- Kronecker product and block diagonal ---")
    K = np.kron(np.eye(2), np.array([[1,2],[3,4]]))
    print(f"  kron(I₂, [[1,2],[3,4]]):\n{K}")

    bd = linalg.block_diag(np.array([[1,2],[3,4]]),
                            np.array([[5,6],[7,8]]),
                            np.array([[9]]))
    print(f"  block_diag(A, B, C):\n{bd}")


    # ══════════════════════════════════════════════════════════════════
    # PART 3 — SCIPY.OPTIMIZE
    # ══════════════════════════════════════════════════════════════════

    print("\n" + "═" * 70)
    print("PART 3 — scipy.optimize  (Optimization & Curve Fitting)")
    print("═" * 70)


    # ------------------------------------------------------------------
    # 9. MINIMIZATION
    # ------------------------------------------------------------------
    section("9. MINIMIZATION")

    print("--- minimize() — unconstrained ---")
    def rosenbrock(x):
        """Classic test function. Global minimum at (1,1) = 0."""
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    result = optimize.minimize(rosenbrock, x0=[0, 0], method='L-BFGS-B')
    print(f"  Rosenbrock function: min at (1, 1) = 0")
    print(f"  Starting point:  x₀ = [0, 0]")
    print(f"  Found minimum:   x* = {result.x.round(6)}")
    print(f"  Minimum value:   f*  = {result.fun:.2e}")
    print(f"  Converged:       {result.success}")
    print(f"  Iterations:      {result.nit}")

    print()
    print("--- minimize_scalar() — 1D minimization ---")
    def f1d(x):
        return x**4 - 3*x**3 + 2

    result_1d = optimize.minimize_scalar(f1d, bounds=(-1, 4), method='bounded')
    print(f"  f(x) = x⁴ - 3x³ + 2")
    print(f"  Minimum at x = {result_1d.x:.6f}   f(x) = {result_1d.fun:.6f}")

    print()
    print("--- minimize() — with constraints ---")
    # Minimize f(x,y) = (x-1)² + (y-2)²  subject to x+y = 3
    def objective(x):
        return (x[0]-1)**2 + (x[1]-2)**2

    constraint = {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 3}
    bounds      = [(0, None), (0, None)]   # x≥0, y≥0

    result_c = optimize.minimize(objective, x0=[1, 1],
                                  constraints=constraint,
                                  bounds=bounds,
                                  method='SLSQP')
    print(f"  Min (x-1)²+(y-2)² s.t. x+y=3, x≥0, y≥0")
    print(f"  Solution: x={result_c.x[0]:.4f}  y={result_c.x[1]:.4f}")
    print(f"  f(x*) = {result_c.fun:.6f}   Check x+y={sum(result_c.x):.4f}")

    print()
    print("  MINIMIZATION METHODS:")
    print(f"  {'Nelder-Mead':<20} No gradient needed, robust, slow")
    print(f"  {'L-BFGS-B':<20} Quasi-Newton, fast, handles bounds")
    print(f"  {'SLSQP':<20} Constraints (equality + inequality)")
    print(f"  {'trust-constr':<20} Robust constrained optimization")
    print(f"  {'CG':<20} Conjugate gradient, large scale")


    # ------------------------------------------------------------------
    # 10. ROOT FINDING
    # ------------------------------------------------------------------
    section("10. ROOT FINDING")

    print("--- brentq() — robust 1D root finding (bracketing) ---")
    def f(x):
        return x**3 - 2*x - 5

    root = optimize.brentq(f, a=1, b=3)
    print(f"  f(x) = x³ - 2x - 5 = 0")
    print(f"  Root in [1, 3]: x = {root:.8f}")
    print(f"  Verify f(root) = {f(root):.2e}")

    print()
    print("--- fsolve() — multi-dimensional root finding ---")
    def system(vars):
        x, y = vars
        eq1 = x**2 + y**2 - 4       # circle x²+y²=4
        eq2 = x - y - 1              # line x-y=1
        return [eq1, eq2]

    solution = optimize.fsolve(system, x0=[1, 1], full_output=False)
    print(f"  System: x²+y²=4  and  x-y=1")
    print(f"  Solution: x={solution[0]:.6f}  y={solution[1]:.6f}")
    print(f"  Verify: {[round(v, 8) for v in system(solution)]}")

    print()
    print("  ROOT FINDING METHODS:")
    print(f"  {'brentq(f, a, b)':<30} Robust bracketing (recommended for 1D)")
    print(f"  {'bisect(f, a, b)':<30} Simple bisection (slower but safe)")
    print(f"  {'newton(f, x0, fprime)':<30} Newton-Raphson (fast with derivative)")
    print(f"  {'fsolve(system, x0)':<30} Multi-dimensional (Newton-like)")
    print(f"  {'root(system, x0, method)':<30} General multi-dim root finder")


    # ------------------------------------------------------------------
    # 11. CURVE FITTING
    # ------------------------------------------------------------------
    section("11. CURVE FITTING")

    print("--- curve_fit() — fit any function to data ---")

    rng = np.random.default_rng(42)
    x_data = np.linspace(0, 4*np.pi, 80)
    y_true = 3.0 * np.sin(2.0 * x_data + 0.5) * np.exp(-0.1 * x_data)
    y_data = y_true + rng.normal(0, 0.3, len(x_data))

    def damped_sine(x, amplitude, frequency, phase, decay):
        return amplitude * np.sin(frequency * x + phase) * np.exp(-decay * x)

    # Initial guess for [amplitude, frequency, phase, decay]
    p0     = [2.5, 1.8, 0.3, 0.08]
    bounds = ([0, 0, -np.pi, 0], [10, 10, np.pi, 1])

    popt, pcov = optimize.curve_fit(damped_sine, x_data, y_data,
                                     p0=p0, bounds=bounds)
    perr = np.sqrt(np.diag(pcov))   # standard errors of parameters

    print(f"  Model: A·sin(ω·x + φ)·e^(-δx)")
    print(f"  {'Param':<12} {'True':<10} {'Fitted':<12} {'Std Error'}")
    print(f"  {'-'*12} {'-'*10} {'-'*12} {'-'*10}")
    params = ['amplitude', 'frequency', 'phase', 'decay']
    trues  = [3.0, 2.0, 0.5, 0.1]
    for name, true, fit, err in zip(params, trues, popt, perr):
        print(f"  {name:<12} {true:<10.4f} {fit:<12.4f} ±{err:.4f}")

    # Residuals
    y_fit  = damped_sine(x_data, *popt)
    ss_res = np.sum((y_data - y_fit)**2)
    ss_tot = np.sum((y_data - y_data.mean())**2)
    r2     = 1 - ss_res / ss_tot
    print(f"\n  R² = {r2:.6f}   RMSE = {np.sqrt(ss_res/len(y_data)):.4f}")

    print()
    print("--- Polynomial fit ---")
    x_poly = np.linspace(-2, 2, 50)
    y_poly = 2*x_poly**3 - x_poly**2 + 3*x_poly - 1 + rng.normal(0, 0.5, 50)

    coeffs = np.polyfit(x_poly, y_poly, deg=3)
    y_pred = np.polyval(coeffs, x_poly)
    print(f"  Fitted coefficients (degree 3): {coeffs.round(4)}")
    print(f"  True coefficients:              [2, -1, 3, -1]")
    print(f"  R² = {1 - np.sum((y_poly-y_pred)**2)/np.sum((y_poly-y_poly.mean())**2):.4f}")

    print()
    print("💡 curve_fit() returns (popt, pcov):")
    print("   popt → optimal parameter values")
    print("   pcov → covariance matrix of parameters")
    print("   perr = np.sqrt(np.diag(pcov)) → 1σ standard errors")


    # ══════════════════════════════════════════════════════════════════
    # PART 4 — SCIPY.INTEGRATE
    # ══════════════════════════════════════════════════════════════════

    print("\n" + "═" * 70)
    print("PART 4 — scipy.integrate  (Numerical Integration & ODEs)")
    print("═" * 70)


    # ------------------------------------------------------------------
    # 12. NUMERICAL INTEGRATION
    # ------------------------------------------------------------------
    section("12. NUMERICAL INTEGRATION")

    print("--- quad() — definite integral of a function ---")

    # ∫₀^π sin(x) dx = 2
    result, error = integrate.quad(np.sin, 0, np.pi)
    print(f"  ∫₀^π sin(x) dx = {result:.10f}  (exact = 2.0)")
    print(f"  Estimated error: {error:.2e}")

    # ∫₀^∞ e^(-x²) dx = √π/2
    import math
    result2, error2 = integrate.quad(lambda x: np.exp(-x**2), 0, np.inf)
    print(f"  ∫₀^∞ e^(-x²) dx = {result2:.10f}  (exact = √π/2 = {math.sqrt(math.pi)/2:.10f})")

    # Function with parameters
    def gaussian(x, mu, sigma):
        return np.exp(-0.5*((x-mu)/sigma)**2) / (sigma*np.sqrt(2*np.pi))

    result3, _ = integrate.quad(gaussian, -np.inf, np.inf, args=(0, 1))
    print(f"  ∫ N(0,1) dx over ℝ = {result3:.10f}  (exact = 1.0)")

    print()
    print("--- dblquad() — double integral ---")
    # ∫₀¹ ∫₀¹ (x + y) dx dy = 1
    def integrand(y, x):   # Note: inner variable first in dblquad!
        return x + y

    result_2d, error_2d = integrate.dblquad(
        integrand,
        0, 1,             # x limits
        lambda x: 0,      # y lower limit (can depend on x)
        lambda x: 1       # y upper limit (can depend on x)
    )
    print(f"  ∫₀¹∫₀¹ (x+y) dx dy = {result_2d:.10f}  (exact = 1.0)")

    print()
    print("--- trapezoid() and simpson() — integrate from discrete data ---")
    x_pts = np.linspace(0, np.pi, 100)
    y_pts = np.sin(x_pts)

    trap_result  = integrate.trapezoid(y_pts, x_pts)
    simp_result  = integrate.simpson(y_pts, x=x_pts)
    print(f"  ∫₀^π sin(x) dx via trapezoid: {trap_result:.8f}")
    print(f"  ∫₀^π sin(x) dx via simpson:   {simp_result:.8f}")
    print(f"  Exact = 2.0")

    print()
    print("--- cumulative_trapezoid() — running integral ---")
    cumul = integrate.cumulative_trapezoid(y_pts, x_pts, initial=0)
    print(f"  Cumulative integral shape: {cumul.shape}")
    print(f"  Final value: {cumul[-1]:.8f}  (should be ≈ 2.0)")

    print()
    print("  INTEGRATION METHODS:")
    print(f"  {'quad(f, a, b)':<35} Adaptive integration of 1D function")
    print(f"  {'dblquad(f, xa,xb, ya,yb)':<35} Double integral")
    print(f"  {'tplquad(f, ...)':<35} Triple integral")
    print(f"  {'trapezoid(y, x)':<35} Trapezoidal rule (from data)")
    print(f"  {'simpson(y, x)':<35} Simpson's rule (from data, more accurate)")
    print(f"  {'cumulative_trapezoid(y, x)':<35} Running integral from data")


    # ------------------------------------------------------------------
    # 13. ORDINARY DIFFERENTIAL EQUATIONS (ODEs)
    # ------------------------------------------------------------------
    section("13. ORDINARY DIFFERENTIAL EQUATIONS (ODEs)")

    print("""
  ODE form:   dy/dt = f(t, y)
  solve_ivp() solves Initial Value Problems (IVP):
    y(t₀) = y₀  →  find y(t) for t in [t₀, t_end]
    """)

    print("--- Example 1: Exponential decay  dy/dt = -k·y ---")
    def exp_decay(t, y, k=0.3):
        return -k * y

    t_span  = (0, 20)
    t_eval  = np.linspace(0, 20, 200)
    y0      = [10.0]   # initial condition

    sol = integrate.solve_ivp(
        fun=exp_decay,
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method='RK45',     # Runge-Kutta 4(5)
        args=(0.3,),       # extra args passed to fun
        rtol=1e-8,         # relative tolerance
        atol=1e-10,        # absolute tolerance
    )

    print(f"  dy/dt = -0.3·y,  y(0) = 10")
    print(f"  Solver status:    {sol.message}")
    print(f"  Solution shape:   t={sol.t.shape}  y={sol.y.shape}")
    print(f"  y(0)  = {sol.y[0, 0]:.4f}  (exact: 10.0000)")
    print(f"  y(10) = {sol.y[0, 100]:.4f}  (exact: {10*np.exp(-0.3*10):.4f})")
    print(f"  y(20) = {sol.y[0, -1]:.4f}  (exact: {10*np.exp(-0.3*20):.4f})")

    print()
    print("--- Example 2: SIR epidemic model (system of ODEs) ---")
    print("""
  dS/dt = -β·S·I/N
  dI/dt =  β·S·I/N - γ·I
  dR/dt =  γ·I

  S = Susceptible,  I = Infected,  R = Recovered
  β = transmission rate,  γ = recovery rate
  R₀ = β/γ  (basic reproduction number)
    """)

    def sir_model(t, y, N, beta, gamma):
        S, I, R = y
        dS = -beta * S * I / N
        dI =  beta * S * I / N - gamma * I
        dR =  gamma * I
        return [dS, dI, dR]

    N     = 10_000   # population
    beta  = 0.3      # transmission rate
    gamma = 0.05     # recovery rate
    R0    = beta / gamma

    I0    = 10       # initial infected
    S0    = N - I0
    R0_ic = 0

    t_sir = np.linspace(0, 200, 1000)
    sol_sir = integrate.solve_ivp(
        sir_model,
        t_span=(0, 200),
        y0=[S0, I0, R0_ic],
        t_eval=t_sir,
        args=(N, beta, gamma),
        method='RK45',
        rtol=1e-8
    )

    peak_idx = np.argmax(sol_sir.y[1])
    print(f"  Population N={N}  β={beta}  γ={gamma}  R₀={R0:.1f}")
    print(f"  Peak infections:  {sol_sir.y[1, peak_idx]:.0f} people "
          f"at day {sol_sir.t[peak_idx]:.1f}")
    print(f"  Final recovered:  {sol_sir.y[2, -1]:.0f} people "
          f"({sol_sir.y[2,-1]/N*100:.1f}%)")
    print(f"  Final susceptible:{sol_sir.y[0, -1]:.0f} people "
          f"({sol_sir.y[0,-1]/N*100:.1f}%)")

    print()
    print("--- Example 3: Van der Pol oscillator (non-linear ODE) ---")
    def van_der_pol(t, y, mu=2.0):
        x, v = y
        dxdt = v
        dvdt = mu * (1 - x**2) * v - x
        return [dxdt, dvdt]

    sol_vdp = integrate.solve_ivp(
        van_der_pol,
        t_span=(0, 30),
        y0=[2.0, 0.0],
        t_eval=np.linspace(0, 30, 1000),
        args=(2.0,),
        method='Radau',    # Radau is better for stiff equations
        rtol=1e-6
    )
    print(f"  Van der Pol (μ=2): solved with Radau (stiff solver)")
    y: np.ndarray = sol_vdp.y
    print(f" x range: [{y[0].min():.4f}, {y[0].max():.4f}]")
    print(f" v range: [{y[1].min():.4f}, {y[1].max():.4f}]")

    print()
    print("  ODE SOLVER METHODS:")
    print(f"  {'RK45 (default)':<20} Runge-Kutta 4(5), non-stiff equations")
    print(f"  {'RK23':<20} Runge-Kutta 2(3), non-stiff, faster")
    print(f"  {'Radau':<20} Implicit, stiff equations ★")
    print(f"  {'BDF':<20} Backward Differentiation, stiff equations")
    print(f"  {'DOP853':<20} Runge-Kutta 8th order, high accuracy")
    print()
    print("  💡 Stiff equations: use Radau or BDF")
    print("     (stiff = system with widely varying time scales,")
    print("      e.g. fast chemistry, electrical circuits)")


    # ══════════════════════════════════════════════════════════════════
    # PART 5 — SCIPY.SPECIAL
    # ══════════════════════════════════════════════════════════════════

    print("\n" + "═" * 70)
    print("PART 5 — scipy.special  (Special Functions)")
    print("═" * 70)


    # ------------------------------------------------------------------
    # 14. SPECIAL MATHEMATICAL FUNCTIONS
    # ------------------------------------------------------------------
    section("14. SPECIAL MATHEMATICAL FUNCTIONS")

    print("--- Gamma and related functions ---")
    print(f"  Γ(5)           = {special.gamma(5):.1f}  (= 4! = 24)")
    print(f"  Γ(0.5)         = {special.gamma(0.5):.6f}  (= √π)")
    print(f"  log Γ(100)     = {special.gammaln(100):.4f}  (avoids overflow)")
    print(f"  Beta(2, 3)     = {special.beta(2, 3):.6f}  (= Γ(2)Γ(3)/Γ(5))")
    print(f"  Digamma ψ(1)   = {special.digamma(1):.6f}  (= -Euler-Mascheroni)")

    print()
    print("--- Error functions (Gaussian integrals) ---")
    print(f"  erf(1)         = {special.erf(1):.6f}  (= ∫₀¹ 2/√π e^(-t²) dt)")
    print(f"  erfc(1)        = {special.erfc(1):.6f}  (= 1 - erf(1))")
    print(f"  P(-1≤X≤1) for N(0,1) = {special.erf(1/np.sqrt(2)):.6f}")

    print()
    print("--- Bessel functions (waves, cylinders) ---")
    x = np.array([0, 1, 2, 3, 5])
    print(f"  J₀(x) = {special.j0(x).round(4)}  (0th order Bessel, 1st kind)")
    print(f"  J₁(x) = {special.j1(x).round(4)}  (1st order Bessel, 1st kind)")

    print()
    print("--- Combinatorial and number theory ---")
    print(f"  comb(10, 3)    = {special.comb(10, 3):.0f}   (C(10,3))")
    print(f"  perm(10, 3)    = {special.perm(10, 3):.0f}  (P(10,3))")
    print(f"  factorial(10)  = {special.factorial(10):.0f}")

    print()
    print("--- Logistic / sigmoid functions ---")
    x = np.array([-3, -1, 0, 1, 3])
    print(f"  x              = {x}")
    print(f"  expit(x)       = {special.expit(x).round(4)}  (sigmoid: 1/(1+e^-x))")
    print(f"  logit(p)       = {special.logit(np.array([0.1, 0.5, 0.9])).round(4)}")
    print(f"  log_softmax(x) = {special.log_softmax(x.astype(float)).round(4)}")
    print()
    print("  💡 special.expit() is the numerically stable sigmoid function.")
    print("     Use it in ML instead of 1/(1+np.exp(-x)) to avoid overflow.")


    # ------------------------------------------------------------------
    # 15. PRACTICAL EXAMPLES (combining modules)
    # ------------------------------------------------------------------
    section("15. PRACTICAL EXAMPLES")

    print("--- Example 1: A/B Test — complete analysis ---")
    rng = np.random.default_rng(42)

    # Simulate conversion rates: A=10%, B=13%
    n_A, n_B = 1000, 1000
    conv_A = rng.binomial(1, 0.10, n_A)
    conv_B = rng.binomial(1, 0.13, n_B)

    rate_A = conv_A.mean()
    rate_B = conv_B.mean()
    lift   = (rate_B - rate_A) / rate_A * 100

    # Two-proportion z-test
    from scipy.stats import chi2_contingency
    table = np.array([[conv_A.sum(), n_A - conv_A.sum()],
                       [conv_B.sum(), n_B - conv_B.sum()]])
    chi2_stat, p_val, _, _ = chi2_contingency(table, correction=False)

    # 95% CI on the difference (using normal approximation)
    p_pool = (conv_A.sum() + conv_B.sum()) / (n_A + n_B)
    se_diff = np.sqrt(p_pool*(1-p_pool)*(1/n_A + 1/n_B))
    diff    = rate_B - rate_A
    z_crit  = stats.norm.ppf(0.975)
    ci_diff = (diff - z_crit*se_diff, diff + z_crit*se_diff)

    print(f"  Control A:   rate = {rate_A:.4f}  (n={n_A})")
    print(f"  Variant  B:  rate = {rate_B:.4f}  (n={n_B})")
    print(f"  Lift:        {lift:+.2f}%")
    print(f"  χ² = {chi2_stat:.4f}   p = {p_val:.4f}")
    print(f"  95% CI on difference: ({ci_diff[0]:.4f}, {ci_diff[1]:.4f})")
    significant = p_val < 0.05
    print(f"  → {'Statistically significant ✓' if significant else 'Not significant ✗'} (α=0.05)")

    print()
    print("--- Example 2: Fitting a learning curve model ---")
    # Power law: accuracy = a * (1 - b * n^(-c))
    def learning_curve_model(n, a, b, c):
        return a * (1 - b * np.power(n, -c))

    rng   = np.random.default_rng(1)
    sizes = np.array([50, 100, 200, 500, 1000, 2000, 5000, 10000])
    true_acc = learning_curve_model(sizes, a=0.95, b=0.8, c=0.4)
    noisy_acc = np.clip(true_acc + rng.normal(0, 0.008, len(sizes)), 0, 1)

    popt, pcov = optimize.curve_fit(
        learning_curve_model, sizes, noisy_acc,
        p0=[0.9, 0.7, 0.3],
        bounds=([0.5, 0, 0], [1.0, 2.0, 2.0])
    )
    perr = np.sqrt(np.diag(pcov))

    print(f"  Power law fit: accuracy = a·(1 - b·n^(-c))")
    print(f"  {'Param':<8} {'True':<8} {'Fitted':<10} {'Std Err'}")
    for name, true, fit, err in zip(['a','b','c'], [0.95,0.8,0.4], popt, perr):
        print(f"  {name:<8} {true:<8.4f} {fit:<10.4f} ±{err:.4f}")

    # Predict: how much data needed for 90% accuracy?
    def needed_samples(target, a, b, c):
        return optimize.brentq(
            lambda n: learning_curve_model(n, a, b, c) - target,
            10, 1e7
        )

    n_90 = needed_samples(0.90, *popt)
    print(f"\n  Predicted samples for 90% accuracy: {n_90:.0f}")

    print()
    print("--- Example 3: Maximum Likelihood Estimation ---")
    # Fit a mixture of two normals to data
    rng     = np.random.default_rng(42)
    data_mx = np.concatenate([rng.normal(0, 1, 300),
                               rng.normal(5, 1.5, 200)])

    def neg_log_likelihood(params, data):
        mu1, sigma1, mu2, sigma2, w = params
        if sigma1 <= 0 or sigma2 <= 0 or not (0 < w < 1):
            return np.inf
        ll = np.log(
            w   * stats.norm.pdf(data, mu1, sigma1) +
            (1-w) * stats.norm.pdf(data, mu2, sigma2)
        )
        return -ll.sum()

    x0      = [0, 1, 4, 1.5, 0.6]
    bounds_ = [(-5,5),(0.1,5),(-5,10),(0.1,5),(0.01,0.99)]
    result  = optimize.minimize(neg_log_likelihood, x0=x0,
                                 args=(data_mx,),
                                 bounds=bounds_,
                                 method='L-BFGS-B')

    mu1, s1, mu2, s2, w = result.x
    print(f"  Gaussian mixture MLE:")
    print(f"  Component 1: μ={mu1:.3f}  σ={s1:.3f}  weight={w:.3f}  (true: 0, 1, 0.6)")
    print(f"  Component 2: μ={mu2:.3f}  σ={s2:.3f}  weight={1-w:.3f}  "
          f"(true: 5, 1.5, 0.4)")


    # ------------------------------------------------------------------
    # 16. COMMON MISTAKES
    # ------------------------------------------------------------------
    section("16. COMMON MISTAKES")
    print("""
  Mistake 1 — Using numpy.linalg when scipy.linalg is more stable:
    np.linalg.solve(A, b)       ← works but less robust
    linalg.solve(A, b)          ← preferred: better error handling

  Mistake 2 — Using matrix inverse to solve a linear system:
    x = linalg.inv(A) @ b       ← SLOW and NUMERICALLY UNSTABLE
    x = linalg.solve(A, b)      ← FAST and STABLE ✅

  Mistake 3 — Forgetting ddof=1 for sample statistics:
    np.std(data)                 ← population std (ddof=0)
    np.std(data, ddof=1)         ← sample std (ddof=1) ← use for data
    stats.sem(data)              ← standard error of mean (already ddof=1)

  Mistake 4 — Misinterpreting p-values:
    p < 0.05 → statistically significant (NOT "large effect"!)
    Always report effect size (Cohen's d) alongside p-value.
    p-value depends on sample size — with n=100,000, almost anything is significant.

  Mistake 5 — Using ttest_ind on non-normal data:
    Check normality first with stats.shapiro()
    If p < 0.05 → use stats.mannwhitneyu() instead

  Mistake 6 — Wrong argument order in dblquad:
    integrate.dblquad(f, x_lo, x_hi, y_lo, y_hi)
    The function signature must be f(y, x) — inner variable first!

  Mistake 7 — Not providing good initial guesses to curve_fit:
    popt, pcov = optimize.curve_fit(f, x, y)       ← risky
    popt, pcov = optimize.curve_fit(f, x, y, p0=good_guess)  ← robust

  Mistake 8 — Stiff ODEs with the wrong solver:
    solve_ivp(f, ..., method='RK45')  ← slow/fails for stiff equations
    solve_ivp(f, ..., method='Radau') ← correct for stiff equations
    """)


    # ------------------------------------------------------------------
    # 17. QUICK REFERENCE TABLE
    # ------------------------------------------------------------------
    section("17. QUICK REFERENCE TABLE")
    print()
    print(f"  {'Function':<45} {'Description'}")
    print(f"  {'-'*45} {'-'*35}")

    ref = [
        ("DISTRIBUTIONS (scipy.stats)", ""),
        ("stats.norm(loc, scale)",                   "Normal distribution"),
        ("stats.t(df)",                              "Student's t"),
        ("stats.chi2(df)",                           "Chi-squared"),
        ("stats.f(dfn, dfd)",                        "F distribution"),
        ("stats.binom(n, p)",                        "Binomial (discrete)"),
        ("stats.poisson(mu)",                        "Poisson (discrete)"),
        ("dist.pdf/cdf/ppf/sf/rvs()",                "PDF/CDF/quantile/survival/sample"),
        ("dist.fit(data)",                           "MLE parameter estimation"),
        ("DESCRIPTIVE STATS (scipy.stats)", ""),
        ("stats.describe(data)",                     "Full summary in one call"),
        ("stats.sem(data)",                          "Standard error of mean"),
        ("stats.iqr(data)",                          "Interquartile range"),
        ("stats.skew(data) / stats.kurtosis(data)",  "Skewness / kurtosis"),
        ("HYPOTHESIS TESTS (scipy.stats)", ""),
        ("stats.ttest_1samp(a, popmean)",            "One-sample t-test"),
        ("stats.ttest_ind(a, b, equal_var)",         "Two-sample t-test"),
        ("stats.ttest_rel(a, b)",                    "Paired t-test"),
        ("stats.f_oneway(g1, g2, ...)",              "One-way ANOVA"),
        ("stats.chi2_contingency(table)",            "Chi-squared independence"),
        ("stats.shapiro(data)",                      "Shapiro-Wilk normality"),
        ("stats.mannwhitneyu(a, b)",                 "Non-param: 2 groups"),
        ("stats.kruskal(g1, g2, ...)",               "Non-param: 3+ groups"),
        ("stats.pearsonr / spearmanr(x, y)",         "Correlation tests"),
        ("stats.kstest(data, 'norm', args=(μ,σ))",   "Kolmogorov-Smirnov test"),
        ("CONFIDENCE INTERVALS", ""),
        ("stats.t.interval(0.95, df, loc, scale)",   "t-based CI for mean"),
        ("stats.bootstrap((data,), statistic)",      "Bootstrap CI"),
        ("LINEAR ALGEBRA (scipy.linalg)", ""),
        ("linalg.solve(A, b)",                       "Solve Ax = b ★"),
        ("linalg.lstsq(A, b)",                       "Least squares Ax ≈ b"),
        ("linalg.lu(A)",                             "LU decomposition"),
        ("linalg.cholesky(A)",                       "Cholesky (SPD matrices)"),
        ("linalg.qr(A)",                             "QR decomposition"),
        ("linalg.svd(A)",                            "SVD decomposition"),
        ("linalg.eig(A) / linalg.eigh(A)",           "Eigendecomposition"),
        ("linalg.inv(A) / linalg.pinv(A)",           "Inverse / pseudoinverse"),
        ("linalg.det(A) / linalg.norm(A)",           "Determinant / norm"),
        ("linalg.expm(A) / linalg.logm(A)",          "Matrix exponential / log"),
        ("OPTIMIZATION (scipy.optimize)", ""),
        ("optimize.minimize(f, x0, method, bounds)", "Unconstrained/bounded min"),
        ("optimize.minimize_scalar(f, bounds)",      "1D minimization"),
        ("optimize.brentq(f, a, b)",                 "1D root finding ★"),
        ("optimize.fsolve(system, x0)",              "Multi-dim root finding"),
        ("optimize.curve_fit(f, x, y, p0)",          "Nonlinear curve fitting"),
        ("INTEGRATION (scipy.integrate)", ""),
        ("integrate.quad(f, a, b)",                  "Definite integral of function"),
        ("integrate.dblquad(f, xa,xb, ya,yb)",       "Double integral"),
        ("integrate.trapezoid(y, x)",                "Trapezoidal rule (data)"),
        ("integrate.simpson(y, x)",                  "Simpson's rule (data)"),
        ("integrate.solve_ivp(f, t_span, y0)",       "Solve ODE system ★"),
        ("SPECIAL (scipy.special)", ""),
        ("special.expit(x)",                         "Sigmoid (numerically stable)"),
        ("special.logit(p)",                         "Logit function"),
        ("special.gamma(x) / special.gammaln(x)",    "Gamma function / log-gamma"),
        ("special.erf(x) / special.erfc(x)",         "Error function"),
        ("special.comb(n, k) / special.perm(n, k)",  "Combinations / permutations"),
    ]

    for item, desc in ref:
        if desc == "":
            print(f"\n  ── {item} {'─'*(65-len(item))}")
        else:
            print(f"  {item:<45} {desc}")

    print()
    print("Done!\n")


main()


"""
SUMMARY — SCIPY
=======================================================

IMPORT PATTERN:
  from scipy import stats, linalg, optimize, integrate, special

SCIPY.STATS:
  Distributions:
    stats.norm(loc, scale).pdf/cdf/ppf/sf/rvs/fit
    stats.t / chi2 / f / binom / poisson / expon / beta / gamma

  Descriptive:
    stats.describe(data)        → full summary
    stats.sem / iqr / skew / kurtosis

  Hypothesis Tests:
    ttest_1samp / ttest_ind / ttest_rel  → t-tests
    f_oneway                             → ANOVA
    chi2_contingency                     → categorical independence
    shapiro / normaltest                 → normality
    mannwhitneyu / wilcoxon / kruskal    → non-parametric
    pearsonr / spearmanr                 → correlation

  CIs:
    stats.t.interval(0.95, df, loc, scale)
    stats.bootstrap((data,), statistic)

SCIPY.LINALG:
  linalg.solve(A, b)      → Ax=b (NEVER use inv(A)@b!)
  linalg.lstsq(A, b)      → overdetermined least squares
  linalg.lu / cholesky / qr / svd / eig / eigh
  linalg.expm / logm / sqrtm  → matrix functions

SCIPY.OPTIMIZE:
  optimize.minimize(f, x0, method, bounds, constraints)
  optimize.brentq(f, a, b)       → robust 1D root finding
  optimize.fsolve(system, x0)    → multi-dim roots
  optimize.curve_fit(f, x, y, p0) → returns (popt, pcov)
    perr = np.sqrt(np.diag(pcov))

SCIPY.INTEGRATE:
  integrate.quad(f, a, b)             → adaptive integration
  integrate.trapezoid / simpson        → from discrete data
  integrate.solve_ivp(f, t_span, y0,  → ODE solver
      method='RK45'/'Radau'/'BDF')

SCIPY.SPECIAL:
  special.expit(x)    → sigmoid (stable)
  special.erf / erfc  → error functions
  special.gamma / gammaln / beta
  special.comb / perm / factorial

KEY RULES:
  • Use linalg.solve(A,b), NEVER inv(A)@b
  • ddof=1 for sample statistics
  • p-value ≠ effect size — always report both
  • Check normality before t-test (use shapiro)
  • Stiff ODEs → method='Radau' or 'BDF'
  • curve_fit → always provide p0 initial guess

REMEMBER:
  "SciPy is NumPy with scientific algorithms:
   statistics for analysis, linalg for numerical work,
   optimize for fitting, integrate for simulation."
"""