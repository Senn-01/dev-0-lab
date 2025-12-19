# Data Cleaning Python Code Patterns

Production-ready code for the data cleaning pipeline.

---

## Setup

```python
"""
Data Cleaning Script Template
=============================
Run this script to clean a dataset through the standard pipeline.

Usage:
    python clean.py input.csv --output cleaned.csv
    python clean.py input.csv --output cleaned.csv --log cleaning_log.md
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import argparse
import json

# Configuration
pd.set_option('display.max_columns', None)
```

---

## Logging & Documentation

```python
class CleaningLog:
    """
    Track all cleaning operations with before/after counts.

    WHY: Every cleaning decision should be documented and reproducible.
    This log is your audit trail.
    """

    def __init__(self, initial_df):
        self.initial_rows = len(initial_df)
        self.initial_cols = len(initial_df.columns)
        self.operations = []
        self.current_rows = len(initial_df)
        self.current_cols = len(initial_df.columns)

    def log(self, operation: str, description: str, rows_before: int,
            rows_after: int, cols_before: int = None, cols_after: int = None):
        """Log a cleaning operation."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'description': description,
            'rows_before': rows_before,
            'rows_after': rows_after,
            'rows_removed': rows_before - rows_after,
            'pct_removed': (rows_before - rows_after) / rows_before * 100 if rows_before > 0 else 0
        }

        if cols_before is not None:
            entry['cols_before'] = cols_before
            entry['cols_after'] = cols_after

        self.operations.append(entry)
        self.current_rows = rows_after
        if cols_after is not None:
            self.current_cols = cols_after

        print(f"[{operation}] {description}")
        print(f"  Rows: {rows_before:,} → {rows_after:,} ({entry['rows_removed']:,} removed, {entry['pct_removed']:.2f}%)")

    def to_markdown(self) -> str:
        """Export log as markdown report."""
        md = f"""# Data Cleaning Log

## Summary
- Initial: {self.initial_rows:,} rows × {self.initial_cols} columns
- Final: {self.current_rows:,} rows × {self.current_cols} columns
- Total rows removed: {self.initial_rows - self.current_rows:,} ({(self.initial_rows - self.current_rows) / self.initial_rows * 100:.2f}%)

## Operations

| Step | Operation | Description | Rows Before | Rows After | Removed | % |
|------|-----------|-------------|-------------|------------|---------|---|
"""
        for i, op in enumerate(self.operations, 1):
            md += f"| {i} | {op['operation']} | {op['description']} | {op['rows_before']:,} | {op['rows_after']:,} | {op['rows_removed']:,} | {op['pct_removed']:.2f}% |\n"

        return md
```

---

## Step 1: Structure

```python
def clean_structure(df: pd.DataFrame, log: CleaningLog) -> pd.DataFrame:
    """
    Step 1: Clean data structure.

    WHY: Clean column names prevent bugs. Empty columns waste space.
    This is the foundation for all subsequent operations.
    """
    rows_before = len(df)
    cols_before = len(df.columns)

    # Clean column names
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(r'[^a-z0-9_]', '_', regex=True)
        .str.replace(r'_+', '_', regex=True)
        .str.strip('_')
    )

    # Remove columns that are entirely null
    null_cols = df.columns[df.isnull().all()].tolist()
    if null_cols:
        df = df.drop(columns=null_cols)
        print(f"  Dropped entirely null columns: {null_cols}")

    # Remove constant columns (single value)
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        df = df.drop(columns=constant_cols)
        print(f"  Dropped constant columns: {constant_cols}")

    log.log(
        'STRUCTURE',
        f'Cleaned column names, dropped {len(null_cols)} null cols, {len(constant_cols)} constant cols',
        rows_before, len(df), cols_before, len(df.columns)
    )

    return df
```

---

## Step 2: Data Types

