---
version: 0.8.1
updated: 2025-12-22
last-session: tested data-analyst skill on Orange CX Intelligence project
rationale: |
  First real-world test of data-analyst skill. Ran /data-understand on Orange Belgium
  customer feedback data (Google Reviews + SMS Surveys). Produced comprehensive business
  understanding doc with header quality assessment, column mappings, and implementation
  plan for clean Google Sheets → BigQuery pipeline.
changelog:
  - version: 0.8.1
    changes:
      - Tested data-analyst skill on real Orange CX Intelligence dataset
      - Created ai-docs/research-bigquery-csv.md (BigQuery CSV loading best practices)
      - Created ai-docs/data-understand-orange-cx-intelligence.md
      - Added header quality assessment with BigQuery naming best practices
      - Designed 3-table star schema (dim_shops, fact_google_reviews, fact_sms_surveys)
      - Decided on "Clean Sheets" approach (restructure source vs transform layer)
      - Added cases/ to .gitignore for test data
  - version: 0.8.0
    changes:
      - Added LangSmith tracing via ~/.claude/hooks/stop_hook.sh
      - Traces sent to LangSmith after each Claude response
      - Hierarchical run structure (turn → LLM calls → tool calls)
      - State persistence across sessions (~/.claude/state/)
      - Configurable via TRACE_TO_LANGSMITH, CC_LANGSMITH_API_KEY, CC_LANGSMITH_PROJECT
      - macOS only (requires jq, curl, uuidgen)
      - Fixed: mkdir -p now runs before first log() call
  - version: 0.7.0
    changes:
      - Enhanced skill-creator with official Anthropic patterns
      - Added description writing guidance (front-load 100 chars, action verbs)
      - Integrated allowed-tools into planning workflow
      - Created 5-debug.md debugging cookbook
      - Added limitations section (no skill chains, no persistent state)
      - Added tool pattern quick-reference (read-only, script, generation)
      - Synced all changes to examples/repo-template/
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

v0.8.1 - **Tested data-analyst skill** on Orange CX Intelligence project. Ran /data-understand phase on real customer feedback data (4 CSVs: Google Reviews, SMS Surveys, Shop Master, Full Shop Info). Produced comprehensive business understanding doc with header quality assessment, column mappings, and implementation plan. Decided on "Clean Sheets" approach: restructure client's Google Sheets into clean 3-tab format that maps directly to BigQuery (no transformation layer).

## Decisions

- **LangSmith tracing via Stop hook** - Observability layer for Claude Code sessions
- **Env var control** - TRACE_TO_LANGSMITH=true enables, CC_LANGSMITH_API_KEY for auth
- **Description is PRIMARY trigger** - Front-load first 100 chars, use action verbs
- **allowed-tools in planning** - Decide tool access level during Step 1 (Plan)
- **5-step skill workflow** - Plan → Structure → Implement → Verify → Debug
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

- LangSmith hook requires `~/.claude/state/` dir (auto-created by script)
- LangSmith hook macOS only (needs jq, curl, uuidgen)
- Set CC_LANGSMITH_DEBUG=true for hook debugging in `~/.claude/state/hook.log`
- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- MCP tools in allowed-tools: unconfirmed if supported
- Tavily advanced search = 2 credits (vs 1 for basic)
- /research outputs to `ai-docs/research-{topic-slug}.md`
- /data-* commands output to `ai-docs/data-{phase}-{project}.md`
- Skills cannot invoke other Skills (no skill chains)
- No persistent state between skill invocations
- Description length impacts activation accuracy

## Next

- [x] Test data-analyst skill on real dataset (Orange CX Intelligence)
- [ ] Complete /data-explore phase for Orange CX project
- [ ] Write migration script for clean Google Sheets
- [ ] Add data-analyst to examples/repo-template/
- [ ] Test repo-template in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
