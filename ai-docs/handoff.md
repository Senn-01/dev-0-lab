---
version: 0.6.1
updated: 2025-12-19
last-session: added /md command for LLM-readable markdown generation
rationale: |
  Consistent markdown formatting requires explicit guidance. The /md command
  enforces user preferences: YAML frontmatter (rationale, changelog, linked_files),
  IDKW style (front-load info, no vague pronouns, structured formats), and
  hierarchical headings. Research confirmed structured formats optimal for LLM input.
changelog:
  - version: 0.6.1
    changes:
      - Added /md command for LLM-readable markdown generation
      - Research doc on LLM-readable markdown patterns
      - IDKW style principles documented
      - YAML frontmatter schema (rationale, changelog, linked_files)
      - Clarified prose vs structure (OUTPUT vs INPUT distinction)
  - version: 0.6.0
    changes:
      - Added data-analyst skill (5th skill)
      - 4-phase workflow: understand → explore → clean → validate
      - Philosophy.md with core analyst principles (always read)
      - WHY-first pattern in every phase
      - Commands: /data-understand, /data-explore, /data-clean, /data-validate
      - 17 cookbook files covering techniques, checklists, code patterns
      - Outputs to ai-docs/data-{phase}-{project}.md
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

v0.6.1 - Added **/md command** for LLM-readable markdown. Researched optimal patterns: IDKW style, structured formats (lists/tables), YAML frontmatter with rationale/changelog. Key insight: "prose preference" applies to LLM OUTPUT, not INPUT docs.

## Decisions

- **IDKW style** - Front-load info, no vague pronouns, structured formats
- **Structured > prose for INPUT** - Lists, tables, headings for LLM-readable docs
- **YAML frontmatter standard** - rationale, changelog (semver 0.1.0+), linked_files
- **WHY-first pattern** - Every phase explains principles before actions
- **Philosophy hub** - `cookbook/philosophy.md` read before any phase
- **Skill + thin commands** - Skill centralizes logic, commands are entry points
- **Outputs to ai-docs/** - `ai-docs/data-{phase}-{project}.md` format
- **Research before implementation** - /research produces understanding docs
- **Specialized agents** - Concept, Docs, Examples, Ecosystem researchers
- **ULTRATHINK for strategy** - Deep reasoning with backpropagation
- **Lowercase skill names** - Official spec: lowercase, numbers, hyphens only

## Gotchas

- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- MCP tools in allowed-tools: unconfirmed if supported
- Tavily advanced search = 2 credits (vs 1 for basic)
- /research outputs to `ai-docs/research-{topic-slug}.md`
- /data-* commands output to `ai-docs/data-{phase}-{project}.md`

## Next

- [ ] Test data-analyst skill on real dataset
- [ ] Add data-analyst to examples/repo-template/
- [ ] Test repo-template in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
