# EDA Statistical Techniques

Reference guide for statistical techniques used in exploratory data analysis.

---

## Descriptive Statistics

### Central Tendency

| Measure | When to Use | Sensitive To | Code |
|---------|-------------|--------------|------|
| **Mean** | Symmetric distributions | Outliers | `df['col'].mean()` |
| **Median** | Skewed distributions | Nothing (robust) | `df['col'].median()` |
| **Mode** | Categorical data | Ties | `df['col'].mode()` |

**Rule of thumb**: If mean ≠ median, your distribution is skewed. Report median.

### Spread

| Measure | When to Use | Interpretation | Code |
|---------|-------------|----------------|------|
| **Std Dev** | Normal distributions | 68% within 1σ | `df['col'].std()` |
| **Variance** | Statistical modeling | σ² | `df['col'].var()` |
| **IQR** | Skewed data | Middle 50% | `df['col'].quantile(.75) - df['col'].quantile(.25)` |
| **Range** | Quick overview | Max - Min | `df['col'].max() - df['col'].min()` |

### Shape

| Measure | What It Tells You | Interpretation |
|---------|-------------------|----------------|
| **Skewness** | Asymmetry | \>0 = right tail, <0 = left tail |
| **Kurtosis** | Tail heaviness | \>3 = heavy tails (leptokurtic), <3 = light tails |

```python
from scipy.stats import skew, kurtosis
skew(df['col'].dropna())
kurtosis(df['col'].dropna())
```

---

## Distribution Analysis

### Visual Assessment

| Distribution Shape | Characteristics | Common In |
|--------------------|-----------------|-----------|
| **Normal** | Symmetric, bell-shaped | Measurement errors, heights |
| **Right-skewed** | Long right tail | Income, prices, counts |
| **Left-skewed** | Long left tail | Age at death, test scores with ceiling |
| **Bimodal** | Two peaks | Mixed populations |
| **Uniform** | Flat | Random IDs, synthetic data |

### Normality Testing

```python
from scipy.stats import shapiro, normaltest

# Shapiro-Wilk (n < 5000)
stat, p = shapiro(df['col'].dropna())
print(f"Shapiro-Wilk: p={p:.4f}")

# D'Agostino-Pearson (larger samples)
stat, p = normaltest(df['col'].dropna())
print(f"D'Agostino: p={p:.4f}")

# Interpretation: p < 0.05 → reject normality
```

**Practical note**: For large samples, normality tests often reject even minor deviations. Visual inspection (Q-Q plot, histogram) is more useful.

---

## Correlation Analysis

### Types of Correlation

| Method | Data Types | Assumes | Range | Code |
|--------|-----------|---------|-------|------|
| **Pearson** | Continuous | Linear relationship | -1 to 1 | `df.corr(method='pearson')` |
| **Spearman** | Ordinal/Continuous | Monotonic relationship | -1 to 1 | `df.corr(method='spearman')` |
| **Kendall** | Ordinal | Monotonic, small samples | -1 to 1 | `df.corr(method='kendall')` |

### Interpretation Guide

| Value | Strength |
|-------|----------|
| 0.0 - 0.2 | Negligible |
| 0.2 - 0.4 | Weak |
| 0.4 - 0.6 | Moderate |
| 0.6 - 0.8 | Strong |
| 0.8 - 1.0 | Very strong |

### Correlation Caveats

**Correlation ≠ Causation**: Ice cream sales correlate with drowning deaths. Both are caused by summer.

**Outliers distort Pearson**: One extreme point can create or destroy correlation.

**Non-linear relationships invisible**: Pearson misses U-shapes, curves, thresholds.

```python
# Always visualize to validate correlation
import seaborn as sns
sns.scatterplot(data=df, x='col1', y='col2')
```

---

## Outlier Detection

### Methods

| Method | Formula | Use When | Code |
|--------|---------|----------|------|
| **IQR** | Outside Q1-1.5×IQR to Q3+1.5×IQR | Skewed data | See below |
| **Z-score** | \|z\| > 3 | Normal distribution | See below |
| **Modified Z** | \|MAD-z\| > 3.5 | Robust to outliers | See below |
| **Domain rules** | Business logic | Known constraints | Manual |

