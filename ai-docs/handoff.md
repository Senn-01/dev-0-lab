---
version: 0.4.3
updated: 2025-12-16
last-session: added /mcp command for MCP tool reference
rationale: |
  Knowledge enables efficiency. When using MCP tools (Tavily, Context7),
  Claude now has a reference guide with all parameters, costs, and best
  practices. The /mcp command loads this before MCP-heavy work, ensuring
  Claude asks about parameters instead of assuming defaults.
changelog:
  - version: 0.4.3
    changes:
      - Added /mcp command for MCP tool reference
      - Documented Tavily parameters (include_answer, chunks_per_source, etc.)
      - Added credit costs and best practices
      - Behavior directive to ASK before executing MCP tools
  - version: 0.4.2
    changes:
      - Fixed skill-creator name field (lowercase per official spec)
      - Documented allowed-tools frontmatter feature
      - Clarified cookbook vs references terminology
  - version: 0.4.1
    changes:
      - Restored changelog to YAML frontmatter
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

v0.4.3 - Added `/mcp` command. Run before MCP-heavy work to load tool reference with parameters, costs, and best practices.

## Decisions

- **ASK before MCP execution** - /mcp directive instructs Claude to clarify params
- **Lowercase skill names** - Official spec: lowercase, numbers, hyphens only
- **cookbook = references** - Same philosophy, our naming is more evocative
- **Trust Claude for /ship** - no prompts, auto-push

## Gotchas

- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- MCP tools in allowed-tools: unconfirmed if supported
- Tavily advanced search = 2 credits (vs 1 for basic)

## Next

- [ ] Test repo-template in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
