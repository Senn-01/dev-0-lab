# Update Handoff Document

User hint: $ARGUMENTS

## Your Task

Update `ai-docs/handoff.md` to reflect current project state for the next Claude instance.

## Workflow

1. **Gather context:**
   - Read current `ai-docs/handoff.md`
   - Run `git status` to see uncommitted changes
   - Run `git diff --stat HEAD~3` to see recent file changes
   - Run `git log --oneline -5` for recent commits
   - Use user's hint (if provided) as directional guidance

2. **Infer what happened:**
   - What files changed and why?
   - What's the current state of the project?
   - What decisions were made?
   - What's unfinished or next?

3. **Update the handoff doc:**
   - Set `updated:` to today's date
   - Set `last-session:` to brief summary of this work
   - Update `## Now` with current state
   - Add any new decisions to `## Decisions`
   - Add any discovered gotchas to `## Gotchas`
   - Update `## Next` with current priorities

## Format

Keep it SHORT. The next Claude can explore - this doc is for context that's NOT obvious from code.

```markdown
---
updated: YYYY-MM-DD
last-session: brief description
---

# Handoff

## Now
2-3 lines. Current state. What's in progress.

## Decisions
- Why X over Y (not what - why)
- User preferences
- Constraints

## Gotchas
- Things that will bite you
- Non-obvious requirements

## Next
- [ ] Prioritized tasks
- [ ] What's blocked
```

## Rules

- Don't duplicate README content
- Don't list all files (git does that)
- Focus on WHY, not WHAT
- Be concise - 30 useful lines > 300 stale lines
- If no handoff.md exists, create it
