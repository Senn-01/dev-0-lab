# Data Validation Python Code Patterns

Production-ready code for data validation.

---

## Setup

```python
"""
Data Validation Script Template
===============================
Run this script to validate a cleaned dataset against quality thresholds.

Usage:
    python validate.py data.csv
    python validate.py data.csv --config validation_config.json --output report.md
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
import json
import argparse
```

---

## Validation Result Classes

```python
@dataclass
class CheckResult:
    """Result of a single validation check."""
    name: str
    dimension: str
    passed: bool
    score: float  # 0-100
    threshold: float
    message: str
    details: dict = None

    def to_dict(self):
        return {
            'name': self.name,
            'dimension': self.dimension,
            'passed': self.passed,
            'score': self.score,
            'threshold': self.threshold,
            'message': self.message,
            'details': self.details
        }


@dataclass
class ValidationReport:
    """Complete validation report."""
    dataset: str
    timestamp: str
    overall_score: float
    overall_passed: bool
    dimension_scores: Dict[str, float]
    checks: List[CheckResult]
    critical_failures: List[CheckResult]
    warnings: List[CheckResult]

    def to_markdown(self) -> str:
        """Export report as markdown."""
        status = "PASSED" if self.overall_passed else "FAILED"
        status_emoji = "✅" if self.overall_passed else "❌"

        md = f"""# Data Validation Report

**Dataset**: {self.dataset}
**Timestamp**: {self.timestamp}
**Status**: {status_emoji} {status}
**Overall Score**: {self.overall_score:.1f}%

## Dimension Scores

| Dimension | Score | Status |
|-----------|-------|--------|
"""
        for dim, score in self.dimension_scores.items():
            status = "✅" if score >= 90 else "⚠️" if score >= 80 else "❌"
            md += f"| {dim.title()} | {score:.1f}% | {status} |\n"

        if self.critical_failures:
            md += "\n## Critical Failures ❌\n\n"
            for check in self.critical_failures:
                md += f"- **{check.name}**: {check.message} (Score: {check.score:.1f}%, Threshold: {check.threshold}%)\n"

        if self.warnings:
            md += "\n## Warnings ⚠️\n\n"
            for check in self.warnings:
                md += f"- **{check.name}**: {check.message} (Score: {check.score:.1f}%)\n"

        md += "\n## All Checks\n\n"
        md += "| Check | Dimension | Score | Threshold | Status |\n"
        md += "|-------|-----------|-------|-----------|--------|\n"
        for check in self.checks:
            status = "✅" if check.passed else "❌"
            md += f"| {check.name} | {check.dimension} | {check.score:.1f}% | {check.threshold}% | {status} |\n"

        return md
```

---

## Dimension Validators

