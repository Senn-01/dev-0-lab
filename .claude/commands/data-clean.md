# Data Clean

**Phase 3 of 4** in the data analyst workflow.

## Purpose

Transform raw data into analysis-ready data. This phase answers: How do we fix the issues found in EDA?

## Workflow

1. **Read philosophy first**
   - Read `.claude/skills/data-analyst/cookbook/philosophy.md`
   - Remember: "Cleaning is about making data truthful"

2. **Read the WHY**
   - Read `.claude/skills/data-analyst/cookbook/clean/why.md`
   - Explain to user WHY cleaning ORDER matters

3. **Check for prior phases**
   - Look for `ai-docs/data-explore-*.md`
   - Read quality issues found in EDA
   - If no EDA exists, recommend running `/data-explore` first

4. **Present the pipeline**
   - Read `.claude/skills/data-analyst/cookbook/clean/pipeline.md`
   - Explain the 7-step pipeline and WHY this order

5. **Get user decisions**
   - For each issue from EDA, ask user's preferred strategy
   - Present options from `cookbook/clean/strategies.md`
   - Document each decision with rationale

6. **Execute cleaning**
   - Follow code patterns from `cookbook/clean/code.md`
   - Use the CleaningLog class to track all changes
   - For each step: explain WHY, then show WHAT changed

7. **Produce outputs**
   - Save cleaned dataset
   - Write cleaning log to `ai-docs/data-clean-{dataset-slug}.md`
   - Include: before/after statistics, decisions made, rows affected

## Code Execution

When running cleaning:
- Use Python with pandas, numpy
- Follow patterns from `cookbook/clean/code.md`
- Log EVERY transformation with before/after counts
- NEVER modify data without explaining why

## Rules

- **Never skip the WHY** - Explain the rationale for each cleaning step
- **Read before write** - Must have EDA output to clean effectively
- **Log everything** - Use CleaningLog for full audit trail
- **Conservative by default** - Flag rather than delete when uncertain

## Argument

If user provides `$ARGUMENTS`:
- Treat as data file path or reference to dataset
- Example: `/data-clean sales_data.csv`
