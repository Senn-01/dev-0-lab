# Business Understanding Output Template

Use this template to document the results of the business understanding phase.

---

```markdown
---
phase: understand
project: [project-slug]
date: [YYYY-MM-DDTHH:MM:SSZ]
status: complete
stakeholders: [list of stakeholders]
---

# Business Understanding: [Project Name]

## Problem Statement

**In one sentence:**
[Clear, specific statement of what we're solving]

**Full context:**
[2-3 paragraph explanation of the business situation, what triggered this analysis, and why it matters now]

---

## Decision Context

### The Decision
[What specific decision will this analysis inform?]

### The Options
[What choices is the stakeholder considering?]

### Decision Threshold
[What would change the recommendation? e.g., "If churn > 10%, invest in retention"]

### Decision Maker
[Who will make the final call?]

---

## Scope

### In Scope
- [Specific item 1]
- [Specific item 2]
- [Specific item 3]

### Out of Scope
- [Explicit exclusion 1]
- [Explicit exclusion 2]

### Time Period
[Start date] to [End date]

### Segments/Filters
[Any specific filters: geography, product line, customer type, etc.]

---

## Success Criteria

### What "Done" Looks Like
[Description of the final deliverable]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Validation Approach
[How will stakeholders verify the analysis is correct?]

---

## Data Landscape

### Primary Data Sources

| Source | Location | Owner | Refresh | Access Status |
|--------|----------|-------|---------|---------------|
| [Source 1] | [DB/File/API] | [Person] | [Frequency] | [Yes/Pending/No] |
| [Source 2] | [DB/File/API] | [Person] | [Frequency] | [Yes/Pending/No] |

### Key Definitions

| Term | Business Definition | Data Representation |
|------|---------------------|---------------------|
| [Term 1] | [What it means to business] | [How it appears in data] |
| [Term 2] | [What it means to business] | [How it appears in data] |

### Known Data Limitations
- [Limitation 1]: [Impact on analysis]
- [Limitation 2]: [Impact on analysis]

---

## Stakeholder Map

| Stakeholder | Role | Interest | Communication Preference |
|-------------|------|----------|--------------------------|
| [Name] | [Title] | [What they care about] | [Email/Slack/Meeting] |
| [Name] | [Title] | [What they care about] | [Email/Slack/Meeting] |

---

## Assumptions

**We are assuming that:**
1. [Assumption 1] — *Impact if wrong: [consequence]*
2. [Assumption 2] — *Impact if wrong: [consequence]*
3. [Assumption 3] — *Impact if wrong: [consequence]*

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Plan] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Plan] |

---

## Timeline

| Milestone | Target Date | Owner |
|-----------|-------------|-------|
| Business understanding complete | [Date] | [Name] |
| Data exploration complete | [Date] | [Name] |
| Data cleaning complete | [Date] | [Name] |
| Analysis complete | [Date] | [Name] |
| Draft review | [Date] | [Name] |
| Final delivery | [Date] | [Name] |

---

## Deliverables

| Deliverable | Format | Audience | Due |
|-------------|--------|----------|-----|
| [Deliverable 1] | [Report/Dashboard/Slides] | [Audience] | [Date] |
| [Deliverable 2] | [Report/Dashboard/Slides] | [Audience] | [Date] |

---

## Sign-Off

**Problem statement approved by:**
- [ ] [Stakeholder 1] — [Date]
- [ ] [Stakeholder 2] — [Date]

**Notes from approval discussion:**
[Any concerns, caveats, or adjustments made]

---

## Next Steps

1. [ ] Proceed to Data Understanding (EDA) phase
2. [ ] Obtain access to [pending data sources]
3. [ ] Schedule [checkpoint meeting] for [date]

---

## Appendix

### Raw Notes from Discovery
[Paste any notes from stakeholder conversations here]

### Reference Documents
- [Link to related doc 1]
- [Link to related doc 2]
```
