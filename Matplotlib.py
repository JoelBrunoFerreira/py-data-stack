"""
MATPLOTLIB - COMPLETE GUIDE
=============================

Matplotlib is Python's foundational plotting library. It provides full control
over every element of a figure — from simple line charts to complex multi-panel
layouts and ML-specific visualizations.

Key Characteristics:
- Two interfaces: pyplot (quick) and OOP (recommended for complex plots)
- Works in scripts (.py), Jupyter Notebooks, and web apps
- Foundation for Seaborn, Pandas .plot(), and many other libraries
- Exports to PNG, PDF, SVG, EPS, and more

Installation:
  pip install matplotlib

Common Uses:
- Exploratory data analysis (EDA)
- Model evaluation (ROC, confusion matrix, learning curves)
- Scientific publication figures
- Dashboard and report generation
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from IPython import get_ipython

# ──────────────────────────────────────────────────────────────────────────────
# ENVIRONMENT SETUP
# ──────────────────────────────────────────────────────────────────────────────
# Detect if running in Jupyter or as a plain script and configure accordingly.
# In a script we save figures to files; in Jupyter they render inline.

def is_jupyter():
    try:
        shell = get_ipython().__class__.__name__
        return shell in ('ZMQInteractiveShell', 'TerminalInteractiveShell')
    except NameError:
        return False

JUPYTER = is_jupyter()
SAVE    = not JUPYTER          # save PNGs when running as a script

if JUPYTER:
    # Renders plots inline in the notebook cell
    # %matplotlib inline   ← run this magic command in the first cell
    print("Running in Jupyter — plots will render inline.")
else:
    # Non-interactive backend: no GUI window, just file output
    matplotlib.use('Agg')
    print("Running as script — plots will be saved as PNG files.")

OUTDIR = "matplotlib_output"   # folder for saved figures

import os
os.makedirs(OUTDIR, exist_ok=True)


def show_or_save(fig, filename):
    """
    Unified display helper.
    - Jupyter : renders the figure inline then closes it.
    - Script  : saves to PNG then closes it (no GUI popup).
    """
    if JUPYTER:
        plt.show()
    else:
        path = os.path.join(OUTDIR, filename)
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  → Saved: {path}")
    plt.close(fig)


def main():

    print("=== MATPLOTLIB - COMPLETE GUIDE ===\n")
    print(f"Matplotlib version: {matplotlib.__version__}\n")


    # ------------------------------------------------------------------
    # 1. TWO INTERFACES: pyplot vs OOP
    # ------------------------------------------------------------------
    print("1. TWO INTERFACES: pyplot vs OOP")
    print("-" * 70)

    print("""
  PYPLOT INTERFACE — quick and simple:
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title("My Plot")
    plt.show()

  OOP INTERFACE — recommended for anything beyond trivial plots:
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    ax.set_title("My Plot")
    plt.show()

  KEY DIFFERENCE:
    pyplot  → implicit "current axes" (plt.xlabel, plt.title, ...)
    OOP     → explicit axes object  (ax.set_xlabel, ax.set_title, ...)

  💡 Always use the OOP interface (fig, ax = plt.subplots()).
     It is explicit, composable, and works cleanly in functions.
     pyplot is fine for quick one-liners in a Jupyter cell.
    """)


    # ------------------------------------------------------------------
    # 2. ANATOMY OF A FIGURE
    # ------------------------------------------------------------------
    print("2. ANATOMY OF A FIGURE")
    print("-" * 70)
    print("""
  Figure          → the entire canvas (the window / the PNG file)
  Axes (ax)       → one plot area (has x-axis, y-axis, title, etc.)
  Axis            → the x-axis or y-axis object (ticks, labels, limits)
  Artist          → everything drawn: lines, text, patches, images

  fig, ax = plt.subplots(figsize=(10, 6))
                            └─ width, height in inches

  ax methods you'll use constantly:
    ax.set_title()   ax.set_xlabel()   ax.set_ylabel()
    ax.set_xlim()    ax.set_ylim()     ax.legend()
    ax.grid()        ax.set_xticks()   ax.tick_params()
    """)


    # ------------------------------------------------------------------
    # 3. LINE PLOT
    # ------------------------------------------------------------------
    print("3. LINE PLOT")
    print("-" * 70)

    x  = np.linspace(0, 2 * np.pi, 300)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.exp(-x / 5)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y1, color='#2E75B6', linewidth=2,   linestyle='-',  label='sin(x)')
    ax.plot(x, y2, color='#C55A11', linewidth=2,   linestyle='--', label='cos(x)')
    ax.plot(x, y3, color='#375623', linewidth=1.5, linestyle=':',  label='sin(x)·e^(-x/5)')

    ax.set_title('Line Plot — Trigonometric Functions', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('x (radians)', fontsize=12)
    ax.set_ylabel('Amplitude',   fontsize=12)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.3, 1.3)
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='-')   # horizontal zero line
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    # Custom x-ticks with π labels
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'], fontsize=11)

    fig.tight_layout()
    show_or_save(fig, '03_line_plot.png')

    print("""
  KEY PARAMETERS for ax.plot():
    color       → '#hex', 'red', 'C0', (r,g,b,a)
    linewidth   → thickness in points
    linestyle   → '-'  '--'  '-.'  ':'
    marker      → 'o'  's'  '^'  'D'  '+'  'x'  '.'
    markersize  → size of markers
    alpha       → transparency 0.0–1.0
    label       → text for legend (call ax.legend() to display)
    zorder      → drawing order (higher = on top)

  USEFUL ax methods:
    ax.axhline(y)         → horizontal reference line
    ax.axvline(x)         → vertical reference line
    ax.axhspan(y1, y2)    → horizontal shaded band
    ax.fill_between(x, y1, y2, alpha=0.2)   → shaded area between two curves
    """)


    # ------------------------------------------------------------------
    # 4. SCATTER PLOT
    # ------------------------------------------------------------------
    print("4. SCATTER PLOT")
    print("-" * 70)

    rng = np.random.default_rng(42)
    n   = 200

    # Simulate two classes
    x0 = rng.normal(2,   1.2, n)
    y0 = rng.normal(2,   1.2, n)
    x1 = rng.normal(5,   1.2, n)
    y1 = rng.normal(5,   1.2, n)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: basic scatter with color map
    all_x    = np.concatenate([x0, x1])
    all_y    = np.concatenate([y0, y1])
    all_vals = np.concatenate([np.zeros(n), np.ones(n)])

    sc = axes[0].scatter(all_x, all_y, c=all_vals, cmap='coolwarm',
                         alpha=0.7, edgecolors='white', linewidths=0.4, s=40)
    plt.colorbar(sc, ax=axes[0], label='Class')
    axes[0].set_title('Scatter with Colormap',   fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Feature 1')
    axes[0].set_ylabel('Feature 2')
    axes[0].grid(True, alpha=0.3)

    # Right: scatter with size encoding (bubble chart)
    sizes  = rng.uniform(20, 300, n)
    bubble = axes[1].scatter(rng.normal(0, 1, n), rng.normal(0, 1, n),
                             s=sizes, c=sizes, cmap='viridis',
                             alpha=0.6, edgecolors='white', linewidths=0.3)
    plt.colorbar(bubble, ax=axes[1], label='Size / Value')
    axes[1].set_title('Bubble Chart (size = 3rd variable)', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    axes[1].grid(True, alpha=0.3)

    fig.suptitle('Scatter Plots', fontsize=15, fontweight='bold', y=1.01)
    fig.tight_layout()
    show_or_save(fig, '04_scatter.png')

    print("""
  KEY PARAMETERS for ax.scatter():
    x, y        → data coordinates
    s           → marker size (scalar or array — bubble chart!)
    c           → color (scalar, array, or string)
    cmap        → colormap: 'viridis' 'coolwarm' 'plasma' 'RdYlGn' ...
    alpha       → transparency
    edgecolors  → border color of each marker ('none', 'white', 'black')
    linewidths  → border thickness
    marker      → shape: 'o'  's'  '^'  'D'  ...

  plt.colorbar(sc, ax=ax, label='...')  → add color scale legend
    """)


    # ------------------------------------------------------------------
    # 5. BAR CHART
    # ------------------------------------------------------------------
    print("5. BAR CHART")
    print("-" * 70)

    categories  = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E']
    accuracy    = [0.82, 0.91, 0.87, 0.79, 0.94]
    f1_scores   = [0.80, 0.89, 0.85, 0.76, 0.93]
    errors      = [0.02, 0.015, 0.018, 0.025, 0.012]

    x    = np.arange(len(categories))
    width = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: grouped bars
    bars1 = axes[0].bar(x - width/2, accuracy,  width, label='Accuracy',
                        color='#2E75B6', alpha=0.85, edgecolor='white')
    bars2 = axes[0].bar(x + width/2, f1_scores, width, label='F1 Score',
                        color='#C55A11', alpha=0.85, edgecolor='white')

    axes[0].set_title('Model Comparison — Grouped Bars', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Model')
    axes[0].set_ylabel('Score')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(categories)
    axes[0].set_ylim(0, 1.08)
    axes[0].legend()
    axes[0].grid(True, axis='y', alpha=0.3)
    axes[0].axhline(0.9, color='green', linestyle='--', linewidth=1, alpha=0.7, label='Target 0.9')

    # Value labels on top of bars
    for bar in bars1:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.005,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.005,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=8)

    # Right: horizontal bars with error bars
    colors = ['#C55A11' if a == max(accuracy) else '#2E75B6' for a in accuracy]
    axes[1].barh(categories, accuracy, xerr=errors,
                 color=colors, alpha=0.85, edgecolor='white',
                 capsize=4, error_kw={'ecolor': 'gray', 'elinewidth': 1.5})
    axes[1].set_title('Horizontal Bar + Error Bars', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Accuracy')
    axes[1].set_xlim(0, 1.05)
    axes[1].axvline(0.9, color='green', linestyle='--', linewidth=1, alpha=0.7)
    axes[1].grid(True, axis='x', alpha=0.3)

    fig.tight_layout()
    show_or_save(fig, '05_bar_chart.png')

    print("""
  KEY PARAMETERS for ax.bar() / ax.barh():
    x / y       → positions
    height/width→ bar size
    width/height→ bar thickness (bar/barh)
    color       → fill color
    edgecolor   → border color
    alpha       → transparency
    xerr/yerr   → error bar values
    capsize     → error bar cap width

  ADDING VALUE LABELS:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h, f'{h:.2f}',
                ha='center', va='bottom')

  ax.grid(True, axis='y')  → gridlines on one axis only
    """)


    # ------------------------------------------------------------------
    # 6. HISTOGRAM
    # ------------------------------------------------------------------
    print("6. HISTOGRAM")
    print("-" * 70)

    rng    = np.random.default_rng(0)
    data_a = rng.normal(loc=0,   scale=1,   size=1000)
    data_b = rng.normal(loc=2,   scale=1.5, size=800)
    data_c = rng.exponential(scale=1, size=600)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Basic histogram
    axes[0].hist(data_a, bins=30, color='#2E75B6', edgecolor='white',
                 alpha=0.85, density=False)
    axes[0].set_title('Basic Histogram\n(counts)', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Value')
    axes[0].set_ylabel('Count')
    axes[0].grid(True, axis='y', alpha=0.3)

    # Overlapping histograms (density=True for comparison)
    axes[1].hist(data_a, bins=35, density=True, alpha=0.6,
                 color='#2E75B6', edgecolor='white', label='Class A  μ=0, σ=1')
    axes[1].hist(data_b, bins=35, density=True, alpha=0.6,
                 color='#C55A11', edgecolor='white', label='Class B  μ=2, σ=1.5')

    # Overlay KDE-style smooth curve
    # from matplotlib.patches import Patch
    axes[1].set_title('Overlapping Histograms\n(density)', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Value')
    axes[1].set_ylabel('Density')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, axis='y', alpha=0.3)

    # Cumulative histogram
    axes[2].hist(data_c, bins=40, cumulative=True, density=True,
                 color='#375623', edgecolor='white', alpha=0.85)
    axes[2].set_title('Cumulative Histogram\n(ECDF)', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Value')
    axes[2].set_ylabel('Cumulative Probability')
    axes[2].axhline(0.5, color='red', linestyle='--', linewidth=1, label='Median')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    fig.suptitle('Histograms', fontsize=14, fontweight='bold', y=1.01)
    fig.tight_layout()
    show_or_save(fig, '06_histogram.png')

    print("""
  KEY PARAMETERS for ax.hist():
    bins        → number of bins (int) or bin edges (array)
    density     → True: y-axis = probability density (area sums to 1)
    cumulative  → True: cumulative distribution
    alpha       → transparency (use < 1 for overlapping histograms)
    color       → bar fill color
    edgecolor   → bar border color
    histtype    → 'bar' (default)  'step'  'stepfilled'
    orientation → 'vertical' (default)  'horizontal'

  💡 Use density=True when comparing distributions of different sizes.
  💡 Overlapping histograms need alpha < 1 to see both distributions.
    """)


    # ------------------------------------------------------------------
    # 7. BOX PLOT & VIOLIN PLOT
    # ------------------------------------------------------------------
    print("7. BOX PLOT & VIOLIN PLOT")
    print("-" * 70)

    rng    = np.random.default_rng(7)
    data   = [rng.normal(m, s, 150) for m, s in
              [(0,1), (1,1.5), (3,0.8), (2,2), (4,1)]]
    labels = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Box plot
    bp = axes[0].boxplot(data, tick_labels=labels, patch_artist=True,
                         medianprops=dict(color='white', linewidth=2.5),
                         whiskerprops=dict(linewidth=1.5),
                         capprops=dict(linewidth=1.5),
                         flierprops=dict(marker='o', markersize=3, alpha=0.5))

    colors = ['#2E75B6', '#C55A11', '#375623', '#7030A0', '#BF8F00']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    axes[0].set_title('Box Plot', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('Score Distribution')
    axes[0].grid(True, axis='y', alpha=0.3)

    # Violin plot
    vp = axes[1].violinplot(data, positions=range(1, len(data)+1),
                            showmeans=True, showmedians=True,
                            showextrema=True)
    for body, color in zip(vp['bodies'], colors):
        body.set_facecolor(color)
        body.set_alpha(0.65)

    vp['cmedians'].set_color('white')
    vp['cmedians'].set_linewidth(2)
    vp['cmeans'].set_color('yellow')

    axes[1].set_xticks(range(1, len(labels)+1))
    axes[1].set_xticklabels(labels)
    axes[1].set_title('Violin Plot\n(shows full distribution shape)', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Score Distribution')
    axes[1].grid(True, axis='y', alpha=0.3)

    fig.tight_layout()
    show_or_save(fig, '07_box_violin.png')

    print("""
  Box plot elements:
    Box          → interquartile range (IQR): Q1 to Q3
    Median line  → Q2 (50th percentile)
    Whiskers     → Q1 - 1.5×IQR  to  Q3 + 1.5×IQR
    Fliers (●)   → outliers beyond whiskers

  Violin plot adds the full distribution shape (KDE curve).

  💡 Use box plots when you want to compare medians and spread quickly.
  💡 Use violin plots when the distribution shape matters (bimodal, skewed).
    """)


    # ------------------------------------------------------------------
    # 8. SUBPLOTS AND LAYOUTS
    # ------------------------------------------------------------------
    print("8. SUBPLOTS AND LAYOUTS")
    print("-" * 70)

    x = np.linspace(0, 4 * np.pi, 300)

    # --- 8a: Regular grid ---
    fig, axes = plt.subplots(2, 3, figsize=(14, 7), sharex=False, sharey=False)
    fig.suptitle('Regular Grid — plt.subplots(2, 3)', fontsize=13, fontweight='bold')

    funcs  = [np.sin, np.cos, np.tan,
              lambda x: x**2 / 50, np.exp, np.log1p]
    titles = ['sin(x)', 'cos(x)', 'tan(x)', 'x²/50', 'exp(x)', 'log1p(x)']
    colors = ['#2E75B6','#C55A11','#375623','#7030A0','#BF8F00','#C00000']

    for ax, func, title, color in zip(axes.flat, funcs, titles, colors):
        y = func(x)
        y = np.clip(y, -5, 5)   # clip tan and exp for readability
        ax.plot(x, y, color=color, linewidth=1.5)
        ax.set_title(title, fontsize=11)
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    show_or_save(fig, '08a_subplots_grid.png')

    # --- 8b: GridSpec for unequal sizes ---
    fig = plt.figure(figsize=(13, 7))
    gs  = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

    ax_main  = fig.add_subplot(gs[0, :])   # top row: spans all 3 columns
    ax_bl    = fig.add_subplot(gs[1, 0])   # bottom left
    ax_bm    = fig.add_subplot(gs[1, 1])   # bottom middle
    ax_br    = fig.add_subplot(gs[1, 2])   # bottom right

    rng = np.random.default_rng(5)
    ax_main.plot(x, np.sin(x), '#2E75B6', lw=2)
    ax_main.fill_between(x, np.sin(x), alpha=0.2, color='#2E75B6')
    ax_main.set_title('Main plot — spans all columns (gs[0, :])', fontsize=12, fontweight='bold')
    ax_main.grid(True, alpha=0.3)

    ax_bl.hist(rng.normal(0,1,500), bins=25, color='#C55A11', edgecolor='white', alpha=0.8)
    ax_bl.set_title('Histogram', fontsize=10)
    ax_bm.scatter(rng.normal(0,1,100), rng.normal(0,1,100), c='#375623', alpha=0.7, s=25)
    ax_bm.set_title('Scatter', fontsize=10)
    ax_br.bar(['A','B','C','D'], rng.integers(10,100,4), color='#7030A0', alpha=0.8, edgecolor='white')
    ax_br.set_title('Bar', fontsize=10)

    for ax in [ax_bl, ax_bm, ax_br]:
        ax.grid(True, alpha=0.3)

    fig.suptitle('GridSpec — Unequal Layout', fontsize=13, fontweight='bold')
    show_or_save(fig, '08b_gridspec.png')

    print("""
  REGULAR GRID:
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, h))
    axes.flat  → iterate over all axes in row-major order
    sharex=True → all subplots share the same x-axis
    sharey=True → all subplots share the same y-axis

  UNEQUAL LAYOUT with GridSpec:
    from matplotlib.gridspec import GridSpec
    gs  = GridSpec(2, 3, figure=fig)
    ax  = fig.add_subplot(gs[0, :])    → spans row 0, all columns
    ax  = fig.add_subplot(gs[1, 0:2])  → spans row 1, cols 0–1

  fig.tight_layout()    → prevent overlapping labels
  fig.suptitle(...)     → title for the entire figure
    """)


    # ------------------------------------------------------------------
    # 9. CUSTOMIZATION
    # ------------------------------------------------------------------
    print("9. CUSTOMIZATION — Colors, Styles, Annotations")
    print("-" * 70)

    x   = np.linspace(0, 10, 300)
    rng = np.random.default_rng(1)

    fig, ax = plt.subplots(figsize=(11, 6))

    # Shaded confidence band
    y_mean = np.sin(x) * np.exp(-x/8)
    y_std  = 0.15 * np.abs(np.sin(x/2))
    ax.fill_between(x, y_mean - y_std, y_mean + y_std,
                    alpha=0.25, color='#2E75B6', label='±1σ confidence band')
    ax.plot(x, y_mean, '#2E75B6', linewidth=2.5, label='Mean prediction')

    # Scatter with noise
    x_pts = rng.uniform(0, 10, 50)
    y_pts = np.sin(x_pts) * np.exp(-x_pts/8) + rng.normal(0, 0.12, 50)
    ax.scatter(x_pts, y_pts, color='#C55A11', s=30, zorder=5,
               alpha=0.8, edgecolors='white', linewidths=0.5, label='Observations')

    # Annotations
    peak_x = np.pi / 2
    peak_y = np.sin(peak_x) * np.exp(-peak_x/8)
    ax.annotate(f'Peak ≈ ({peak_x:.2f}, {peak_y:.2f})',
                xy=(peak_x, peak_y), xytext=(peak_x + 1.5, peak_y + 0.3),
                fontsize=10, color='#1F3864',
                arrowprops=dict(arrowstyle='->', color='#1F3864', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                          edgecolor='#BF8F00', alpha=0.9))

    # Reference lines
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--', alpha=0.6)
    ax.axvspan(7, 10, alpha=0.07, color='red', label='Decay region')

    # Text box inside plot
    ax.text(0.02, 0.05, 'Model: sin(x)·e^(−x/8)',
            transform=ax.transAxes,     # axes-relative coordinates (0–1)
            fontsize=9, color='gray',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    ax.set_title('Customization — Annotations, Bands, Styles', fontsize=14, fontweight='bold')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(0, 10)

    fig.tight_layout()
    show_or_save(fig, '09_customization.png')

    print("""
  COLORS:
    Named colors   : 'red', 'blue', 'green', 'gray', ...
    Hex codes      : '#2E75B6', '#C55A11'
    CN aliases     : 'C0' 'C1' 'C2' ...  (cycles through default palette)
    RGBA tuple     : (0.2, 0.4, 0.6, 0.8)

  COMMON COLORMAPS:
    Sequential  : 'viridis' 'plasma' 'Blues' 'Greens' 'YlOrRd'
    Diverging   : 'coolwarm' 'RdYlGn' 'seismic'
    Qualitative : 'tab10' 'Set1' 'Paired'
    Reverse any : append '_r'  →  'viridis_r'

  ANNOTATIONS:
    ax.annotate(text, xy=point, xytext=label_pos, arrowprops={...})
    ax.text(x, y, text)                  → data coordinates
    ax.text(x, y, text, transform=ax.transAxes)  → 0–1 axes coords

  SHADING:
    ax.fill_between(x, y1, y2, alpha=0.2)
    ax.axhspan(y1, y2, alpha=0.1)
    ax.axvspan(x1, x2, alpha=0.1)

  LEGEND:
    loc: 'best' 'upper right' 'lower left' 'center' ...
    ncol=2          → two-column legend
    framealpha=0.9  → semi-transparent background
    """)


    # ------------------------------------------------------------------
    # 10. STYLES AND THEMES
    # ------------------------------------------------------------------
    print("10. STYLES AND THEMES")
    print("-" * 70)

    print("""
  Available built-in styles:
    plt.style.use('seaborn-v0_8')       ← seaborn-inspired (clean)
    plt.style.use('ggplot')             ← R's ggplot2 look
    plt.style.use('dark_background')    ← dark theme
    plt.style.use('fivethirtyeight')    ← FiveThirtyEight journalism style
    plt.style.use('bmh')                ← Bayesian Methods for Hackers
    plt.style.use('default')            ← Matplotlib default

  Temporary style (only inside the block):
    with plt.style.context('ggplot'):
        fig, ax = plt.subplots()
        ax.plot(...)

  List all available styles:
    print(plt.style.available)

  FIGURE SIZE AND DPI:
    fig, ax = plt.subplots(figsize=(10, 6))   ← width × height in inches
    fig.set_dpi(150)                           ← dots per inch
    fig.savefig('out.png', dpi=300)            ← high-res export
    """)

    # Show two styles side by side
    x  = np.linspace(0, 2*np.pi, 100)

    with plt.style.context('ggplot'):
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].plot(x, np.sin(x), lw=2)
        axes[0].set_title("Style: 'ggplot'",  fontsize=12, fontweight='bold')
        axes[0].grid(True)

    with plt.style.context('dark_background'):
        axes[1].plot(x, np.cos(x), lw=2, color='cyan')
        axes[1].set_title("Style: 'dark_background'", fontsize=12, fontweight='bold', color='white')
        axes[1].grid(True)

    show_or_save(fig, '10_styles.png')


    # ------------------------------------------------------------------
    # 11. ML PLOTS — CONFUSION MATRIX
    # ------------------------------------------------------------------
    print("11. ML PLOTS — CONFUSION MATRIX")
    print("-" * 70)

    def plot_confusion_matrix(cm, class_names, title='Confusion Matrix'):
        """
        Renders a labeled, color-coded confusion matrix.

        Parameters
        ----------
        cm          : 2D array-like, shape (n_classes, n_classes)
        class_names : list of str
        title       : str
        """
        cm = np.array(cm)
        n  = len(class_names)

        fig, ax = plt.subplots(figsize=(6 + n * 0.5, 5 + n * 0.4))

        # Normalize for color intensity; keep raw counts for text
        cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
        im = ax.imshow(cm_norm, interpolation='nearest', cmap='Blues', vmin=0, vmax=1)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Recall per class')

        # Cell annotations
        thresh = cm_norm.max() / 2.0
        for i in range(n):
            for j in range(n):
                color = 'white' if cm_norm[i, j] > thresh else '#1F3864'
                ax.text(j, i, f'{cm[i, j]}\n({cm_norm[i, j]:.1%})',
                        ha='center', va='center', fontsize=9,
                        fontweight='bold', color=color)

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(class_names, rotation=30, ha='right', fontsize=10)
        ax.set_yticklabels(class_names, fontsize=10)
        ax.set_xlabel('Predicted Label', fontsize=11, fontweight='bold')
        ax.set_ylabel('True Label',      fontsize=11, fontweight='bold')
        ax.set_title(title,              fontsize=13, fontweight='bold', pad=14)

        # Diagonal highlight
        for i in range(n):
            ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1,
                                       fill=False, edgecolor='#C55A11',
                                       linewidth=2.5))
        fig.tight_layout()
        return fig

    # 3-class example
    cm3 = np.array([[85,  8,  7],
                    [ 5, 90,  5],
                    [ 3,  4, 93]])
    fig = plot_confusion_matrix(cm3, ['Cat', 'Dog', 'Bird'],
                                'Confusion Matrix — 3 Classes')
    show_or_save(fig, '11_confusion_matrix.png')

    # 5-class example
    rng = np.random.default_rng(99)
    cm5 = (np.eye(5) * 80 + rng.integers(0, 20, (5,5))).astype(int)
    fig = plot_confusion_matrix(cm5,
                                ['Healthy','Pneumonia','COVID','Flu','RSV'],
                                'Confusion Matrix — 5 Classes (Medical)')
    show_or_save(fig, '11_confusion_matrix_5class.png')

    print("""
  Confusion Matrix cheat-sheet:
    Diagonal   → correct predictions
    Off-diag   → misclassifications (row = true class, col = predicted)

  Reading the matrix:
    cm[i, j]  → predicted class j when true class was i
    Normalize row-wise  → Recall per class
    Normalize col-wise  → Precision per class
    """)


    # ------------------------------------------------------------------
    # 12. ML PLOTS — ROC CURVE
    # ------------------------------------------------------------------
    print("12. ML PLOTS — ROC CURVE")
    print("-" * 70)

    def plot_roc_curves(models_data, title='ROC Curves'):
        """
        Plots one ROC curve per model.

        models_data : list of (name, fpr_array, tpr_array, auc_score)
        """
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        colors = ['#2E75B6','#C55A11','#375623','#7030A0','#BF8F00']

        for (name, fpr, tpr, auc), color in zip(models_data, colors):
            axes[0].plot(fpr, tpr, color=color, linewidth=2,
                         label=f'{name}  (AUC = {auc:.3f})')

        axes[0].plot([0,1],[0,1], 'k--', linewidth=1, alpha=0.5, label='Random (AUC=0.5)')
        axes[0].fill_between([0,1],[0,1],[0,1], alpha=0.05, color='gray')

        axes[0].set_title(title, fontsize=13, fontweight='bold')
        axes[0].set_xlabel('False Positive Rate (FPR)', fontsize=11)
        axes[0].set_ylabel('True Positive Rate (TPR = Recall)', fontsize=11)
        axes[0].legend(loc='lower right', fontsize=9)
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xlim(-0.01, 1.01)
        axes[0].set_ylim(-0.01, 1.05)

        # Zoom on top-left corner (high-sensitivity region)
        for (name, fpr, tpr, auc), color in zip(models_data, colors):
            axes[1].plot(fpr, tpr, color=color, linewidth=2, label=name)

        axes[1].plot([0,1],[0,1], 'k--', linewidth=1, alpha=0.4)
        axes[1].set_xlim(-0.005, 0.3)
        axes[1].set_ylim(0.6, 1.01)
        axes[1].set_title('Zoomed — Low FPR region', fontsize=13, fontweight='bold')
        axes[1].set_xlabel('False Positive Rate')
        axes[1].set_ylabel('True Positive Rate')
        axes[1].legend(fontsize=9)
        axes[1].grid(True, alpha=0.3)

        fig.tight_layout()
        return fig

    # Simulate ROC data for 3 models
    rng = np.random.default_rng(42)

    def _sim_roc(auc_target, n=300):
        """Simulate (fpr, tpr) that approximates a given AUC."""
        t   = np.linspace(0, 1, n)
        fpr = t
        # Parametric curve that gives approximately auc_target
        tpr = np.clip(t ** (1 / (auc_target / (1 - auc_target + 1e-9))), 0, 1)
        tpr = np.sort(tpr)[::-1]
        tpr = np.clip(tpr + rng.normal(0, 0.01, n), 0, 1)
        tpr = np.maximum.accumulate(tpr[::-1])[::-1]
        return fpr, np.clip(tpr, 0, 1)

    models = [
        ('Random Forest', *_sim_roc(0.94), 0.940),
        ('Logistic Reg.',  *_sim_roc(0.87), 0.870),
        ('SVM',            *_sim_roc(0.91), 0.910),
    ]
    fig = plot_roc_curves(models, 'ROC Curves — Binary Classification')
    show_or_save(fig, '12_roc_curves.png')

    print("""
  ROC Curve components:
    x-axis  → FPR = FP / (FP + TN)   (= 1 - Specificity)
    y-axis  → TPR = TP / (TP + FN)   (= Recall = Sensitivity)
    AUC     → Area Under the Curve  (1.0 = perfect, 0.5 = random)

  With sklearn:
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    """)


    # ------------------------------------------------------------------
    # 13. ML PLOTS — LEARNING CURVES
    # ------------------------------------------------------------------
    print("13. ML PLOTS — LEARNING CURVES")
    print("-" * 70)

    def plot_learning_curves(train_sizes, train_scores, val_scores,
                             metric='Accuracy', title='Learning Curves'):
        """
        Plots training and validation score vs training set size.
        Scores arrays shape: (n_sizes, n_cv_folds)
        """
        train_mean = train_scores.mean(axis=1)
        train_std  = train_scores.std(axis=1)
        val_mean   = val_scores.mean(axis=1)
        val_std    = val_scores.std(axis=1)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(train_sizes, train_mean, 'o-', color='#2E75B6',
                linewidth=2, markersize=6, label='Training score')
        ax.fill_between(train_sizes,
                        train_mean - train_std, train_mean + train_std,
                        alpha=0.15, color='#2E75B6')

        ax.plot(train_sizes, val_mean, 's-', color='#C55A11',
                linewidth=2, markersize=6, label='Validation score')
        ax.fill_between(train_sizes,
                        val_mean - val_std, val_mean + val_std,
                        alpha=0.15, color='#C55A11')

        # Gap annotation
        gap = train_mean[-1] - val_mean[-1]
        ax.annotate(f'Generalization gap\n≈ {gap:.3f}',
                    xy=(train_sizes[-1], (train_mean[-1] + val_mean[-1]) / 2),
                    xytext=(train_sizes[-1] * 0.55, 0.72),
                    fontsize=9, color='#7030A0',
                    arrowprops=dict(arrowstyle='->', color='#7030A0'))

        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.set_xlabel('Training set size', fontsize=11)
        ax.set_ylabel(metric, fontsize=11)
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0.5, 1.05)

        fig.tight_layout()
        return fig

    # Simulate learning curve data
    rng   = np.random.default_rng(3)
    sizes = np.array([50, 100, 200, 400, 800, 1600, 3000])
    train_s = np.column_stack([
        1.0 - 0.05 * np.log1p(sizes/50) + rng.normal(0, 0.008, len(sizes))
        for _ in range(5)])
    val_s = np.column_stack([
        0.60 + 0.28 * (1 - np.exp(-sizes/600)) + rng.normal(0, 0.012, len(sizes))
        for _ in range(5)])

    fig = plot_learning_curves(sizes, train_s, val_s,
                               metric='Accuracy',
                               title='Learning Curves — Random Forest')
    show_or_save(fig, '13_learning_curves.png')

    print("""
  Diagnosing from learning curves:
    Large gap (train >> val)  → High variance (overfitting)
                                 → More data, regularization, simpler model
    Both curves low           → High bias (underfitting)
                                 → More features, more complex model
    Curves converge + plateau → Irreducible error — near optimal

  With sklearn:
    from sklearn.model_selection import learning_curve
    sizes, train_s, val_s = learning_curve(model, X, y, cv=5,
                                           scoring='accuracy')
    """)


    # ------------------------------------------------------------------
    # 14. ML PLOTS — FEATURE IMPORTANCE
    # ------------------------------------------------------------------
    print("14. ML PLOTS — FEATURE IMPORTANCE")
    print("-" * 70)

    rng          = np.random.default_rng(11)
    features     = ['Age', 'Income', 'Credit Score', 'Debt Ratio',
                    'Employment Years', 'Num Accounts', 'Late Payments',
                    'Loan Amount', 'Interest Rate', 'Collateral Value']
    importances  = np.sort(rng.uniform(0.01, 0.25, len(features)))[::-1]
    importances /= importances.sum()
    std_devs     = rng.uniform(0.005, 0.03, len(features))

    # Sort ascending for horizontal bar chart (largest at top)
    order       = np.argsort(importances)
    feat_sorted = [features[i] for i in order]
    imp_sorted  = importances[order]
    std_sorted  = std_devs[order]

    # Color: top 3 highlighted
    bar_colors = ['#2E75B6'] * len(features)
    for i in range(len(features)-3, len(features)):
        bar_colors[i] = '#C55A11'

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(feat_sorted, imp_sorted, xerr=std_sorted,
                   color=bar_colors, edgecolor='white',
                   capsize=3, error_kw={'ecolor': 'gray', 'elinewidth': 1.2})

    # Value labels
    for bar, val in zip(bars, imp_sorted):
        ax.text(val + 0.003, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', fontsize=9, color='#1F3864')

    ax.axvline(0, color='gray', linewidth=0.8)
    ax.set_xlabel('Feature Importance (normalized)', fontsize=11)
    ax.set_title('Feature Importance — Loan Default Model', fontsize=13, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)

    legend_patches = [mpatches.Patch(color='#C55A11', label='Top 3 features'),
                      mpatches.Patch(color='#2E75B6', label='Other features')]
    ax.legend(handles=legend_patches, loc='lower right', fontsize=10)

    fig.tight_layout()
    show_or_save(fig, '14_feature_importance.png')


    # ------------------------------------------------------------------
    # 15. SAVING FIGURES
    # ------------------------------------------------------------------
    print("15. SAVING FIGURES")
    print("-" * 70)
    print("""
  BASIC SAVE:
    fig.savefig('plot.png')                   ← default dpi (~100)
    fig.savefig('plot.png', dpi=300)          ← high resolution (print)
    fig.savefig('plot.pdf')                   ← vector, perfect for LaTeX
    fig.savefig('plot.svg')                   ← vector, editable in Inkscape
    fig.savefig('plot.eps')                   ← vector, journals

  OPTIONS:
    bbox_inches='tight'    ← remove extra whitespace (almost always use this)
    facecolor='white'      ← explicit white background (for dark themes)
    transparent=True       ← transparent background (PNG only)

  RECOMMENDED:
    fig.savefig('output.png', dpi=150, bbox_inches='tight')

  CLOSE AFTER SAVING (important in scripts to free memory):
    plt.close(fig)         ← close specific figure
    plt.close('all')       ← close all open figures

  FORMATS SUMMARY:
    .png  → raster, great for web and documents
    .pdf  → vector, best for LaTeX/reports
    .svg  → vector, best for web (D3, CSS styling)
    .eps  → vector, required by some journals
    """)


    # ------------------------------------------------------------------
    # 16. COMMON MISTAKES
    # ------------------------------------------------------------------
    print("16. COMMON MISTAKES")
    print("-" * 70)
    print("""
  Mistake 1 — Forgetting plt.close() in loops:
    for i in range(100):
        fig, ax = plt.subplots()  # creates 100 figure objects in memory!
        ax.plot(...)
        fig.savefig(f'plot_{i}.png')
        plt.close(fig)            ← ALWAYS close after saving

  Mistake 2 — Modifying after tight_layout():
    fig.tight_layout()            ← call LAST, after all ax modifications
    ax.set_title('...')           ← this may be clipped — do BEFORE tight_layout

  Mistake 3 — pyplot vs OOP confusion:
    fig, ax = plt.subplots()
    ax.plot(...)
    plt.xlabel('X')               ← works, but mixes interfaces
    ax.set_xlabel('X')            ← preferred: stay on one interface

  Mistake 4 — Color on imshow with wrong vmin/vmax:
    ax.imshow(data)               ← auto-scales per image (misleading in grids)
    ax.imshow(data, vmin=0, vmax=1) ← fixed scale → comparable across subplots

  Mistake 5 — Legend without labels:
    ax.plot(x, y)                 ← no label= argument
    ax.legend()                   ← legend is empty!
    ax.plot(x, y, label='sin(x)') ← always add label= when you'll call legend()

  Mistake 6 — Not using tight_layout():
    Axis labels and titles often overlap in multi-subplot figures.
    Always call fig.tight_layout() before saving or showing.
    """)


    # ------------------------------------------------------------------
    # 17. QUICK REFERENCE
    # ------------------------------------------------------------------
    print("17. QUICK REFERENCE")
    print("-" * 70)
    print()
    print(f"  {'Method':<42} {'Description'}")
    print(f"  {'-'*42} {'-'*38}")

    ref = [
        ("FIGURE & AXES", ""),
        ("fig, ax = plt.subplots(r,c,figsize=(w,h))", "Create figure with r×c subplots"),
        ("fig = plt.figure(figsize=(w,h))",           "Blank figure (use with GridSpec)"),
        ("gs = GridSpec(r, c, figure=fig)",           "Flexible unequal grid"),
        ("ax = fig.add_subplot(gs[r, c])",            "Add subplot at GridSpec position"),
        ("fig.tight_layout()",                        "Fix overlapping labels"),
        ("fig.suptitle('...', fontsize=14)",          "Title for entire figure"),
        ("fig.savefig('f.png', dpi=150, bbox_inches='tight')", "Save figure"),
        ("plt.close(fig)",                            "Free figure memory"),
        ("PLOT TYPES", ""),
        ("ax.plot(x, y, color, lw, ls, marker)",     "Line plot"),
        ("ax.scatter(x, y, s, c, cmap, alpha)",      "Scatter / bubble chart"),
        ("ax.bar(x, h, width, color, edgecolor)",    "Vertical bar chart"),
        ("ax.barh(y, w, xerr=, color)",              "Horizontal bar chart"),
        ("ax.hist(x, bins, density, alpha)",         "Histogram"),
        ("ax.boxplot(data, patch_artist=True)",      "Box plot"),
        ("ax.violinplot(data, showmedians=True)",    "Violin plot"),
        ("ax.imshow(matrix, cmap, vmin, vmax)",      "Heatmap / image"),
        ("ax.fill_between(x, y1, y2, alpha)",        "Shaded area between curves"),
        ("AXES SETTINGS", ""),
        ("ax.set_title('...', fontsize, fontweight)", "Axes title"),
        ("ax.set_xlabel / set_ylabel('...')",        "Axis labels"),
        ("ax.set_xlim(a, b) / set_ylim(a, b)",      "Axis range"),
        ("ax.set_xticks([...]) / set_xticklabels([...])", "Custom ticks"),
        ("ax.tick_params(axis='x', rotation=45)",   "Rotate tick labels"),
        ("ax.grid(True, alpha=0.3)",                 "Grid lines"),
        ("ax.legend(loc='best', fontsize, ncol)",    "Legend"),
        ("ax.invert_yaxis()",                        "Flip y-axis (e.g. confusion matrix)"),
        ("REFERENCE LINES", ""),
        ("ax.axhline(y, color, lw, ls)",             "Horizontal line"),
        ("ax.axvline(x, color, lw, ls)",             "Vertical line"),
        ("ax.axhspan(y1, y2, alpha)",                "Horizontal shaded band"),
        ("ax.axvspan(x1, x2, alpha)",                "Vertical shaded band"),
        ("ANNOTATIONS", ""),
        ("ax.annotate(text, xy=pt, xytext=pos, arrowprops={})", "Arrow annotation"),
        ("ax.text(x, y, text, transform, fontsize)", "Text at data or axes coords"),
        ("plt.colorbar(im, ax=ax, label='...')",     "Add colorbar"),
        ("STYLES", ""),
        ("plt.style.use('ggplot')",                  "Apply a global style"),
        ("with plt.style.context('dark_background'):", "Temporary style"),
    ]

    for item, desc in ref:
        if desc == "":
            print(f"\n  ── {item} {'─'*(65-len(item))}")
        else:
            print(f"  {item:<42} {desc}")

    print()
    print(f"\nDone! Check the '{OUTDIR}/' folder for all saved figures.\n" if SAVE
          else "\nDone! All plots rendered inline.\n")


main()


"""
SUMMARY — MATPLOTLIB
=======================================================

