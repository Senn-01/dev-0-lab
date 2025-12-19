# Data Validate

**Phase 4 of 4** in the data analyst workflow.

## Purpose

Certify that data meets quality standards. This phase answers: Is the data good enough to use?

## Workflow

1. **Read philosophy first**
   - Read `.claude/skills/data-analyst/cookbook/philosophy.md`
   - Remember: "Cleaning fixes data. Validation proves it's fixed."

2. **Read the WHY**
   - Read `.claude/skills/data-analyst/cookbook/validate/why.md`
   - Explain WHY validation is SEPARATE from cleaning

3. **Check for prior phases**
   - Look for `ai-docs/data-clean-*.md`
   - Understand what cleaning was done
   - If no cleaning exists, validate raw data (may have many failures)

4. **Define quality dimensions**
   - Read `.claude/skills/data-analyst/cookbook/validate/dimensions.md`
   - Explain the 6 dimensions to user:
     - Completeness, Accuracy, Consistency
     - Uniqueness, Timeliness, Conformity

5. **Set thresholds**
   - Read `.claude/skills/data-analyst/cookbook/validate/thresholds.md`
   - Ask user: What's acceptable for this use case?
   - Default to 95% for most checks, 100% for critical fields

6. **Run validation**
   - Use code patterns from `cookbook/validate/code.md`
   - Check each dimension
   - Report pass/fail against thresholds

7. **Produce certification**
   - Write validation report to `ai-docs/data-validate-{dataset-slug}.md`
   - Include: dimension scores, failed checks, overall verdict
   - State clearly: PASSED or FAILED

## Code Execution

When running validation:
- Use Python with pandas, numpy
- Follow patterns from `cookbook/validate/code.md`
- Generate ValidationReport with all checks
- Export as markdown for stakeholder review

## Rules

- **Never skip the WHY** - Explain what each dimension measures
- **Threshold-driven** - Every check has pass/fail criteria
- **Document failures** - Failed checks need explanation
- **Clear verdict** - End with explicit PASS or FAIL

## Argument

If user provides `$ARGUMENTS`:
- Treat as data file path or validation config
- Example: `/data-validate cleaned_sales.csv`

## Output Decision

Based on validation results:

| Overall Score | Verdict | Action |
|---------------|---------|--------|
| ≥95% | EXCELLENT | Proceed with confidence |
| 90-95% | GOOD | Proceed with monitoring |
| 85-90% | ACCEPTABLE | Proceed with documentation |
| 80-85% | MARGINAL | Review with stakeholders |
| <80% | POOR | Do not use, return to cleaning |
