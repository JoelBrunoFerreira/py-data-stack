"""
PLOTLY - COMPLETE GUIDE
=========================

Plotly is an interactive visualization library. Unlike Matplotlib/Seaborn
(which produce static images), Plotly generates interactive HTML charts:
hover tooltips, zoom, pan, click filters, and animations — all built-in.

Two interfaces:
  plotly.express (px)       → high-level, one-liner charts (recommended start)
  plotly.graph_objects (go) → full control, used to customize px output

Key Characteristics:
- Every chart is interactive by default (hover, zoom, pan)
- Output is an HTML file or renders inline in Jupyter/Dash
- Works with Pandas DataFrames directly
- Exports to HTML, PNG, PDF, SVG (PNG/PDF require kaleido)
- Foundation for Dash (Python dashboards)

Installation:
  pip install plotly
  pip install kaleido       ← required for PNG/PDF/SVG export

Common Uses:
- Interactive EDA
- Shareable HTML reports
- Web dashboards (with Dash)
- Presentations and storytelling
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import statsmodels
from IPython import get_ipython
import os

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
OUTDIR  = "plotly_output"
os.makedirs(OUTDIR, exist_ok=True)


def show_or_save(fig, filename, width=1100, height=600):
    """
    Jupyter  → fig.show()   renders interactive chart inline.
    Script   → saves as self-contained HTML (interactive!) +
               tries PNG via kaleido (static preview).
    """
    if JUPYTER:
        fig.show()
    else:
        # Always save interactive HTML
        html_path = os.path.join(OUTDIR, filename.replace('.html', '') + '.html')
        fig.write_html(html_path)
        print(f"  → HTML: {html_path}")

        # Try static PNG (needs kaleido)
        try:
            png_path = os.path.join(OUTDIR, filename.replace('.html','') + '.png')
            fig.write_image(png_path, width=width, height=height, scale=1.5)
            print(f"  → PNG:  {png_path}")
        except Exception:
            print(f"     (PNG skipped — install kaleido: pip install kaleido)")


# ──────────────────────────────────────────────────────────────────────────────
# SHARED DATASETS
# ──────────────────────────────────────────────────────────────────────────────

def make_sales_df(seed=42):
    rng      = np.random.default_rng(seed)
    n        = 500
    regions  = rng.choice(['North','South','East','West'], n)
    products = rng.choice(['Laptop','Phone','Tablet','Watch'], n)
    quarters = rng.choice(['Q1','Q2','Q3','Q4'], n)
    months   = rng.choice(range(1, 13), n)
    base     = {'Laptop':1200,'Phone':800,'Tablet':500,'Watch':300}
    revenue  = np.array([base[p] for p in products])
    revenue  = revenue * rng.uniform(0.7, 1.4, n) + rng.normal(0, 50, n)
    units    = (rng.integers(5, 30, n)).astype(int)
    margin   = np.clip(rng.normal(0.28, 0.08, n), 0.05, 0.55)
    sat      = np.clip(rng.normal(3.8, 0.6, n), 1, 5).round(1)
    return pd.DataFrame({
        'region': regions, 'product': products,
        'quarter': quarters, 'month': months,
        'revenue': revenue.round(2), 'units': units,
        'margin': margin.round(3), 'satisfaction': sat,
        'experience_years': rng.integers(1, 15, n),
    })


def make_monthly_df(seed=42):
    rng      = np.random.default_rng(seed)
    products = ['Laptop','Phone','Tablet','Watch']
    rows     = []
    for p in products:
        base = {'Laptop':1200,'Phone':800,'Tablet':500,'Watch':300}[p]
        for month in range(1, 13):
            trend = 1 + 0.04 * month
            rows.append({
                'product': p, 'month': month,
                'revenue': base * trend * rng.uniform(0.85, 1.15),
                'units':   int(rng.integers(50, 200)),
            })
    return pd.DataFrame(rows)


def make_ml_df(seed=7):
    rng    = np.random.default_rng(seed)
    models = ['Random Forest','XGBoost','SVM','Logistic Reg.','KNN']
    rows   = []
    base   = {'Random Forest':0.91,'XGBoost':0.93,'SVM':0.88,
              'Logistic Reg.':0.85,'KNN':0.82}
    for model in models:
        for fold in range(10):
            rows.append({
                'model': model, 'fold': fold + 1,
                'accuracy':  np.clip(rng.normal(base[model],       0.015), 0.7, 1.0),
                'f1_score':  np.clip(rng.normal(base[model]-0.02,  0.018), 0.7, 1.0),
                'precision': np.clip(rng.normal(base[model]+0.01,  0.016), 0.7, 1.0),
                'recall':    np.clip(rng.normal(base[model]-0.015, 0.020), 0.7, 1.0),
            })
    return pd.DataFrame(rows)


df_sales   = make_sales_df()
df_monthly = make_monthly_df()
df_ml      = make_ml_df()


# ──────────────────────────────────────────────────────────────────────────────
# PLOTLY COLOR PALETTE (consistent across all charts)
# ──────────────────────────────────────────────────────────────────────────────
COLORS = px.colors.qualitative.D3       # D3, Plotly, Safe, Vivid, Pastel, ...


def apply_theme(fig, title=None, height=500):
    """Apply a consistent, clean theme to any Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='#1F3864'),
                   x=0.5, xanchor='center') if title else {},
        height=height,
        font=dict(family='Arial', size=13, color='#404040'),
        paper_bgcolor='white',
        plot_bgcolor='#F8F9FA',
        legend=dict(bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='#CCCCCC', borderwidth=1),
        margin=dict(l=60, r=40, t=80, b=60),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#E0E0E0', zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='#E0E0E0', zeroline=False)
    return fig


