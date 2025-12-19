# Data Quality Thresholds

Standard thresholds for pass/fail quality decisions.

---

## Threshold Philosophy

### Why Thresholds Matter

Without thresholds, quality is subjective:
- "This data seems okay" → Not actionable
- "This data passes all quality checks" → Actionable

Thresholds turn quality assessment into quality certification.

### Setting Thresholds

| Factor | Impact on Threshold |
|--------|---------------------|
| **Criticality** | Higher stakes → stricter thresholds |
| **Use case** | ML model → tighter than exploratory |
| **Historical baseline** | Match or improve on past quality |
| **Stakeholder agreement** | Align on what's acceptable |

### The 100/95/90 Rule

For most business applications:
- **Critical fields**: 100% (zero tolerance)
- **Important fields**: ≥95%
- **Other fields**: ≥90%

---

## Completeness Thresholds

### By Field Criticality

| Criticality | Threshold | Example Fields |
|-------------|-----------|----------------|
| **Critical** | 100% | Primary key, Required identifiers |
| **High** | ≥98% | Name, Email, Core metrics |
| **Medium** | ≥95% | Address, Phone |
| **Low** | ≥90% | Preferences, Optional fields |
| **Informational** | ≥80% | Notes, Comments |

### By Use Case

| Use Case | Overall Threshold | Rationale |
|----------|-------------------|-----------|
| **Financial reporting** | 100% critical, ≥99% all | Regulatory requirement |
| **ML training** | ≥95% | Imputation can handle small gaps |
| **Exploratory analysis** | ≥85% | Directional insights are valid |
| **Real-time dashboards** | ≥90% | Visual trends robust to minor gaps |

### Threshold Configuration

```python
COMPLETENESS_THRESHOLDS = {
    'critical': {
        'threshold': 100.0,
        'action': 'BLOCK',  # Cannot proceed
        'fields': ['customer_id', 'transaction_id', 'amount']
    },
    'high': {
        'threshold': 98.0,
        'action': 'WARN',  # Proceed with warning
        'fields': ['customer_name', 'email', 'product_id']
    },
    'medium': {
        'threshold': 95.0,
        'action': 'LOG',  # Log and proceed
        'fields': ['phone', 'address_line1']
    },
    'low': {
        'threshold': 90.0,
        'action': 'IGNORE',  # Proceed silently
        'fields': ['address_line2', 'notes']
    }
}
```

---

## Accuracy Thresholds

### By Validation Type

| Validation | Threshold | Rationale |
|------------|-----------|-----------|
| **Range checks** | ≥99% | Few edge cases expected |
| **Format checks** | ≥98% | Allow for legacy formats |
| **Reference checks** | 100% | Foreign keys must exist |
| **Business rules** | ≥99% | Core logic must hold |

### Common Rules and Thresholds

| Rule | Threshold | Action if Failed |
|------|-----------|------------------|
| Age in [0, 120] | 99.9% | Flag outliers |
| Date not in future | 100% | Block, investigate |
| Email valid format | 98% | Log invalid |
| Currency is positive | 100% | Block, investigate |
| Country in ISO list | 100% | Standardize |

### Threshold Configuration

```python
ACCURACY_THRESHOLDS = {
    'age': {
        'rule': lambda x: (x >= 0) & (x <= 120),
        'threshold': 99.9,
        'action': 'FLAG'
    },
    'transaction_date': {
        'rule': lambda x: x <= pd.Timestamp.now(),
        'threshold': 100.0,
        'action': 'BLOCK'
    },
    'email': {
        'rule': lambda x: x.str.contains(r'^[\w.-]+@[\w.-]+\.\w+$', na=False),
        'threshold': 98.0,
        'action': 'LOG'
    },
    'amount': {
        'rule': lambda x: x >= 0,
        'threshold': 100.0,
        'action': 'BLOCK'
    }
}
```

---

## Consistency Thresholds

### Cross-Field Consistency

| Rule | Threshold | Rationale |
|------|-----------|-----------|
| Calculated fields match | 100% | Math must be correct |
| Date sequences valid | 100% | Logic must hold |
| Category combinations valid | ≥99% | Some edge cases allowed |

### Cross-Table Consistency

| Check | Threshold | Action |
|-------|-----------|--------|
| Totals match | 100% | Block if mismatch |
| Reference integrity | 100% | Block if orphans |
| Counts align | ≥99.5% | Investigate variance |

### Threshold Configuration

