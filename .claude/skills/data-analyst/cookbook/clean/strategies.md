# Data Cleaning Strategies

Detailed strategies for common cleaning scenarios.

---

## Missing Value Strategies

### Strategy Selection Guide

```
                     MISSING VALUE DECISION TREE

                    How much is missing?
                           │
            ┌──────────────┼──────────────┐
            │              │              │
         <5%           5-30%           >30%
            │              │              │
     Can drop rows    Must handle     Question if
     if MCAR                          column is usable
            │              │              │
            ▼              ▼              ▼
     df.dropna()      Imputation    Consider dropping
                      strategies    or special handling
```

### Numeric Column Strategies

| Strategy | Code | When to Use | Caveats |
|----------|------|-------------|---------|
| **Drop rows** | `df.dropna(subset=['col'])` | <5% missing, MCAR | Loses data |
| **Mean** | `df['col'].fillna(df['col'].mean())` | Normal distribution | Sensitive to outliers |
| **Median** | `df['col'].fillna(df['col'].median())` | Skewed distribution | Robust default |
| **Zero** | `df['col'].fillna(0)` | Zero is meaningful | Often wrong choice |
| **Forward fill** | `df['col'].ffill()` | Time series | Requires sorted data |
| **Interpolation** | `df['col'].interpolate()` | Ordered, smooth | Assumes continuity |
| **Group mean** | See code below | Varies by segment | More accurate |

#### Group-Based Imputation

```python
# WHY: Missing values may differ by segment
# A customer's average differs from overall average

def impute_by_group(df, value_col, group_col, method='median'):
    """Impute missing values using group statistics."""
    if method == 'median':
        group_stats = df.groupby(group_col)[value_col].transform('median')
    else:
        group_stats = df.groupby(group_col)[value_col].transform('mean')

    return df[value_col].fillna(group_stats)

# Usage
df['income'] = impute_by_group(df, 'income', 'region', method='median')
```

### Categorical Column Strategies

| Strategy | Code | When to Use | Caveats |
|----------|------|-------------|---------|
| **Mode** | `df['col'].fillna(df['col'].mode()[0])` | Single dominant value | Inflates mode |
| **"Unknown"** | `df['col'].fillna('Unknown')` | Missing is informative | Adds category |
| **"Missing"** | `df['col'].fillna('Missing')` | Explicit tracking | Same as above |
| **Proportional** | See code below | Maintain distribution | Complex |

#### Proportional Fill

```python
# WHY: Preserve original category distribution
# Randomly assign based on existing frequencies

def fill_proportional(series):
    """Fill missing values proportionally to existing distribution."""
    non_null = series.dropna()
    distribution = non_null.value_counts(normalize=True)

    n_missing = series.isna().sum()
    fill_values = np.random.choice(
        distribution.index,
        size=n_missing,
        p=distribution.values
    )

    result = series.copy()
    result.loc[result.isna()] = fill_values
    return result
```

### Missingness Indicators

```python
# WHY: Sometimes the FACT that data is missing is informative
# Customer didn't provide income might indicate something

def add_missing_indicator(df, columns):
    """Create binary indicators for missing values."""
    for col in columns:
        df[f'{col}_was_missing'] = df[col].isna().astype(int)
    return df

# Usage: Add indicator BEFORE imputing
df = add_missing_indicator(df, ['income', 'age'])
df['income'] = df['income'].fillna(df['income'].median())
```

---

## Outlier Strategies

### Detection Methods

#### IQR Method (Recommended for Most Cases)

```python
def detect_outliers_iqr(series, multiplier=1.5):
    """
    Detect outliers using IQR method.

    WHY: IQR is robust to outliers themselves (unlike z-score which
    uses mean/std that are affected by outliers).
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outlier_mask': (series < lower_bound) | (series > upper_bound),
        'n_outliers': ((series < lower_bound) | (series > upper_bound)).sum()
    }
```

#### Z-Score Method

```python
from scipy.stats import zscore

def detect_outliers_zscore(series, threshold=3):
    """
    Detect outliers using Z-score.

    WHY: Good for normally distributed data.
    CAVEAT: The mean and std used are themselves affected by outliers.
    """
    z = zscore(series.dropna())
    return abs(z) > threshold
```

### Handling Strategies

| Strategy | When | Code |
|----------|------|------|
| **Keep** | Valid business data | Document, no action |
| **Remove** | Errors, irrelevant | `df = df[~outlier_mask]` |
| **Cap (Winsorize)** | Reduce influence | `series.clip(lower, upper)` |
| **Transform** | Compress scale | `np.log1p(series)` |
| **Flag** | Separate analysis | `df['is_outlier'] = outlier_mask` |

#### Winsorization (Capping)

```python
def winsorize_column(series, lower_percentile=0.01, upper_percentile=0.99):
    """
    Cap extreme values at percentile bounds.

    WHY: Keeps all data but limits influence of extremes.
    Useful when outliers are valid but would dominate analysis.
    """
    lower = series.quantile(lower_percentile)
    upper = series.quantile(upper_percentile)

    return series.clip(lower=lower, upper=upper)

# Usage
df['revenue_capped'] = winsorize_column(df['revenue'])
```

