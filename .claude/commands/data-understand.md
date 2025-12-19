# Data Understand

**Phase 1 of 4** in the data analyst workflow.

## Purpose

Define the business problem before touching data. This phase answers: What are we solving and why?

## Workflow

1. **Read philosophy first**
   - Read `.claude/skills/data-analyst/cookbook/philosophy.md`
   - Internalize the core principles before proceeding

2. **Read the WHY**
   - Read `.claude/skills/data-analyst/cookbook/understand/why.md`
   - Explain to the user WHY this phase matters

3. **Gather context**
   - Ask: What problem are we solving?
   - Ask: What data do we have?
   - Ask: Who are the stakeholders?

4. **Work through the checklist**
   - Read `.claude/skills/data-analyst/cookbook/understand/checklist.md`
   - Guide user through each section
   - For each item: explain WHY it matters, then capture the answer

5. **Ask stakeholder questions**
   - Read `.claude/skills/data-analyst/cookbook/understand/questions.md`
   - Use the 5W1H framework
   - Document all answers

6. **Produce output**
   - Read `.claude/skills/data-analyst/cookbook/understand/template.md`
   - Fill in the template with gathered information
   - Write to `ai-docs/data-understand-{project-slug}.md`

## Rules

- **Never skip the WHY** - Before any action, explain the principle
- **Ask, don't assume** - Gather information from the user
- **Document everything** - All outputs go to ai-docs/
- **Check for prior work** - Look for existing ai-docs/data-*.md files

## Argument

If user provides `$ARGUMENTS`:
- Use it as the project name/context
- Example: `/data-understand customer churn analysis`
