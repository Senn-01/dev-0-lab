# Stakeholder Questions Framework

## The 5W1H Method

Structure your discovery around six fundamental questions. Each must be answered before proceeding.

---

## WHY — Purpose & Motivation

Understanding why this analysis is needed reveals the true problem.

### Questions to Ask

- **Why is this analysis needed now?** (What triggered the request?)
- **Why do you think [problem] is happening?** (Reveals hypotheses to test)
- **Why hasn't this been solved before?** (Uncovers past attempts, constraints)
- **Why is this important to the business?** (Establishes stakes)
- **Why will this analysis change anything?** (Validates actionability)

### Red Flags

- "We just want to see what the data shows" → No clear purpose
- "Management asked for it" → No ownership
- "We've always done this" → May be unnecessary

### Good Answers Sound Like

- "We noticed a 15% drop in retention and need to understand if it's segment-specific"
- "We're deciding between two product strategies and need data to choose"
- "The board needs evidence to approve the expansion budget"

---

## WHAT — Scope & Deliverables

Defining what we're analyzing and what we'll produce.

### Questions to Ask

- **What specific question should this analysis answer?** (The core question)
- **What decision will be made based on this?** (The action)
- **What data do you believe exists for this?** (The inputs)
- **What does success look like?** (The criteria)
- **What have you tried before?** (Previous approaches)
- **What is explicitly out of scope?** (Boundaries)

### Red Flags

- "We want to understand everything about X" → Unbounded scope
- "Whatever you find is fine" → No clear deliverable
- "We don't have data for that" → May be unsolvable

### Good Answers Sound Like

- "We need to identify which customer segments are churning fastest"
- "If churn is above 10%, we'll invest in retention; below, we'll focus on growth"
- "We have CRM data, transaction history, and support tickets"

---

## WHO — Stakeholders & Audience

Identifying who matters for this analysis.

### Questions to Ask

- **Who will use this analysis?** (Primary consumer)
- **Who needs to approve the methodology?** (Validators)
- **Who has context I should talk to?** (Domain experts)
- **Who will be affected by the decisions?** (Impact scope)
- **Who can override conclusions?** (Power dynamics)

### Red Flags

- "Just send it to me" → May not reach decision-maker
- "Everyone" → No prioritization
- "I'll handle the stakeholder" → You're isolated from context

### Good Answers Sound Like

- "The VP of Marketing will present this to the exec team"
- "Talk to Sarah in Customer Success—she knows the edge cases"
- "Finance needs to validate the revenue calculations"

---

## WHEN — Timeline & Deadlines

Understanding temporal constraints and data windows.

### Questions to Ask

- **When do you need results?** (Deadline)
- **When is the decision being made?** (True deadline)
- **When should we check in on progress?** (Cadence)
- **What time period should the data cover?** (Analysis window)
- **When did the problem start?** (Temporal context)

### Red Flags

- "ASAP" → No real deadline
- "Take your time" → Low priority, may get deprioritized
- "Last 5 years" → Probably unnecessary scope

### Good Answers Sound Like

- "Board meeting is March 15, I need draft by March 10"
- "The issue started in Q3, so compare Q2 vs Q3"
- "Let's do a 30-minute check-in on Friday"

---

## WHERE — Data Sources & Systems

Locating the data and understanding its provenance.

### Questions to Ask

- **Where does the data live?** (Systems, databases, files)
- **Where does the data come from originally?** (Source of truth)
- **Where are there known data quality issues?** (Problem areas)
- **Where can I find documentation?** (Data dictionaries)
- **Where have others analyzed this before?** (Prior work)

### Red Flags

- "It's in the data warehouse somewhere" → No clear ownership
- "We manually export it from Excel" → Likely quality issues
- "That system was replaced last year" → Data lineage problems

### Good Answers Sound Like

- "Customer data is in Salesforce, transactions in our Postgres DB"
- "Finance maintains the revenue definitions—here's their doc"
- "Last year's analysis is in the shared drive, folder X"

---

## HOW — Methodology & Constraints

Understanding how to approach the analysis and what limits exist.

### Questions to Ask

- **How will you validate my conclusions?** (Acceptance criteria)
- **How precise does this need to be?** (Accuracy requirements)
- **How should results be presented?** (Format preferences)
- **How will you handle findings you disagree with?** (Conflict resolution)
- **How much can I question the premise?** (Freedom to challenge)

### Red Flags

- "Just make it look good" → Decoration, not analysis
- "We need exact numbers" → Unrealistic precision expectations
- "Don't question the strategy" → You're just validating a decision

### Good Answers Sound Like

- "I'll review methodology with our data team before presenting up"
- "Directional is fine—within 10% is good enough"
- "If you find our assumptions are wrong, I want to know"

---

## Question Sequencing

### Opening Questions
Start broad, then narrow:
1. "Tell me about the business context—what's happening?"
2. "What's the specific question you're trying to answer?"
3. "What will you do differently based on the answer?"

### Probing Questions
Go deeper on vague answers:
- "Can you give me an example?"
- "What would that look like specifically?"
- "How would you know if that's true?"

### Closing Questions
Confirm understanding:
- "Let me play back what I heard..."
- "What did I miss?"
- "If I had to summarize in one sentence, would it be...?"

---

## Template: Problem Statement

After all questions, synthesize into this format:

```
We need to [ANALYSIS TYPE] in order to [DECISION/ACTION]
because [BUSINESS CONTEXT/TRIGGER].

Success means [MEASURABLE OUTCOME].

The analysis will cover [SCOPE] using [DATA SOURCES]
and is needed by [DEADLINE] for [AUDIENCE].

Key assumptions:
- [ASSUMPTION 1]
- [ASSUMPTION 2]

Out of scope:
- [EXCLUSION 1]
- [EXCLUSION 2]
```
