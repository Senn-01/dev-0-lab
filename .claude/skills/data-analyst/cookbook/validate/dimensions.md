# Data Quality Dimensions

The standard dimensions for measuring data quality.

---

## The Six Core Dimensions

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA QUALITY DIMENSIONS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ COMPLETENESS │  │   ACCURACY   │  │ CONSISTENCY  │          │
│  │              │  │              │  │              │          │
│  │  "Is it      │  │  "Is it      │  │  "Does it    │          │
│  │   all here?" │  │   correct?"  │  │   match?"    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  UNIQUENESS  │  │  TIMELINESS  │  │  CONFORMITY  │          │
│  │              │  │              │  │              │          │
│  │  "Is it      │  │  "Is it      │  │  "Does it    │          │
│  │   distinct?" │  │   current?"  │  │   fit?"      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Completeness

**Definition**: The degree to which all required data is present.

### Why It Matters

Missing data creates:
- Biased statistics (non-random missingness)
- Failed operations (null pointer errors)
- Incomplete analysis (missing segments)

### What to Measure

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Record completeness** | Complete rows / Total rows | % of records with all fields |
| **Column completeness** | Non-null / Total values | % filled per column |
| **Critical field completeness** | Non-null in key columns | Must be 100% |

### How to Check

```python
def completeness_check(df, critical_cols=None):
    """Check completeness dimension."""
    results = {
        'record_completeness': len(df.dropna()) / len(df) * 100,
        'column_completeness': {},
        'critical_completeness': {}
    }

    for col in df.columns:
        results['column_completeness'][col] = df[col].notna().mean() * 100

    if critical_cols:
        for col in critical_cols:
            results['critical_completeness'][col] = df[col].notna().mean() * 100

    return results
```

---

## 2. Accuracy

**Definition**: The degree to which data correctly represents the real-world entity.

### Why It Matters

Inaccurate data leads to:
- Wrong conclusions
- Invalid models
- Mistaken decisions

### What to Measure

| Metric | Method | Example |
|--------|--------|---------|
| **Range validity** | Value in expected range | Age ∈ [0, 120] |
| **Format validity** | Matches expected pattern | Email has @ |
| **Cross-field validity** | Logical rules hold | End > Start |
| **Reference validity** | Exists in reference data | Country in country list |

### How to Check

```python
def accuracy_check(df, rules):
    """
    Check accuracy dimension against business rules.

    rules = {
        'age': {'type': 'range', 'min': 0, 'max': 120},
        'email': {'type': 'regex', 'pattern': r'^[\w.-]+@[\w.-]+\.\w+$'},
        'country': {'type': 'values', 'allowed': ['US', 'UK', 'CA', ...]},
    }
    """
    results = {}

    for col, rule in rules.items():
        if col not in df.columns:
            continue

        if rule['type'] == 'range':
            valid = (df[col] >= rule['min']) & (df[col] <= rule['max'])
        elif rule['type'] == 'regex':
            valid = df[col].str.match(rule['pattern'], na=False)
        elif rule['type'] == 'values':
            valid = df[col].isin(rule['allowed'])

        results[col] = {
            'valid_count': valid.sum(),
            'valid_pct': valid.mean() * 100,
            'invalid_count': (~valid).sum()
        }

    return results
```

---

## 3. Consistency

**Definition**: The degree to which data is uniform and coherent across the dataset.

### Why It Matters

Inconsistent data causes:
- Failed joins
- Incorrect aggregations
- Confusing reports

### What to Measure

| Metric | Check | Example |
|--------|-------|---------|
| **Format consistency** | Same format throughout | All dates YYYY-MM-DD |
| **Value consistency** | Same codes/values | "Yes" not "Y", "yes", "1" |
| **Cross-field consistency** | Related values agree | State matches ZIP |
| **Cross-table consistency** | Tables agree | Same totals across reports |

### How to Check

```python
def consistency_check(df, consistency_rules):
    """
    Check consistency dimension.

    consistency_rules = {
        'total_check': lambda df: df['qty'] * df['price'] == df['total'],
        'date_order': lambda df: df['end_date'] >= df['start_date'],
    }
    """
    results = {}

    for name, rule_func in consistency_rules.items():
        try:
            consistent = rule_func(df)
            results[name] = {
                'consistent_count': consistent.sum(),
                'consistent_pct': consistent.mean() * 100,
                'inconsistent_count': (~consistent).sum()
            }
        except Exception as e:
            results[name] = {'error': str(e)}

    return results
```

---

## 4. Uniqueness

**Definition**: The degree to which there is no redundant data.

### Why It Matters

Duplicate data causes:
- Inflated counts
- Biased statistics
- Double-processing

### What to Measure

| Metric | Formula | Expected |
|--------|---------|----------|
| **Row uniqueness** | Unique rows / Total rows | 100% (usually) |
| **Key uniqueness** | Unique keys / Total rows | 100% (required) |
| **Near-duplicate rate** | Fuzzy matches / Total | Low |

### How to Check