```python
def clean_types(df: pd.DataFrame, log: CleaningLog,
                numeric_cols: list = None,
                date_cols: list = None,
                category_cols: list = None) -> pd.DataFrame:
    """
    Step 2: Convert columns to correct types.

    WHY: Correct types enable proper operations (math on numbers,
    sorting on dates) and surface hidden data quality issues.
    """
    rows_before = len(df)
    conversions = []

    # Auto-detect numeric columns if not specified
    if numeric_cols is None:
        numeric_cols = []
        for col in df.select_dtypes(include=['object']).columns:
            # Try to convert
            numeric = pd.to_numeric(df[col], errors='coerce')
            # If >80% converted successfully, it's probably numeric
            if numeric.notna().mean() > 0.8:
                numeric_cols.append(col)

    # Convert numeric columns
    for col in numeric_cols:
        if col in df.columns:
            before_type = df[col].dtype
            df[col] = pd.to_numeric(df[col], errors='coerce')
            conversions.append(f"{col}: {before_type} → numeric")

    # Convert date columns
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                before_type = df[col].dtype
                df[col] = pd.to_datetime(df[col], errors='coerce')
                conversions.append(f"{col}: {before_type} → datetime")

    # Convert categorical columns
    if category_cols:
        for col in category_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')
                conversions.append(f"{col} → category")

    # Auto-convert low-cardinality strings to category
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() < 50:
            df[col] = df[col].astype('category')

    log.log(
        'TYPES',
        f'Converted {len(conversions)} columns',
        rows_before, len(df)
    )

    if conversions:
        print(f"  Conversions: {', '.join(conversions[:5])}" +
              (f" + {len(conversions) - 5} more" if len(conversions) > 5 else ""))

    return df
```

---

## Step 3: Duplicates

```python
def clean_duplicates(df: pd.DataFrame, log: CleaningLog,
                     key_cols: list = None,
                     keep: str = 'first') -> pd.DataFrame:
    """
    Step 3: Remove duplicate records.

    WHY: Duplicates bias statistics and inflate counts.
    They're usually ETL artifacts or data entry errors.
    """
    rows_before = len(df)

    # Remove exact duplicates
    exact_dupes = df.duplicated().sum()
    df = df.drop_duplicates(keep=keep)

    # Handle key duplicates if specified
    key_dupes = 0
    if key_cols:
        key_dupes = df.duplicated(subset=key_cols).sum()
        df = df.drop_duplicates(subset=key_cols, keep=keep)

    log.log(
        'DUPLICATES',
        f'Removed {exact_dupes} exact dupes' + (f', {key_dupes} key dupes' if key_dupes else ''),
        rows_before, len(df)
    )

    return df
```

---

## Step 4: Invalid Values

```python
def clean_invalid(df: pd.DataFrame, log: CleaningLog,
                  rules: dict = None) -> pd.DataFrame:
    """
    Step 4: Handle invalid values based on business rules.

    WHY: Invalid values are ERRORS, not outliers. They must be
    corrected or removed before any analysis.
    """
    rows_before = len(df)
    fixes = []

    # Default rules if none provided
    if rules is None:
        rules = {}

    # Apply each rule
    for col, rule in rules.items():
        if col not in df.columns:
            continue

        if rule['type'] == 'range':
            # Values outside range → NaN
            mask = (df[col] < rule['min']) | (df[col] > rule['max'])
            n_invalid = mask.sum()
            if n_invalid > 0:
                df.loc[mask, col] = np.nan
                fixes.append(f"{col}: {n_invalid} out-of-range → NaN")

        elif rule['type'] == 'values':
            # Values not in allowed set → NaN
            mask = ~df[col].isin(rule['allowed'])
            n_invalid = mask.sum()
            if n_invalid > 0:
                df.loc[mask, col] = np.nan
                fixes.append(f"{col}: {n_invalid} invalid → NaN")

        elif rule['type'] == 'replace':
            # Replace specific values
            for old_val, new_val in rule['mapping'].items():
                mask = df[col] == old_val
                n_replaced = mask.sum()
                if n_replaced > 0:
                    df.loc[mask, col] = new_val
                    fixes.append(f"{col}: {n_replaced} '{old_val}' → '{new_val}'")

    # Common placeholder values → NaN
    placeholder_values = [-999, 9999, -1, '', 'NA', 'N/A', 'NULL', 'null', 'None', 'none']
    for col in df.columns:
        mask = df[col].isin(placeholder_values)
        n_placeholders = mask.sum()
        if n_placeholders > 0:
            df.loc[mask, col] = np.nan
            fixes.append(f"{col}: {n_placeholders} placeholders → NaN")

    log.log(
        'INVALID',
        f'Fixed {len(fixes)} value issues',
        rows_before, len(df)
    )

    if fixes:
        print(f"  Fixes: {'; '.join(fixes[:3])}" +
              (f" + {len(fixes) - 3} more" if len(fixes) > 3 else ""))

    return df
```