```python
CONSISTENCY_THRESHOLDS = {
    'calculated_total': {
        'rule': lambda df: abs(df['qty'] * df['price'] - df['total']) < 0.01,
        'threshold': 100.0,
        'action': 'BLOCK'
    },
    'date_sequence': {
        'rule': lambda df: df['end_date'] >= df['start_date'],
        'threshold': 100.0,
        'action': 'BLOCK'
    },
    'valid_category_combo': {
        'rule': lambda df: df.apply(valid_category_combo, axis=1),
        'threshold': 99.0,
        'action': 'WARN'
    }
}
```

---

## Uniqueness Thresholds

### By Entity Type

| Entity | Duplicate Threshold | Rationale |
|--------|---------------------|-----------|
| **Primary keys** | 0% | Must be unique by definition |
| **Business keys** | 0% | Should be unique |
| **Exact duplicates** | <0.1% | Almost always errors |
| **Near-duplicates** | <1% | May need fuzzy matching |

### Threshold Configuration

```python
UNIQUENESS_THRESHOLDS = {
    'primary_key': {
        'columns': ['id'],
        'max_duplicate_pct': 0.0,
        'action': 'BLOCK'
    },
    'business_key': {
        'columns': ['customer_id', 'transaction_date'],
        'max_duplicate_pct': 0.0,
        'action': 'BLOCK'
    },
    'exact_row': {
        'columns': None,  # All columns
        'max_duplicate_pct': 0.1,
        'action': 'WARN'
    }
}
```

---

## Timeliness Thresholds

### By Data Type

| Data Type | Max Staleness | Rationale |
|-----------|---------------|-----------|
| **Real-time events** | Minutes | Operational decisions |
| **Daily metrics** | 24 hours | End-of-day reporting |
| **Weekly reports** | 7 days | Weekly reviews |
| **Monthly reports** | 30 days | Monthly close |
| **Reference data** | 90 days | Slowly changing |

### Threshold Configuration

```python
from datetime import timedelta

TIMELINESS_THRESHOLDS = {
    'real_time': {
        'max_age': timedelta(minutes=15),
        'action': 'BLOCK'
    },
    'daily': {
        'max_age': timedelta(hours=26),  # Buffer for processing
        'action': 'WARN'
    },
    'weekly': {
        'max_age': timedelta(days=8),
        'action': 'LOG'
    }
}
```

---

## Conformity Thresholds

### Schema Conformity

| Check | Threshold | Action |
|-------|-----------|--------|
| Required columns present | 100% | Block |
| Column types correct | 100% | Block |
| No unexpected columns | Warning only | Log |

### Format Conformity

| Format | Threshold | Example |
|--------|-----------|---------|
| Date format | 100% | ISO 8601 |
| Phone format | ≥95% | E.164 |
| Currency format | 100% | 2 decimal places |

---

## Composite Thresholds

### Overall Quality Score

| Score | Rating | Action |
|-------|--------|--------|
| ≥95% | Excellent | Proceed |
| 90-95% | Good | Proceed with monitoring |
| 85-90% | Acceptable | Proceed with documentation |
| 80-85% | Marginal | Review with stakeholders |
| <80% | Poor | Do not use, escalate |

### Configuration

```python
OVERALL_THRESHOLDS = {
    'excellent': {'min_score': 95, 'action': 'PROCEED'},
    'good': {'min_score': 90, 'action': 'PROCEED_WITH_MONITORING'},
    'acceptable': {'min_score': 85, 'action': 'PROCEED_WITH_DOCUMENTATION'},
    'marginal': {'min_score': 80, 'action': 'STAKEHOLDER_REVIEW'},
    'poor': {'min_score': 0, 'action': 'BLOCK'}
}

def get_quality_rating(score):
    """Determine quality rating from score."""
    for rating, config in OVERALL_THRESHOLDS.items():
        if score >= config['min_score']:
            return rating, config['action']
    return 'poor', 'BLOCK'
```

---

## Threshold Documentation Template

```markdown
## Data Quality Thresholds: [Dataset Name]

### Completeness
| Field | Threshold | Rationale |
|-------|-----------|-----------|
| [field] | [X]% | [why this threshold] |

### Accuracy
| Rule | Threshold | Rationale |
|------|-----------|-----------|
| [rule] | [X]% | [why] |

### Consistency
| Check | Threshold | Rationale |
|-------|-----------|-----------|
| [check] | [X]% | [why] |

### Uniqueness
| Key | Threshold | Rationale |
|-----|-----------|-----------|
| [key] | [X]% | [why] |

### Timeliness
| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Max staleness | [X] hours/days | [why] |

### Overall
| Minimum Score | [X]% |
| Blocking Score | [Y]% |

### Approval
- Approved by: [Name]
- Date: [Date]
- Review frequency: [Quarterly/Annually]
```
