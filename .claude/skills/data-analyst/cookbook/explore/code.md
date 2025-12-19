# EDA Python Code Patterns

Production-ready code patterns for exploratory data analysis.

---

## Setup

```python
"""
EDA Script Template
==================
Run this script to perform comprehensive exploratory data analysis.

Usage:
    python eda.py data.csv
    python eda.py data.csv --output reports/eda_report.md
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import argparse

# Configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', '{:.2f}'.format)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
```

---

## Data Loading

```python
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data with automatic type inference and basic validation.

    WHY: Consistent loading ensures reproducible analysis.
    Automatic parsing catches common format issues early.
    """
    filepath = Path(filepath)

    if filepath.suffix == '.csv':
        df = pd.read_csv(filepath, parse_dates=True, infer_datetime_format=True)
    elif filepath.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    elif filepath.suffix == '.parquet':
        df = pd.read_parquet(filepath)
    elif filepath.suffix == '.json':
        df = pd.read_json(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    print(f"Loaded {len(df):,} rows × {len(df.columns)} columns from {filepath.name}")
    return df
```

---

## Overview Functions

```python
def data_overview(df: pd.DataFrame) -> dict:
    """
    Generate comprehensive data overview.

    WHY: First step in any EDA is understanding what you're working with.
    This function answers: How big? What types? What's the grain?
    """
    overview = {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / 1e6,
        'duplicates': df.duplicated().sum(),
        'complete_rows': len(df.dropna()),
        'complete_row_pct': len(df.dropna()) / len(df) * 100
    }

    # Type breakdown
    type_counts = df.dtypes.value_counts()
    overview['types'] = type_counts.to_dict()

    print(f"""
╔══════════════════════════════════════════════════╗
║                  DATA OVERVIEW                    ║
╠══════════════════════════════════════════════════╣
║ Rows:           {overview['rows']:>12,}                    ║
║ Columns:        {overview['columns']:>12}                    ║
║ Memory:         {overview['memory_mb']:>12.2f} MB               ║
║ Duplicates:     {overview['duplicates']:>12,}                    ║
║ Complete rows:  {overview['complete_row_pct']:>11.1f}%                    ║
╚══════════════════════════════════════════════════╝
    """)

    return overview


def column_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate per-column summary statistics.

    WHY: Each column has different characteristics. This function
    creates a unified view of all columns for comparison.
    """
    summary = []

    for col in df.columns:
        info = {
            'column': col,
            'dtype': str(df[col].dtype),
            'non_null': df[col].notna().sum(),
            'null': df[col].isna().sum(),
            'null_pct': df[col].isna().mean() * 100,
            'unique': df[col].nunique(),
            'unique_pct': df[col].nunique() / len(df) * 100,
        }

        # Add numeric stats
        if pd.api.types.is_numeric_dtype(df[col]):
            info['mean'] = df[col].mean()
            info['std'] = df[col].std()
            info['min'] = df[col].min()
            info['max'] = df[col].max()

        # Add categorical stats
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
            mode = df[col].mode()
            info['mode'] = mode.iloc[0] if not mode.empty else None
            info['mode_freq'] = (df[col] == info['mode']).mean() * 100 if info['mode'] else 0

        summary.append(info)

    return pd.DataFrame(summary)
```

---

## Missing Value Analysis