```python
class CompletenessValidator:
    """
    Validate completeness dimension.

    WHY: Missing data is the most common quality issue.
    This validator quantifies what's missing and where.
    """

    def __init__(self, thresholds: dict = None):
        self.thresholds = thresholds or {
            'critical': {'threshold': 100.0, 'fields': []},
            'high': {'threshold': 98.0, 'fields': []},
            'default': {'threshold': 95.0}
        }

    def validate(self, df: pd.DataFrame) -> List[CheckResult]:
        """Run all completeness checks."""
        results = []

        # Overall completeness
        overall_complete = df.notna().mean().mean() * 100
        results.append(CheckResult(
            name='overall_completeness',
            dimension='completeness',
            passed=overall_complete >= self.thresholds['default']['threshold'],
            score=overall_complete,
            threshold=self.thresholds['default']['threshold'],
            message=f'Overall completeness: {overall_complete:.1f}%'
        ))

        # Critical field completeness
        for field in self.thresholds['critical'].get('fields', []):
            if field not in df.columns:
                continue
            complete_pct = df[field].notna().mean() * 100
            threshold = self.thresholds['critical']['threshold']
            results.append(CheckResult(
                name=f'completeness_{field}',
                dimension='completeness',
                passed=complete_pct >= threshold,
                score=complete_pct,
                threshold=threshold,
                message=f'{field} completeness: {complete_pct:.1f}% (critical field)',
                details={'field': field, 'missing_count': df[field].isna().sum()}
            ))

        # Per-column completeness
        for col in df.columns:
            complete_pct = df[col].notna().mean() * 100
            threshold = self.thresholds['default']['threshold']
            results.append(CheckResult(
                name=f'completeness_{col}',
                dimension='completeness',
                passed=complete_pct >= threshold,
                score=complete_pct,
                threshold=threshold,
                message=f'{col}: {complete_pct:.1f}% complete'
            ))

        return results


class AccuracyValidator:
    """
    Validate accuracy dimension.

    WHY: Data must represent reality correctly.
    This validator checks against business rules.
    """

    def __init__(self, rules: dict = None):
        """
        rules = {
            'age_valid': {
                'column': 'age',
                'check': lambda x: (x >= 0) & (x <= 120),
                'threshold': 99.9,
                'message': 'Age must be between 0 and 120'
            },
            ...
        }
        """
        self.rules = rules or {}

    def validate(self, df: pd.DataFrame) -> List[CheckResult]:
        """Run all accuracy checks."""
        results = []

        for name, rule in self.rules.items():
            col = rule['column']
            if col not in df.columns:
                continue

            check_func = rule['check']
            valid_mask = check_func(df[col])
            valid_pct = valid_mask.mean() * 100
            threshold = rule.get('threshold', 99.0)

            results.append(CheckResult(
                name=name,
                dimension='accuracy',
                passed=valid_pct >= threshold,
                score=valid_pct,
                threshold=threshold,
                message=rule.get('message', f'{name}: {valid_pct:.1f}% valid'),
                details={
                    'column': col,
                    'invalid_count': (~valid_mask).sum(),
                    'invalid_examples': df.loc[~valid_mask, col].head(5).tolist()
                }
            ))

        return results


class ConsistencyValidator:
    """
    Validate consistency dimension.

    WHY: Data must be internally coherent.
    This validator checks cross-field logic.
    """

    def __init__(self, rules: dict = None):
        """
        rules = {
            'total_matches': {
                'check': lambda df: abs(df['qty'] * df['price'] - df['total']) < 0.01,
                'threshold': 100.0,
                'message': 'Calculated total must match total field'
            },
            ...
        }
        """
        self.rules = rules or {}

    def validate(self, df: pd.DataFrame) -> List[CheckResult]:
        """Run all consistency checks."""
        results = []

        for name, rule in self.rules.items():
            try:
                check_func = rule['check']
                consistent_mask = check_func(df)
                consistent_pct = consistent_mask.mean() * 100
                threshold = rule.get('threshold', 100.0)

                results.append(CheckResult(
                    name=name,
                    dimension='consistency',
                    passed=consistent_pct >= threshold,
                    score=consistent_pct,
                    threshold=threshold,
                    message=rule.get('message', f'{name}: {consistent_pct:.1f}% consistent'),
                    details={'inconsistent_count': (~consistent_mask).sum()}
                ))
            except Exception as e:
                results.append(CheckResult(
                    name=name,
                    dimension='consistency',
                    passed=False,
                    score=0,
                    threshold=rule.get('threshold', 100.0),
                    message=f'Check failed: {str(e)}'
                ))

        return results


class UniquenessValidator:
    """
    Validate uniqueness dimension.

    WHY: Duplicate data biases everything.
    This validator ensures entities are distinct.
    """

    def __init__(self, key_columns: List[str] = None):
        self.key_columns = key_columns or []

    def validate(self, df: pd.DataFrame) -> List[CheckResult]:
        """Run all uniqueness checks."""
        results = []

        # Exact duplicate check
        exact_dupes = df.duplicated().sum()
        unique_pct = (1 - exact_dupes / len(df)) * 100

        results.append(CheckResult(
            name='exact_duplicates',
            dimension='uniqueness',
            passed=exact_dupes == 0,
            score=unique_pct,
            threshold=100.0,
            message=f'{exact_dupes} exact duplicate rows found',
            details={'duplicate_count': exact_dupes}
        ))

        # Key uniqueness check
        if self.key_columns:
            existing_keys = [c for c in self.key_columns if c in df.columns]
            if existing_keys:
                key_dupes = df.duplicated(subset=existing_keys).sum()
                key_unique_pct = (1 - key_dupes / len(df)) * 100

                results.append(CheckResult(
                    name='key_uniqueness',
                    dimension='uniqueness',
                    passed=key_dupes == 0,
                    score=key_unique_pct,
                    threshold=100.0,
                    message=f'{key_dupes} duplicate keys on {existing_keys}',
                    details={
                        'key_columns': existing_keys,
                        'duplicate_count': key_dupes
                    }
                ))

        return results


class TimelinessValidator:
    """
    Validate timeliness dimension.

    WHY: Stale data leads to stale decisions.
    This validator checks data freshness.
    """

    def __init__(self, date_column: str, max_age: timedelta = None):
        self.date_column = date_column
        self.max_age = max_age or timedelta(days=1)

    def validate(self, df: pd.DataFrame) -> List[CheckResult]:
        """Run timeliness check."""
        results = []

        if self.date_column not in df.columns:
            results.append(CheckResult(
                name='timeliness',
                dimension='timeliness',
                passed=False,
                score=0,
                threshold=100.0,
                message=f'Date column {self.date_column} not found'
            ))
            return results

        dates = pd.to_datetime(df[self.date_column], errors='coerce')
        most_recent = dates.max()
        now = pd.Timestamp.now()
        age = now - most_recent

        is_fresh = age <= self.max_age
        # Score: 100% if within threshold, decreasing after
        if is_fresh:
            score = 100.0
        else:
            # Decay score based on how much over threshold
            excess_hours = (age - self.max_age).total_seconds() / 3600
            score = max(0, 100 - excess_hours * 5)  # Lose 5% per hour over

        results.append(CheckResult(
            name='data_freshness',
            dimension='timeliness',
            passed=is_fresh,
            score=score,
            threshold=100.0,
            message=f'Data age: {age}, max allowed: {self.max_age}',
            details={
                'most_recent': str(most_recent),
                'age_hours': age.total_seconds() / 3600,
                'max_age_hours': self.max_age.total_seconds() / 3600
            }
        ))

        return results


class ConformityValidator:
    """
    Validate conformity dimension.

    WHY: Data must match expected schema.
    This validator checks structure and formats.
    """

    def __init__(self, schema: dict = None):
        """
        schema = {
            'id': {'type': 'int64', 'required': True},
            'name': {'type': 'object', 'required': True},
            'amount': {'type': 'float64', 'required': True},
        }
        """
        self.schema = schema or {}

    def validate(self, df: pd.DataFrame) -> List[CheckResult]:
        """Run conformity checks."""
        results = []

        # Check required columns exist
        required_cols = [col for col, spec in self.schema.items()
                        if spec.get('required')]
        missing_required = [col for col in required_cols if col not in df.columns]

        results.append(CheckResult(
            name='required_columns',
            dimension='conformity',
            passed=len(missing_required) == 0,
            score=100 if len(missing_required) == 0 else 0,
            threshold=100.0,
            message=f'Missing required columns: {missing_required}' if missing_required else 'All required columns present',
            details={'missing': missing_required}
        ))

        # Check column types
        type_mismatches = []
        for col, spec in self.schema.items():
            if col not in df.columns:
                continue
            expected_type = spec.get('type')
            if expected_type:
                actual_type = str(df[col].dtype)
                if expected_type not in actual_type:
                    type_mismatches.append({
                        'column': col,
                        'expected': expected_type,
                        'actual': actual_type
                    })

        type_score = 100 * (1 - len(type_mismatches) / max(len(self.schema), 1))
        results.append(CheckResult(
            name='column_types',
            dimension='conformity',
            passed=len(type_mismatches) == 0,
            score=type_score,
            threshold=100.0,
            message=f'{len(type_mismatches)} type mismatches' if type_mismatches else 'All types correct',
            details={'mismatches': type_mismatches}
        ))

        return results
```