---

## Step 5: Missing Values

```python
def clean_missing(df: pd.DataFrame, log: CleaningLog,
                  strategies: dict = None,
                  drop_threshold: float = 0.5) -> pd.DataFrame:
    """
    Step 5: Handle missing values.

    WHY: Missing values break many operations. Strategy depends on
    how much is missing and why.
    """
    rows_before = len(df)
    actions = []

    # Drop columns with too much missing
    missing_pct = df.isnull().mean()
    high_missing_cols = missing_pct[missing_pct > drop_threshold].index.tolist()
    if high_missing_cols:
        df = df.drop(columns=high_missing_cols)
        actions.append(f"Dropped {len(high_missing_cols)} cols with >{drop_threshold*100}% missing")

    # Apply column-specific strategies
    if strategies is None:
        strategies = {}

    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue

        strategy = strategies.get(col, 'default')

        if strategy == 'drop':
            df = df.dropna(subset=[col])
            actions.append(f"{col}: dropped rows")

        elif strategy == 'mean':
            df[col] = df[col].fillna(df[col].mean())
            actions.append(f"{col}: mean imputation")

        elif strategy == 'median':
            df[col] = df[col].fillna(df[col].median())
            actions.append(f"{col}: median imputation")

        elif strategy == 'mode':
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val.iloc[0])
            actions.append(f"{col}: mode imputation")

        elif strategy == 'ffill':
            df[col] = df[col].ffill()
            actions.append(f"{col}: forward fill")

        elif strategy == 'zero':
            df[col] = df[col].fillna(0)
            actions.append(f"{col}: zero fill")

        elif strategy == 'unknown':
            df[col] = df[col].fillna('Unknown')
            actions.append(f"{col}: 'Unknown' fill")

        elif strategy == 'default':
            # Default: median for numeric, mode for categorical
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
                actions.append(f"{col}: median (default)")
            else:
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val.iloc[0])
                actions.append(f"{col}: mode (default)")

    log.log(
        'MISSING',
        f'{len(actions)} imputation actions',
        rows_before, len(df)
    )

    return df
```

---

## Step 6: Outliers

```python
def clean_outliers(df: pd.DataFrame, log: CleaningLog,
                   numeric_cols: list = None,
                   method: str = 'cap',
                   multiplier: float = 1.5) -> pd.DataFrame:
    """
    Step 6: Handle outliers in numeric columns.

    WHY: Outliers can dominate statistics and models. But they may
    also be the most important data points. Handle with care.
    """
    rows_before = len(df)
    actions = []

    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR

        outliers = ((df[col] < lower) | (df[col] > upper)).sum()

        if outliers > 0:
            if method == 'cap':
                # Winsorize: cap at bounds
                df[col] = df[col].clip(lower=lower, upper=upper)
                actions.append(f"{col}: capped {outliers} outliers")

            elif method == 'remove':
                # Remove outlier rows
                df = df[(df[col] >= lower) & (df[col] <= upper)]
                actions.append(f"{col}: removed {outliers} outliers")

            elif method == 'flag':
                # Add indicator column
                df[f'{col}_outlier'] = ((df[col] < lower) | (df[col] > upper)).astype(int)
                actions.append(f"{col}: flagged {outliers} outliers")

    log.log(
        'OUTLIERS',
        f'{len(actions)} columns processed ({method} method)',
        rows_before, len(df)
    )

    return df
```