```python
def uniqueness_check(df, key_cols=None):
    """Check uniqueness dimension."""
    results = {
        'exact_duplicate_count': df.duplicated().sum(),
        'exact_duplicate_pct': df.duplicated().mean() * 100,
        'unique_row_pct': 100 - df.duplicated().mean() * 100
    }

    if key_cols:
        key_dupes = df.duplicated(subset=key_cols).sum()
        results['key_duplicate_count'] = key_dupes
        results['key_duplicate_pct'] = key_dupes / len(df) * 100
        results['key_unique_pct'] = 100 - results['key_duplicate_pct']

    return results
```

---

## 5. Timeliness

**Definition**: The degree to which data is current and available when needed.

### Why It Matters

Stale data leads to:
- Decisions on outdated information
- Missed opportunities
- Compliance issues

### What to Measure

| Metric | Description | Example |
|--------|-------------|---------|
| **Data freshness** | Age of most recent record | Last update: 2 hours ago |
| **Update frequency** | How often data refreshes | Daily at 6 AM |
| **Latency** | Time from event to data | Real-time vs batch |

### How to Check

```python
from datetime import datetime, timedelta

def timeliness_check(df, date_col, max_age_days=1):
    """Check timeliness dimension."""
    if date_col not in df.columns:
        return {'error': f'Column {date_col} not found'}

    # Ensure datetime
    dates = pd.to_datetime(df[date_col], errors='coerce')

    most_recent = dates.max()
    oldest = dates.min()
    now = datetime.now()

    age = now - most_recent
    is_fresh = age <= timedelta(days=max_age_days)

    return {
        'most_recent_record': str(most_recent),
        'oldest_record': str(oldest),
        'data_age_hours': age.total_seconds() / 3600,
        'data_age_days': age.days,
        'is_fresh': is_fresh,
        'freshness_threshold_days': max_age_days
    }
```

---

## 6. Conformity

**Definition**: The degree to which data adheres to specified formats and standards.

### Why It Matters

Non-conforming data:
- Fails schema validation
- Breaks downstream systems
- Requires manual handling

### What to Measure

| Metric | Check | Example |
|--------|-------|---------|
| **Schema compliance** | Matches expected schema | All required columns present |
| **Type compliance** | Correct data types | Integer columns are integers |
| **Format compliance** | Standard formats | ISO 8601 dates |
| **Length compliance** | Within size limits | VARCHAR(50) ≤ 50 chars |

### How to Check

```python
def conformity_check(df, schema):
    """
    Check conformity dimension against schema.

    schema = {
        'id': {'type': 'int64', 'required': True, 'unique': True},
        'name': {'type': 'object', 'required': True, 'max_length': 100},
        'created_at': {'type': 'datetime64', 'required': True},
    }
    """
    results = {'columns': {}, 'missing_required': [], 'extra_columns': []}

    # Check required columns exist
    for col, spec in schema.items():
        if spec.get('required') and col not in df.columns:
            results['missing_required'].append(col)

    # Check for unexpected columns
    expected_cols = set(schema.keys())
    actual_cols = set(df.columns)
    results['extra_columns'] = list(actual_cols - expected_cols)

    # Check each column
    for col, spec in schema.items():
        if col not in df.columns:
            continue

        col_results = {'conforms': True, 'issues': []}

        # Type check
        actual_type = str(df[col].dtype)
        expected_type = spec.get('type')
        if expected_type and expected_type not in actual_type:
            col_results['conforms'] = False
            col_results['issues'].append(f'Type mismatch: expected {expected_type}, got {actual_type}')

        # Length check (for strings)
        max_length = spec.get('max_length')
        if max_length and df[col].dtype == 'object':
            over_length = df[col].str.len() > max_length
            if over_length.any():
                col_results['conforms'] = False
                col_results['issues'].append(f'{over_length.sum()} values exceed max length {max_length}')

        results['columns'][col] = col_results

    return results
```

---

## Dimension Summary

| Dimension | Question | Critical When |
|-----------|----------|---------------|
| **Completeness** | Is it all here? | Missing data affects calculations |
| **Accuracy** | Is it correct? | Wrong values lead to wrong decisions |
| **Consistency** | Does it match? | Data from multiple sources |
| **Uniqueness** | Is it distinct? | Counting, aggregating |
| **Timeliness** | Is it current? | Time-sensitive decisions |
| **Conformity** | Does it fit? | System integration |

---

## Composite Quality Score

```python
def calculate_quality_score(dimension_results, weights=None):
    """
    Calculate overall quality score from dimension results.

    WHY: A single score helps communicate overall quality
    while dimension scores identify specific issues.
    """
    if weights is None:
        weights = {
            'completeness': 0.2,
            'accuracy': 0.25,
            'consistency': 0.2,
            'uniqueness': 0.15,
            'timeliness': 0.1,
            'conformity': 0.1
        }

    # Extract dimension scores (0-100)
    scores = {}
    for dim, weight in weights.items():
        if dim in dimension_results:
            # Logic to extract score depends on dimension result structure
            scores[dim] = dimension_results[dim].get('score', 100)

    # Weighted average
    total_weight = sum(weights.values())
    weighted_sum = sum(scores.get(dim, 100) * weight
                      for dim, weight in weights.items())

    return {
        'overall_score': weighted_sum / total_weight,
        'dimension_scores': scores,
        'weights': weights
    }
```
