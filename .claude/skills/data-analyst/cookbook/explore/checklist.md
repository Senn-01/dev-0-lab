# Exploratory Data Analysis Checklist

Systematic checklist for thorough data exploration.

---

## Phase 1: Data Overview

### Structure Check
- [ ] Loaded data and confirmed row/column count
- [ ] Examined first and last rows (`head()`, `tail()`)
- [ ] Reviewed all column names
- [ ] Identified data types for each column
- [ ] Determined the grain (one row represents what?)

### Memory & Performance
- [ ] Checked memory usage (`df.info(memory_usage='deep')`)
- [ ] Identified columns that could use more efficient types
- [ ] Noted any performance concerns for downstream analysis

### Initial Questions
- [ ] Does row count match expectations?
- [ ] Are all expected columns present?
- [ ] Are data types correct? (dates as datetime, not object)

---

## Phase 2: Data Quality Profile

### Missing Values
- [ ] Calculated missing count per column
- [ ] Calculated missing percentage per column
- [ ] Identified columns with >50% missing (candidate for drop)
- [ ] Identified columns with 0% missing (validate—is this real?)
- [ ] Analyzed missingness patterns (random vs systematic)
- [ ] Correlated missingness between columns

### Duplicates
- [ ] Counted exact duplicate rows
- [ ] Identified potential duplicate keys (e.g., same ID, different values)
- [ ] Investigated cause of duplicates (data issue vs valid repeats)

### Data Type Issues
- [ ] Identified numeric columns stored as strings
- [ ] Identified date columns stored as strings
- [ ] Checked for mixed types within columns
- [ ] Noted columns needing type conversion

### Invalid Values
- [ ] Checked for impossible values (negative ages, future dates)
- [ ] Verified values against business rules
- [ ] Identified placeholder values (e.g., -999, "N/A", "Unknown")
- [ ] Checked for whitespace issues in strings

---

## Phase 3: Univariate Analysis

### Numeric Columns
For each numeric column:
- [ ] Computed descriptive statistics (mean, median, std, min, max)
- [ ] Created histogram to visualize distribution
- [ ] Identified skewness direction and magnitude
- [ ] Detected outliers (IQR or Z-score method)
- [ ] Noted any concerning patterns (spikes, gaps, clipping)

### Categorical Columns
For each categorical column:
- [ ] Counted unique values
- [ ] Generated frequency table (value_counts)
- [ ] Identified mode and its dominance
- [ ] Checked for typos/inconsistencies (e.g., "Yes", "yes", "Y")
- [ ] Noted high-cardinality columns (may need special handling)

### Date/Time Columns
For each date column:
- [ ] Identified date range (min to max)
- [ ] Checked for gaps in time series
- [ ] Verified timezone consistency
- [ ] Looked for suspicious dates (1900-01-01, 1970-01-01)

---

## Phase 4: Multivariate Analysis

### Correlations
- [ ] Computed correlation matrix for numeric columns
- [ ] Identified highly correlated pairs (>0.8)
- [ ] Visualized with heatmap
- [ ] Verified correlations with scatter plots (checking for non-linear)

### Relationships with Target (if applicable)
- [ ] Explored how features relate to target variable
- [ ] Identified strongest predictors
- [ ] Checked for potential data leakage

### Segmentation Checks
- [ ] Compared distributions across key segments
- [ ] Identified segment-specific patterns
- [ ] Noted any segments with different data quality

---

## Phase 5: Business Validation

### Definition Verification
- [ ] Verified "customer" matches business definition
- [ ] Verified "revenue" calculation matches finance
- [ ] Confirmed date fields align with business calendar
- [ ] Validated any derived metrics

### Reality Checks
- [ ] Do totals match known benchmarks?
- [ ] Do trends align with business knowledge?
- [ ] Are extreme values explainable?
- [ ] Does the data make business sense?

### Cross-Reference
- [ ] Compared key metrics to external sources (if available)
- [ ] Validated sample against known ground truth
- [ ] Checked for consistency across related tables

---

## Phase 6: Documentation

### Findings Log
- [ ] Documented all anomalies discovered
- [ ] Recorded questions that arose
- [ ] Noted assumptions made
- [ ] Listed items needing stakeholder clarification

### Quality Issues Register
For each issue found:
- [ ] Description of the issue
- [ ] Affected column(s)
- [ ] Number of records affected
- [ ] Severity (Critical/Major/Minor)
- [ ] Proposed remediation

### Visualizations
- [ ] Saved key distribution plots
- [ ] Saved correlation heatmap
- [ ] Saved any anomaly visualizations
- [ ] Organized in report-ready format

---

## Exit Criteria

**You are ready to move to Data Cleaning when:**

1. You understand the structure of every column
2. You have quantified all data quality issues
3. You have a prioritized list of cleaning tasks
4. You have validated data against business definitions
5. You have documented your findings
6. Stakeholders have reviewed critical findings

**If ANY of these are missing, continue EDA.** You cannot clean what you don't understand.

---

## Red Flags Requiring Investigation

Stop and investigate if you find:

| Finding | Possible Cause |
|---------|----------------|
| 100% complete data | Data might be synthetically filled |
| Column with single value | Constant—probably drop |
| Column with unique values = rows | ID column—not useful for analysis |
| Future dates in historical data | ETL bug or timezone issue |
| Perfect correlation (1.0 or -1.0) | Likely derived column or data leakage |
| Sudden distribution change over time | System change, definition change |
| Missing values only in recent data | Data pipeline issue |
| Round numbers everywhere | Data was estimated, not measured |

---

## Output Template

At minimum, your EDA report should include:

```markdown
## Dataset Overview
- Rows: X, Columns: Y
- Time range: [start] to [end]
- Grain: One row = one [entity]

## Data Quality Summary
- Missing: X columns have missing data
- Duplicates: X exact duplicates found
- Type issues: X columns need conversion

## Key Distributions
[Charts + commentary for important columns]

## Correlations
[Heatmap + notable relationships]

## Quality Issues
| Issue | Severity | Records | Remediation |
|-------|----------|---------|-------------|
| ... | ... | ... | ... |

## Questions for Stakeholders
1. [Question about finding]
2. [Clarification needed]

## Recommended Cleaning Steps
1. [Step 1]
2. [Step 2]
```
