"""
PANDAS - COMPLETE GUIDE
=========================

Pandas is the foundational library for data manipulation and analysis in Python.
It provides two core data structures — Series and DataFrame — and a vast toolkit
for loading, cleaning, transforming, aggregating, and exporting data.

Key Characteristics:
- DataFrame = 2D labeled table (rows + columns), like a spreadsheet in memory
- Series    = 1D labeled array (one column of a DataFrame)
- Tight integration with NumPy, Matplotlib, Seaborn, Plotly, and Scikit-learn
- Handles missing data, time series, categorical data, and large files

Installation:
  pip install pandas
  pip install openpyxl    ← required for Excel (.xlsx) read/write
  pip install sqlalchemy  ← required for SQL read/write

Common Uses:
- Loading and exploring datasets (CSV, Excel, JSON, SQL, Parquet)
- Data cleaning (missing values, duplicates, type conversion)
- Data transformation (groupby, pivot, merge, reshape)
- Feature engineering for Machine Learning
- Time series analysis
"""

import numpy as np
import pandas as pd
import io

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 100)
pd.set_option('display.float_format', '{:.3f}'.format)


# ──────────────────────────────────────────────────────────────────────────────
# SHARED DATASET  (used throughout the file)
# ──────────────────────────────────────────────────────────────────────────────

def make_sales_df(seed=42):
    rng      = np.random.default_rng(seed)
    n        = 300
    products = rng.choice(['Laptop', 'Phone', 'Tablet', 'Watch'], n)
    regions  = rng.choice(['North', 'South', 'East', 'West'], n)
    quarters = rng.choice(['Q1', 'Q2', 'Q3', 'Q4'], n)
    base     = {'Laptop': 1200, 'Phone': 800, 'Tablet': 500, 'Watch': 300}
    revenue  = np.array([base[p] for p in products])
    revenue  = (revenue * rng.uniform(0.7, 1.4, n) + rng.normal(0, 30, n)).round(2)
    units    = rng.integers(1, 30, n)
    sat      = np.clip(rng.normal(3.8, 0.6, n), 1, 5).round(1)
    exp_yrs  = rng.integers(1, 15, n).astype(float)

    # Introduce some missing values intentionally
    missing_idx = rng.choice(n, 20, replace=False)
    sat[missing_idx[:10]]     = np.nan
    exp_yrs[missing_idx[10:]] = np.nan

    dates = pd.date_range('2023-01-01', periods=n, freq='D')

    return pd.DataFrame({
        'date':     dates,
        'product':  products,
        'region':   regions,
        'quarter':  quarters,
        'revenue':  revenue,
        'units':    units,
        'satisfaction': sat,
        'experience_years': exp_yrs,
    })


def make_customers_df(seed=7):
    rng = np.random.default_rng(seed)
    n   = 80
    return pd.DataFrame({
        'customer_id': range(1, n + 1),
        'name':        [f'Customer_{i:03d}' for i in range(1, n + 1)],
        'region':      rng.choice(['North', 'South', 'East', 'West'], n),
        'tier':        rng.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], n,
                                   p=[0.4, 0.3, 0.2, 0.1]),
        'age':         rng.integers(25, 65, n),
        'active':      rng.choice([True, False], n, p=[0.85, 0.15]),
    })


