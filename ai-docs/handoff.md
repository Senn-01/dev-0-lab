---
updated: 2025-12-16
last-session: added repo-template and workflow commands
---

# Handoff

## Now

v0.4.0 - Added `examples/repo-template/` as a starter kit for new repos. Created workflow commands: `/handoff`, `/commit`, `/ship`.

## Decisions

- **Conventional commits** - Using standard types (feat, fix, docs, refactor, chore) for git log as changelog
- **Handoff structure** - Short and fresh > comprehensive and stale. Focus on WHY not WHAT
- **Command philosophy** - Granular (`/handoff`, `/commit`) + combined (`/ship`) for flexibility
- **macOS only** - Hooks use osascript, no cross-platform needed

## Gotchas

- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger from conversation, no `/command` needed
- Handoff.md format changed - now simpler (Now, Decisions, Gotchas, Next)

## Next

- [ ] Test repo-template in fresh repo
- [ ] Consider global installation `~/.claude/skills/`
- [ ] Add PreToolUse validation hooks cookbook

## Structure

```
.claude/
├── commands/
│   ├── prime.md       # Understand codebase
│   ├── handoff.md     # Update LLM context
│   ├── commit.md      # Conventional commit
│   └── ship.md        # Full workflow
├── hooks/             # Notification scripts
├── settings.json      # Hooks config
└── skills/            # 4 skills

examples/
├── algorithmic-art/   # Neural Bloom (p5.js)
└── repo-template/     # Starter kit for new repos
```

## Files Changed (v0.4.0)

- `examples/repo-template/` - NEW: 25 files (starter template)
- `.claude/commands/handoff.md` - NEW: update LLM context
- `.claude/commands/commit.md` - NEW: conventional commits
- `.claude/commands/ship.md` - NEW: full workflow
- `ai-docs/handoff.md` - Simplified format