SETUP:
  import matplotlib.pyplot as plt
  import matplotlib
  matplotlib.use('Agg')       ← use in scripts (no GUI)
  %matplotlib inline          ← use in Jupyter

GOLDEN RULE:
  Always use OOP interface:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(...)
    fig.tight_layout()
    fig.savefig('out.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

PLOT TYPES:
  Line       → ax.plot(x, y, color, lw, ls, marker, label)
  Scatter    → ax.scatter(x, y, s, c, cmap, alpha, edgecolors)
  Bar        → ax.bar / ax.barh(positions, values, color, xerr/yerr)
  Histogram  → ax.hist(x, bins, density, cumulative, alpha)
  Box        → ax.boxplot(data, patch_artist=True)
  Violin     → ax.violinplot(data, showmedians=True)
  Heatmap    → ax.imshow(matrix, cmap, vmin, vmax)

LAYOUTS:
  fig, axes = plt.subplots(r, c, figsize=(w,h), sharex, sharey)
  GridSpec for unequal panels: gs = GridSpec(r, c)
  axes.flat  →  iterate all subplots

CUSTOMIZATION:
  Colors: '#hex', 'named', 'C0', (r,g,b,a)
  Annotations: ax.annotate(text, xy, xytext, arrowprops)
  Shading: ax.fill_between / axhspan / axvspan
  Styles: plt.style.use('ggplot' / 'seaborn-v0_8' / 'dark_background')

ML PLOTS:
  Confusion Matrix  → ax.imshow + ax.text for cell labels
  ROC Curve         → ax.plot(fpr, tpr) + AUC in legend
  Learning Curves   → train vs val score vs dataset size
  Feature Importance→ ax.barh sorted by importance

SAVE:
  fig.savefig('file.png', dpi=150, bbox_inches='tight')
  plt.close(fig)   ← always close after saving!

COMMON PITFALLS:
  • Forget plt.close()   → memory leak in loops
  • legend() without label= → empty legend
  • tight_layout() too early → gets overridden
  • imshow without vmin/vmax → inconsistent color scale
  • Mixing pyplot and OOP → confusing and fragile

REMEMBER:
  "Matplotlib gives you complete control.
   fig, ax = plt.subplots() is your starting point for everything."
"""