def main():

    print("=== PANDAS - COMPLETE GUIDE ===\n")
    print(f"Pandas version:  {pd.__version__}")
    print(f"NumPy  version:  {np.__version__}\n")

    df       = make_sales_df()
    df_cust  = make_customers_df()


    # ------------------------------------------------------------------
    # 1. CORE DATA STRUCTURES
    # ------------------------------------------------------------------
    print("1. CORE DATA STRUCTURES")
    print("-" * 70)

    print("--- Series: 1D labeled array ---")
    s = pd.Series([10, 20, 30, 40, 50],
                  index=['a', 'b', 'c', 'd', 'e'],
                  name='my_series')
    print(s)
    print(f"\ns.dtype   = {s.dtype}")
    print(f"s.shape   = {s.shape}")
    print(f"s['b']    = {s['b']}")
    print(f"s[1:3]    = {s[1:3].tolist()}")
    print(f"s[s > 20] = {s[s > 20].tolist()}")

    print()
    print("--- DataFrame: 2D labeled table ---")
    df_small = pd.DataFrame({
        'name':    ['Alice', 'Bob', 'Carol', 'Dave'],
        'age':     [28, 35, 42, 31],
        'score':   [88.5, 92.0, 78.3, 95.1],
        'passed':  [True, True, False, True],
    })
    print(df_small)
    print(f"\nShape:    {df_small.shape}   → (rows, columns)")
    print(f"Columns:  {df_small.columns.tolist()}")
    print(f"Index:    {df_small.index.tolist()}")
    print(f"dtypes:\n{df_small.dtypes}")

    print()
    print("--- Series vs DataFrame relationship ---")
    print("  df['score']        → Series  (one column)")
    print("  df[['score']]      → DataFrame (one-column DataFrame)")
    print("  df.loc[0]          → Series  (one row)")
    print("  df.iloc[0:2]       → DataFrame (slice of rows)")
    print()


    # ------------------------------------------------------------------
    # 2. CREATING DATAFRAMES
    # ------------------------------------------------------------------
    print("2. CREATING DATAFRAMES")
    print("-" * 70)

    print("--- From dict of lists ---")
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    print(df1)

    print()
    print("--- From list of dicts (common from APIs/JSON) ---")
    df2 = pd.DataFrame([
        {'name': 'Alice', 'score': 88},
        {'name': 'Bob',   'score': 92},
    ])
    print(df2)

    print()
    print("--- From NumPy array ---")
    arr = np.random.default_rng(0).integers(0, 100, (3, 4))
    df3 = pd.DataFrame(arr, columns=['W', 'X', 'Y', 'Z'])
    print(df3)

    print()
    print("--- Useful constructors ---")
    print("pd.DataFrame({'a': range(5)})")
    print("pd.DataFrame(np.eye(3), columns=['x','y','z'])")
    print("pd.DataFrame(index=range(5), columns=['a','b'])  ← empty DataFrame")
    print()


    # ------------------------------------------------------------------
    # 3. READING AND WRITING DATA
    # ------------------------------------------------------------------
    print("3. READING AND WRITING DATA")
    print("-" * 70)

    print("""
  ── CSV ──────────────────────────────────────────────────────────────
  df = pd.read_csv('data.csv')
  df = pd.read_csv('data.csv',
        sep=';',                   ← delimiter (default ',')
        header=0,                  ← row to use as column names
        index_col='id',            ← column to use as row index
        usecols=['a', 'b', 'c'],   ← load only these columns
        dtype={'col': float},      ← force column dtype
        na_values=['NA', '?', ''], ← extra values to treat as NaN
        parse_dates=['date_col'],  ← auto-parse date columns
        nrows=1000,                ← load only first N rows
        skiprows=2,                ← skip first N rows
        encoding='utf-8',          ← file encoding
        chunksize=10_000)          ← iterator for large files

  df.to_csv('output.csv', index=False)   ← index=False avoids extra column

  ── EXCEL ────────────────────────────────────────────────────────────
  df = pd.read_excel('data.xlsx',
        sheet_name='Sheet1',       ← or 0 for first sheet
        skiprows=1)                ← skip header rows

  df.to_excel('output.xlsx', sheet_name='Results', index=False)

  # Multiple sheets:
  with pd.ExcelWriter('output.xlsx') as writer:
      df1.to_excel(writer, sheet_name='Sales')
      df2.to_excel(writer, sheet_name='Customers')

  ── JSON ─────────────────────────────────────────────────────────────
  df = pd.read_json('data.json')
  df = pd.read_json('data.json', orient='records')
  df.to_json('output.json', orient='records', indent=2)

  ── SQL ──────────────────────────────────────────────────────────────
  from sqlalchemy import create_engine
  engine = create_engine('postgresql://user:pass@host/db')
  df = pd.read_sql('SELECT * FROM sales WHERE year = 2024', engine)
  df = pd.read_sql_table('sales', engine)
  df.to_sql('results', engine, if_exists='append', index=False)

  ── PARQUET (fast, columnar — great for ML pipelines) ────────────────
  df = pd.read_parquet('data.parquet')           ← needs pyarrow/fastparquet
  df.to_parquet('data.parquet', index=False)

  ── CLIPBOARD ────────────────────────────────────────────────────────
  df = pd.read_clipboard()    ← paste from Excel/spreadsheet (great for EDA!)
  df.to_clipboard()           ← copy to clipboard

  💡 For large CSV files, use chunksize= to process in batches:
     for chunk in pd.read_csv('big.csv', chunksize=50_000):
         process(chunk)
    """)

    # Demonstrate reading from a string (simulates a file)
    csv_string = """product,revenue,units
Laptop,1250.50,5
Phone,820.00,12
Tablet,490.75,8"""
    df_from_csv = pd.read_csv(io.StringIO(csv_string))
    print("Example — read_csv from string:")
    print(df_from_csv)
    print()


    # ------------------------------------------------------------------
    # 4. EXPLORING A DATAFRAME
    # ------------------------------------------------------------------
    print("4. EXPLORING A DATAFRAME")
    print("-" * 70)

    print("--- First look ---")
    print(f"df.shape     = {df.shape}")
    print(f"df.columns   = {df.columns.tolist()}")
    print(f"df.dtypes:\n{df.dtypes}\n")

    print("df.head(5):")
    print(df.head(5))

    print("\ndf.info():")
    df.info()

    print("\ndf.describe():")
    print(df.describe())

    print()
    print("--- Useful exploration methods ---")
    print(f"df['product'].value_counts():\n{df['product'].value_counts()}\n")
    print(f"df['product'].nunique()      = {df['product'].nunique()}")
    print(f"df['revenue'].mean()         = {df['revenue'].mean():.2f}")
    print(f"df['revenue'].median()       = {df['revenue'].median():.2f}")
    print(f"df['revenue'].std()          = {df['revenue'].std():.2f}")
    print(f"df['revenue'].min()          = {df['revenue'].min():.2f}")
    print(f"df['revenue'].max()          = {df['revenue'].max():.2f}")
    print(f"df['revenue'].quantile(0.75) = {df['revenue'].quantile(0.75):.2f}")
    print(f"df.isnull().sum():\n{df.isnull().sum()}\n")

    print("--- Memory usage ---")
    print(f"df.memory_usage(deep=True).sum() / 1024: "
          f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    print()


    # ------------------------------------------------------------------
    # 5. INDEXING AND SELECTION
    # ------------------------------------------------------------------
    print("5. INDEXING AND SELECTION")
    print("-" * 70)

    sample = df.head(6).copy()

    print("--- Column selection ---")
    print(f"df['revenue']           → Series  (shape {df['revenue'].shape})")
    print(f"df[['revenue','units']] → DataFrame (shape {df[['revenue','units']].shape})")

    print()
    print("--- .loc  — label-based (row label, column name) ---")
    print(f"df.loc[0, 'revenue']           = {df.loc[0, 'revenue']}")
    print(f"df.loc[0:2, ['product','revenue']]:\n{df.loc[0:2, ['product','revenue']]}")
    print(f"df.loc[df['product']=='Laptop', 'revenue'].mean() = "
          f"{df.loc[df['product']=='Laptop', 'revenue'].mean():.2f}")

    print()
    print("--- .iloc — integer-based (row number, col number) ---")
    print(f"df.iloc[0, 0]         = {df.iloc[0, 0]}")
    print(f"df.iloc[0:3, 0:3]:\n{df.iloc[0:3, 0:3]}")
    print(f"df.iloc[-5:, -3:]:\n{df.iloc[-5:, -3:]}")

    print()
    print("--- Boolean indexing (filtering) ---")
    laptops     = df[df['product'] == 'Laptop']
    high_rev    = df[df['revenue'] > 1000]
    north_phone = df[(df['region'] == 'North') & (df['product'] == 'Phone')]
    multi_prod  = df[df['product'].isin(['Laptop', 'Tablet'])]

    print(f"df[df['product']=='Laptop']            → {len(laptops)} rows")
    print(f"df[df['revenue'] > 1000]               → {len(high_rev)} rows")
    print(f"df[(region=='North') & (prod=='Phone')] → {len(north_phone)} rows")
    print(f"df[df['product'].isin([...])]           → {len(multi_prod)} rows")

    print()
    print("--- .query() — readable string filtering ---")
    result = df.query("product == 'Laptop' and revenue > 1000")
    print(f"df.query(\"product=='Laptop' and revenue>1000\") → {len(result)} rows")

    # Using external variable in query
    threshold = 1200
    result2 = df.query("revenue > @threshold")
    print(f"df.query('revenue > @threshold')  → {len(result2)} rows  "
          f"(@ references Python variable)")

    print()
    print("⚠️  df.loc[0:3]  includes row 3 (label-based, inclusive!)")
    print("   df.iloc[0:3] excludes row 3 (integer-based, like Python slices)")
    print()


    # ------------------------------------------------------------------
    # 6. ADDING, MODIFYING AND DELETING COLUMNS
    # ------------------------------------------------------------------
    print("6. ADDING, MODIFYING AND DELETING COLUMNS")
    print("-" * 70)

    df_mod = df.head(8).copy()

    print("--- Adding columns ---")
    df_mod['profit']       = df_mod['revenue'] * df_mod['units'] * 0.25
    df_mod['revenue_k']    = (df_mod['revenue'] / 1000).round(3)
    df_mod['is_premium']   = df_mod['product'].isin(['Laptop', 'Phone'])
    df_mod['rev_category'] = pd.cut(df_mod['revenue'],
                                     bins=[0, 500, 800, 1200, np.inf],
                                     labels=['Low', 'Mid', 'High', 'Premium'])
    print(df_mod[['product', 'revenue', 'profit',
                   'revenue_k', 'is_premium', 'rev_category']])

    print()
    print("--- assign() — chainable column addition ---")
    df_chain = (df.head(4)
                  .assign(profit   = lambda x: x['revenue'] * 0.25,
                          margin_k = lambda x: (x['revenue'] * 0.25 / 1000).round(4))
               )
    print(df_chain[['product', 'revenue', 'profit', 'margin_k']])

    print()
    print("--- Modifying columns ---")
    df_mod2 = df.head(4).copy()
    df_mod2['product']  = df_mod2['product'].str.upper()
    df_mod2['revenue']  = df_mod2['revenue'].round(0)
    df_mod2['quarter']  = df_mod2['quarter'].str.replace('Q', 'Quarter ')
    print(df_mod2[['product', 'revenue', 'quarter']])

    print()
    print("--- Renaming columns ---")
    renamed = df.rename(columns={'revenue': 'rev_eur',
                                  'units':   'qty',
                                  'product': 'item'})
    print(f"Renamed columns: {renamed.columns.tolist()}")

    print()
    print("--- Dropping columns and rows ---")
    df_drop = df.drop(columns=['satisfaction', 'experience_years'])
    print(f"After dropping cols: {df_drop.columns.tolist()}")
    df_drop2 = df.drop(index=[0, 1, 2])
    print(f"After dropping rows 0-2: shape = {df_drop2.shape}")
    print()


    # ------------------------------------------------------------------
    # 7. DATA CLEANING
    # ------------------------------------------------------------------
    print("7. DATA CLEANING")
    print("-" * 70)

    print("--- Missing values (NaN) ---")
    print(f"Total NaN per column:\n{df.isnull().sum()}")
    print(f"\nTotal NaN in entire DataFrame: {df.isnull().sum().sum()}")
    print(f"% missing per column:\n"
          f"{(df.isnull().sum() / len(df) * 100).round(1)}")

    print()
    print("--- Strategies for handling NaN ---")

    # Drop rows with any NaN
    df_dropped = df.dropna()
    print(f"dropna()                      → {len(df_dropped)} rows  "
          f"(dropped {len(df) - len(df_dropped)} rows)")

    # Drop rows only if ALL values are NaN
    df_dropped2 = df.dropna(how='all')
    print(f"dropna(how='all')             → {len(df_dropped2)} rows")

    # Drop rows with NaN only in specific columns
    df_dropped3 = df.dropna(subset=['satisfaction'])
    print(f"dropna(subset=['satisfaction'])→ {len(df_dropped3)} rows")

    # Fill with scalar
    df_fill1 = df.copy()
    df_fill1['satisfaction']    = df_fill1['satisfaction'].fillna(0)
    df_fill1['experience_years']= df_fill1['experience_years'].fillna(-1)
    print(f"fillna(scalar)                → NaN count: "
          f"{df_fill1.isnull().sum().sum()}")

    # Fill with mean/median (common in ML)
    df_fill2 = df.copy()
    df_fill2['satisfaction']     = df_fill2['satisfaction'].fillna(
                                        df_fill2['satisfaction'].mean())
    df_fill2['experience_years'] = df_fill2['experience_years'].fillna(
                                        df_fill2['experience_years'].median())
    print(f"fillna(mean/median)           → NaN count: "
          f"{df_fill2.isnull().sum().sum()}")

    # Forward fill / backward fill (time series)
    df_fill3 = df.copy()
    df_fill3['satisfaction']     = df_fill3['satisfaction'].ffill()
    df_fill3['experience_years'] = df_fill3['experience_years'].bfill()
    print(f"ffill() / bfill()             → NaN count: "
          f"{df_fill3.isnull().sum().sum()}")

    print()
    print("--- Duplicates ---")
    df_dupes = pd.concat([df.head(10), df.head(3)])  # add duplicate rows
    print(f"df.duplicated().sum()              = {df_dupes.duplicated().sum()}")
    print(f"df.duplicated(subset=['product']) = "
          f"{df_dupes.duplicated(subset=['product']).sum()}")
    df_clean = df_dupes.drop_duplicates()
    print(f"After drop_duplicates():    {len(df_clean)} rows (was {len(df_dupes)})")
    df_clean2 = df_dupes.drop_duplicates(subset=['product'], keep='last')
    print(f"drop_duplicates(subset, keep='last'): {len(df_clean2)} rows")

    print()
    print("--- Data types ---")
    print(f"df.dtypes:\n{df.dtypes}")

    df_typed = df.copy()
    df_typed['product']  = df_typed['product'].astype('category')
    df_typed['quarter']  = df_typed['quarter'].astype('category')
    df_typed['units']    = df_typed['units'].astype(np.int32)
    df_typed['revenue']  = df_typed['revenue'].astype(np.float32)

    print(f"\nAfter type optimization:\n{df_typed.dtypes}")
    orig_mem  = df.memory_usage(deep=True).sum() / 1024
    typed_mem = df_typed.memory_usage(deep=True).sum() / 1024
    print(f"\nMemory: {orig_mem:.1f} KB → {typed_mem:.1f} KB  "
          f"({(1 - typed_mem/orig_mem)*100:.0f}% reduction)")

    print()
    print("--- String cleaning ---")
    df_str = pd.DataFrame({'name': ['  Alice ', 'BOB', 'carol  ', 'Dave'],
                           'email': ['alice@test.com', 'bob@TEST.COM',
                                     ' carol@test.com', 'dave@test.com']})
    df_str['name']  = df_str['name'].str.strip().str.title()
    df_str['email'] = df_str['email'].str.strip().str.lower()
    print(df_str)

    print()
    print("--- Outlier detection ---")
    Q1  = df['revenue'].quantile(0.25)
    Q3  = df['revenue'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['revenue'] < Q1 - 1.5 * IQR) |
                  (df['revenue'] > Q3 + 1.5 * IQR)]
    print(f"IQR method: Q1={Q1:.1f}  Q3={Q3:.1f}  IQR={IQR:.1f}")
    print(f"Outliers detected: {len(outliers)} rows")
    print()


    # ------------------------------------------------------------------
    # 8. STRING OPERATIONS (.str accessor)
    # ------------------------------------------------------------------
    print("8. STRING OPERATIONS (.str accessor)")
    print("-" * 70)

    s = pd.Series(['Laptop Pro X1', 'phone 12 MAX', '  Tablet   ', 'SMART WATCH'])

    print(f"Original:          {s.tolist()}")
    print(f"str.lower():       {s.str.lower().tolist()}")
    print(f"str.upper():       {s.str.upper().tolist()}")
    print(f"str.title():       {s.str.title().tolist()}")
    print(f"str.strip():       {s.str.strip().tolist()}")
    print(f"str.len():         {s.str.len().tolist()}")
    print(f"str.contains('Pro'):{s.str.contains('Pro').tolist()}")
    print(f"str.startswith('L'):{s.str.startswith('L').tolist()}")
    print(f"str.replace(' ','_'):{s.str.replace(' ', '_').tolist()}")
    print(f"str.split().str[0]: {s.str.strip().str.split().str[0].tolist()}")

    print()
    print("--- Regex operations ---")
    emails = pd.Series(['alice@gmail.com', 'bob@yahoo.co.uk',
                        'invalid-email', 'carol@company.org'])
    print(f"str.contains(regex): {emails.str.contains(r'@\w+\.\w+').tolist()}")
    print(f"str.extract domain:  "
          f"{emails.str.extract(r'@([\w.]+)')[0].tolist()}")

    print()
    print("--- str accessor methods ---")
    print("  s.str.lower() / upper() / title() / capitalize()")
    print("  s.str.strip() / lstrip() / rstrip()")
    print("  s.str.split(sep, expand=True)  → splits into multiple columns")
    print("  s.str.contains(pat, regex=True)")
    print("  s.str.startswith() / endswith()")
    print("  s.str.replace(old, new, regex=True)")
    print("  s.str.extract(r'(pattern)')    → extract regex group")
    print("  s.str.extractall(r'(pattern)') → extract all matches")
    print("  s.str.len()                    → length of each string")
    print("  s.str.zfill(5)                 → pad with leading zeros")
    print()


    # ------------------------------------------------------------------
    # 9. APPLY, MAP AND VECTORIZED OPERATIONS
    # ------------------------------------------------------------------
    print("9. APPLY, MAP AND VECTORIZED OPERATIONS")
    print("-" * 70)

    sample = df.head(6).copy()

    print("--- Vectorized operations (FASTEST — always prefer) ---")
    sample['rev_doubled']  = sample['revenue'] * 2
    sample['rev_log']      = np.log1p(sample['revenue'])
    sample['above_mean']   = sample['revenue'] > sample['revenue'].mean()
    print(sample[['revenue', 'rev_doubled', 'rev_log', 'above_mean']])

    print()
    print("--- map() — element-wise on Series (scalar → scalar) ---")
    tier_map = {'Laptop': 'Premium', 'Phone': 'Mid', 'Tablet': 'Mid', 'Watch': 'Low'}
    sample['tier'] = sample['product'].map(tier_map)
    print(sample[['product', 'tier']])

    print()
    print("--- apply() on Series — custom function per element ---")
    def revenue_band(rev):
        if rev < 500:   return 'Low'
        elif rev < 900: return 'Mid'
        else:           return 'High'

    sample['band'] = sample['revenue'].apply(revenue_band)
    print(sample[['revenue', 'band']])

    print()
    print("--- apply() on DataFrame — function per row or column ---")
    # axis=1 → apply function to each ROW
    sample['summary'] = sample.apply(
        lambda row: f"{row['product']} ({row['region']}): €{row['revenue']:.0f}",
        axis=1
    )
    print(sample[['summary']])

    print()
    print("--- np.where() and np.select() — fast conditional columns ---")
    sample['label'] = np.where(sample['revenue'] > 1000, 'High', 'Low')

    conditions = [
        sample['revenue'] < 500,
        sample['revenue'] < 900,
        sample['revenue'] < 1200,
    ]
    choices = ['Budget', 'Mid-range', 'Premium']
    sample['category'] = np.select(conditions, choices, default='Luxury')
    print(sample[['revenue', 'label', 'category']])

    print()
    print("--- pd.cut() and pd.qcut() --- binning ---")
    df_cut = df.copy()
    df_cut['rev_bin']    = pd.cut(df_cut['revenue'],
                                   bins=4, labels=['Q1','Q2','Q3','Q4'])
    df_cut['rev_qbin']   = pd.qcut(df_cut['revenue'],
                                    q=4, labels=['Q1','Q2','Q3','Q4'])
    print(f"pd.cut  (equal width bins): \n{df_cut['rev_bin'].value_counts()}")
    print(f"pd.qcut (equal frequency):  \n{df_cut['rev_qbin'].value_counts()}")

    print()
    print("Performance order (fastest → slowest):")
    print("  Vectorized ops (+, *, np.func) > map() > apply() > iterrows()")
    print("⚠️  Avoid iterrows() — it is extremely slow on large DataFrames.")
    print("   Prefer vectorized operations or apply() at worst.")
    print()


    # ------------------------------------------------------------------
    # 10. GROUPBY AND AGGREGATION
    # ------------------------------------------------------------------
    print("10. GROUPBY AND AGGREGATION")
    print("-" * 70)

    print("--- Basic groupby ---")
    g = df.groupby('product')['revenue']
    print(g.mean().round(2))

    print()
    print("--- Multiple aggregations with agg() ---")
    summary = df.groupby('product').agg(
        count       = ('revenue', 'count'),
        mean_rev    = ('revenue', 'mean'),
        median_rev  = ('revenue', 'median'),
        total_rev   = ('revenue', 'sum'),
        std_rev     = ('revenue', 'std'),
        mean_units  = ('units',   'mean'),
        mean_sat    = ('satisfaction', 'mean'),
    ).round(2)
    print(summary)

    print()
    print("--- Multiple groupby keys ---")
    by_prod_region = (df.groupby(['product', 'region'])['revenue']
                        .agg(['mean', 'count', 'sum'])
                        .round(2))
    print(by_prod_region.head(8))

    print()
    print("--- transform() — returns same-size result (for new columns) ---")
    df['group_mean_rev'] = df.groupby('product')['revenue'].transform('mean')
    df['rev_vs_mean']    = df['revenue'] - df['group_mean_rev']
    df['rank_in_group']  = df.groupby('product')['revenue'].rank(ascending=False)
    print(df[['product', 'revenue', 'group_mean_rev',
               'rev_vs_mean', 'rank_in_group']].head(8))

    print()
    print("--- filter() — keep only groups meeting a condition ---")
    active_products = df.groupby('product').filter(lambda g: g['revenue'].mean() > 700)
    print(f"Products with mean revenue > 700: "
          f"{active_products['product'].unique().tolist()}")

    print()
    print("--- Custom aggregation functions ---")
    custom = df.groupby('product')['revenue'].agg(
        mean='mean',
        range=lambda x: x.max() - x.min(),
        coeff_var=lambda x: x.std() / x.mean()
    ).round(3)
    print(custom)

    # Clean up added columns
    df.drop(columns=['group_mean_rev', 'rev_vs_mean', 'rank_in_group'],
            inplace=True)
    print()


    # ------------------------------------------------------------------
    # 11. PIVOT TABLES AND CROSSTABS
    # ------------------------------------------------------------------
    print("11. PIVOT TABLES AND CROSSTABS")
    print("-" * 70)

    print("--- pivot_table() ---")
    pivot = df.pivot_table(
        values   = 'revenue',
        index    = 'region',
        columns  = 'product',
        aggfunc  = 'mean',
        margins  = True,       # add row/col totals
        margins_name = 'TOTAL',
    ).round(0)
    print(pivot)

    print()
    print("--- Multiple values and aggfuncs ---")
    pivot2 = df.pivot_table(
        values  = ['revenue', 'units'],
        index   = 'quarter',
        columns = 'product',
        aggfunc = {'revenue': 'sum', 'units': 'mean'}
    ).round(1)
    print(pivot2)

    print()
    print("--- pd.crosstab() — frequency table ---")
    ct = pd.crosstab(df['region'], df['product'],
                     values=df['revenue'], aggfunc='mean',
                     margins=True, margins_name='TOTAL').round(0)
    print(ct)

    print()
    print("--- pivot() vs pivot_table() ---")
    print("  pivot()       → simple reshape, no aggregation, fails on duplicates")
    print("  pivot_table() → aggregates duplicates, supports multiple aggfuncs")
    print()


    # ------------------------------------------------------------------
    # 12. MERGE, JOIN AND CONCAT
    # ------------------------------------------------------------------
    print("12. MERGE, JOIN AND CONCAT")
    print("-" * 70)

    # Sample DataFrames
    orders   = pd.DataFrame({
        'order_id':    [1, 2, 3, 4, 5],
        'customer_id': [10, 20, 10, 30, 40],
        'amount':      [500, 1200, 800, 300, 950],
    })
    customers = pd.DataFrame({
        'customer_id': [10, 20, 30, 50],
        'name':        ['Alice', 'Bob', 'Carol', 'Eve'],
        'tier':        ['Gold', 'Silver', 'Bronze', 'Platinum'],
    })

    print("Orders DataFrame:")
    print(orders)
    print("\nCustomers DataFrame:")
    print(customers)

    print()
    print("--- INNER JOIN — only matching rows ---")
    inner = pd.merge(orders, customers, on='customer_id', how='inner')
    print(inner)

    print()
    print("--- LEFT JOIN — all orders, NaN for unmatched customers ---")
    left = pd.merge(orders, customers, on='customer_id', how='left')
    print(left)

    print()
    print("--- RIGHT JOIN ---")
    right = pd.merge(orders, customers, on='customer_id', how='right')
    print(right)

    print()
    print("--- OUTER JOIN ---")
    outer = pd.merge(orders, customers, on='customer_id', how='outer')
    print(outer)

    print()
    print("--- Merge on different column names ---")
    df_a = pd.DataFrame({'id': [1,2,3], 'val': ['a','b','c']})
    df_b = pd.DataFrame({'ref': [2,3,4], 'info': ['x','y','z']})
    merged = pd.merge(df_a, df_b, left_on='id', right_on='ref', how='inner')
    print(merged)

    print()
    print("--- Merge with suffixes (when both have same column names) ---")
    df_x = pd.DataFrame({'id':[1,2], 'value':[10,20]})
    df_y = pd.DataFrame({'id':[1,2], 'value':[100,200]})
    with_sfx = pd.merge(df_x, df_y, on='id', suffixes=('_x', '_y'))
    print(with_sfx)

    print()
    print("--- pd.concat() — stack DataFrames ---")
    top    = df.head(3).copy()
    bottom = df.tail(3).copy()
    stacked = pd.concat([top, bottom], ignore_index=True)
    print(f"concat (axis=0 — rows): {stacked.shape}")

    df_a2 = df[['product', 'revenue']].head(3)
    df_b2 = df[['units', 'satisfaction']].head(3)
    side = pd.concat([df_a2, df_b2], axis=1)
    print(f"concat (axis=1 — cols): {side.shape}")
    print(side)

    print()
    print("💡 merge() vs join() vs concat():")
    print("   merge()  → SQL-style join on key columns (most flexible)")
    print("   join()   → merge on index (df1.join(df2))")
    print("   concat() → stack DataFrames vertically (axis=0) or horizontally (axis=1)")
    print()


    # ------------------------------------------------------------------
    # 13. RESHAPING: MELT, STACK, UNSTACK
    # ------------------------------------------------------------------
    print("13. RESHAPING: MELT, STACK, UNSTACK")
    print("-" * 70)

    print("--- Wide → Long with melt() ---")
    wide = pd.DataFrame({
        'model':     ['RF', 'XGB', 'SVM'],
        'accuracy':  [0.91, 0.93, 0.88],
        'f1_score':  [0.89, 0.92, 0.86],
        'precision': [0.90, 0.94, 0.87],
    })
    print("Wide format:")
    print(wide)

    long = wide.melt(id_vars='model',
                     value_vars=['accuracy', 'f1_score', 'precision'],
                     var_name='metric',
                     value_name='score')
    print("\nLong format (after melt):")
    print(long)

    print()
    print("--- Long → Wide with pivot() ---")
    back_wide = long.pivot(index='model', columns='metric', values='score')
    back_wide.columns.name = None
    back_wide = back_wide.reset_index()
    print("Back to wide (after pivot):")
    print(back_wide)

    print()
    print("--- stack() / unstack() ---")
    stk = df.groupby(['product', 'quarter'])['revenue'].mean().round(0)
    print("MultiIndex Series (product × quarter):")
    print(stk.head(8))
    print("\nunstack() → Wide DataFrame:")
    print(stk.unstack())
    print()


    # ------------------------------------------------------------------
    # 14. TIME SERIES
    # ------------------------------------------------------------------
    print("14. TIME SERIES")
    print("-" * 70)

    print("--- Creating date ranges ---")
    daily   = pd.date_range('2024-01-01', periods=10, freq='D')
    monthly = pd.date_range('2024-01-01', periods=12, freq='MS')  # Month Start
    busdays = pd.date_range('2024-01-01', periods=10, freq='B')   # Business days
    print(f"Daily:    {daily[:3].tolist()} ...")
    print(f"Monthly:  {monthly[:3].tolist()} ...")
    print(f"Business: {busdays[:3].tolist()} ...")

    print()
    print("--- Parsing dates ---")
    df_ts = df.copy()
    df_ts['date'] = pd.to_datetime(df_ts['date'])
    print(f"dtype after to_datetime: {df_ts['date'].dtype}")

    print()
    print("--- Date component extraction ---")
    df_ts = df.assign(
        date=pd.to_datetime(df['date']),
        year=lambda x: x['date'].dt.year,
        month=lambda x: x['date'].dt.month,
        month_name=lambda x: x['date'].dt.month_name(),
        day=lambda x: x['date'].dt.day,
        dayofweek=lambda x: x['date'].dt.dayofweek,
        weekday=lambda x: x['date'].dt.day_name(),
        quarter_n=lambda x: x['date'].dt.quarter,
        is_weekend=lambda x: x['date'].dt.dayofweek >= 5
    )
    print(df_ts[['date','year','month','month_name',
                  'dayofweek','weekday','is_weekend']].head(5))

    print()
    print("--- Filtering by date ---")
    jan = df_ts[df_ts['date'].dt.month == 1]
    q1  = df_ts[df_ts['date'].between('2023-01-01', '2023-03-31')]
    print(f"January rows:  {len(jan)}")
    print(f"Q1 2023 rows:  {len(q1)}")

    print()
    print("--- Resample (time-based groupby) ---")
    df_ts2 = df_ts.set_index('date').sort_index()

    monthly_rev = df_ts2['revenue'].resample('ME').sum()      # Month End
    weekly_avg  = df_ts2['revenue'].resample('W').mean()
    print("Monthly revenue (resample 'ME'):")
    print(monthly_rev.round(0))

    print()
    print("--- Rolling statistics ---")
    df_ts2['rolling_7d_mean']  = df_ts2['revenue'].rolling(window=7).mean()
    df_ts2['rolling_30d_std']  = df_ts2['revenue'].rolling(window=30).std()
    df_ts2['expanding_cummax'] = df_ts2['revenue'].expanding().max()
    print(df_ts2[['revenue', 'rolling_7d_mean',
                   'rolling_30d_std', 'expanding_cummax']].head(10))

    print()
    print("--- Date offsets and arithmetic ---")
    ts = pd.Timestamp('2024-06-15')
    print(f"Original:     {ts}")
    print(f"+ 30 days:    {ts + pd.Timedelta(days=30)}")
    print(f"+ 1 month:    {ts + pd.DateOffset(months=1)}")
    print(f"Month start:  {ts.to_period('M').to_timestamp()}")
    print(f"Month end:    {ts + pd.offsets.MonthEnd(0)}")
    print()


    # ------------------------------------------------------------------
    # 15. CATEGORICAL DATA
    # ------------------------------------------------------------------
    print("15. CATEGORICAL DATA")
    print("-" * 70)

    df_cat = df.copy()
    df_cat['product'] = df_cat['product'].astype('category')
    df_cat['region']  = df_cat['region'].astype('category')
    df_cat['quarter'] = pd.Categorical(
        df_cat['quarter'],
        categories=['Q1','Q2','Q3','Q4'],
        ordered=True
    )

    print(f"product categories: {df_cat['product'].cat.categories.tolist()}")
    print(f"quarter categories: {df_cat['quarter'].cat.categories.tolist()}")
    print(f"quarter is ordered: {df_cat['quarter'].cat.ordered}")

    print()
    print("--- Categorical operations ---")
    print(f"value_counts:\n{df_cat['product'].value_counts()}")
    print(f"\nRenaming categories:")
    df_cat2 = df_cat.copy()
    df_cat2['product'] = df_cat2['product'].cat.rename_categories({
        'Laptop': 'Notebook', 'Watch': 'Smartwatch'
    })
    print(df_cat2['product'].cat.categories.tolist())

    print()
    print("--- Memory savings from category dtype ---")
    obj_mem = df['product'].astype(str).memory_usage(deep=True)
    cat_mem = df['product'].astype('category').memory_usage(deep=True)
    print(f"object dtype:   {obj_mem} bytes")
    print(f"category dtype: {cat_mem} bytes  "
          f"({(1-cat_mem/obj_mem)*100:.0f}% smaller)")
    print()


    # ------------------------------------------------------------------
    # 16. ML DATA PREPARATION
    # ------------------------------------------------------------------
    print("16. ML DATA PREPARATION")
    print("-" * 70)

    print("--- Step 1: Start with a clean copy ---")
    df_ml = df.copy()
    df_ml = df_ml.drop(columns=['date'])
    print(f"Shape: {df_ml.shape}")
    print(f"Dtypes:\n{df_ml.dtypes}")

    print()
    print("--- Step 2: Handle missing values ---")
    num_cols = df_ml.select_dtypes(include='number').columns.tolist()
    cat_cols = df_ml.select_dtypes(include='object').columns.tolist()

    for col in num_cols:
        df_ml[col] = df_ml[col].fillna(df_ml[col].median())

    for col in cat_cols:
        df_ml[col] = df_ml[col].fillna(df_ml[col].mode()[0])

    print(f"NaN after imputation: {df_ml.isnull().sum().sum()}")

    print()
    print("--- Step 3: Encoding categorical variables ---")

    # One-Hot Encoding (for nominal categories — no order)
    df_ohe = pd.get_dummies(df_ml,
                             columns=['product', 'region', 'quarter'],
                             drop_first=True,      # avoid dummy variable trap
                             dtype=int)
    print(f"After get_dummies: {df_ohe.shape} columns")
    ohe_cols = [c for c in df_ohe.columns if any(
        c.startswith(p) for p in ['product_', 'region_', 'quarter_'])]
    print(f"New OHE columns: {ohe_cols}")

    # Label Encoding (for ordinal or tree-based models)
    df_label = df_ml.copy()
    df_label['product_code'] = df_label['product'].astype('category').cat.codes
    df_label['region_code']  = df_label['region'].astype('category').cat.codes
    print(f"\nLabel encoding sample:")
    print(df_label[['product', 'product_code',
                     'region', 'region_code']].drop_duplicates().sort_values('product_code'))

    # Ordinal Encoding (when order matters)
    quarter_order = {'Q1': 0, 'Q2': 1, 'Q3': 2, 'Q4': 3}
    df_label['quarter_ord'] = df_label['quarter'].map(quarter_order)
    print(f"\nOrdinal encoding (quarter):")
    print(df_label[['quarter', 'quarter_ord']].drop_duplicates().sort_values('quarter_ord'))

    print()
    print("--- Step 4: Feature scaling ---")
    df_scaled = df_ml.copy()
    num_features = ['revenue', 'units', 'satisfaction', 'experience_years']

    # Min-Max Scaling [0, 1]
    for col in num_features:
        col_min = df_scaled[col].min()
        col_max = df_scaled[col].max()
        df_scaled[f'{col}_minmax'] = (df_scaled[col] - col_min) / (col_max - col_min)

    # Z-score Standardization [mean=0, std=1]
    for col in num_features:
        df_scaled[f'{col}_zscore'] = (
            (df_scaled[col] - df_scaled[col].mean()) / df_scaled[col].std()
        )

    print("Min-Max scaled (should be [0,1]):")
    print(df_scaled[[f'{c}_minmax' for c in num_features]].describe().round(3))

    print("\nZ-score standardized (mean≈0, std≈1):")
    print(df_scaled[[f'{c}_zscore' for c in num_features]].describe().round(3))

    print()
    print("--- Step 5: Feature engineering ---")
    df_feat = df_ml.copy()
    df_feat['revenue_per_unit'] = df_feat['revenue'] / df_feat['units']
    df_feat['log_revenue']      = np.log1p(df_feat['revenue'])
    df_feat['is_high_value']    = (df_feat['revenue'] > df_feat['revenue'].median()).astype(int)
    df_feat['is_premium']       = df_feat['product'].isin(['Laptop','Phone']).astype(int)

    print(f"New features added: revenue_per_unit, log_revenue, "
          f"is_high_value, is_premium")
    print(df_feat[['revenue', 'revenue_per_unit', 'log_revenue',
                    'is_high_value', 'is_premium']].head())

    print()
    print("--- Step 6: Train/Test split (without sklearn) ---")
    df_shuffled = df_feat.sample(frac=1, random_state=42).reset_index(drop=True)
    split       = int(len(df_shuffled) * 0.8)
    df_train    = df_shuffled.iloc[:split]
    df_test     = df_shuffled.iloc[split:]
    print(f"Train set: {df_train.shape}")
    print(f"Test  set: {df_test.shape}")

    print()
    print("--- With sklearn (recommended for real projects) ---")
    print("  from sklearn.model_selection import train_test_split")
    print("  X = df.drop(columns=['target'])")
    print("  y = df['target']")
    print("  X_train, X_test, y_train, y_test = train_test_split(")
    print("      X, y, test_size=0.2, random_state=42, stratify=y)")
    print()


    # ------------------------------------------------------------------
    # 17. PERFORMANCE TIPS
    # ------------------------------------------------------------------
    print("17. PERFORMANCE TIPS")
    print("-" * 70)
    print("""
  ── READING LARGE FILES ───────────────────────────────────────────────
  # Only load needed columns
  df = pd.read_csv('big.csv', usecols=['col1', 'col2', 'col3'])

  # Specify dtypes upfront (avoids inference overhead)
  df = pd.read_csv('big.csv', dtype={'id': np.int32, 'val': np.float32})

  # Process in chunks
  results = []
  for chunk in pd.read_csv('big.csv', chunksize=100_000):
      results.append(chunk.groupby('key')['val'].sum())
  final = pd.concat(results).groupby(level=0).sum()

  ── MEMORY OPTIMIZATION ───────────────────────────────────────────────
  # Convert string columns to category (when cardinality is low)
  df['region']  = df['region'].astype('category')
  df['product'] = df['product'].astype('category')

  # Downcast numerics
  df['units']   = pd.to_numeric(df['units'],   downcast='integer')
  df['revenue'] = pd.to_numeric(df['revenue'], downcast='float')

  ── FAST OPERATIONS ───────────────────────────────────────────────────
  # Always prefer vectorized over apply/iterrows
  df['new'] = df['a'] * df['b']                   # ✅ fast
  df['new'] = df.apply(lambda r: r['a']*r['b'], axis=1)  # ❌ slow

  # Use isin() instead of multiple OR conditions
  df[df['product'].isin(['Laptop','Phone'])]       # ✅ fast
  df[(df['product']=='Laptop')|(df['product']=='Phone')]  # ❌ verbose

  # Use query() for readable multi-condition filters
  df.query("revenue > 1000 and region == 'North'") # ✅ readable + fast

  ── AVOID COMMON SLOW PATTERNS ────────────────────────────────────────
  ❌ for idx, row in df.iterrows(): ...    → extremely slow
  ❌ df['new'] = ''
     for i in range(len(df)):              → also slow
         df['new'][i] = ...

  ✅ Use vectorized ops, apply(), or np.vectorize() for custom logic
    """)


    # ------------------------------------------------------------------
    # 18. COMMON MISTAKES
    # ------------------------------------------------------------------
    print("18. COMMON MISTAKES")
    print("-" * 70)
    print("""
  Mistake 1 — SettingWithCopyWarning: modifying a slice
    df_sub = df[df['product']=='Laptop']
    df_sub['revenue'] = 0              ← WARNING or silent failure!
    Fix: df_sub = df[df['product']=='Laptop'].copy()
         df_sub['revenue'] = 0         ← safe

  Mistake 2 — df.loc[0:3] includes row 3 (label-inclusive)
    df.loc[0:3]   → rows 0, 1, 2, 3  (INCLUSIVE of 3!)
    df.iloc[0:3]  → rows 0, 1, 2     (exclusive of 3, like Python)

  Mistake 3 — Comparing with NaN using ==
    df[df['col'] == np.nan]     ← always empty! NaN != NaN
    df[df['col'].isna()]        ← correct

  Mistake 4 — Chained indexing
    df['col'][df['col'] > 5] = 0    ← may not work or raises warning
    df.loc[df['col'] > 5, 'col'] = 0  ← correct

  Mistake 5 — Not resetting index after filter/drop
    df_filtered = df[df['revenue'] > 1000]
    df_filtered.iloc[0]   ← index may be 42, not 0!
    Fix: df_filtered = df[df['revenue'] > 1000].reset_index(drop=True)

  Mistake 6 — inplace=True does not chain
    df.dropna(inplace=True)
    df.fillna(0, inplace=True)  ← works, but can't chain
    df = df.dropna().fillna(0)  ← cleaner and chainable

  Mistake 7 — Forgetting drop_first=True in get_dummies
    pd.get_dummies(df, columns=['product'])         ← creates 4 cols (dummy trap)
    pd.get_dummies(df, columns=['product'],
                   drop_first=True)                 ← creates 3 cols (correct for linear models)

  Mistake 8 — groupby losing column names
    df.groupby('product').mean()      ← column 'product' is now the index!
    df.groupby('product').mean().reset_index()  ← restore as column
    df.groupby('product', as_index=False).mean()  ← same result
    """)


    # ------------------------------------------------------------------
    # 19. QUICK REFERENCE TABLE
    # ------------------------------------------------------------------
    print("19. QUICK REFERENCE TABLE")
    print("-" * 70)
    print()
    print(f"  {'Method':<45} {'Description'}")
    print(f"  {'-'*45} {'-'*35}")

    ref = [
        ("CREATION", ""),
        ("pd.DataFrame({'a':[1,2], 'b':[3,4]})",     "From dict of lists"),
        ("pd.read_csv('f.csv', usecols, dtype)",      "Read CSV"),
        ("pd.read_excel('f.xlsx', sheet_name)",       "Read Excel"),
        ("pd.read_json / read_parquet / read_sql",    "Read other formats"),
        ("EXPLORATION", ""),
        ("df.shape / df.dtypes / df.columns",         "Basic attributes"),
        ("df.head(n) / df.tail(n) / df.sample(n)",    "Preview rows"),
        ("df.info() / df.describe()",                 "Summary statistics"),
        ("df.isnull().sum() / df.value_counts()",     "Missing / frequencies"),
        ("df.memory_usage(deep=True).sum()",          "Memory footprint"),
        ("SELECTION", ""),
        ("df['col'] / df[['a','b']]",                 "Column selection"),
        ("df.loc[rows, cols]",                        "Label-based indexing"),
        ("df.iloc[rows, cols]",                       "Integer-based indexing"),
        ("df[df['col'] > x]",                         "Boolean filter"),
        ("df.query(\"col > x and col2 == 'y'\")",     "String query filter"),
        ("df['col'].isin([...])",                     "Membership filter"),
        ("CLEANING", ""),
        ("df.dropna(subset, how)",                    "Drop NaN rows"),
        ("df.fillna(val) / ffill() / bfill()",        "Fill NaN"),
        ("df.drop_duplicates(subset, keep)",          "Remove duplicates"),
        ("df.astype(dtype)",                          "Change column type"),
        ("df.rename(columns={old: new})",             "Rename columns"),
        ("df.drop(columns=[...]) / drop(index=[...])", "Drop cols/rows"),
        ("pd.to_datetime(df['col'])",                 "Parse dates"),
        ("df['col'].str.strip().str.lower()",         "String cleaning"),
        ("TRANSFORMATION", ""),
        ("df['col'].apply(func)",                     "Apply function per element"),
        ("df.apply(func, axis=1)",                    "Apply function per row"),
        ("df['col'].map(dict_or_func)",               "Map values"),
        ("np.where(cond, a, b)",                      "Conditional column"),
        ("pd.cut(col, bins, labels)",                 "Equal-width binning"),
        ("pd.qcut(col, q, labels)",                   "Equal-frequency binning"),
        ("df.assign(new_col=lambda x: ...)",          "Chainable column add"),
        ("GROUPBY", ""),
        ("df.groupby('col').agg(name=('col','func'))", "Named aggregation"),
        ("df.groupby('col')['val'].transform('mean')", "Group metric as new col"),
        ("df.groupby('col').filter(lambda g: ...)",   "Filter whole groups"),
        ("PIVOT", ""),
        ("df.pivot_table(values, index, columns, aggfunc, margins)", "Pivot table"),
        ("pd.crosstab(df['a'], df['b'], margins=True)", "Frequency crosstab"),
        ("df.melt(id_vars, value_vars, var_name)",    "Wide → Long"),
        ("df.pivot(index, columns, values)",          "Long → Wide"),
        ("stk.unstack() / stk.stack()",               "MultiIndex reshape"),
        ("JOIN / CONCAT", ""),
        ("pd.merge(df1, df2, on, how)",               "SQL-style join"),
        ("pd.concat([df1, df2], axis=0/1)",           "Stack DataFrames"),
        ("df1.join(df2, on, how)",                    "Join on index"),
        ("TIME SERIES", ""),
        ("pd.to_datetime(col) / pd.date_range()",     "Create/parse dates"),
        ("df['date'].dt.year / .month / .dayofweek",  "Date components"),
        ("df.set_index('date').resample('ME').sum()",  "Resample aggregate"),
        ("df['col'].rolling(7).mean()",               "Rolling window"),
        ("df['col'].expanding().max()",               "Expanding window"),
        ("ML PREP", ""),
        ("df.select_dtypes(include='number')",        "Select numeric cols"),
        ("pd.get_dummies(df, columns, drop_first=True)", "One-hot encoding"),
        ("df['col'].astype('category').cat.codes",    "Label encoding"),
        ("df['col'].map({'a':0,'b':1})",              "Ordinal encoding"),
        ("(col-col.min())/(col.max()-col.min())",     "Min-Max scaling"),
        ("(col - col.mean()) / col.std()",            "Z-score standardization"),
        ("EXPORT", ""),
        ("df.to_csv('f.csv', index=False)",           "Save CSV"),
        ("df.to_excel('f.xlsx', index=False)",        "Save Excel"),
        ("df.to_parquet('f.parquet')",                "Save Parquet"),
        ("df.to_json('f.json', orient='records')",    "Save JSON"),
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
SUMMARY — PANDAS
=======================================================

CORE STRUCTURES:
  Series    → 1D labeled array  (df['col'])
  DataFrame → 2D labeled table  (rows + columns)

READ / WRITE:
  pd.read_csv / read_excel / read_json / read_sql / read_parquet
  df.to_csv / to_excel / to_json / to_sql / to_parquet
  → Always use index=False when saving unless you need the index

SELECTION:
  df['col']              → Series
  df[['a','b']]          → DataFrame
  df.loc[rows, cols]     → label-based (INCLUSIVE of stop)
  df.iloc[rows, cols]    → integer-based (exclusive of stop)
  df[df['col'] > x]      → boolean filter
  df.query("col > x")    → readable string filter

CLEANING:
  dropna / fillna / ffill / bfill
  drop_duplicates(subset, keep)
  astype / pd.to_datetime / str.strip()
  Outliers: IQR method  Q1 - 1.5*IQR  to  Q3 + 1.5*IQR

TRANSFORMATION:
  map(dict)              → replace values using a mapping
  apply(func)            → custom function per element / row
  np.where(cond, a, b)   → fast conditional column
  assign(col=lambda x:)  → chainable column addition
  pd.cut / pd.qcut       → binning

GROUPBY:
  df.groupby('col').agg(name=('col','func'))
  transform('mean')      → same-size result (new column)
  filter(lambda g: cond) → keep/drop whole groups

PIVOT / RESHAPE:
  pivot_table(values, index, columns, aggfunc, margins)
  melt(id_vars, value_vars)   → wide → long
  pivot(index, columns, values) → long → wide
  unstack() / stack()          → MultiIndex reshape

MERGE / CONCAT:
  pd.merge(df1, df2, on='key', how='inner/left/right/outer')
  pd.concat([df1, df2], axis=0)   → stack rows
  pd.concat([df1, df2], axis=1)   → stack columns

TIME SERIES:
  pd.to_datetime / pd.date_range
  .dt.year / .month / .day / .dayofweek / .day_name()
  resample('ME') / rolling(7) / expanding()

ML PREP PIPELINE:
  1. dropna / fillna (median for num, mode for cat)
  2. get_dummies(drop_first=True)  ← one-hot encoding
  3. cat.codes / map(dict)         ← label / ordinal encoding
  4. (x - x.min()) / (x.max()-x.min())  ← min-max
  5. (x - x.mean()) / x.std()     ← z-score
  6. sample(frac=1).reset_index()  ← shuffle before split

COMMON PITFALLS:
  • Always .copy() before modifying a filtered subset
  • df.loc[0:3] includes 3; df.iloc[0:3] excludes 3
  • NaN == NaN is False → use .isna() / .notna()
  • Use .loc[mask, col] = val, never chained indexing
  • reset_index(drop=True) after filtering
  • drop_first=True in get_dummies to avoid dummy trap
  • groupby(..., as_index=False) to keep col as column

REMEMBER:
  "Pandas = Excel in Python, but with the full power of programming.
   Master loc/iloc, groupby, merge, and melt —
   and you can handle 95% of real-world data tasks."
"""