```python
def analyze_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing value patterns.

    WHY: Missing data is rarely random. Understanding WHAT is missing
    and WHERE helps determine appropriate handling strategies.
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    missing_df = pd.DataFrame({
        'column': missing.index,
        'missing_count': missing.values,
        'missing_pct': missing_pct.values,
        'dtype': df.dtypes.values
    })

    missing_df = missing_df[missing_df['missing_count'] > 0].sort_values(
        'missing_pct', ascending=False
    )

    if len(missing_df) == 0:
        print("No missing values found.")
    else:
        print(f"\n{'='*50}")
        print("MISSING VALUE ANALYSIS")
        print(f"{'='*50}")
        print(f"Columns with missing: {len(missing_df)}/{len(df.columns)}")
        print(f"Total missing cells: {df.isnull().sum().sum():,}")
        print(f"\nTop missing columns:")
        print(missing_df.head(10).to_string(index=False))

    return missing_df


def missing_correlation(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Find correlations in missingness patterns.

    WHY: If missing values in column A correlate with missing in column B,
    they likely have a common cause (systematic, not random).
    """
    missing_matrix = df.isnull().astype(int)

    # Only analyze columns with some missing
    cols_with_missing = missing_matrix.columns[missing_matrix.sum() > 0]
    if len(cols_with_missing) < 2:
        return pd.DataFrame()

    corr = missing_matrix[cols_with_missing].corr()

    # Find pairs above threshold
    pairs = []
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            if abs(corr.iloc[i, j]) >= threshold:
                pairs.append({
                    'col1': corr.columns[i],
                    'col2': corr.columns[j],
                    'correlation': corr.iloc[i, j]
                })

    return pd.DataFrame(pairs).sort_values('correlation', ascending=False)
```

---

## Distribution Analysis

```python
def analyze_numeric(df: pd.DataFrame, col: str) -> dict:
    """
    Comprehensive analysis of a numeric column.

    WHY: Numeric distributions reveal outliers, skewness, and patterns
    that affect every downstream decision (cleaning, modeling, reporting).
    """
    series = df[col].dropna()

    stats = {
        'column': col,
        'count': len(series),
        'mean': series.mean(),
        'std': series.std(),
        'min': series.min(),
        'q25': series.quantile(0.25),
        'median': series.median(),
        'q75': series.quantile(0.75),
        'max': series.max(),
        'iqr': series.quantile(0.75) - series.quantile(0.25),
        'skewness': series.skew(),
        'kurtosis': series.kurtosis(),
        'zeros': (series == 0).sum(),
        'negatives': (series < 0).sum(),
    }

    # Outlier detection (IQR method)
    Q1, Q3 = stats['q25'], stats['q75']
    IQR = stats['iqr']
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = series[(series < lower_bound) | (series > upper_bound)]

    stats['outliers_count'] = len(outliers)
    stats['outliers_pct'] = len(outliers) / len(series) * 100
    stats['lower_bound'] = lower_bound
    stats['upper_bound'] = upper_bound

    return stats


def analyze_categorical(df: pd.DataFrame, col: str, top_n: int = 10) -> dict:
    """
    Comprehensive analysis of a categorical column.

    WHY: Categorical columns need special attention for cardinality,
    imbalance, and consistency issues (typos, casing).
    """
    series = df[col].dropna()
    value_counts = series.value_counts()

    stats = {
        'column': col,
        'count': len(series),
        'unique': series.nunique(),
        'cardinality_ratio': series.nunique() / len(series),
        'mode': value_counts.index[0] if len(value_counts) > 0 else None,
        'mode_count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
        'mode_pct': value_counts.iloc[0] / len(series) * 100 if len(value_counts) > 0 else 0,
        'top_values': value_counts.head(top_n).to_dict(),
    }

    # Check for potential issues
    if series.dtype == 'object':
        # Whitespace issues
        has_leading_space = series.str.startswith(' ', na=False).any()
        has_trailing_space = series.str.endswith(' ', na=False).any()
        stats['whitespace_issues'] = has_leading_space or has_trailing_space

        # Case inconsistency (might indicate same values with different casing)
        lower_unique = series.str.lower().nunique()
        stats['case_inconsistency'] = lower_unique < series.nunique()

    return stats
```

---

## Correlation Analysis

