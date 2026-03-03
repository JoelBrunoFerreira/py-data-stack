"""
SEABORN - COMPLETE GUIDE
==========================

Seaborn is a statistical data visualization library built on top of Matplotlib.
It provides a high-level interface for drawing attractive and informative
statistical graphics, with tight integration with Pandas DataFrames.

Key Characteristics:
- Works directly with Pandas DataFrames (pass column names as strings)
- Automatic statistical aggregation (mean, CI, KDE, regression lines)
- Beautiful default themes out of the box
- Figure-level vs Axes-level function distinction
- Built on Matplotlib → full customization still available via ax / fig

Installation:
  pip install seaborn

Common Uses:
- Exploratory Data Analysis (EDA)
- Distribution analysis
- Correlation and relationship discovery
- Categorical comparisons
- Statistical summaries with confidence intervals

Relationship to Matplotlib:
  Seaborn  → high-level, opinionated, statistical
  Matplotlib → low-level, full control, manual everything
  Use both: Seaborn for the plot, Matplotlib for fine-tuning.
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from IPython import get_ipython
from importlib.metadata import version

# ──────────────────────────────────────────────────────────────────────────────
# ENVIRONMENT SETUP
# ──────────────────────────────────────────────────────────────────────────────

def is_jupyter():
    try:
        shell = get_ipython().__class__.__name__
        return shell in ('ZMQInteractiveShell', 'TerminalInteractiveShell')
    except NameError:
        return False

JUPYTER = is_jupyter()
SAVE    = not JUPYTER

if not JUPYTER:
    matplotlib.use('Agg')
    print("Running as script — plots will be saved as PNG files.")
else:
    print("Running in Jupyter — plots will render inline.")

OUTDIR = "seaborn_output"
import os
os.makedirs(OUTDIR, exist_ok=True)


def show_or_save(fig, filename):
    if JUPYTER:
        plt.show()
    else:
        path = os.path.join(OUTDIR, filename)
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  → Saved: {path}")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────────────
# SHARED DATASETS  (used throughout the file)
# ──────────────────────────────────────────────────────────────────────────────

def make_sales_df(seed=42):
    """Synthetic sales dataset — mimics a real-world Pandas workflow."""
    rng = np.random.default_rng(seed)
    n   = 400
    regions   = rng.choice(['North', 'South', 'East', 'West'], n)
    products  = rng.choice(['Laptop', 'Phone', 'Tablet', 'Watch'], n)
    quarters  = rng.choice(['Q1', 'Q2', 'Q3', 'Q4'], n)
    base      = {'Laptop': 1200, 'Phone': 800, 'Tablet': 500, 'Watch': 300}
    revenue   = np.array([base[p] for p in products])
    revenue   = revenue * rng.uniform(0.7, 1.4, n) + rng.normal(0, 50, n)
    units     = (revenue / np.array([base[p] for p in products])
                 * rng.integers(5, 30, n)).astype(int)
    satisfaction = np.clip(rng.normal(3.8, 0.6, n), 1, 5).round(1)
    return pd.DataFrame({
        'region': regions, 'product': products, 'quarter': quarters,
        'revenue': revenue.round(2), 'units': units,
        'satisfaction': satisfaction,
        'experience_years': rng.integers(1, 15, n),
    })


def make_ml_df(seed=7):
    """Synthetic ML model results dataset."""
    rng    = np.random.default_rng(seed)
    models = ['Random Forest', 'XGBoost', 'SVM', 'Logistic Reg.', 'KNN']
    rows   = []
    for model in models:
        base_acc = {'Random Forest':0.91,'XGBoost':0.93,'SVM':0.88,
                    'Logistic Reg.':0.85,'KNN':0.82}[model]
        for fold in range(10):
            rows.append({
                'model': model,
                'fold': fold + 1,
                'accuracy':  np.clip(rng.normal(base_acc,       0.015), 0.7, 1.0),
                'f1_score':  np.clip(rng.normal(base_acc-0.02,  0.018), 0.7, 1.0),
                'precision': np.clip(rng.normal(base_acc+0.01,  0.016), 0.7, 1.0),
                'recall':    np.clip(rng.normal(base_acc-0.015, 0.020), 0.7, 1.0),
            })
    return pd.DataFrame(rows)


df_sales = make_sales_df()
df_ml    = make_ml_df()


def main():

    print("=== SEABORN - COMPLETE GUIDE ===\n")
    print(f"Seaborn version: {version('seaborn')}")
    print(f"Pandas version:  {version('pandas')}")


    # ------------------------------------------------------------------
    # 1. IMPORTING AND SETUP
    # ------------------------------------------------------------------
    print("1. IMPORTING AND SETUP")
    print("-" * 70)
    print("""
  import seaborn as sns
  import matplotlib.pyplot as plt
  import pandas as pd
  import numpy as np

  THEMES  (call once at the top of your script / notebook):
    sns.set_theme()                        ← Seaborn defaults (recommended)
    sns.set_theme(style='whitegrid')       ← white background + grid
    sns.set_theme(style='darkgrid')        ← dark background + grid
    sns.set_theme(style='white')           ← white, no grid
    sns.set_theme(style='ticks')           ← ticks only, minimal
    sns.set_theme(context='talk')          ← larger fonts for presentations
    sns.set_theme(context='paper')         ← smaller fonts for publications
    sns.set_theme(palette='deep')          ← color palette

  PALETTES:
    Qualitative : 'deep' 'muted' 'pastel' 'bright' 'dark' 'colorblind'
    Sequential  : 'Blues' 'Greens' 'rocket' 'mako' 'flare'
    Diverging   : 'coolwarm' 'vlag' 'icefire' 'RdYlGn'

    sns.color_palette('deep', n_colors=5)  ← preview a palette
    sns.palplot(sns.color_palette('deep')) ← visualize palette

  RESETTING:
    sns.reset_defaults()   ← revert to Matplotlib defaults
    """)

    sns.set_theme(style='whitegrid', palette='deep')


    # ------------------------------------------------------------------
    # 2. FIGURE-LEVEL vs AXES-LEVEL FUNCTIONS
    # ------------------------------------------------------------------
    print("2. FIGURE-LEVEL vs AXES-LEVEL FUNCTIONS")
    print("-" * 70)
    print("""
  AXES-LEVEL functions:
    Work like Matplotlib — return an Axes object.
    Can be embedded in any fig/ax layout.
    Examples: sns.histplot, sns.scatterplot, sns.boxplot, sns.heatmap

    fig, axes = plt.subplots(1, 2)
    sns.histplot(data=df, x='col', ax=axes[0])
    sns.boxplot(data=df,  x='cat', y='val', ax=axes[1])

  FIGURE-LEVEL functions:
    Create their own Figure internally. Return a FacetGrid object.
    Support faceting (row=, col= for small multiples automatically).
    Examples: sns.displot, sns.relplot, sns.catplot, sns.lmplot

    g = sns.displot(data=df, x='col', col='category', kind='hist')
    g.set_axis_labels('X Label', 'Y Label')
    g.set_titles(col_template='{col_name}')
    g.figure.savefig('out.png', bbox_inches='tight')

  KEY DIFFERENCE:
    Axes-level  → ax.set_title()   ax.set_xlabel()
    Figure-level→ g.set_titles()   g.set_axis_labels()
                  g.figure  (not g.fig in older seaborn)

  💡 Use axes-level when you control the layout (subplots grid).
  💡 Use figure-level when you want automatic faceting by a variable.
    """)


    # ------------------------------------------------------------------
    # 3. DISTRIBUTION PLOTS
    # ------------------------------------------------------------------
    print("3. DISTRIBUTION PLOTS")
    print("-" * 70)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Distribution Plots', fontsize=15, fontweight='bold', y=1.01)

    # 3a: histplot — basic
    sns.histplot(data=df_sales, x='revenue', bins=30,
                 color='#2E75B6', edgecolor='white', ax=axes[0, 0])
    axes[0, 0].set_title('histplot — basic', fontweight='bold')
    axes[0, 0].set_xlabel('Revenue (€)')

    # 3b: histplot — hue split
    sns.histplot(data=df_sales, x='revenue', hue='product',
                 bins=25, alpha=0.6, element='step', ax=axes[0, 1])
    axes[0, 1].set_title('histplot — hue split by product', fontweight='bold')
    axes[0, 1].set_xlabel('Revenue (€)')

    # 3c: histplot — kde overlay
    sns.histplot(data=df_sales, x='satisfaction', bins=15,
                 kde=True, color='#C55A11', edgecolor='white', ax=axes[0, 2])
    axes[0, 2].set_title('histplot — kde=True overlay', fontweight='bold')
    axes[0, 2].set_xlabel('Customer Satisfaction')

    # 3d: kdeplot — multiple
    for product, color in zip(['Laptop','Phone','Tablet','Watch'],
                               ['#2E75B6','#C55A11','#375623','#7030A0']):
        subset = df_sales[df_sales['product'] == product]['revenue']
        sns.kdeplot(data=subset, label=product, color=color,
                    linewidth=2, fill=True, alpha=0.12, ax=axes[1, 0])
    axes[1, 0].set_title('kdeplot — filled, per product', fontweight='bold')
    axes[1, 0].set_xlabel('Revenue (€)')
    axes[1, 0].legend(fontsize=9)

    # 3e: ecdfplot
    sns.ecdfplot(data=df_sales, x='revenue', hue='product', ax=axes[1, 1])
    axes[1, 1].set_title('ecdfplot — Empirical CDF', fontweight='bold')
    axes[1, 1].set_xlabel('Revenue (€)')
    axes[1, 1].set_ylabel('Cumulative Proportion')

    # 3f: rug + kde combined
    sns.kdeplot(data=df_sales, x='satisfaction', hue='region',
                fill=True, alpha=0.15, linewidth=1.8, ax=axes[1, 2])
    sns.rugplot(data=df_sales, x='satisfaction', hue='region',
                height=0.06, alpha=0.4, ax=axes[1, 2])
    axes[1, 2].set_title('kdeplot + rugplot combined', fontweight='bold')
    axes[1, 2].set_xlabel('Customer Satisfaction')

    fig.tight_layout()
    show_or_save(fig, '03_distribution_plots.png')

    print("""
  sns.histplot(data, x, hue, bins, kde, stat, element, fill, ax)
    stat      → 'count' (default)  'density'  'probability'  'percent'
    element   → 'bars' (default)  'step'  'poly'
    kde=True  → overlay KDE curve
    multiple  → 'layer' (default)  'dodge'  'stack'  'fill'

  sns.kdeplot(data, x, hue, fill, alpha, linewidth, bw_adjust, cut, ax)
    fill=True     → shaded area under curve
    bw_adjust     → bandwidth multiplier (>1 smoother, <1 more detail)
    cut=0         → clip KDE at data range
    common_norm   → normalize each hue group independently

  sns.ecdfplot(data, x, hue, ax)
    → Empirical Cumulative Distribution Function

  sns.rugplot(data, x, hue, height, ax)
    → Tick marks showing individual data points (combine with KDE)
    """)


    # ------------------------------------------------------------------
    # 4. BOX PLOT, VIOLIN, AND STRIP PLOTS
    # ------------------------------------------------------------------
    print("4. BOX PLOT, VIOLIN, AND STRIP PLOTS")
    print("-" * 70)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Box, Violin & Strip Plots', fontsize=15, fontweight='bold', y=1.01)

    # 4a: boxplot
    sns.boxplot(data=df_sales, x='product', y='revenue',
                hue='product', palette='deep', legend=False,
                width=0.5, linewidth=1.5, fliersize=3, ax=axes[0, 0])
    axes[0, 0].set_title('boxplot', fontweight='bold')
    axes[0, 0].set_xlabel('')

    # 4b: violinplot
    sns.violinplot(data=df_sales, x='product', y='revenue',
                   hue='product', palette='muted', legend=False,
                   inner='quartile', linewidth=1.2, ax=axes[0, 1])
    axes[0, 1].set_title('violinplot — inner=quartile', fontweight='bold')
    axes[0, 1].set_xlabel('')

    # 4c: boxenplot (letter-value plot)
    sns.boxenplot(data=df_sales, x='product', y='revenue',
                  hue='product', palette='pastel', legend=False,
                  linewidth=1, ax=axes[0, 2])
    axes[0, 2].set_title('boxenplot (letter-value plot)', fontweight='bold')
    axes[0, 2].set_xlabel('')

    # 4d: stripplot
    sns.stripplot(data=df_ml, x='model', y='accuracy',
                  hue='model', palette='deep', legend=False,
                  size=6, alpha=0.7, jitter=True, ax=axes[1, 0])
    axes[1, 0].set_title('stripplot — individual points', fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=20)
    axes[1, 0].set_xlabel('')

    # 4e: swarmplot
    sns.swarmplot(data=df_ml, x='model', y='accuracy',
                  hue='model', palette='muted', legend=False,
                  size=5, ax=axes[1, 1])
    axes[1, 1].set_title('swarmplot — non-overlapping points', fontweight='bold')
    axes[1, 1].tick_params(axis='x', rotation=20)
    axes[1, 1].set_xlabel('')

    # 4f: violin + strip overlay (best of both worlds)
    sns.violinplot(data=df_ml, x='model', y='accuracy',
                   hue='model', palette='pastel', legend=False,
                   inner=None, linewidth=1, alpha=0.6, ax=axes[1, 2])
    sns.stripplot(data=df_ml, x='model', y='accuracy',
                  color='#1F3864', size=4, alpha=0.6,
                  jitter=True, ax=axes[1, 2])
    axes[1, 2].set_title('violin + strip overlay ★', fontweight='bold')
    axes[1, 2].tick_params(axis='x', rotation=20)
    axes[1, 2].set_xlabel('')

    fig.tight_layout()
    show_or_save(fig, '04_box_violin_strip.png')

    print("""
  sns.boxplot(data, x, y, hue, palette, width, fliersize, linewidth, ax)
    → Box = IQR, whiskers = 1.5×IQR, dots = outliers

  sns.violinplot(data, x, y, hue, inner, palette, ax)
    inner → 'box' (default)  'quartile'  'point'  'stick'  None

  sns.boxenplot(data, x, y, hue, ax)
    → Extended box plot: shows more quantiles — best for large datasets

  sns.stripplot(data, x, y, hue, size, alpha, jitter, ax)
    → All individual points (use alpha for overplotting)
    jitter=True  → add horizontal noise to separate overlapping points

  sns.swarmplot(data, x, y, hue, size, ax)
    → Non-overlapping points (slower, avoid with n > 500)

  💡 Combine violin (shape) + strip (individual points) for the richest view.
  💡 boxenplot is better than boxplot for large datasets (n > 1000).
    """)


    # ------------------------------------------------------------------
    # 5. SCATTER AND LINE PLOTS
    # ------------------------------------------------------------------
    print("5. SCATTER AND LINE PLOTS")
    print("-" * 70)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Scatter & Line Plots', fontsize=15, fontweight='bold', y=1.01)

    # 5a: basic scatterplot
    sns.scatterplot(data=df_sales, x='experience_years', y='revenue',
                    hue='product', palette='deep',
                    alpha=0.65, s=40, ax=axes[0, 0])
    axes[0, 0].set_title('scatterplot — hue by product', fontweight='bold')

    # 5b: scatter with size encoding
    sns.scatterplot(data=df_sales, x='experience_years', y='satisfaction',
                    hue='region', size='units',
                    sizes=(20, 200), palette='muted',
                    alpha=0.7, ax=axes[0, 1])
    axes[0, 1].set_title('scatterplot — hue + size encoding', fontweight='bold')
    axes[0, 1].legend(fontsize=8, ncol=2)

    # 5c: scatter with style encoding
    sns.scatterplot(data=df_sales.sample(120, random_state=1),
                    x='experience_years', y='revenue',
                    hue='region', style='quarter',
                    palette='deep', s=55, alpha=0.8, ax=axes[0, 2])
    axes[0, 2].set_title('scatterplot — hue + style (marker shape)', fontweight='bold')
    axes[0, 2].legend(fontsize=8)

    # 5d: lineplot with CI
    quarterly = (df_sales.groupby(['quarter', 'product'])['revenue']
                 .agg(['mean', 'std']).reset_index())
    quarterly.columns = ['quarter', 'product', 'mean_rev', 'std_rev']
    sns.lineplot(data=df_sales, x='quarter', y='revenue',
                 hue='product', palette='deep',
                 errorbar='sd', linewidth=2,
                 markers=True, dashes=False, ax=axes[1, 0])
    axes[1, 0].set_title('lineplot — with SD error band', fontweight='bold')
    axes[1, 0].set_xlabel('Quarter')

    # 5e: lineplot — multiple metrics
    ml_long = df_ml.melt(id_vars=['model', 'fold'],
                          value_vars=['accuracy', 'f1_score', 'precision', 'recall'],
                          var_name='metric', value_name='score')
    sns.lineplot(data=ml_long[ml_long['model'] == 'Random Forest'],
                 x='fold', y='score', hue='metric',
                 palette='Set2', linewidth=2, markers=True,
                 dashes=False, ax=axes[1, 1])
    axes[1, 1].set_title('lineplot — multiple metrics (Random Forest)', fontweight='bold')
    axes[1, 1].set_xlabel('CV Fold')
    axes[1, 1].set_ylabel('Score')

    # 5f: regplot (scatter + regression line)
    sns.regplot(data=df_sales, x='experience_years', y='revenue',
                scatter_kws={'alpha': 0.4, 's': 25, 'color': '#2E75B6'},
                line_kws={'color': '#C55A11', 'linewidth': 2.5},
                ci=95, ax=axes[1, 2])
    axes[1, 2].set_title('regplot — linear regression + 95% CI', fontweight='bold')

    fig.tight_layout()
    show_or_save(fig, '05_scatter_line.png')

    print("""
  sns.scatterplot(data, x, y, hue, size, style, palette, alpha, s, ax)
    hue   → color by column
    size  → marker size by column  (set sizes=(min, max))
    style → marker shape by column

  sns.lineplot(data, x, y, hue, style, errorbar, linewidth, markers, ax)
    errorbar → 'ci' (95% CI)  'sd' (std dev)  'se' (std error)  None
    markers  → True/False or dict of markers per hue
    dashes   → True/False or dict

  sns.regplot(data, x, y, ci, order, scatter_kws, line_kws, ax)
    ci    → confidence interval width (default 95)
    order → polynomial degree (1=linear, 2=quadratic, ...)

  sns.lmplot(data, x, y, hue, col, row, ci, ...)
    → Figure-level regplot: supports faceting by col= and row=
    """)


    # ------------------------------------------------------------------
    # 6. CATEGORICAL PLOTS
    # ------------------------------------------------------------------
    print("6. CATEGORICAL PLOTS")
    print("-" * 70)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Categorical Plots', fontsize=15, fontweight='bold', y=1.01)

    # 6a: barplot (with CI)
    sns.barplot(data=df_sales, x='product', y='revenue',
                hue='product', palette='deep', legend=False,
                errorbar='ci', capsize=0.1,
                edgecolor='white', linewidth=1.2, ax=axes[0, 0])
    axes[0, 0].set_title('barplot — mean + 95% CI', fontweight='bold')
    axes[0, 0].set_xlabel('')

    # 6b: barplot grouped by region
    sns.barplot(data=df_sales, x='region', y='revenue',
                hue='product', palette='muted',
                errorbar=None, edgecolor='white',
                linewidth=0.8, ax=axes[0, 1])
    axes[0, 1].set_title('barplot — grouped (hue=product)', fontweight='bold')
    axes[0, 1].set_xlabel('')
    axes[0, 1].legend(fontsize=9, title='Product')

    # 6c: countplot
    sns.countplot(data=df_sales, x='product', hue='quarter',
                  palette='pastel', edgecolor='white',
                  linewidth=0.8, ax=axes[0, 2])
    axes[0, 2].set_title('countplot — frequency by quarter', fontweight='bold')
    axes[0, 2].set_xlabel('')
    axes[0, 2].legend(fontsize=9, title='Quarter')

    # 6d: pointplot
    sns.pointplot(data=df_sales, x='quarter', y='revenue',
                  hue='product', palette='deep',
                  markers=['o','s','^','D'], linestyles=['-','--','-.',':'],
                  errorbar='ci', capsize=0.1,
                  dodge=True, ax=axes[1, 0])
    axes[1, 0].set_title('pointplot — mean + CI per quarter', fontweight='bold')
    axes[1, 0].legend(fontsize=9)

    # 6e: catplot-style: satisfaction by product and region (horizontal)
    region_prod = (df_sales.groupby(['region', 'product'])['satisfaction']
                   .mean().reset_index())
    sns.barplot(data=region_prod, y='region', x='satisfaction',
                hue='product', palette='deep',
                orient='h', errorbar=None, ax=axes[1, 1])
    axes[1, 1].set_title('barplot — horizontal, satisfaction by region', fontweight='bold')
    axes[1, 1].axvline(3.8, color='gray', linestyle='--', linewidth=1)
    axes[1, 1].legend(fontsize=9)

    # 6f: countplot sorted + annotated
    order = df_sales['product'].value_counts().index
    ax_c  = axes[1, 2]
    sns.countplot(data=df_sales, y='product', order=order,
                  hue='product', palette='muted', legend=False,
                  edgecolor='white', ax=ax_c)
    for bar in ax_c.patches:
        w = bar.get_width()
        if w > 0:
            ax_c.text(w + 1, bar.get_y() + bar.get_height() / 2,
                      f'{int(w)}', va='center', fontsize=9)
    ax_c.set_title('countplot — horizontal + value labels', fontweight='bold')
    ax_c.set_xlabel('Count')

    fig.tight_layout()
    show_or_save(fig, '06_categorical_plots.png')

    print("""
  sns.barplot(data, x, y, hue, errorbar, capsize, order, palette, ax)
    errorbar → 'ci' (95% CI, default)  'sd'  'se'  None
    capsize  → width of error bar caps
    order    → list to control category order
    estimator→ function to aggregate (default: mean)
               e.g. estimator=np.median for median bars

  sns.countplot(data, x, hue, order, palette, ax)
    → Counts occurrences of each category (no y= needed)

  sns.pointplot(data, x, y, hue, dodge, markers, linestyles, errorbar, ax)
    → Shows means as points connected by lines — useful for trends
    dodge → offset hue groups horizontally to avoid overlap

  💡 barplot  → best for comparing means across categories
  💡 countplot → best for showing frequency distributions
  💡 pointplot → best for showing trends over ordered categories (e.g. time)
    """)


    # ------------------------------------------------------------------
    # 7. HEATMAP AND CORRELATION
    # ------------------------------------------------------------------
    print("7. HEATMAP AND CORRELATION")
    print("-" * 70)

    fig, axes = plt.subplots(1, 3, figsize=(19, 6))
    fig.suptitle('Heatmaps & Correlation', fontsize=15, fontweight='bold', y=1.02)

    # 7a: correlation heatmap
    numeric_cols = ['revenue', 'units', 'satisfaction', 'experience_years']
    corr = df_sales[numeric_cols].corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))   # upper triangle mask
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', center=0,
                vmin=-1, vmax=1, linewidths=0.5,
                square=True, ax=axes[0],
                annot_kws={'size': 11, 'weight': 'bold'})
    axes[0].set_title('Correlation Matrix\n(lower triangle)', fontweight='bold')

    # 7b: pivot heatmap — revenue by region × product
    pivot = df_sales.pivot_table(values='revenue', index='region',
                                  columns='product', aggfunc='mean')
    sns.heatmap(pivot, annot=True, fmt='.0f',
                cmap='YlOrRd', linewidths=0.5,
                linecolor='white', ax=axes[1],
                cbar_kws={'label': 'Mean Revenue (€)'},
                annot_kws={'size': 10})
    axes[1].set_title('Pivot Heatmap\nMean Revenue: Region × Product', fontweight='bold')
    axes[1].set_xlabel('Product')
    axes[1].set_ylabel('Region')

    # 7c: model performance heatmap
    perf = df_ml.groupby('model')[['accuracy','f1_score','precision','recall']].mean()
    perf.columns = ['Accuracy', 'F1 Score', 'Precision', 'Recall']
    sns.heatmap(perf, annot=True, fmt='.3f',
                cmap='RdYlGn', vmin=0.78, vmax=0.96,
                linewidths=0.5, linecolor='white',
                ax=axes[2], annot_kws={'size': 10, 'weight': 'bold'},
                cbar_kws={'label': 'Score'})
    axes[2].set_title('Model Performance Heatmap\n(mean over 10 CV folds)', fontweight='bold')
    axes[2].set_xlabel('')
    axes[2].tick_params(axis='y', rotation=0)

    fig.tight_layout()
    show_or_save(fig, '07_heatmap.png')

    print("""
  sns.heatmap(data, annot, fmt, cmap, center, vmin, vmax,
              mask, linewidths, square, ax)
    data      → 2D array or DataFrame (e.g. corr matrix or pivot table)
    annot     → True: show values in cells
    fmt       → format string: '.2f'  '.0f'  'd'  '.1%'
    cmap      → colormap: 'coolwarm' 'RdYlGn' 'Blues' 'YlOrRd'
    center    → value to center the colormap (use 0 for correlations)
    vmin/vmax → fix color scale range
    mask      → boolean array: True = hide that cell
    square    → True: make cells square
    linewidths→ grid line width between cells

  CORRELATION MATRIX PATTERN:
    corr = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))  ← hide upper triangle
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', center=0)

  PIVOT TABLE PATTERN:
    pivot = df.pivot_table(values='metric', index='rowvar',
                           columns='colvar', aggfunc='mean')
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='Blues')
    """)


    # ------------------------------------------------------------------
    # 8. PAIRPLOT AND JOINTPLOT
    # ------------------------------------------------------------------
    print("8. PAIRPLOT AND JOINTPLOT")
    print("-" * 70)

    # 8a: pairplot
    sample = df_sales[['revenue', 'units', 'satisfaction',
                        'experience_years', 'product']].sample(200, random_state=1)
    g = sns.pairplot(sample, hue='product', palette='deep',
                     diag_kind='kde',
                     plot_kws={'alpha': 0.5, 's': 20},
                     diag_kws={'fill': True, 'alpha': 0.4})
    g.figure.suptitle('Pairplot — All numeric vs All numeric, hue=product',
                       fontsize=13, fontweight='bold', y=1.02)
    show_or_save(g.figure, '08a_pairplot.png')

    # 8b: pairplot — corner only
    g2 = sns.pairplot(sample[['revenue','units','satisfaction']],
                      corner=True, diag_kind='hist',
                      plot_kws={'alpha':0.5, 'color':'#2E75B6'},
                      diag_kws={'color':'#2E75B6', 'edgecolor':'white'})
    g2.figure.suptitle('Pairplot — corner=True (lower triangle only)',
                        fontsize=13, fontweight='bold', y=1.02)
    show_or_save(g2.figure, '08b_pairplot_corner.png')

    # 8c: jointplot — scatter + marginals
    fig_j = sns.jointplot(data=df_sales, x='experience_years', y='revenue',
                          hue='product', palette='deep',
                          alpha=0.5, height=7)
    fig_j.figure.suptitle('Jointplot — scatter + marginal KDE',
                           fontsize=12, fontweight='bold', y=1.02)
    show_or_save(fig_j.figure, '08c_jointplot_scatter.png')

    # 8d: jointplot — hexbin
    fig_h = sns.jointplot(data=df_sales, x='experience_years', y='revenue',
                          kind='hex', height=7,
                          joint_kws={'cmap': 'Blues', 'gridsize': 20},
                          marginal_kws={'color': '#2E75B6', 'fill': True})
    fig_h.figure.suptitle('Jointplot — hexbin (density)',
                           fontsize=12, fontweight='bold', y=1.02)
    show_or_save(fig_h.figure, '08d_jointplot_hex.png')

    print("""
  sns.pairplot(data, hue, palette, vars, diag_kind, kind,
               plot_kws, diag_kws, corner)
    → Grid of scatterplots for all variable pairs
    hue       → color by a categorical column
    vars      → subset of columns to include
    diag_kind → 'auto' 'hist' 'kde' None
    kind      → 'scatter' (default)  'kde'  'hist'  'reg'
    corner    → True: show only lower triangle (faster)
    Returns   → PairGrid object (use g.figure to access Figure)

  sns.jointplot(data, x, y, hue, kind, height, ratio, marginal_kws)
    kind → 'scatter' (default)  'kde'  'hex'  'hist'  'reg'  'resid'
    height   → figure size (square)
    ratio    → size ratio of joint to marginal plots
    Returns  → JointGrid object (use g.figure for the Figure)

  💡 pairplot is the fastest way to get an overview of all variable relationships.
  💡 jointplot is best when focusing on two specific variables.
  💡 With n > 1000, use corner=True and sample your data first.
    """)


    # ------------------------------------------------------------------
    # 9. FACET GRIDS (Figure-level small multiples)
    # ------------------------------------------------------------------
    print("9. FACET GRIDS — Small Multiples")
    print("-" * 70)

    # 9a: displot with col faceting
    g = sns.displot(data=df_sales, x='revenue', col='product',
                    hue='region', kind='kde', fill=True, alpha=0.3,
                    height=4, aspect=1.1, palette='deep')
    g.set_titles(col_template='{col_name}', fontweight='bold')
    g.set_axis_labels('Revenue (€)', 'Density')
    g.figure.suptitle('displot — KDE per product, hue=region',
                       fontsize=13, fontweight='bold', y=1.04)
    show_or_save(g.figure, '09a_displot_facet.png')

    # 9b: relplot — scatter with col + row faceting
    g2 = sns.relplot(data=df_sales.sample(200, random_state=5),
                     x='experience_years', y='revenue',
                     col='product', row='quarter',
                     hue='region', palette='deep',
                     alpha=0.6, s=35, height=2.8, aspect=1.1)
    g2.set_titles(row_template='{row_name}', col_template='{col_name}',
                  fontweight='bold')
    g2.set_axis_labels('Experience (years)', 'Revenue (€)')
    g2.figure.suptitle('relplot — product × quarter facet grid',
                        fontsize=13, fontweight='bold', y=1.02)
    show_or_save(g2.figure, '09b_relplot_facet.png')

    # 9c: catplot — box per product
    g3 = sns.catplot(data=df_ml, x='model', y='accuracy',
                     kind='box', col='model', col_wrap=3,
                     hue='model', legend=False,
                     palette='pastel', height=4, aspect=0.9,
                     sharey=True)
    g3.set_titles(col_template='{col_name}', fontweight='bold')
    g3.set_axis_labels('', 'Accuracy')
    g3.set_xticklabels([])
    g3.figure.suptitle('catplot — boxplot per model (col_wrap=3)',
                        fontsize=13, fontweight='bold', y=1.03)
    show_or_save(g3.figure, '09c_catplot_facet.png')

    print("""
  FIGURE-LEVEL FUNCTIONS:
    sns.displot(data, x, hue, col, row, kind, height, aspect, col_wrap)
      kind → 'hist'  'kde'  'ecdf'

    sns.relplot(data, x, y, hue, size, style, col, row, kind, height, aspect)
      kind → 'scatter'  'line'

    sns.catplot(data, x, y, hue, col, row, kind, height, aspect, col_wrap)
      kind → 'strip'  'swarm'  'box'  'violin'  'boxen'  'point'  'bar'  'count'

  COMMON PARAMETERS:
    col       → facet by column (one subplot per unique value)
    row       → facet by row
    col_wrap  → wrap columns after n (avoids very wide figures)
    height    → height of each subplot in inches
    aspect    → width = height × aspect

  CUSTOMIZING FacetGrid / PairGrid:
    g.set_titles(col_template='{col_name}', row_template='{row_name}')
    g.set_axis_labels('X Label', 'Y Label')
    g.set(xlim=(0, 100))             ← set axis limits on all subplots
    g.add_legend()                   ← add/move legend
    g.figure.suptitle('...')         ← overall figure title
    g.figure.savefig('out.png', bbox_inches='tight')

  💡 Figure-level functions make it trivial to create small multiples.
  💡 Use col_wrap to avoid excessively wide figures.
    """)


    # ------------------------------------------------------------------
    # 10. SEABORN + MATPLOTLIB INTEGRATION
    # ------------------------------------------------------------------
    print("10. SEABORN + MATPLOTLIB INTEGRATION")
    print("-" * 70)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Seaborn + Matplotlib Integration', fontsize=14,
                 fontweight='bold')

    # Left: Seaborn plot + Matplotlib annotations
    ax = axes[0]
    sns.boxplot(data=df_ml, x='model', y='accuracy',
                hue='model', palette='deep', legend=False,
                width=0.5, ax=ax)

    # Matplotlib fine-tuning on top
    ax.axhline(0.90, color='red', linestyle='--', linewidth=1.5,
               label='Target 0.90', zorder=5)
    ax.axhline(df_ml['accuracy'].mean(), color='gray', linestyle=':',
               linewidth=1.2, label=f"Overall mean ({df_ml['accuracy'].mean():.3f})")
    ax.set_title('Seaborn boxplot +\nMatplotlib reference lines', fontweight='bold')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=15)
    ax.legend(fontsize=9)
    ax.set_ylim(0.75, 1.0)

    # Annotate best model
    best_model = df_ml.groupby('model')['accuracy'].mean().idxmax()
    best_val   = df_ml.groupby('model')['accuracy'].mean().max()
    best_x     = list(df_ml['model'].unique()).index(best_model)
    ax.annotate(f'Best: {best_model}\n({best_val:.3f})',
                xy=(best_x, best_val),
                xytext=(best_x - 1.5, best_val + 0.02),
                fontsize=9, color='#1F3864',
                arrowprops=dict(arrowstyle='->', color='#1F3864'))

    # Right: dual-axis — Seaborn bar + Matplotlib line
    ax2   = axes[1]
    ax2_r = ax2.twinx()   # second y-axis on the right

    prod_stats = df_sales.groupby('product').agg(
        mean_rev=('revenue', 'mean'),
        mean_sat=('satisfaction', 'mean')
    ).reset_index()

    colors = sns.color_palette('deep', 4)
    bars   = ax2.bar(prod_stats['product'], prod_stats['mean_rev'],
                     color=colors, edgecolor='white', alpha=0.8, width=0.5)
    ax2_r.plot(prod_stats['product'], prod_stats['mean_sat'],
               'o-', color='#C55A11', linewidth=2.5, markersize=9,
               zorder=5, label='Satisfaction')

    ax2.set_title('Seaborn palette + Matplotlib dual axis', fontweight='bold')
    ax2.set_ylabel('Mean Revenue (€)', color='#1F3864')
    ax2_r.set_ylabel('Mean Satisfaction', color='#C55A11')
    ax2_r.set_ylim(3.0, 4.5)
    ax2_r.tick_params(axis='y', colors='#C55A11')
    ax2_r.legend(loc='upper right', fontsize=10)

    for bar, val in zip(bars, prod_stats['mean_rev']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 f'€{val:.0f}', ha='center', va='bottom', fontsize=9,
                 fontweight='bold')

    fig.tight_layout()
    show_or_save(fig, '10_seaborn_matplotlib.png')

    print("""
  THE PATTERN:
    1. Create fig/axes with plt.subplots()
    2. Draw with Seaborn (pass ax=ax)
    3. Fine-tune with Matplotlib (ax.set_*, ax.annotate, ax.axhline, ...)

  USEFUL MATPLOTLIB ADDITIONS ON SEABORN PLOTS:
    ax.axhline(val, color, ls)        → reference line
    ax.annotate(text, xy, xytext)     → arrow + label
    ax.set_ylim(a, b)                 → fix axis range
    ax.tick_params(rotation=45)       → rotate labels
    ax2 = ax.twinx()                  → second y-axis

  ACCESSING FIGURE FROM FIGURE-LEVEL FUNCTIONS:
    g = sns.displot(...)
    g.figure.set_size_inches(12, 5)
    g.figure.savefig('out.png', bbox_inches='tight')
    """)


    # ------------------------------------------------------------------
    # 11. THEMES AND STYLING
    # ------------------------------------------------------------------
    print("11. THEMES AND STYLING")
    print("-" * 70)

    styles  = ['white', 'whitegrid', 'dark', 'darkgrid', 'ticks']
    x       = np.linspace(0, 2 * np.pi, 100)

    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    fig.suptitle('Seaborn Styles', fontsize=13, fontweight='bold', y=1.03)

    for ax, style in zip(axes, styles):
        with sns.axes_style(style): # noqa
            ax2 = ax
            sns.lineplot(x=x, y=np.sin(x), ax=ax2, color='#2E75B6', linewidth=2)
            sns.lineplot(x=x, y=np.cos(x), ax=ax2, color='#C55A11', linewidth=2)
            ax2.set_title(f"style='{style}'", fontweight='bold', fontsize=10)
            ax2.set_xticks([])

    fig.tight_layout()
    show_or_save(fig, '11_styles.png')

    print("""
  STYLES (background + grid):
    sns.set_theme(style='whitegrid')   ← most common for EDA
    sns.set_theme(style='darkgrid')    ← good for dark presentations
    sns.set_theme(style='white')       ← clean, no grid
    sns.set_theme(style='ticks')       ← minimal, publication-ready
    sns.set_theme(style='dark')        ← dark background, no grid

  CONTEXT (font / element size):
    sns.set_theme(context='paper')     ← small (8pt) — publications
    sns.set_theme(context='notebook')  ← medium (default) — notebooks
    sns.set_theme(context='talk')      ← large — presentations
    sns.set_theme(context='poster')    ← very large — posters

  FONT SCALE:
    sns.set_theme(font_scale=1.4)      ← multiply all font sizes

  TEMPORARY (for one plot only):
    with sns.axes_style('ticks'):
        sns.histplot(...)

  PALETTES:
    sns.set_palette('colorblind')      ← accessible to colorblind users ★
    sns.color_palette('husl', n)       ← n evenly spaced colors (HLS space)
    sns.color_palette('rocket', n)     ← perceptually uniform sequential
    sns.light_palette('navy', n)       ← light-to-dark single hue
    sns.diverging_palette(240, 10, n=n)← custom diverging palette

  💡 For publications: style='ticks', context='paper'
  💡 For notebooks/EDA: style='whitegrid', context='notebook'
  💡 For accessibility: palette='colorblind'
    """)


    # ------------------------------------------------------------------
    # 12. COMMON MISTAKES
    # ------------------------------------------------------------------
    print("12. COMMON MISTAKES")
    print("-" * 70)
    print("""
  Mistake 1 — Mixing axes-level and figure-level incorrectly:
    g = sns.displot(data=df, x='col')       ← figure-level
    g.set_title('...')                       ← AttributeError! g is a FacetGrid
    g.figure.suptitle('...')                ← correct
    g.set_titles(col_template='{col_name}') ← correct for subplot titles

  Mistake 2 — Forgetting ax= in multi-subplot layouts:
    fig, axes = plt.subplots(1, 2)
    sns.histplot(data=df, x='col')          ← plots on wrong/new axes!
    sns.histplot(data=df, x='col', ax=axes[0])  ← correct

  Mistake 3 — Not resetting theme between plots:
    sns.set_theme(style='dark')
    # All subsequent plots will use dark style!
    sns.reset_defaults()                    ← reset when done

  Mistake 4 — hue without a column name string:
    sns.scatterplot(data=df, x='a', y='b', hue=df['col'])  ← can cause issues
    sns.scatterplot(data=df, x='a', y='b', hue='col')      ← correct

  Mistake 5 — Saving figure-level plots:
    g = sns.pairplot(df)
    plt.savefig('out.png')                  ← may save blank figure!
    g.figure.savefig('out.png', bbox_inches='tight')  ← correct

  Mistake 6 — barplot default changed in Seaborn 0.13+:
    Old: sns.barplot showed mean with bootstrapped CI
    New: estimator=mean is still default but errorbar='ci' must be explicit
    Always specify: sns.barplot(..., errorbar='ci')  or  errorbar=None

  Mistake 7 — pairplot with too many variables:
    sns.pairplot(df)                        ← with 20 cols → 400 subplots!
    sns.pairplot(df, vars=['a','b','c'])    ← select relevant columns
    """)


    # ------------------------------------------------------------------
    # 13. QUICK REFERENCE
    # ------------------------------------------------------------------
    print("13. QUICK REFERENCE")
    print("-" * 70)
    print()
    print(f"  {'Function':<38} {'Description'}")
    print(f"  {'-'*38} {'-'*42}")

    ref = [
        ("SETUP", ""),
        ("sns.set_theme(style, context, palette)", "Set global theme"),
        ("sns.reset_defaults()",                   "Revert to Matplotlib defaults"),
        ("sns.color_palette(name, n)",             "Get/preview a palette"),
        ("DISTRIBUTION", ""),
        ("sns.histplot(data, x, hue, bins, kde, stat, ax)", "Histogram"),
        ("sns.kdeplot(data, x, hue, fill, bw_adjust, ax)",  "KDE curve"),
        ("sns.ecdfplot(data, x, hue, ax)",                  "Empirical CDF"),
        ("sns.rugplot(data, x, hue, height, ax)",           "Rug (tick marks)"),
        ("BOX / VIOLIN / STRIP", ""),
        ("sns.boxplot(data, x, y, hue, width, ax)",         "Box plot"),
        ("sns.violinplot(data, x, y, hue, inner, ax)",      "Violin plot"),
        ("sns.boxenplot(data, x, y, hue, ax)",              "Letter-value plot"),
        ("sns.stripplot(data, x, y, hue, jitter, alpha, ax)","Individual points"),
        ("sns.swarmplot(data, x, y, hue, size, ax)",        "Non-overlapping points"),
        ("SCATTER / LINE", ""),
        ("sns.scatterplot(data, x, y, hue, size, style, ax)","Scatter plot"),
        ("sns.lineplot(data, x, y, hue, errorbar, ax)",     "Line + error band"),
        ("sns.regplot(data, x, y, ci, order, ax)",          "Regression line + CI"),
        ("sns.lmplot(data, x, y, hue, col, row)",           "regplot with facets"),
        ("CATEGORICAL", ""),
        ("sns.barplot(data, x, y, hue, errorbar, order, ax)","Bar + CI"),
        ("sns.countplot(data, x, hue, order, ax)",          "Frequency bars"),
        ("sns.pointplot(data, x, y, hue, dodge, ax)",       "Points + line"),
        ("HEATMAP", ""),
        ("sns.heatmap(data, annot, fmt, cmap, center, mask)","Heatmap"),
        ("PAIRPLOT / JOINTPLOT", ""),
        ("sns.pairplot(data, hue, vars, diag_kind, corner)", "All-vs-all scatter"),
        ("sns.jointplot(data, x, y, hue, kind, height)",    "Two-variable joint"),
        ("FIGURE-LEVEL (FACETING)", ""),
        ("sns.displot(data, x, hue, col, row, kind)",       "Distribution facets"),
        ("sns.relplot(data, x, y, hue, col, row, kind)",    "Relation facets"),
        ("sns.catplot(data, x, y, hue, col, row, kind)",    "Categorical facets"),
        ("FACETGRID METHODS", ""),
        ("g.set_titles(col_template='{col_name}')",         "Set subplot titles"),
        ("g.set_axis_labels('X', 'Y')",                     "Set axis labels"),
        ("g.set(xlim=(a,b), ylim=(c,d))",                   "Set limits on all axes"),
        ("g.figure.suptitle('...')",                        "Overall figure title"),
        ("g.figure.savefig('out.png', bbox_inches='tight')","Save figure-level plot"),
    ]

    for item, desc in ref:
        if desc == "":
            print(f"\n  ── {item} {'─'*(65-len(item))}")
        else:
            print(f"  {item:<38} {desc}")

    print()
    print(f"\nDone! Check '{OUTDIR}/' for all saved figures.\n" if SAVE
          else "\nDone! All plots rendered inline.\n")


main()


"""
SUMMARY — SEABORN
=======================================================

