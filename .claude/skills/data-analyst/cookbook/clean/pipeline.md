# Data Cleaning Pipeline

The 7-step cleaning pipeline in correct order.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA CLEANING PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: STRUCTURE      ─── Clean column names, organize         │
│           │                                                      │
│           ▼                                                      │
│  Step 2: DATA TYPES     ─── Convert to correct types             │
│           │                                                      │
│           ▼                                                      │
│  Step 3: DUPLICATES     ─── Remove duplicate records             │
│           │                                                      │
│           ▼                                                      │
│  Step 4: INVALID        ─── Fix impossible/incorrect values      │
│           │                                                      │
│           ▼                                                      │
│  Step 5: MISSING        ─── Handle null/NaN values               │
│           │                                                      │
│           ▼                                                      │
│  Step 6: OUTLIERS       ─── Detect and handle extremes           │
│           │                                                      │
│           ▼                                                      │
│  Step 7: TRANSFORM      ─── Prepare for analysis                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Structure

**Goal**: Create a clean, consistent data structure.

### Tasks

| Task | Why | How |
|------|-----|-----|
| Clean column names | Prevent bugs from spaces/special chars | `df.columns = df.columns.str.lower().str.replace(' ', '_')` |
| Remove empty columns | No information value | `df.dropna(axis=1, how='all')` |
| Remove constant columns | No variance = no insight | `df.loc[:, df.nunique() > 1]` |
| Order columns logically | Easier to work with | Group IDs, then features, then targets |

### Entry Criteria
- Raw data loaded

### Exit Criteria
- All column names are lowercase, underscore-separated
- No columns with 100% missing
- No columns with single value
- Column order is logical

---

## Step 2: Data Types

**Goal**: Ensure every column has the correct type for its content.

### Tasks

| Task | Why | How |
|------|-----|-----|
| Convert numeric strings | Enable math operations | `pd.to_numeric(df['col'], errors='coerce')` |
| Parse dates | Enable time operations | `pd.to_datetime(df['col'], errors='coerce')` |
| Convert categoricals | Memory efficiency | `df['col'].astype('category')` |
| Fix boolean columns | Proper True/False | Map strings to bool |

### Common Type Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Numeric column is `object` | Mixed types or string numbers | `pd.to_numeric(errors='coerce')` |
| Date column is `object` | Parsing failed | `pd.to_datetime(format='...')` |
| Large memory usage | String columns with few values | Convert to `category` |

### Entry Criteria
- Structure is clean

### Exit Criteria
- All numeric columns are numeric types
- All date columns are datetime
- Low-cardinality strings are categorical
- No accidental type mismatches

---

## Step 3: Duplicates

**Goal**: Remove redundant records that bias analysis.

### Types of Duplicates

| Type | Definition | Detection |
|------|------------|-----------|
| Exact duplicates | Identical across ALL columns | `df.duplicated()` |
| Key duplicates | Same ID, different values | `df.duplicated(subset=['id'])` |
| Fuzzy duplicates | Similar but not identical | Similarity matching |

### Decision Framework

| Scenario | Action |
|----------|--------|
| Exact duplicate, no explanation | Drop (keep first) |
| Key duplicate, older timestamp | Keep most recent |
| Key duplicate, no timestamp | Investigate—data error |
| Intentional duplicates (e.g., events) | Keep—they're valid |

### Entry Criteria
- Types are correct

### Exit Criteria
- No unintended exact duplicates
- Key duplicates investigated and resolved
- Duplicate count documented

---

## Step 4: Invalid Values

**Goal**: Correct or remove values that violate business rules.

### Common Invalid Values

| Category | Examples | Detection |
|----------|----------|-----------|
| Out of range | Age = -5, Age = 150 | Domain rules |
| Future dates | Transaction date = 2099 | `df['date'] > pd.Timestamp.now()` |
| Placeholder values | 9999, -999, 0000-00-00 | Value counts, domain knowledge |
| Format violations | Phone = "abc123" | Regex validation |
| Logical impossibilities | End date < Start date | Cross-field validation |

### Decision Framework