def main():

    print("=== PLOTLY - COMPLETE GUIDE ===\n")

    import plotly
    print(f"Plotly version: {plotly.__version__}\n")


    # ------------------------------------------------------------------
    # 1. IMPORTING AND CORE CONCEPTS
    # ------------------------------------------------------------------
    print("1. IMPORTING AND CORE CONCEPTS")
    print("-" * 70)
    print("""
  import plotly.express as px               # high-level (start here)
  import plotly.graph_objects as go         # full control / customization
  from plotly.subplots import make_subplots # multi-panel layouts

  CORE CONCEPTS:
    Every Plotly chart is a Figure object:
      fig = px.scatter(df, x='col1', y='col2')

    A Figure has two main components:
      fig.data    → list of traces (the actual chart elements)
      fig.layout  → everything else (title, axes, legend, colors, ...)

    Updating a figure:
      fig.update_layout(title='My Chart', height=500)
      fig.update_traces(marker_size=8, opacity=0.7)
      fig.update_xaxes(title='X Label', showgrid=True)
      fig.update_yaxes(title='Y Label', range=[0, 100])

  DISPLAYING:
    fig.show()                    ← opens in browser / renders in Jupyter
    fig.write_html('chart.html')  ← save interactive HTML (shareable!)
    fig.write_image('chart.png')  ← save static PNG (needs kaleido)
    fig.write_image('chart.pdf')  ← save PDF (needs kaleido)

  JUPYTER SETUP:
    import plotly.io as pio
    pio.renderers.default = 'notebook'   ← inline in classic Jupyter
    pio.renderers.default = 'iframe'     ← inline in JupyterLab

  💡 fig.write_html() produces a fully self-contained file you can
     email or share — no server needed, opens in any browser.
    """)


    # ------------------------------------------------------------------
    # 2. LINE CHART
    # ------------------------------------------------------------------
    print("2. LINE CHART")
    print("-" * 70)

    # 2a: basic line
    fig = px.line(df_monthly, x='month', y='revenue',
                  color='product',
                  color_discrete_sequence=COLORS,
                  markers=True,
                  labels={'revenue': 'Revenue (€)', 'month': 'Month',
                          'product': 'Product'},
                  title='Monthly Revenue by Product')

    fig.update_traces(line_width=2.5, marker_size=7)
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        hovermode='x unified',   # show all series on hover at same x
    )
    apply_theme(fig, height=480)
    show_or_save(fig, '02_line_chart')

    # 2b: line with range selector (time-series style)
    fig2 = px.line(df_monthly, x='month', y='units',
                   color='product',
                   color_discrete_sequence=COLORS,
                   markers=True,
                   title='Monthly Units Sold — with Range Selector')
    fig2.update_layout(
        hovermode='x unified',
        xaxis=dict(
            rangeslider=dict(visible=True),   # ← interactive range slider
            tickmode='linear', tick0=1, dtick=1,
        )
    )
    apply_theme(fig2, height=500)
    show_or_save(fig2, '02b_line_range_slider')

    print("""
  px.line(data, x, y, color, line_dash, markers, symbol,
          facet_col, facet_row, animation_frame, labels, title)

    color       → separate line per category
    line_dash   → dashed lines by category
    markers     → True: show markers on line
    facet_col   → small multiples by column

  HOVER MODES:
    hovermode='closest'    ← one tooltip per point (default)
    hovermode='x unified'  ← all series in one tooltip at same x ★
    hovermode='x'          ← crosshair on x

  RANGE SLIDER:
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

  CUSTOM HOVER TEXT:
    px.line(..., hover_data=['extra_col'],
            hover_name='label_col')
    """)


    # ------------------------------------------------------------------
    # 3. SCATTER PLOT
    # ------------------------------------------------------------------
    print("3. SCATTER PLOT")
    print("-" * 70)

    # 3a: scatter — hue + size + hover
    fig = px.scatter(df_sales, x='experience_years', y='revenue',
                     color='product', size='units',
                     size_max=20,
                     symbol='region',
                     hover_data=['satisfaction', 'margin', 'quarter'],
                     color_discrete_sequence=COLORS,
                     opacity=0.7,
                     labels={'experience_years': 'Experience (years)',
                              'revenue': 'Revenue (€)', 'product': 'Product'},
                     title='Revenue vs Experience — size=units, symbol=region')
    apply_theme(fig, height=520)
    show_or_save(fig, '03a_scatter')

    # 3b: scatter with trendline (OLS regression)
    fig2 = px.scatter(df_sales, x='experience_years', y='revenue',
                      color='product',
                      color_discrete_sequence=COLORS,
                      trendline='ols',          # OLS regression line per color
                      trendline_scope='overall', # one overall line
                      opacity=0.5,
                      title='Scatter with OLS Trendline')
    apply_theme(fig2, height=480)
    show_or_save(fig2, '03b_scatter_trendline')

    # 3c: animated scatter (animation_frame)
    fig3 = px.scatter(df_sales, x='experience_years', y='revenue',
                      animation_frame='quarter',
                      animation_group='product',
                      color='product', size='units', size_max=20,
                      color_discrete_sequence=COLORS,
                      opacity=0.7,
                      range_x=[0, 16], range_y=[100, 2000],
                      title='Animated Scatter — play through quarters')
    apply_theme(fig3, height=520)
    show_or_save(fig3, '03c_scatter_animated')

    print("""
  px.scatter(data, x, y, color, size, symbol, facet_col, facet_row,
             trendline, animation_frame, hover_data, opacity, title)

    color       → color by column
    size        → bubble size by column  (size_max=n caps the max size)
    symbol      → marker shape by column
    trendline   → 'ols' (linear)  'lowess' (smooth)
    trendline_scope → 'trace' (per color)  'overall' (one line)
    animation_frame → column to animate over (adds Play button)
    hover_data  → extra columns shown on hover tooltip

  CUSTOM HOVER:
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>Revenue: €%{y:.0f}<extra></extra>'
    )
    """)


    # ------------------------------------------------------------------
    # 4. BAR CHART
    # ------------------------------------------------------------------
    print("4. BAR CHART")
    print("-" * 70)

    # 4a: grouped bar
    prod_region = (df_sales.groupby(['product', 'region'])['revenue']
                   .mean().reset_index())
    prod_region.columns = ['product', 'region', 'mean_revenue']

    fig = px.bar(prod_region, x='product', y='mean_revenue',
                 color='region', barmode='group',
                 color_discrete_sequence=COLORS,
                 text_auto='.0f',
                 labels={'mean_revenue': 'Mean Revenue (€)', 'product': 'Product'},
                 title='Mean Revenue — Grouped by Region')
    fig.update_traces(textposition='outside', textfont_size=10)
    apply_theme(fig, height=480)
    show_or_save(fig, '04a_bar_grouped')

    # 4b: stacked bar
    fig2 = px.bar(prod_region, x='region', y='mean_revenue',
                  color='product', barmode='stack',
                  color_discrete_sequence=COLORS,
                  text_auto='.0f',
                  labels={'mean_revenue': 'Mean Revenue (€)', 'region': 'Region'},
                  title='Mean Revenue — Stacked by Product')
    apply_theme(fig2, height=480)
    show_or_save(fig2, '04b_bar_stacked')

    # 4c: horizontal bar — sorted
    model_perf = df_ml.groupby('model')['accuracy'].mean().reset_index()
    model_perf = model_perf.sort_values('accuracy')

    fig3 = px.bar(model_perf, y='model', x='accuracy',
                  orientation='h',
                  color='accuracy',
                  color_continuous_scale='Blues',
                  text_auto='.3f',
                  title='Model Accuracy — Horizontal Bar (sorted)')
    fig3.update_traces(textposition='outside')
    fig3.update_layout(coloraxis_showscale=False)
    apply_theme(fig3, height=420)
    show_or_save(fig3, '04c_bar_horizontal')

    print("""
  px.bar(data, x, y, color, barmode, orientation, text_auto,
         facet_col, facet_row, animation_frame, title)

    barmode     → 'group' (side by side)  'stack'  'relative'  'overlay'
    orientation → 'v' (vertical, default)  'h' (horizontal)
    text_auto   → True / '.2f' / '.0f' → show values on bars
    color_continuous_scale → for numeric color columns

  SORTING BARS:
    df_sorted = df.sort_values('col')         → sort DataFrame first
    px.bar(..., category_orders={'x': order}) → explicit order list

  FACETED BARS:
    px.bar(..., facet_col='category', facet_row='region')
    """)


    # ------------------------------------------------------------------
    # 5. HISTOGRAM
    # ------------------------------------------------------------------
    print("5. HISTOGRAM")
    print("-" * 70)

    # 5a: basic histogram with marginal
    fig = px.histogram(df_sales, x='revenue',
                       color='product',
                       color_discrete_sequence=COLORS,
                       nbins=40, opacity=0.75,
                       barmode='overlay',
                       marginal='box',        # box / violin / rug
                       title='Revenue Distribution — marginal=box')
    apply_theme(fig, height=520)
    show_or_save(fig, '05a_histogram')

    # 5b: histogram with KDE + rug
    fig2 = px.histogram(df_sales, x='satisfaction',
                        color='region',
                        color_discrete_sequence=COLORS,
                        nbins=20, opacity=0.65,
                        barmode='overlay',
                        marginal='violin',
                        histnorm='probability density',
                        title='Satisfaction Distribution — histnorm=density, marginal=violin')
    apply_theme(fig2, height=520)
    show_or_save(fig2, '05b_histogram_density')

    print("""
  px.histogram(data, x, y, color, nbins, barmode, histnorm,
               marginal, opacity, cumulative, title)

    nbins       → number of bins
    barmode     → 'overlay' (transparent overlap)  'stack'  'group'
    histnorm    → None (counts)  'percent'  'probability'
                  'probability density'  'density'
    marginal    → 'box'  'violin'  'rug'  → adds marginal plot on top ★
    cumulative  → True: cumulative histogram
    opacity     → transparency (use < 1 for overlapping histograms)

  💡 marginal='box' or marginal='violin' is unique to Plotly and gives
     distribution + statistics in one chart with no extra code.
    """)


    # ------------------------------------------------------------------
    # 6. BOX AND VIOLIN PLOTS
    # ------------------------------------------------------------------
    print("6. BOX AND VIOLIN PLOTS")
    print("-" * 70)

    # 6a: box with points
    fig = px.box(df_sales, x='product', y='revenue',
                 color='product',
                 color_discrete_sequence=COLORS,
                 points='outliers',      # 'all' / 'outliers' / 'suspectedoutliers' / False
                 notched=True,           # notch shows CI on median
                 labels={'revenue': 'Revenue (€)', 'product': 'Product'},
                 title='Revenue Distribution — Box Plot (notched)')
    apply_theme(fig, height=480)
    show_or_save(fig, '06a_box')

    # 6b: violin
    fig2 = px.violin(df_sales, x='product', y='revenue',
                     color='product',
                     color_discrete_sequence=COLORS,
                     box=True,           # embed box inside violin
                     points='all',       # show all individual points
                     hover_data=['region', 'quarter'],
                     title='Revenue Distribution — Violin + Box + Points')
    apply_theme(fig2, height=500)
    show_or_save(fig2, '06b_violin')

    # 6c: box grouped by two variables
    fig3 = px.box(df_sales, x='region', y='revenue',
                  color='product',
                  color_discrete_sequence=COLORS,
                  points=False,
                  labels={'revenue': 'Revenue (€)', 'region': 'Region'},
                  title='Revenue by Region and Product')
    apply_theme(fig3, height=500)
    show_or_save(fig3, '06c_box_grouped')

    print("""
  px.box(data, x, y, color, points, notched, facet_col, title)
    points  → 'outliers' (default)  'all'  'suspectedoutliers'  False
    notched → True: shows confidence interval on median
    boxmode → 'group' (default)  'overlay'

  px.violin(data, x, y, color, box, points, violinmode, title)
    box=True    → embed mini box plot inside violin ★
    points='all'→ show all data points
    violinmode  → 'group'  'overlay'
    """)


    # ------------------------------------------------------------------
    # 7. PIE, DONUT AND SUNBURST
    # ------------------------------------------------------------------
    print("7. PIE, DONUT AND SUNBURST")
    print("-" * 70)

    prod_rev = df_sales.groupby('product')['revenue'].sum().reset_index()

    # 7a: pie chart
    fig = px.pie(prod_rev, values='revenue', names='product',
                 color_discrete_sequence=COLORS,
                 hole=0,
                 title='Revenue Share by Product')
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      pull=[0.05, 0, 0, 0])   # pull first slice out
    apply_theme(fig, height=460)
    show_or_save(fig, '07a_pie')

    # 7b: donut chart
    fig2 = px.pie(prod_rev, values='revenue', names='product',
                  color_discrete_sequence=COLORS,
                  hole=0.45,           # hole > 0 → donut ★
                  title='Revenue Share — Donut Chart')
    fig2.update_traces(textposition='outside', textinfo='percent+label')
    apply_theme(fig2, height=460)
    show_or_save(fig2, '07b_donut')

    # 7c: sunburst (hierarchical)
    fig3 = px.sunburst(df_sales, path=['region', 'product', 'quarter'],
                       values='revenue',
                       color='product',
                       color_discrete_sequence=COLORS,
                       title='Revenue Sunburst — Region → Product → Quarter')
    apply_theme(fig3, height=560)
    show_or_save(fig3, '07c_sunburst')

    # 7d: treemap (alternative to sunburst)
    fig4 = px.treemap(df_sales, path=[px.Constant('All'), 'region', 'product'],
                      values='revenue',
                      color='satisfaction',
                      color_continuous_scale='RdYlGn',
                      color_continuous_midpoint=3.8,
                      title='Revenue Treemap — colored by Satisfaction')
    apply_theme(fig4, height=520)
    show_or_save(fig4, '07d_treemap')

    print("""
  px.pie(data, values, names, hole, color, title)
    hole    → 0 (pie)  to  0.9 (thin donut) — 0.4–0.5 is a classic donut

  px.sunburst(data, path, values, color, title)
    path    → list of columns defining hierarchy (outer to inner)
    → Click slices to zoom in!

  px.treemap(data, path, values, color, title)
    path    → same as sunburst — [px.Constant('root'), 'col1', 'col2']
    → Best when size differences matter more than hierarchy

  💡 Both sunburst and treemap are interactive — click to drill down.
    """)


    # ------------------------------------------------------------------
    # 8. HEATMAP AND CORRELATION
    # ------------------------------------------------------------------
    print("8. HEATMAP AND CORRELATION")
    print("-" * 70)

    # 8a: correlation heatmap
    numeric_cols = ['revenue', 'units', 'satisfaction',
                    'experience_years', 'margin']
    corr = df_sales[numeric_cols].corr().round(3)

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale='RdBu', zmid=0, zmin=-1, zmax=1,
        text=corr.values.round(2),
        texttemplate='%{text}',
        textfont=dict(size=13),
        hoverongaps=False,
        showscale=True,
        colorbar=dict(title='Correlation')
    ))
    fig.update_layout(title='Correlation Matrix', height=460,
                      font=dict(size=12))
    apply_theme(fig)
    show_or_save(fig, '08a_correlation_heatmap')

    # 8b: pivot heatmap using px.imshow
    pivot = df_sales.pivot_table(values='revenue', index='region',
                                  columns='product', aggfunc='mean').round(0)
    fig2 = px.imshow(pivot,
                     color_continuous_scale='YlOrRd',
                     text_auto='.0f',
                     aspect='auto',
                     title='Mean Revenue Heatmap — Region × Product')
    fig2.update_traces(textfont_size=13)
    apply_theme(fig2, height=380)
    show_or_save(fig2, '08b_pivot_heatmap')

    print("""
  CORRELATION HEATMAP (via go.Heatmap):
    go.Heatmap(z=matrix, x=cols, y=rows,
               colorscale='RdBu', zmid=0,
               text=matrix, texttemplate='%{text}')

  PIVOT HEATMAP (via px.imshow):
    pivot = df.pivot_table(values='v', index='r', columns='c', aggfunc='mean')
    px.imshow(pivot, text_auto='.1f', color_continuous_scale='Blues')

  COMMON COLORSCALES:
    Diverging   : 'RdBu'  'RdYlGn'  'Picnic'  'Portland'
    Sequential  : 'Blues'  'Reds'  'YlOrRd'  'Viridis'  'Plasma'
    Custom      : [[0,'blue'], [0.5,'white'], [1,'red']]
    """)


    # ------------------------------------------------------------------
    # 9. 3D PLOTS
    # ------------------------------------------------------------------
    print("9. 3D PLOTS")
    print("-" * 70)

    # 9a: 3D scatter
    fig = px.scatter_3d(df_sales, x='experience_years', y='revenue',
                        z='satisfaction',
                        color='product', size='units',
                        size_max=12,
                        color_discrete_sequence=COLORS,
                        opacity=0.7,
                        hover_data=['region', 'quarter'],
                        labels={'experience_years': 'Experience',
                                'revenue': 'Revenue', 'satisfaction': 'Satisfaction'},
                        title='3D Scatter — Experience × Revenue × Satisfaction')
    fig.update_layout(height=580, scene=dict(
        xaxis_title='Experience (years)',
        yaxis_title='Revenue (€)',
        zaxis_title='Satisfaction',
    ))
    show_or_save(fig, '09a_scatter_3d')

    # 9b: 3D surface
    rng = np.random.default_rng(1)
    x   = np.linspace(-3, 3, 50)
    y   = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z    = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.2 * (X**2 + Y**2))

    fig2 = go.Figure(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=True,
        contours=dict(z=dict(show=True, usecolormap=True,
                              highlightcolor='white', project_z=True))
    ))
    fig2.update_layout(title='3D Surface — sin(r)·e^(-0.2r²)',
                       height=560,
                       scene=dict(xaxis_title='X', yaxis_title='Y',
                                  zaxis_title='Z'))
    show_or_save(fig2, '09b_surface_3d')

    # 9c: 3D line (trajectory)
    t   = np.linspace(0, 4 * np.pi, 300)
    df_helix = pd.DataFrame({
        'x': np.cos(t), 'y': np.sin(t), 'z': t / (2 * np.pi),
        't': t
    })
    fig3 = px.line_3d(df_helix, x='x', y='y', z='z',
                      color_discrete_sequence=['#2E75B6'],
                      title='3D Line — Helix Trajectory')
    fig3.update_traces(line=dict(width=5))
    fig3.update_layout(height=520)
    show_or_save(fig3, '09c_line_3d')

    print("""
  px.scatter_3d(data, x, y, z, color, size, symbol, opacity, title)
    → Interactive 3D scatter — rotate/zoom with mouse

  px.line_3d(data, x, y, z, color, title)
    → 3D line / trajectory

  go.Surface(x, y, z, colorscale, contours)
    → 3D surface from a 2D grid

  SCENE CONFIGURATION:
    fig.update_layout(scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))  ← camera angle
    ))

  💡 All 3D charts are interactive — drag to rotate, scroll to zoom,
     double-click to reset the view.
    """)


    # ------------------------------------------------------------------
    # 10. MAPS
    # ------------------------------------------------------------------
    print("10. MAPS")
    print("-" * 70)

    # 10a: choropleth — world map
    country_data = px.data.gapminder().query("year == 2007")
    fig = px.choropleth(country_data,
                        locations='iso_alpha',
                        color='gdpPercap',
                        hover_name='country',
                        hover_data=['lifeExp', 'pop'],
                        color_continuous_scale='Plasma',
                        projection='natural earth',
                        title='GDP per Capita — World Map (2007)')
    fig.update_layout(height=480)
    show_or_save(fig, '10a_choropleth_world')

    # 10b: scatter map (bubble map)
    fig2 = px.scatter_geo(country_data,
                          locations='iso_alpha',
                          size='pop',
                          color='continent',
                          hover_name='country',
                          hover_data=['gdpPercap', 'lifeExp'],
                          size_max=50,
                          color_discrete_sequence=COLORS,
                          projection='natural earth',
                          title='Population Bubble Map by Continent (2007)')
    fig2.update_layout(height=480)
    show_or_save(fig2, '10b_scatter_geo')

    # 10c: density map (uses mapbox — no token needed for open tiles)
    fig3 = px.density_mapbox(
        df_sales.assign(
            lat=np.random.default_rng(42).uniform(36, 42, len(df_sales)),
            lon=np.random.default_rng(43).uniform(-9, -6, len(df_sales))
        ),
        lat='lat', lon='lon', z='revenue',
        radius=15,
        center=dict(lat=39, lon=-7.5),
        zoom=5,
        mapbox_style='open-street-map',
        color_continuous_scale='YlOrRd',
        title='Revenue Density Map — Portugal (simulated data)'
    )
    fig3.update_layout(height=500)
    show_or_save(fig3, '10c_density_map')

    print("""
  px.choropleth(data, locations, color, hover_name,
                color_continuous_scale, projection)
    locations → ISO alpha-3 codes (e.g. 'PRT', 'USA') or country names
    projection → 'natural earth'  'mercator'  'orthographic'  'mollweide'

  px.scatter_geo(data, locations, size, color, hover_name, projection)
    → Bubble map — size encodes a numeric variable

  px.scatter_mapbox / px.density_mapbox (needs mapbox tiles):
    mapbox_style → 'open-street-map' (free, no token)
                   'carto-positron'  'carto-darkmatter'
                   'stamen-terrain'  'white-bg'

  px.choropleth_mapbox (detailed regional maps — needs GeoJSON):
    px.choropleth_mapbox(df, geojson=geojson, locations='id',
                         color='value', mapbox_style='carto-positron')

  💡 For Portugal / European maps, use choropleth_mapbox with a
     GeoJSON file of regions (nuts2/nuts3 level).
    """)


    # ------------------------------------------------------------------
    # 11. MULTI-PANEL LAYOUTS (make_subplots)
    # ------------------------------------------------------------------
    print("11. MULTI-PANEL LAYOUTS (make_subplots)")
    print("-" * 70)

    # 11a: 2×2 grid mixing chart types
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Product', 'Monthly Trend',
                        'Revenue Distribution', 'Satisfaction vs Revenue'),
        vertical_spacing=0.12, horizontal_spacing=0.08
    )

    # Top-left: bar chart
    prod_rev = df_sales.groupby('product')['revenue'].mean().reset_index()
    for i, (_, row) in enumerate(prod_rev.iterrows()):
        fig.add_trace(go.Bar(name=row['product'], x=[row['product']],
                             y=[row['revenue']],
                             marker_color=COLORS[i],
                             showlegend=True),
                      row=1, col=1)

    # Top-right: line chart
    for i, prod in enumerate(['Laptop', 'Phone', 'Tablet', 'Watch']):
        d = df_monthly[df_monthly['product'] == prod]
        fig.add_trace(go.Scatter(name=prod, x=d['month'], y=d['revenue'],
                                 mode='lines+markers',
                                 line=dict(color=COLORS[i], width=2),
                                 showlegend=False),
                      row=1, col=2)

    # Bottom-left: histogram
    fig.add_trace(go.Histogram(x=df_sales['revenue'], nbinsx=30,
                               marker=dict(color='#2E75B6'), opacity=0.75,
                               showlegend=False, name='Revenue Distribution'),
                  row=2, col=1)

    # Bottom-right: scatter
    for i, prod in enumerate(['Laptop', 'Phone', 'Tablet', 'Watch']):
        d = df_sales[df_sales['product'] == prod]
        fig.add_trace(go.Scatter(x=d['revenue'], y=d['satisfaction'],
                                 hovertemplate='Revenue: %{x}<br>Count: %{y}<extra></extra>',
                                 mode='markers',
                                 marker=dict(color=COLORS[i], size=5, opacity=0.5),
                                 name=prod, showlegend=False),
                      row=2, col=2)

    fig.update_layout(title_text='Multi-Panel Dashboard',
                      title_x=0.5, height=680,
                      font=dict(family='Arial', size=12),
                      paper_bgcolor='white', plot_bgcolor='#F8F9FA',
                      barmode='group')
    fig.update_xaxes(showgrid=True, gridcolor='#E0E0E0')
    fig.update_yaxes(showgrid=True, gridcolor='#E0E0E0')
    show_or_save(fig, '11_subplots', height=700)

    print("""
  from plotly.subplots import make_subplots

  fig = make_subplots(rows, cols,
                      subplot_titles=[...],
                      specs=[[{'type':'xy'}, {'type':'pie'}], ...],
                      shared_xaxes=False, shared_yaxes=False,
                      vertical_spacing=0.1, horizontal_spacing=0.08)

  fig.add_trace(go.Bar(...),      row=1, col=1)
  fig.add_trace(go.Scatter(...),  row=1, col=2)
  fig.add_trace(go.Histogram(...),row=2, col=1)

  MIXED CHART TYPES (use specs):
    specs=[[{'type':'xy'},  {'type':'pie'}],
           [{'type':'xy'},  {'type':'scene'}]]  ← 'scene' for 3D

  UPDATE SPECIFIC SUBPLOTS:
    fig.update_xaxes(title='Month', row=1, col=2)
    fig.update_yaxes(title='Revenue', row=1, col=1)
    """)


    # ------------------------------------------------------------------
    # 12. ML PLOTS
    # ------------------------------------------------------------------
    print("12. ML PLOTS")
    print("-" * 70)

    # 12a: Feature importance
    rng         = np.random.default_rng(11)
    features    = ['Credit Score','Income','Debt Ratio','Age',
                   'Employment Years','Loan Amount','Num Accounts',
                   'Late Payments','Interest Rate','Collateral']
    importances = np.sort(rng.uniform(0.01, 0.25, len(features)))[::-1]
    importances /= importances.sum()
    df_feat = pd.DataFrame({'feature': features, 'importance': importances,
                             'std': rng.uniform(0.005, 0.03, len(features))})
    df_feat = df_feat.sort_values('importance')

    fig = px.bar(df_feat, y='feature', x='importance',
                 orientation='h',
                 color='importance',
                 color_continuous_scale='Blues',
                 error_x='std',
                 text_auto='.3f',
                 title='Feature Importance — Loan Default Model')
    fig.update_traces(textposition='outside', textfont_size=10)
    fig.update_layout(coloraxis_showscale=False, yaxis_title='',
                      xaxis_title='Importance (normalized)')
    apply_theme(fig, height=480)
    show_or_save(fig, '12a_feature_importance')

    # 12b: Confusion matrix (interactive)
    cm = np.array([[85,  8,  7],
                   [ 5, 90,  5],
                   [ 3,  4, 93]])
    classes  = ['Cat', 'Dog', 'Bird']
    cm_norm  = cm / cm.sum(axis=1, keepdims=True)
    cm_text  = [[f'{cm[i,j]}<br>({cm_norm[i,j]:.1%})'
                 for j in range(3)] for i in range(3)]

    fig2 = go.Figure(go.Heatmap(
        z=cm_norm, x=classes, y=classes,
        colorscale='Blues', zmin=0, zmax=1,
        text=cm_text, texttemplate='%{text}',
        textfont=dict(size=14),
        showscale=True,
        colorbar=dict(title='Recall'),
        hovertemplate='True: %{y}<br>Predicted: %{x}<br>Count: %{text}<extra></extra>'
    ))
    fig2.update_layout(
        title='Confusion Matrix — Interactive',
        xaxis_title='Predicted Label', yaxis_title='True Label',
        height=420, font=dict(size=13),
        yaxis=dict(autorange='reversed')   # ← row 0 (Cat) on top
    )
    show_or_save(fig2, '12b_confusion_matrix')

    # 12c: ROC curves
    def sim_roc(auc_target, n=200, seed=0):
        rng = np.random.default_rng(seed)
        t   = np.linspace(0, 1, n)
        tpr = np.clip(t ** (1/(max(auc_target/(1-auc_target+1e-9), 0.01))), 0, 1)
        tpr = np.maximum.accumulate(np.clip(
              np.sort(tpr)[::-1] + rng.normal(0, 0.01, n), 0, 1)[::-1])[::-1]
        return t, np.clip(tpr, 0, 1)

    models_roc = [('Random Forest', 0.940, 0),
                  ('XGBoost',        0.952, 1),
                  ('SVM',            0.910, 2),
                  ('Logistic Reg.',  0.875, 3)]

    fig3 = go.Figure()
    for name, auc, seed in models_roc:
        fpr, tpr = sim_roc(auc, seed=seed)
        fig3.add_trace(go.Scatter(
            x=fpr, y=tpr, mode='lines',
            name=f'{name} (AUC={auc:.3f})',
            line=dict(width=2.5, color=COLORS[seed])
        ))
    fig3.add_trace(go.Scatter(
        x=[0,1], y=[0,1], mode='lines',
        name='Random (AUC=0.500)',
        line=dict(width=1.5, color='gray', dash='dash')
    ))
    fig3.update_layout(
        title='ROC Curves — Binary Classification',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate (Recall)',
        height=500, hovermode='x unified',
    )
    apply_theme(fig3)
    show_or_save(fig3, '12c_roc_curves')

    # 12d: Learning curves
    rng   = np.random.default_rng(3)
    sizes = np.array([50, 100, 200, 400, 800, 1600, 3000])
    train_mean = 1.0 - 0.05 * np.log1p(sizes/50)
    val_mean   = 0.60 + 0.28 * (1 - np.exp(-sizes/600))
    train_std  = rng.uniform(0.005, 0.015, len(sizes))
    val_std    = rng.uniform(0.008, 0.018, len(sizes))

    fig4 = go.Figure()
    # Training band
    fig4.add_trace(go.Scatter(
        x=np.concatenate([sizes, sizes[::-1]]),
        y=np.concatenate([train_mean + train_std, (train_mean - train_std)[::-1]]),
        fill='toself', fillcolor='rgba(46,117,182,0.15)',
        line=dict(color='rgba(255,255,255,0)'), showlegend=False, hoverinfo='skip'
    ))
    fig4.add_trace(go.Scatter(x=sizes, y=train_mean, mode='lines+markers',
                              name='Training score',
                              line=dict(color='#2E75B6', width=2.5),
                              marker=dict(size=8)))
    # Validation band
    fig4.add_trace(go.Scatter(
        x=np.concatenate([sizes, sizes[::-1]]),
        y=np.concatenate([val_mean + val_std, (val_mean - val_std)[::-1]]),
        fill='toself', fillcolor='rgba(197,90,17,0.15)',
        line=dict(color='rgba(255,255,255,0)'), showlegend=False, hoverinfo='skip'
    ))
    fig4.add_trace(go.Scatter(x=sizes, y=val_mean, mode='lines+markers',
                              name='Validation score',
                              line=dict(color='#C55A11', width=2.5),
                              marker=dict(size=8)))
    fig4.update_layout(title='Learning Curves — Random Forest',
                       xaxis_title='Training set size',
                       yaxis_title='Accuracy', height=460,
                       hovermode='x unified', yaxis=dict(range=[0.5, 1.05]))
    apply_theme(fig4)
    show_or_save(fig4, '12d_learning_curves')

    # 12e: Parallel coordinates (multi-metric model comparison)
    fig5 = px.parallel_coordinates(
        df_ml,
        color='accuracy',
        dimensions=['accuracy', 'f1_score', 'precision', 'recall'],
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=df_ml['accuracy'].mean(),
        title='Parallel Coordinates — Model Metrics Across CV Folds'
    )
    fig5.update_layout(height=460)
    show_or_save(fig5, '12e_parallel_coordinates')

    print("""
  FEATURE IMPORTANCE:
    px.bar(df, y='feature', x='importance', orientation='h',
           color='importance', color_continuous_scale='Blues',
           error_x='std', text_auto='.3f')

  CONFUSION MATRIX:
    go.Heatmap(z=cm_norm, x=classes, y=classes,
               text=labels, texttemplate='%{text}',
               colorscale='Blues', zmin=0, zmax=1)
    fig.update_layout(yaxis=dict(autorange='reversed'))  ← row 0 on top!

  ROC CURVES:
    go.Scatter(x=fpr, y=tpr, mode='lines', name='Model (AUC=...)')

  LEARNING CURVES (with shaded bands):
    go.Scatter(x=concat([sizes, sizes[::-1]]),
               y=concat([mean+std, (mean-std)[::-1]]),
               fill='toself', ...)   ← fills between upper and lower bound

  PARALLEL COORDINATES (compare all metrics at once):
    px.parallel_coordinates(df, color='accuracy',
                             dimensions=['acc','f1','precision','recall'],
                             color_continuous_scale='RdYlGn')
    → Drag axes to reorder, brush to filter — very powerful for model comparison!
    """)


    # ------------------------------------------------------------------
    # 13. DASH — INTERACTIVE DASHBOARDS
    # ------------------------------------------------------------------
    print("13. DASH — INTERACTIVE DASHBOARDS")
    print("-" * 70)
    print("""
  Dash is Plotly's framework for building interactive web dashboards
  entirely in Python — no JavaScript required.

  INSTALLATION:
    pip install dash

  MINIMAL DASH APP:
  ─────────────────────────────────────────────────────────────────────
  from dash import Dash, dcc, html, Input, Output
  import plotly.express as px
  import pandas as pd

  app = Dash(__name__)
  df  = px.data.gapminder()

  app.layout = html.Div([
      html.H1('My Dashboard'),

      html.Label('Select Continent:'),
      dcc.Dropdown(
          id='continent-filter',
          options=[{'label': c, 'value': c}
                   for c in df['continent'].unique()],
          value='Europe',
          clearable=False
      ),

      dcc.Graph(id='gdp-chart'),
  ])

  @app.callback(
      Output('gdp-chart', 'figure'),
      Input('continent-filter', 'value')
  )
  def update_chart(continent):
      filtered = df[df['continent'] == continent]
      fig = px.scatter(filtered, x='gdpPercap', y='lifeExp',
                       size='pop', color='country',
                       hover_name='country',
                       animation_frame='year',
                       log_x=True, title=f'GDP vs Life Expectancy — {continent}')
      return fig

  if __name__ == '__main__':
      app.run(debug=True)
  ─────────────────────────────────────────────────────────────────────

  KEY CONCEPTS:
    app.layout       → defines the HTML structure (components)
    @app.callback    → connects inputs (user interactions) to outputs (charts)
    Input(id, prop)  → what triggers the callback
    Output(id, prop) → what gets updated

  COMMON COMPONENTS:
    dcc.Graph(id)                → Plotly chart (the output)
    dcc.Dropdown(options, value) → dropdown selector
    dcc.Slider(min, max, step)   → slider
    dcc.RangeSlider(min, max)    → range slider
    dcc.Checklist(options)       → checkboxes
    dcc.RadioItems(options)      → radio buttons
    dcc.DatePickerRange()        → date range picker
    html.Div / html.H1 / html.P  → HTML layout elements

  RUNNING:
    python app.py
    → Opens at http://127.0.0.1:8050

  DEPLOYMENT:
    Render.com, Railway, Heroku, AWS, Azure — all support Dash.

  💡 Dash = Plotly charts + React.js frontend + Flask backend,
     all written in pure Python.
    """)


    # ------------------------------------------------------------------
    # 14. EXPORT AND SHARING
    # ------------------------------------------------------------------
    print("14. EXPORT AND SHARING")
    print("-" * 70)
    print("""
  INTERACTIVE HTML (no dependencies, opens in any browser):
    fig.write_html('chart.html')
    fig.write_html('chart.html', include_plotlyjs='cdn')  ← smaller file
    fig.write_html('chart.html', full_html=False)         ← HTML snippet only

  STATIC IMAGES (requires kaleido: pip install kaleido):
    fig.write_image('chart.png',  width=1200, height=600, scale=2)
    fig.write_image('chart.pdf')   ← vector, best for reports/LaTeX
    fig.write_image('chart.svg')   ← vector, editable in Inkscape
    fig.write_image('chart.eps')   ← for academic journals

  JSON (save/restore figure state):
    fig.write_json('chart.json')
    fig = pio.read_json('chart.json')

  EMBED IN NOTEBOOK:
    import plotly.io as pio
    pio.renderers.default = 'notebook'    ← classic Jupyter
    pio.renderers.default = 'iframe'      ← JupyterLab
    pio.renderers.default = 'browser'     ← open in browser tab

  SHARE AS IMAGE (quick):
    import plotly.io as pio
    pio.show(fig, renderer='png')         ← display as static PNG in notebook
    """)


    # ------------------------------------------------------------------
    # 15. COMMON MISTAKES
    # ------------------------------------------------------------------
    print("15. COMMON MISTAKES")
    print("-" * 70)
    print("""
  Mistake 1 — fig.show() in a script with no browser:
    In a headless script, fig.show() may open a browser or fail.
    Always use fig.write_html() in scripts — interactive and shareable.

  Mistake 2 — No kaleido for PNG export:
    fig.write_image('chart.png')  → ValueError: kaleido not found
    Fix: pip install kaleido

  Mistake 3 — Mixing px and go incorrectly:
    fig = px.scatter(df, x='a', y='b')
    fig.add_trace(go.Bar(...))    ← OK! px returns a go.Figure
    The key insight: px creates go.Figure objects — you can always
    add go traces to a px figure.

  Mistake 4 — Forgetting yaxis autorange='reversed' in heatmaps:
    Confusion matrices should have row 0 at the top.
    fig.update_layout(yaxis=dict(autorange='reversed'))

  Mistake 5 — animation_frame with unequal category sizes:
    Plotly animations require range_x and range_y to be fixed,
    otherwise the axes rescale each frame (misleading!).
    Always set: range_x=[xmin, xmax], range_y=[ymin, ymax]

  Mistake 6 — Large datasets with px.scatter:
    Plotly renders everything in the browser — too many points = slow.
    With n > 50,000: sample first or use px.density_heatmap instead.
    """)


    # ------------------------------------------------------------------
    # 16. QUICK REFERENCE
    # ------------------------------------------------------------------
    print("16. QUICK REFERENCE")
    print("-" * 70)
    print()
    print(f"  {'Function':<45} {'Description'}")
    print(f"  {'-'*45} {'-'*35}")

    ref = [
        ("SETUP", ""),
        ("import plotly.express as px",               "High-level interface"),
        ("import plotly.graph_objects as go",         "Low-level / customization"),
        ("from plotly.subplots import make_subplots", "Multi-panel layouts"),
        ("BASIC CHARTS (px)", ""),
        ("px.line(data, x, y, color, markers)",        "Line chart"),
        ("px.scatter(data, x, y, color, size, symbol)","Scatter / bubble"),
        ("px.bar(data, x, y, color, barmode, text_auto)","Bar chart"),
        ("px.histogram(data, x, color, nbins, marginal)","Histogram"),
        ("px.box(data, x, y, color, points, notched)", "Box plot"),
        ("px.violin(data, x, y, color, box, points)",  "Violin plot"),
        ("PART-OF-WHOLE (px)", ""),
        ("px.pie(data, values, names, hole)",           "Pie / Donut chart"),
        ("px.sunburst(data, path, values, color)",      "Hierarchical sunburst"),
        ("px.treemap(data, path, values, color)",       "Hierarchical treemap"),
        ("HEATMAP", ""),
        ("px.imshow(matrix, text_auto, color_continuous_scale)", "Pivot heatmap"),
        ("go.Heatmap(z, x, y, colorscale, text, texttemplate)", "Custom heatmap"),
        ("3D (px / go)", ""),
        ("px.scatter_3d(data, x, y, z, color, size)",  "3D scatter"),
        ("px.line_3d(data, x, y, z)",                  "3D line"),
        ("go.Surface(x, y, z, colorscale)",             "3D surface"),
        ("MAPS (px)", ""),
        ("px.choropleth(data, locations, color)",       "World choropleth map"),
        ("px.scatter_geo(data, locations, size, color)","Bubble geo map"),
        ("px.density_mapbox(data, lat, lon, z)",        "Density map (mapbox)"),
        ("MULTI-PANEL (go)", ""),
        ("make_subplots(rows, cols, subplot_titles)",   "Create subplot grid"),
        ("fig.add_trace(go.Bar(...), row=r, col=c)",    "Add trace to subplot"),
        ("ML CHARTS", ""),
        ("px.parallel_coordinates(data, color, dimensions)", "Parallel coords"),
        ("go.Scatter(x=fpr, y=tpr)",                   "ROC curve trace"),
        ("go.Heatmap for confusion matrix",             "Confusion matrix"),
        ("FIGURE METHODS", ""),
        ("fig.update_layout(title, height, font, ...)", "Update layout"),
        ("fig.update_traces(marker_size, opacity, ...)", "Update all traces"),
        ("fig.update_xaxes / update_yaxes(...)",        "Update axes"),
        ("fig.add_hline / add_vline(y/x, ...)",         "Add reference line"),
        ("fig.add_annotation(x, y, text, ...)",         "Add annotation"),
        ("EXPORT", ""),
        ("fig.show()",                                  "Display (browser/Jupyter)"),
        ("fig.write_html('f.html')",                    "Save interactive HTML ★"),
        ("fig.write_image('f.png', width, height)",     "Save PNG (needs kaleido)"),
        ("fig.write_image('f.pdf')",                    "Save PDF (needs kaleido)"),
    ]

    for item, desc in ref:
        if desc == "":
            print(f"\n  ── {item} {'─'*(65-len(item))}")
        else:
            print(f"  {item:<45} {desc}")

    print()
    print(f"\nDone! Check '{OUTDIR}/' for all saved HTML/PNG files.\n" if not JUPYTER
          else "\nDone! All charts rendered inline.\n")