#### Log Transformation

```python
def log_transform(series, handle_zeros=True):
    """
    Apply log transformation to compress range.

    WHY: Useful for right-skewed data (income, prices, counts).
    Makes outliers less extreme while preserving order.
    """
    if handle_zeros:
        # log1p handles zeros: log(1 + x)
        return np.log1p(series)
    else:
        return np.log(series)

# IMPORTANT: Document that values are log-transformed
# Interpret coefficients accordingly in models
```

---

## Duplicate Strategies

### Exact Duplicates

```python
def handle_exact_duplicates(df, keep='first', log=True):
    """
    Handle exact duplicate rows.

    WHY: Exact duplicates are usually data errors or ETL artifacts.
    They bias counts and statistics.
    """
    n_duplicates = df.duplicated().sum()

    if log:
        print(f"Found {n_duplicates} exact duplicate rows ({n_duplicates/len(df)*100:.2f}%)")

    if n_duplicates > 0:
        df_clean = df.drop_duplicates(keep=keep)
        if log:
            print(f"Removed {len(df) - len(df_clean)} rows")
        return df_clean

    return df
```

### Key Duplicates

```python
def investigate_key_duplicates(df, key_columns, sort_by=None):
    """
    Investigate duplicates based on key columns.

    WHY: Same ID with different values needs investigation.
    Could be updates, errors, or valid multiple records.
    """
    duplicates = df[df.duplicated(subset=key_columns, keep=False)]

    if sort_by:
        duplicates = duplicates.sort_values(key_columns + [sort_by])

    print(f"Found {len(duplicates)} rows with duplicate keys")
    return duplicates


def deduplicate_keep_latest(df, key_columns, date_column):
    """
    Keep only the most recent record for each key.

    WHY: When duplicates represent updates, keep latest version.
    """
    df_sorted = df.sort_values(date_column, ascending=False)
    return df_sorted.drop_duplicates(subset=key_columns, keep='first')
```

---

## Data Type Conversion Strategies

### Safe Numeric Conversion

```python
def safe_to_numeric(series, fill_value=np.nan):
    """
    Convert to numeric, handling errors gracefully.

    WHY: Real data often has mixed types. This surfaces issues
    instead of silently failing.
    """
    # First attempt conversion
    numeric = pd.to_numeric(series, errors='coerce')

    # Check what couldn't be converted
    failed = series[numeric.isna() & series.notna()]
    if len(failed) > 0:
        print(f"Warning: {len(failed)} values couldn't be converted:")
        print(failed.value_counts().head())

    return numeric
```

### Safe Date Conversion

```python
def safe_to_datetime(series, format=None, errors='coerce'):
    """
    Convert to datetime with error handling.

    WHY: Dates come in many formats. This handles common cases
    and reports what couldn't be parsed.
    """
    parsed = pd.to_datetime(series, format=format, errors=errors)

    # Check what couldn't be converted
    failed = series[parsed.isna() & series.notna()]
    if len(failed) > 0:
        print(f"Warning: {len(failed)} values couldn't be parsed as dates:")
        print(failed.value_counts().head())

    return parsed
```

### Categorical Conversion

```python
def optimize_categories(df, max_cardinality=50):
    """
    Convert low-cardinality string columns to categorical.

    WHY: Categories use less memory and can speed up operations.
    Only convert if cardinality is reasonable.
    """
    for col in df.select_dtypes(include=['object']).columns:
        n_unique = df[col].nunique()
        if n_unique <= max_cardinality:
            df[col] = df[col].astype('category')
            print(f"Converted {col} to category ({n_unique} unique values)")

    return df
```

---

## Validation Strategies

### Domain Rule Validation

```python
def validate_domain_rules(df, rules):
    """
    Validate data against business rules.

    WHY: Business rules catch errors that statistical methods miss.
    Age can't be negative. End date can't precede start date.
    """
    violations = {}

    for rule_name, rule_func in rules.items():
        mask = ~rule_func(df)
        n_violations = mask.sum()
        if n_violations > 0:
            violations[rule_name] = {
                'count': n_violations,
                'percent': n_violations / len(df) * 100,
                'examples': df[mask].head()
            }

    return violations

# Usage
rules = {
    'age_positive': lambda df: df['age'] >= 0,
    'age_reasonable': lambda df: df['age'] <= 120,
    'end_after_start': lambda df: df['end_date'] >= df['start_date'],
    'price_positive': lambda df: df['price'] > 0,
}

violations = validate_domain_rules(df, rules)
```

### Cross-Field Validation

```python
def validate_cross_field(df, validations):
    """
    Validate relationships between columns.

    WHY: Some rules involve multiple columns.
    Total should equal sum of parts. Percentages should sum to 100.
    """
    results = {}

    for name, check_func in validations.items():
        failures = df[~check_func(df)]
        results[name] = {
            'passed': len(failures) == 0,
            'failures': len(failures),
            'examples': failures.head() if len(failures) > 0 else None
        }

    return results
```