| Scenario | Action |
|----------|--------|
| Clearly wrong, correct value known | Fix it |
| Clearly wrong, correct value unknown | Set to NaN |
| Ambiguous | Flag for review |
| Placeholder value | Replace with NaN |

### Entry Criteria
- Duplicates removed

### Exit Criteria
- All values pass business rule validation
- Placeholders replaced with proper NaN
- Invalid values either fixed or set to NaN
- Count of corrections documented

---

## Step 5: Missing Values

**Goal**: Handle NaN/null values appropriately.

### Strategies

| Strategy | When to Use | Trade-off |
|----------|-------------|-----------|
| **Drop row** | <5% missing, MCAR | Lose data |
| **Drop column** | >50% missing, not critical | Lose feature |
| **Mean imputation** | Numeric, ~normal distribution | Reduces variance |
| **Median imputation** | Numeric, skewed distribution | Robust to outliers |
| **Mode imputation** | Categorical | May increase mode dominance |
| **Forward fill** | Time series, values persist | Assumes continuity |
| **Backward fill** | Time series, look-ahead OK | Assumes continuity |
| **Interpolation** | Ordered numeric | Assumes smoothness |
| **Indicator + impute** | Missingness is informative | Adds complexity |
| **Model-based** | Complex patterns | Expensive |

### Decision Process

```
Is >50% missing?
├── Yes → Consider dropping column
└── No
    Is missingness random (MCAR)?
    ├── Yes → Can drop rows if <5%
    └── No (MAR or MNAR)
        Is it numeric?
        ├── Yes → Impute with median (robust)
        └── No (categorical)
            → Impute with mode or create "Missing" category
```

### Entry Criteria
- Invalid values handled

### Exit Criteria
- Every column has a documented missing value strategy
- Strategies applied consistently
- No remaining NaN in critical columns
- Imputation assumptions documented

---

## Step 6: Outliers

**Goal**: Identify and appropriately handle extreme values.

### Detection Methods

| Method | Formula | Best For |
|--------|---------|----------|
| IQR | Outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR] | Skewed data |
| Z-Score | \|z\| > 3 | Normal distributions |
| Modified Z | \|MAD-z\| > 3.5 | Robust detection |
| Domain rules | Business logic | Known constraints |

### Handling Options

| Option | When | How |
|--------|------|-----|
| **Keep** | Valid extreme values | Document as-is |
| **Remove** | Errors, test data | Drop rows |
| **Cap** (Winsorize) | Limit influence | Clip to bounds |
| **Transform** | Compress range | Log, sqrt |
| **Flag** | Separate analysis | Add indicator column |

### Decision Process

```
Is it a data error?
├── Yes → Fix or remove
└── No (valid but extreme)
    Does it represent something real?
    ├── Yes → Keep (maybe flag)
    └── Maybe
        What's the impact on analysis?
        ├── High → Cap or transform
        └── Low → Keep
```

### Entry Criteria
- Missing values handled

### Exit Criteria
- Outliers identified in each numeric column
- Decision made and documented for each
- Treatment applied consistently
- Impact on statistics documented

---

## Step 7: Transform

**Goal**: Prepare data for specific analysis use.

### Common Transformations

| Transform | Purpose | When |
|-----------|---------|------|
| **Scaling** | Normalize ranges | For ML models |
| **Log transform** | Handle skewness | Right-skewed data |
| **One-hot encoding** | Numeric categoricals | For ML models |
| **Binning** | Create categories | High cardinality numerics |
| **Feature engineering** | Create new features | Domain knowledge |

### Entry Criteria
- All previous steps complete

### Exit Criteria
- Transformations applied for intended use case
- Original values preserved if needed
- Transformation logic documented
- Final dataset validated

---

## Pipeline Summary

| Step | Input State | Output State | Key Metric |
|------|-------------|--------------|------------|
| 1. Structure | Raw | Clean names | Column count |
| 2. Types | Clean names | Correct types | Type errors |
| 3. Duplicates | Correct types | Deduplicated | Rows removed |
| 4. Invalid | Deduplicated | Valid values | Values corrected |
| 5. Missing | Valid values | Complete | Imputation count |
| 6. Outliers | Complete | Bounded | Outliers handled |
| 7. Transform | Bounded | Analysis-ready | Final shape |
