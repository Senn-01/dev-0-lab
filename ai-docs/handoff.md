---
version: 0.4.2
updated: 2025-12-16
last-session: aligned skill-creator with official Anthropic standards
rationale: |
  Quality over speed. After researching official Anthropic docs, we found
  our skill-creator needed alignment: name field must be lowercase,
  allowed-tools feature was undocumented, and terminology differences
  (cookbook vs references) needed clarification. Now exhaustive without
  being complex.
changelog:
  - version: 0.4.2
    changes:
      - Fixed skill-creator name field (lowercase per official spec)
      - Documented allowed-tools frontmatter feature
      - Clarified cookbook vs references terminology
      - Added reference to official Anthropic scripts
  - version: 0.4.1
    changes:
      - Restored changelog to YAML frontmatter
      - Added rationale field for version bumps
      - Automated /ship (no prompts, auto-push)
  - version: 0.4.0
    changes:
      - Added examples/repo-template/ starter kit
      - Added /handoff, /commit, /ship workflow commands
  - version: 0.3.0
    changes:
      - Added skill-creator meta-skill (IndyDevDan methodology)
  - version: 0.2.0
    changes:
      - Added examples/algorithmic-art/ (Neural Bloom)
  - version: 0.1.0
    changes:
      - Forked from disler/fork-repository-skill
      - Added osascript, hooks skills
---

# Handoff

## Now

v0.4.2 - Skill-creator aligned with official Anthropic standards. Researched docs, fixed gaps, documented differences.

## Decisions

- **Lowercase skill names** - Official spec: lowercase, numbers, hyphens only
- **allowed-tools documented** - Security feature for restricting tool access
- **cookbook = references** - Same philosophy, our naming is more evocative
- **Coaching > automation** - We explain; official scripts scaffold
- **Trust Claude for /ship** - no prompts, auto-push

## Gotchas

- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- MCP tools in allowed-tools: unconfirmed if supported
- `/ship` pushes automatically - use `/commit` if you want control

## Next

- [ ] Test repo-template in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