main()


"""
SUMMARY — PLOTLY EXPRESS
=======================================================

SETUP:
  import plotly.express as px
  import plotly.graph_objects as go
  from plotly.subplots import make_subplots

GOLDEN RULES:
  1. px creates go.Figure → you can always add go traces to px figures
  2. Always use fig.write_html() in scripts — interactive + shareable
  3. Install kaleido for PNG/PDF: pip install kaleido
  4. Large datasets (n>50k): sample first or use density charts

CHART TYPES:
  Line        → px.line(x, y, color, markers, hovermode='x unified')
  Scatter     → px.scatter(x, y, color, size, symbol, trendline)
  Bar         → px.bar(x, y, color, barmode, text_auto, orientation)
  Histogram   → px.histogram(x, color, nbins, marginal, histnorm)
  Box         → px.box(x, y, color, points, notched)
  Violin      → px.violin(x, y, color, box=True, points)
  Pie/Donut   → px.pie(values, names, hole=0.45)
  Sunburst    → px.sunburst(path=[...], values, color)
  Treemap     → px.treemap(path=[px.Constant('All'), 'col1'], values)
  Heatmap     → px.imshow(pivot, text_auto, color_continuous_scale)

3D:
  px.scatter_3d(x, y, z, color, size)
  px.line_3d(x, y, z)
  go.Surface(x, y, z, colorscale)

MAPS:
  px.choropleth(locations, color, projection)
  px.scatter_geo(locations, size, color)
  px.density_mapbox(lat, lon, z, mapbox_style='open-street-map')

ML CHARTS:
  Feature importance → px.bar horizontal + color_continuous_scale
  Confusion matrix   → go.Heatmap + yaxis autorange='reversed'
  ROC curves         → go.Scatter(x=fpr, y=tpr)
  Learning curves    → go.Scatter fill='toself' for bands
  Parallel coords    → px.parallel_coordinates(color, dimensions)

SUBPLOTS:
  fig = make_subplots(rows, cols, subplot_titles)
  fig.add_trace(go.Bar(...), row=1, col=1)
  fig.update_layout(...)

UPDATE PATTERN:
  fig.update_layout(title, height, font, hovermode)
  fig.update_traces(marker_size, opacity, line_width)
  fig.update_xaxes / update_yaxes(title, range, showgrid)
  fig.add_hline / add_vline(y/x, line_dash, annotation_text)

EXPORT:
  fig.write_html('f.html')              ← interactive, no dependencies ★
  fig.write_image('f.png', scale=2)    ← high-res (needs kaleido)

DASH (dashboards):
  pip install dash
  app = Dash(__name__)
  app.layout = html.Div([dcc.Dropdown(...), dcc.Graph(id='chart')])
  @app.callback(Output('chart','figure'), Input('dropdown','value'))
  def update(val): return px.scatter(...)
  app.run(debug=True)   → http://127.0.0.1:8050

REMEMBER:
  "Plotly = interactive by default.
   write_html() to share, write_image() to publish,
   Dash to build a full web dashboard."
"""