SETUP:
  import seaborn as sns
  sns.set_theme(style='whitegrid', palette='deep')

GOLDEN RULE:
  Axes-level  → pass ax=ax, returns Axes → use ax.set_*()
  Figure-level → creates its own Figure, returns FacetGrid
               → use g.set_titles(), g.figure.suptitle()

DISTRIBUTION:
  sns.histplot    → histogram (+ optional KDE overlay)
  sns.kdeplot     → smooth density curve
  sns.ecdfplot    → cumulative distribution
  sns.rugplot     → individual data ticks (combine with KDE)

BOX / VIOLIN / STRIP:
  sns.boxplot     → IQR box, whiskers, outlier dots
  sns.violinplot  → distribution shape (inner='quartile' is great)
  sns.boxenplot   → letter-value plot (better for large n)
  sns.stripplot   → all individual points (jitter=True)
  sns.swarmplot   → non-overlapping points (slow for n>500)
  ★ Combine violinplot(inner=None) + stripplot for richest view

SCATTER / LINE:
  sns.scatterplot → hue + size + style encoding
  sns.lineplot    → mean + confidence band (errorbar='ci'/'sd')
  sns.regplot     → scatter + regression line + CI
  sns.lmplot      → regplot with col/row faceting

CATEGORICAL:
  sns.barplot     → mean + CI bars (errorbar='ci')
  sns.countplot   → frequency bars (no y= needed)
  sns.pointplot   → connected means (good for trends)

HEATMAP:
  sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
              center=0, mask=np.triu(ones))

PAIRPLOT / JOINTPLOT:
  sns.pairplot(df, hue='cat', corner=True, vars=[...])
  sns.jointplot(data, x, y, kind='scatter'/'kde'/'hex')

FACETING (Figure-level):
  sns.displot / relplot / catplot  → col=, row=, col_wrap=

INTEGRATION WITH MATPLOTLIB:
  fig, ax = plt.subplots()
  sns.anyplot(data=df, ax=ax)      # draw with Seaborn
  ax.set_title(...)                # fine-tune with Matplotlib

COMMON PITFALLS:
  • g.set_title() → wrong; use g.figure.suptitle() or g.set_titles()
  • Forget ax= in subplots → plots on wrong axes
  • pairplot with too many columns → sample and select vars=[...]
  • barplot CI changed in v0.13 → always set errorbar= explicitly
  • Save figure-level: g.figure.savefig(...), not plt.savefig(...)

REMEMBER:
  "Seaborn = Matplotlib + statistics + DataFrames.
   Use Seaborn for the plot, Matplotlib for the finishing touches."
"""