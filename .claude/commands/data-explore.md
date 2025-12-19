# Data Explore (EDA)

**Phase 2 of 4** in the data analyst workflow.

## Purpose

Explore data to understand its structure, quality, and patterns. This phase answers: What does the data look like?

## Workflow

1. **Read philosophy first**
   - Read `.claude/skills/data-analyst/cookbook/philosophy.md`
   - Remember: "EDA is detective work, not random poking"

2. **Read the WHY**
   - Read `.claude/skills/data-analyst/cookbook/explore/why.md`
   - Explain to user WHY we do EDA BEFORE cleaning

3. **Check for prior phase**
   - Look for `ai-docs/data-understand-*.md`
   - If exists, read it for context
   - If not, ask user for problem context

4. **Get the data**
   - Ask user for data file path
   - Load and confirm row/column count

5. **Work through EDA checklist**
   - Read `.claude/skills/data-analyst/cookbook/explore/checklist.md`
   - For each section:
     - Explain WHY we check this
     - Run the check using code from `cookbook/explore/code.md`
     - Document findings

6. **Use techniques reference**
   - Read `.claude/skills/data-analyst/cookbook/explore/techniques.md`
   - Apply appropriate statistical techniques
   - Explain what each reveals and why it matters

7. **Produce output**
   - Write EDA report to `ai-docs/data-explore-{dataset-slug}.md`
   - Include: overview, quality issues, distributions, correlations
   - List recommended cleaning steps

## Code Execution

When running analysis:
- Use Python with pandas, numpy, matplotlib, seaborn
- Follow patterns from `cookbook/explore/code.md`
- Save visualizations to `eda_output/plots/`
- ALWAYS explain what each output means

## Rules

- **Never skip the WHY** - Explain the purpose of each analysis
- **Read before write** - Check for prior phase outputs
- **Show your work** - Display code and explain results
- **Document quality issues** - Every problem found gets logged

## Argument

If user provides `$ARGUMENTS`:
- Treat as data file path or dataset name
- Example: `/data-explore sales_data.csv`
