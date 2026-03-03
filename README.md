# 🐍 PyDataStack

> **Executable Python reference guides for the core Data Science & ML stack.**
> Each file runs, prints its output, and teaches by example.

---

## 📖 What is PyDataStack?

PyDataStack is a collection of **self-contained, executable `.py` reference files** — one per library — covering the entire Python data stack from mathematical foundations to interactive visualizations.

Each file is structured as a **hands-on reference guide**:
- ✅ Runs from top to bottom with zero errors
- 💡 Explains *why*, not just *what*
- ⚠️ Highlights common mistakes and pitfalls
- 📋 Ends with a complete quick-reference table and summary

---

## 📦 The Stack

| File | Library | Topics Covered |
|------|---------|----------------|
| [`Math.py`](Math.py) | `math` | Constants, rounding, powers, trigonometry, combinatorics, float precision |
| [`Numpy.py`](Numpy.py) | `numpy` | Arrays, indexing, broadcasting, linear algebra, random, NaN handling, ML patterns |
| [`Pandas.py`](Pandas.py) | `pandas` | DataFrames, I/O, cleaning, groupby, merge, pivot, time series, ML preparation |
| [`Matplotlib.py`](Matplotlib.py) | `matplotlib` | Line, scatter, bar, histogram, subplots, GridSpec, ML plots, customization |
| [`Seaborn.py`](Seaborn.py) | `seaborn` | Distributions, categorical, heatmaps, pairplot, facet grids, Matplotlib integration |
| [`Plotly.py`](Plotly.py) | `plotly` | Interactive charts, 3D, maps, Dash dashboards, ML visualizations |
| [`Scipy.py`](Scipy.py) | `scipy` | Statistics, hypothesis tests, linear algebra, optimization, ODEs, special functions |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com:JoelBrunoFerreira/py-data-stack.git
cd PyDataStack

# Install dependencies
pip install numpy pandas matplotlib seaborn plotly scipy

# Optional (for Plotly PNG export)
pip install kaleido pandas-stubs 

# Run any reference file
python Math.py
python Numpy.py
python Pandas.py
# ... etc
```

---

## 📚 What's Inside Each File

### 🔢 `Math.py` — Python `math` module
Standard library mathematical functions. No dependencies required.

**Sections:** Constants · Rounding · Powers & Roots · Logarithms · Trigonometry · Combinatorics · Float Precision · Practical Examples

---

### 🔢 `Numpy.py` — NumPy
The foundation of the entire Python data stack. Covers arrays, vectorized operations, and linear algebra.

**Sections:** Array Creation · Data Types · Indexing & Slicing · Reshaping · Vectorized Operations · Broadcasting · Aggregates · Linear Algebra · Random · Sorting · NaN Handling · ML Patterns (normalization, one-hot, cosine similarity, F1)

---

### 🐼 `Pandas.py` — Pandas
The workhorse of data analysis. From raw CSV to ML-ready feature matrix.

**Sections:** Series & DataFrame · Reading & Writing (CSV, Excel, JSON, SQL, Parquet) · Exploration · Indexing (loc/iloc) · Adding & Modifying Columns · Data Cleaning · String Operations · Apply/Map/Vectorized · GroupBy & Aggregation · Pivot Tables · Merge/Join/Concat · Reshaping (melt/stack) · Time Series · Categorical Data · **ML Preparation Pipeline** (imputation → encoding → scaling → feature engineering → train/test split)

---

### 📊 `Matplotlib.py` — Matplotlib
Full control over static visualizations. Saves all charts as PNG files when run as a script.

**Sections:** pyplot vs OOP Interface · Figure Anatomy · Line · Scatter · Bar · Histogram · Box & Violin · Subplots & GridSpec · Customization (annotations, shading, styles) · **ML Plots** (confusion matrix, ROC curves, learning curves, feature importance)

---

### 🎨 `Seaborn.py` — Seaborn
Statistical visualization with a beautiful high-level API. Tight integration with Pandas DataFrames.

**Sections:** Themes & Palettes · Axes-level vs Figure-level · Distributions (histplot, kdeplot, ecdfplot) · Box/Violin/Strip/Swarm · Scatter & Line (with error bands) · Categorical (barplot, countplot, pointplot) · Heatmaps & Correlation · Pairplot & Jointplot · Facet Grids (displot, relplot, catplot) · Seaborn + Matplotlib Integration

---

### 📈 `Plotly.py` — Plotly Express
Interactive charts that run in the browser. Saves `.html` files (fully interactive, no server needed) when run as a script.

**Sections:** Core Concepts (fig.data / fig.layout) · Line (range slider, hovermode) · Scatter (trendlines, animation) · Bar (grouped, stacked, horizontal) · Histogram (with marginals) · Box & Violin · Pie/Donut/Sunburst/Treemap · Heatmaps · **3D** (scatter, surface, line) · **Maps** (choropleth, bubble, density) · Multi-panel Layouts (make_subplots) · **ML Plots** (feature importance, confusion matrix, ROC, learning curves, parallel coordinates) · **Dash Dashboard** (complete minimal example) · Export & Sharing

---

### 🔬 `Scipy.py` — SciPy
Scientific computing algorithms. Organized into 5 parts.

**Part 1 — scipy.stats:** Probability Distributions · Descriptive Statistics · Hypothesis Testing (t-tests, ANOVA, chi², normality, non-parametric, correlation) · Bootstrap Confidence Intervals

**Part 2 — scipy.linalg:** LU / Cholesky / QR / SVD / Eigendecomposition · Solving Linear Systems · Least Squares · Matrix Functions (expm, logm, sqrtm)

**Part 3 — scipy.optimize:** Minimization (constrained & unconstrained) · Root Finding · Curve Fitting (with parameter uncertainty)

**Part 4 — scipy.integrate:** Numerical Integration · ODE Solvers (exponential decay, SIR epidemic model, Van der Pol oscillator)

**Part 5 — scipy.special:** Sigmoid (expit) · Error functions · Gamma · Combinatorics

---

## 🗺️ Learning Path

```
Math.py  →  Numpy.py  →  Pandas.py  →  Matplotlib.py
                                              ↓
                              Seaborn.py  ←──┘
                                  ↓
                             Plotly.py
                                  ↓
                             Scipy.py
```

> **Recommended order for beginners:** follow the path above.
> **For data analysts:** focus on Pandas → Seaborn → Plotly.
> **For ML engineers:** focus on Numpy → Pandas → Scipy → Matplotlib (ML plots).

---

## 🧰 Dependencies

```txt
numpy
pandas
matplotlib
seaborn
plotly
scipy
openpyxl      # pandas Excel support
kaleido       # plotly PNG/PDF export (optional)
```

Install all at once:
```bash
pip install numpy pandas matplotlib seaborn plotly scipy openpyxl kaleido
```

---

## 💡 Design Philosophy

Each reference file follows the same conventions:

| Convention | Meaning |
|---|---|
| `💡` | Tip or best practice |
| `⚠️` | Warning or common pitfall |
| `✅` | Recommended approach |
| `❌` | Approach to avoid |
| `★` | Especially useful / most common pattern |

Every section ends with a concise explanation of **key parameters**, so you can use the file as a quick lookup without re-reading the full examples.

---

## 📄 Author

Joel Bruno Ferreira — but feel free to use, adapt, and share.

---

*Built with 🐍 Python · Maintained as a living reference — contributions welcome!*\
*btw... I use Arch 😎* 