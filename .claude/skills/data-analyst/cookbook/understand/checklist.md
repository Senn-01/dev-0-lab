# Business Understanding Checklist

Use this checklist to ensure thorough problem definition before touching data.

---

## Phase 1: Initial Discovery

### Stakeholder Identification
- [ ] Identified the primary decision-maker
- [ ] Listed all stakeholders who will consume the analysis
- [ ] Identified domain experts to consult
- [ ] Documented each stakeholder's specific interests

### Problem Framing
- [ ] Asked "why" at least 3 times to get to root problem
- [ ] Distinguished between symptom and cause
- [ ] Clarified if this is diagnostic, predictive, or prescriptive
- [ ] Confirmed this is an analysis problem (not a data engineering or reporting problem)

### Context Gathering
- [ ] Understood the business context triggering this request
- [ ] Learned about previous attempts to solve this
- [ ] Identified any existing hypotheses stakeholders have
- [ ] Documented any recent changes (pricing, product, market) that might matter

---

## Phase 2: Scope Definition

### Boundaries
- [ ] Defined what IS in scope (specific and measurable)
- [ ] Defined what is NOT in scope (explicit exclusions)
- [ ] Agreed on time period for analysis
- [ ] Agreed on geographic/segment/product scope

### Success Criteria
- [ ] Defined what "done" looks like
- [ ] Established measurable success criteria
- [ ] Agreed on how conclusions will be validated
- [ ] Set expectations for precision/confidence level

### Decision Context
- [ ] Identified the specific decision this informs
- [ ] Documented what options are being considered
- [ ] Defined what threshold would change the recommendation
- [ ] Confirmed stakeholder will act on findings

---

## Phase 3: Data Landscape

### Data Identification
- [ ] Listed all potentially relevant data sources
- [ ] Confirmed access to each data source
- [ ] Identified data owner/steward for each source
- [ ] Documented data refresh frequency

### Data Understanding (Preliminary)
- [ ] Located data dictionaries or documentation
- [ ] Identified known data quality issues
- [ ] Understood key business definitions (e.g., what is a "customer"?)
- [ ] Noted any data transformations already applied

### Gaps & Risks
- [ ] Identified data that would be helpful but doesn't exist
- [ ] Assessed impact of missing data on conclusions
- [ ] Documented assumptions about data quality
- [ ] Planned for how to handle data limitations

---

## Phase 4: Planning

### Timeline
- [ ] Confirmed final deadline
- [ ] Set intermediate check-in points
- [ ] Built buffer for unexpected issues
- [ ] Aligned on communication cadence

### Deliverables
- [ ] Agreed on output format (report, dashboard, presentation)
- [ ] Defined level of detail required
- [ ] Planned how findings will be presented
- [ ] Identified who reviews before final delivery

### Resources
- [ ] Confirmed analyst capacity
- [ ] Identified any external dependencies
- [ ] Secured necessary access/permissions
- [ ] Allocated time for stakeholder reviews

---

## Phase 5: Documentation

### Problem Statement Document
- [ ] Written single-sentence problem statement
- [ ] Documented all 5W1H answers
- [ ] Listed explicit assumptions
- [ ] Listed explicit exclusions

### Stakeholder Alignment
- [ ] Shared problem statement with stakeholders
- [ ] Received explicit agreement on scope
- [ ] Documented any disagreements or concerns
- [ ] Obtained sign-off to proceed

---

## Exit Criteria

**You are ready to move to Data Understanding (EDA) when:**

1. You can state the problem in one clear sentence
2. You know what decision this analysis will inform
3. You know what data you need and have access to it
4. You have documented scope boundaries
5. Stakeholders have agreed on the problem definition
6. You have a realistic timeline with check-ins

**If ANY of these are missing, do not proceed.** Go back and fill the gap.

---

## Anti-Patterns to Avoid

### "Let's just start and see"
Analysis without direction is exploration. Exploration is fine for learning, but stakeholders expect answers. Define the question first.

### "We can adjust scope later"
Scope creep is the #1 killer of data projects. Get agreement NOW, in writing, before work begins.

### "The data will tell us what to ask"
Data tells you nothing. You ask questions; data provides evidence. Without questions, you're just counting.

### "I'll figure out the data as I go"
Understanding data sources is part of this phase, not the next. If you don't know what data exists, you can't bound the problem.

### "The stakeholder knows what they want"
They often don't. Your job is to help them articulate it. Push for specificity.
