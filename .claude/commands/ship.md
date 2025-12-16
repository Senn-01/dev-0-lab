# Ship

User hint: $ARGUMENTS

## Your Task

Complete shipping workflow: update docs → commit → optionally push.

## Workflow

### Step 1: Update Handoff

Run the `/handoff` workflow:
1. Read current `ai-docs/handoff.md`
2. Run `git status`, `git diff --stat HEAD~3`, `git log --oneline -5`
3. Infer what changed, update handoff with current state
4. Use user hint if provided

### Step 2: Check README

Evaluate if README.md needs updates:
- New features added? → Update features section
- New commands added? → Update commands table
- New skills added? → Update skills section
- Structure changed significantly? → Update structure

**Ask user:** "README changes detected. Update? [Y/n]"
- If yes, make minimal targeted updates
- If no, skip

### Step 3: Stage Changes

```bash
git add -A
```

Show what will be committed.

### Step 4: Commit

Run the `/commit` workflow:
1. Analyze staged changes
2. Generate conventional commit message:
   ```
   type(scope): description

   [body if needed]
   ```
3. **Show for approval** - never auto-commit
4. On approval, commit

### Step 5: Push (Optional)

Ask: "Push to origin? [y/N]"
- If yes, push
- If no, done

## Conventional Commit Types

| Type | Use for |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Docs only |
| `refactor` | Code restructure |
| `chore` | Maintenance |

## Rules

- Always show what you're doing at each step
- Never auto-commit - require explicit approval
- Keep README updates minimal and targeted
- If nothing changed, say so and exit early
- User hint guides the narrative but infer from actual changes