---

## Main Validation Pipeline

```python
class DataValidator:
    """
    Main validation orchestrator.

    WHY: Centralizes all validation logic and produces
    a comprehensive, actionable report.
    """

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.validators = []

    def add_completeness(self, thresholds: dict = None):
        """Add completeness validation."""
        self.validators.append(CompletenessValidator(thresholds))
        return self

    def add_accuracy(self, rules: dict):
        """Add accuracy validation."""
        self.validators.append(AccuracyValidator(rules))
        return self

    def add_consistency(self, rules: dict):
        """Add consistency validation."""
        self.validators.append(ConsistencyValidator(rules))
        return self

    def add_uniqueness(self, key_columns: List[str] = None):
        """Add uniqueness validation."""
        self.validators.append(UniquenessValidator(key_columns))
        return self

    def add_timeliness(self, date_column: str, max_age: timedelta = None):
        """Add timeliness validation."""
        self.validators.append(TimelinessValidator(date_column, max_age))
        return self

    def add_conformity(self, schema: dict):
        """Add conformity validation."""
        self.validators.append(ConformityValidator(schema))
        return self

    def validate(self, df: pd.DataFrame, dataset_name: str = 'dataset') -> ValidationReport:
        """Run all validators and produce report."""
        all_checks = []

        # Run all validators
        for validator in self.validators:
            checks = validator.validate(df)
            all_checks.extend(checks)

        # Calculate dimension scores
        dimension_scores = {}
        for dim in ['completeness', 'accuracy', 'consistency', 'uniqueness', 'timeliness', 'conformity']:
            dim_checks = [c for c in all_checks if c.dimension == dim]
            if dim_checks:
                dimension_scores[dim] = np.mean([c.score for c in dim_checks])

        # Calculate overall score
        overall_score = np.mean(list(dimension_scores.values())) if dimension_scores else 0

        # Identify failures and warnings
        critical_failures = [c for c in all_checks if not c.passed and c.threshold >= 99]
        warnings = [c for c in all_checks if not c.passed and c.threshold < 99]

        # Determine overall pass/fail
        overall_passed = len(critical_failures) == 0 and overall_score >= 80

        return ValidationReport(
            dataset=dataset_name,
            timestamp=datetime.now().isoformat(),
            overall_score=overall_score,
            overall_passed=overall_passed,
            dimension_scores=dimension_scores,
            checks=all_checks,
            critical_failures=critical_failures,
            warnings=warnings
        )


def run_validation(filepath: str, config: dict = None, output_path: str = None) -> ValidationReport:
    """
    Run complete validation pipeline.

    WHY: This is the entry point for validating any dataset
    against quality thresholds.
    """
    print("="*60)
    print("DATA VALIDATION")
    print("="*60 + "\n")

    # Load data
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df):,} rows × {len(df.columns)} columns\n")

    # Build validator
    config = config or {}
    validator = DataValidator(config)

    # Add default validators
    validator.add_completeness(config.get('completeness_thresholds'))
    validator.add_uniqueness(config.get('key_columns'))

    if config.get('accuracy_rules'):
        validator.add_accuracy(config['accuracy_rules'])

    if config.get('consistency_rules'):
        validator.add_consistency(config['consistency_rules'])

    if config.get('date_column'):
        max_age = timedelta(hours=config.get('max_age_hours', 24))
        validator.add_timeliness(config['date_column'], max_age)

    if config.get('schema'):
        validator.add_conformity(config['schema'])

    # Run validation
    report = validator.validate(df, Path(filepath).stem)

    # Print summary
    status = "✅ PASSED" if report.overall_passed else "❌ FAILED"
    print(f"\nValidation {status}")
    print(f"Overall Score: {report.overall_score:.1f}%")
    print(f"\nDimension Scores:")
    for dim, score in report.dimension_scores.items():
        print(f"  {dim}: {score:.1f}%")

    if report.critical_failures:
        print(f"\n❌ Critical Failures: {len(report.critical_failures)}")
        for failure in report.critical_failures:
            print(f"  - {failure.name}: {failure.message}")

    # Save report
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report.to_markdown())
        print(f"\nReport saved to {output_path}")

    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate a dataset')
    parser.add_argument('filepath', help='Path to data file')
    parser.add_argument('--config', help='Path to config JSON file')
    parser.add_argument('--output', help='Path to save validation report')
    args = parser.parse_args()

    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    run_validation(args.filepath, config, args.output)
```