### IQR Method

```python
def outliers_iqr(series, multiplier=1.5):
    """Detect outliers using IQR method."""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return (series < lower) | (series > upper)

# Usage
outlier_mask = outliers_iqr(df['revenue'])
print(f"Outliers: {outlier_mask.sum()} ({outlier_mask.mean()*100:.1f}%)")
```

### Z-Score Method

```python
from scipy.stats import zscore

def outliers_zscore(series, threshold=3):
    """Detect outliers using Z-score."""
    z = zscore(series.dropna())
    return abs(z) > threshold

# Usage (only for roughly normal data)
outlier_mask = outliers_zscore(df['revenue'])
```

### Modified Z-Score (Robust)

```python
from scipy.stats import median_abs_deviation

def outliers_modified_z(series, threshold=3.5):
    """Detect outliers using modified Z-score (MAD-based)."""
    median = series.median()
    mad = median_abs_deviation(series.dropna())
    modified_z = 0.6745 * (series - median) / mad
    return abs(modified_z) > threshold
```

---

## Missing Data Analysis

### Missingness Patterns

| Type | Definition | Test | Handling |
|------|------------|------|----------|
| **MCAR** | Missing Completely At Random | Little's test | Safe to drop or impute |
| **MAR** | Missing At Random (depends on observed) | Compare groups | Impute with care |
| **MNAR** | Missing Not At Random (depends on unobserved) | Domain knowledge | Problematic—model it |

### Missingness Profile

```python
def missing_profile(df):
    """Generate missing data profile."""
    missing = df.isnull().sum()
    percent = (missing / len(df) * 100).round(2)

    profile = pd.DataFrame({
        'missing': missing,
        'percent': percent,
        'dtype': df.dtypes
    })

    return profile[profile['missing'] > 0].sort_values('percent', ascending=False)

# Visualize missingness pattern
import missingno as msno
msno.matrix(df)
```

### Missing Correlation

```python
# Check if missingness in one column predicts missingness in another
missing_df = df.isnull().astype(int)
missing_corr = missing_df.corr()
# High correlation suggests systematic missingness
```

---

## Cardinality Analysis

### For Categorical Variables

| Metric | Interpretation |
|--------|----------------|
| **Unique count** | Number of distinct values |
| **Cardinality ratio** | unique / total rows |
| **Mode frequency** | How dominant is the most common value? |

```python
def cardinality_profile(series):
    """Profile cardinality of a categorical variable."""
    return {
        'unique': series.nunique(),
        'cardinality_ratio': series.nunique() / len(series),
        'mode': series.mode()[0] if not series.mode().empty else None,
        'mode_freq': series.value_counts().iloc[0] / len(series) if len(series) > 0 else 0,
        'top_5': series.value_counts().head(5).to_dict()
    }
```

### High Cardinality Flags

- **Cardinality = row count**: Likely an ID column (not useful for analysis)
- **Cardinality = 1**: Constant column (drop it)
- **Very high cardinality categorical**: May need binning or encoding strategy

---

## Quick Reference: pandas Methods

```python
# Overview
df.shape                    # (rows, columns)
df.dtypes                   # Data types
df.info()                   # Memory, non-null counts
df.describe()               # Statistics for numeric
df.describe(include='all')  # Include categorical

# Missing
df.isnull().sum()           # Missing per column
df.isnull().sum().sum()     # Total missing
df.dropna().shape[0]        # Complete rows

# Unique values
df['col'].nunique()         # Unique count
df['col'].value_counts()    # Frequency table
df['col'].unique()          # Array of unique values

# Distribution
df['col'].hist()            # Histogram
df['col'].quantile([.25, .5, .75])  # Quartiles
df.boxplot()                # Box plots

# Correlation
df.corr()                   # Correlation matrix
df['col1'].corr(df['col2']) # Pairwise correlation
```
