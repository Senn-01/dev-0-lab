---
version: 0.5.0
updated: 2025-12-16
last-session: added /research command for deep external research
rationale: |
  Research before implementation prevents wasted effort. The /research command
  provides structured knowledge acquisition with specialized agents (Concept,
  Docs, Examples, Ecosystem researchers), ULTRATHINK strategy phase, approval
  gates for deep research, and comprehensive output to ai-docs/research-{topic}.md.
  Inspired by research-code.md patterns: read-first discipline, wait-for-all,
  metadata tracking, follow-up handling.
changelog:
  - version: 0.5.0
    changes:
      - Added /research command for deep external research
      - ULTRATHINK phase for strategy with backpropagation thinking
      - Specialized agents (Concept, Docs, Examples, Ecosystem)
      - Conditional approval gate (quick vs deep research)
      - Structured output with metadata and query tracking
      - Follow-up handling (append to same doc)
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

v0.5.0 - Added `/research` command for deep external research before implementation. Uses specialized agents, ULTRATHINK strategy, approval gates.

## Decisions

- **Research before implementation** - /research produces understanding docs
- **Specialized agents** - Concept, Docs, Examples, Ecosystem researchers
- **ULTRATHINK for strategy** - Deep reasoning with backpropagation
- **Conditional approval** - Quick (<3 queries) auto-executes, deep requires approval
- **ASK before MCP execution** - /mcp directive instructs Claude to clarify params
- **Lowercase skill names** - Official spec: lowercase, numbers, hyphens only

## Gotchas

- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- MCP tools in allowed-tools: unconfirmed if supported
- Tavily advanced search = 2 credits (vs 1 for basic)
- /research outputs to `ai-docs/research-{topic-slug}.md`

## Next

- [ ] Test /research command with real topic
- [ ] Test repo-template in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