```python
def correlation_analysis(df: pd.DataFrame, threshold: float = 0.7) -> dict:
    """
    Analyze correlations between numeric columns.

    WHY: High correlations indicate redundancy (drop one) or
    potential multicollinearity issues for modeling.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) < 2:
        return {'message': 'Need at least 2 numeric columns for correlation'}

    corr_matrix = df[numeric_cols].corr()

    # Find highly correlated pairs
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                high_corr_pairs.append({
                    'col1': corr_matrix.columns[i],
                    'col2': corr_matrix.columns[j],
                    'correlation': round(corr_val, 3)
                })

    return {
        'correlation_matrix': corr_matrix,
        'high_correlations': pd.DataFrame(high_corr_pairs).sort_values(
            'correlation', key=abs, ascending=False
        ) if high_corr_pairs else pd.DataFrame()
    }
```

---

## Visualization Functions

```python
def plot_distributions(df: pd.DataFrame, output_dir: str = 'plots'):
    """
    Generate distribution plots for all numeric columns.

    WHY: Visual inspection catches patterns that statistics miss
    (bimodality, clustering, discrete spikes).
    """
    Path(output_dir).mkdir(exist_ok=True)
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Histogram
        df[col].hist(ax=axes[0], bins=50, edgecolor='black', alpha=0.7)
        axes[0].set_title(f'{col} - Distribution')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')

        # Box plot
        df.boxplot(column=col, ax=axes[1])
        axes[1].set_title(f'{col} - Box Plot')

        plt.tight_layout()
        plt.savefig(f'{output_dir}/{col}_distribution.png', dpi=100)
        plt.close()

    print(f"Saved {len(numeric_cols)} distribution plots to {output_dir}/")


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str = 'plots/correlation_heatmap.png'):
    """
    Generate correlation heatmap.

    WHY: Heatmaps reveal patterns in correlation structure
    that tables cannot show (clusters of related variables).
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) < 2:
        print("Not enough numeric columns for correlation heatmap")
        return

    corr = df[numeric_cols].corr()

    plt.figure(figsize=(max(10, len(numeric_cols)), max(8, len(numeric_cols) * 0.8)))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', square=True, linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.tight_layout()

    Path(output_path).parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=100)
    plt.close()

    print(f"Saved correlation heatmap to {output_path}")
```

---

## Main EDA Pipeline

```python
def run_eda(filepath: str, output_dir: str = 'eda_output') -> dict:
    """
    Run complete EDA pipeline.

    WHY: A standardized pipeline ensures nothing is missed
    and results are reproducible.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print("="*60)
    print("EXPLORATORY DATA ANALYSIS")
    print("="*60)

    # Load data
    df = load_data(filepath)

    # Overview
    overview = data_overview(df)

    # Column summary
    col_summary = column_summary(df)
    col_summary.to_csv(output_path / 'column_summary.csv', index=False)

    # Missing analysis
    missing = analyze_missing(df)
    if len(missing) > 0:
        missing.to_csv(output_path / 'missing_analysis.csv', index=False)

    # Numeric analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_stats = [analyze_numeric(df, col) for col in numeric_cols]
    pd.DataFrame(numeric_stats).to_csv(output_path / 'numeric_analysis.csv', index=False)

    # Categorical analysis
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    cat_stats = [analyze_categorical(df, col) for col in cat_cols]

    # Correlation analysis
    corr_results = correlation_analysis(df)
    if 'correlation_matrix' in corr_results:
        corr_results['correlation_matrix'].to_csv(output_path / 'correlation_matrix.csv')

    # Generate plots
    plot_distributions(df, output_dir=str(output_path / 'plots'))
    plot_correlation_heatmap(df, output_path=str(output_path / 'plots' / 'correlation_heatmap.png'))

    print(f"\nEDA complete. Results saved to {output_path}/")

    return {
        'overview': overview,
        'column_summary': col_summary,
        'missing': missing,
        'numeric_stats': numeric_stats,
        'categorical_stats': cat_stats,
        'correlations': corr_results
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run EDA on a dataset')
    parser.add_argument('filepath', help='Path to data file')
    parser.add_argument('--output', default='eda_output', help='Output directory')
    args = parser.parse_args()

    run_eda(args.filepath, args.output)
```
