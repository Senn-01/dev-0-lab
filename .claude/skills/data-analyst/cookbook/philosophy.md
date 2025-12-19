# Core Philosophy of Data Analysis

> Read this BEFORE every phase. These principles govern ALL data work.

## The Fundamental Truth

**Data does not speak for itself.**

Data is inert. It has no opinions, no recommendations, no insights. YOU give it meaning through context, interpretation, and translation. A number in a spreadsheet is just a number until a human decides what it represents and why it matters.

This is why the analyst's job is not to "find insights in data" but to **answer business questions using data as evidence**.

---

## The Three Questions

Before ANY analysis, you must be able to answer:

### 1. What decision will this analysis inform?

If you cannot name a specific decision, stop. Analysis without a decision target is just curiosity dressed as work. Someone, somewhere, will use your output to choose between options. Know what those options are.

**Bad**: "We want to understand customer behavior"
**Good**: "We need to decide whether to invest in retention or acquisition"

### 2. What would change your recommendation?

Define the threshold BEFORE you analyze. If churn is above X%, you'll recommend Y. If below, Z. This prevents post-hoc rationalization where you massage findings to match your preconceptions.

**Bad**: "Let's see what the data shows"
**Good**: "If NPS drops below 30, we'll prioritize UX fixes over new features"

### 3. How will you know if you're wrong?

Every analysis has assumptions. State them explicitly. Define what evidence would prove your conclusions incorrect. If nothing could disprove you, you're not doing analysis—you're doing confirmation.

---

## The Hierarchy of Data Problems

Not all data problems are equal. Solve them in this order:

```
1. WRONG DATA       → You're answering the wrong question
2. MISSING DATA     → You can't answer the question
3. DIRTY DATA       → Your answer might be wrong
4. SLOW DATA        → Your answer comes too late
5. UGLY DATA        → Your answer is hard to understand
```

Most analysts obsess over levels 3-5 while ignoring 1-2. Don't clean data until you're sure it's the RIGHT data. Don't optimize queries until you're sure they answer the RIGHT question.

---

## The Analyst's Oath

When you sit down with data, commit to these:

### I will seek to be wrong

The goal is truth, not validation. Actively search for evidence that contradicts your hypothesis. The most valuable finding is often "we were wrong about this."

### I will state my assumptions

Every number comes with asterisks. Make them explicit. "This assumes the sample is representative." "This assumes linear relationships." Hidden assumptions become hidden failures.

### I will not torture the data

Given enough manipulation, any dataset will confess to anything. P-hacking, cherry-picking, and selective reporting are not analysis—they're fraud. If the story isn't in the data, say so.

### I will translate, not just report

A table of numbers is not insight. Your job is to say "this means X, and you should do Y because Z." Executives don't want data; they want recommendations backed by data.

### I will admit uncertainty

"I don't know" is a valid answer. "The data is insufficient to conclude" is valuable information. False confidence is worse than acknowledged ignorance.

---

## The Data Quality Paradox

**The cleaner you want your data, the more you must understand it dirty.**

You cannot know what "clean" means without first understanding:
- What makes it dirty?
- Why is it dirty?
- What impact does the dirt have?
- What will you lose by cleaning it?

This is why EDA comes BEFORE cleaning. You must diagnose before you treat.

---

## The 80/20 of Data Work

| Activity | Time Spent | Value Created |
|----------|-----------|---------------|
| Understanding the problem | 20% | 50% |
| Getting & cleaning data | 60% | 30% |
| Analysis & modeling | 15% | 15% |
| Presenting results | 5% | 5% |

Most analysts invert this. They rush through problem definition, spend weeks cleaning data they don't fully understand, run fancy models on garbage inputs, and wonder why stakeholders ignore their beautifully formatted PowerPoints.

**The fix**: Spend more time understanding, less time doing.

---

## Red Flags in Data Work

Stop and reassess if you notice:

- **"The data shows what we expected"** → Confirmation bias likely
- **"We just need more data"** → Problem is probably in the question, not quantity
- **"The outliers are just noise"** → Outliers often ARE the story
- **"This is obvious from the data"** → If it's obvious, why did we need analysis?
- **"The model is 99% accurate"** → Probably leakage or target encoding
- **"Trust me, I've seen this before"** → Experience without evidence is bias

---

## The Output Test

Before delivering any analysis, ask:

1. **Can a decision-maker act on this?** (If not, it's trivia)
2. **Would I bet my job on this conclusion?** (If not, state the uncertainty)
3. **Could I explain this to a smart 10-year-old?** (If not, simplify)
4. **What would make this wrong?** (If nothing, you're overconfident)

---

## Remember

You are not a SQL monkey. You are not a Python script. You are not a report generator.

You are a translator between the messy world of data and the clear world of decisions. Act accordingly.