---

## Step 7: Transform

```python
def clean_transform(df: pd.DataFrame, log: CleaningLog,
                    transforms: dict = None) -> pd.DataFrame:
    """
    Step 7: Apply final transformations for analysis.

    WHY: Some analyses require specific data formats (scaled features,
    encoded categories). This step prepares for the use case.
    """
    rows_before = len(df)
    actions = []

    if transforms is None:
        transforms = {}

    for col, transform in transforms.items():
        if col not in df.columns:
            continue

        if transform == 'log':
            df[f'{col}_log'] = np.log1p(df[col])
            actions.append(f"{col}: log transform")

        elif transform == 'sqrt':
            df[f'{col}_sqrt'] = np.sqrt(df[col].clip(lower=0))
            actions.append(f"{col}: sqrt transform")

        elif transform == 'zscore':
            mean = df[col].mean()
            std = df[col].std()
            df[f'{col}_zscore'] = (df[col] - mean) / std
            actions.append(f"{col}: z-score")

        elif transform == 'minmax':
            min_val = df[col].min()
            max_val = df[col].max()
            df[f'{col}_scaled'] = (df[col] - min_val) / (max_val - min_val)
            actions.append(f"{col}: min-max scaled")

    log.log(
        'TRANSFORM',
        f'{len(actions)} transformations applied',
        rows_before, len(df)
    )

    return df
```

---

## Main Pipeline

```python
def run_cleaning_pipeline(filepath: str, output_path: str = None,
                          config: dict = None) -> pd.DataFrame:
    """
    Run the complete cleaning pipeline.

    WHY: A standardized pipeline ensures consistent, reproducible cleaning
    across all datasets.
    """
    print("="*60)
    print("DATA CLEANING PIPELINE")
    print("="*60 + "\n")

    # Load data
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df):,} rows × {len(df.columns)} columns from {filepath}\n")

    # Initialize log
    log = CleaningLog(df)

    # Configuration
    config = config or {}

    # Execute pipeline
    df = clean_structure(df, log)
    df = clean_types(df, log,
                     numeric_cols=config.get('numeric_cols'),
                     date_cols=config.get('date_cols'),
                     category_cols=config.get('category_cols'))
    df = clean_duplicates(df, log,
                          key_cols=config.get('key_cols'))
    df = clean_invalid(df, log,
                       rules=config.get('validation_rules'))
    df = clean_missing(df, log,
                       strategies=config.get('missing_strategies'))
    df = clean_outliers(df, log,
                        method=config.get('outlier_method', 'cap'))
    df = clean_transform(df, log,
                         transforms=config.get('transforms'))

    # Summary
    print("\n" + "="*60)
    print("CLEANING COMPLETE")
    print("="*60)
    print(f"Final: {len(df):,} rows × {len(df.columns)} columns")
    print(f"Rows retained: {len(df)/log.initial_rows*100:.1f}%")

    # Save outputs
    if output_path:
        df.to_csv(output_path, index=False)
        print(f"\nSaved cleaned data to {output_path}")

        # Save log
        log_path = Path(output_path).with_suffix('.cleaning_log.md')
        with open(log_path, 'w') as f:
            f.write(log.to_markdown())
        print(f"Saved cleaning log to {log_path}")

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean a dataset')
    parser.add_argument('filepath', help='Path to input data file')
    parser.add_argument('--output', default=None, help='Path to save cleaned data')
    parser.add_argument('--config', default=None, help='Path to config JSON file')
    args = parser.parse_args()

    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    run_cleaning_pipeline(args.filepath, args.output, config)
```
