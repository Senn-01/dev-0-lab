---
version: 0.9.0
updated: 2025-12-22
last-session: completed full data-analyst workflow on Orange CX Intelligence
rationale: |
  Completed all 4 phases of data-analyst skill on real Orange Belgium customer feedback
  data. Produced 3 BigQuery-ready tables (dim_shops, fact_google_reviews, fact_sms_surveys).
  Discovered and solved multiple real-world data issues: MOBIS case mismatch, CSV multiline
  parsing failures, incomplete shop master data. Data certified at 99.9% quality.
changelog:
  - version: 0.9.0
    changes:
      - Completed full 4-phase data-analyst workflow (understand → explore → clean → validate)
      - Created 3 clean tables: dim_shops (161), fact_google_reviews (1,815), fact_sms_surveys (5,268)
      - Built validation gate with 4 quality dimensions (completeness, uniqueness, validity, consistency)
      - Data certified at 99.9% quality score (threshold 95%)
      - Discovered CSV multiline text breaks BigQuery - switched to JSONL format
      - Fixed MOBIS code case mismatch (mobis467 vs MOBIS467)
      - Inferred language from Belgian postal codes (100% coverage)
      - Documented 28 MOBIS codes in SMS not in shop master (data gap)
      - Created eda_orange_cx.py, clean_orange_cx.py, validate_orange_cx.py scripts
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

v0.9.0 - **Completed full data-analyst workflow** on Orange CX Intelligence. All 4 phases done:

| Phase | Output | Key Finding |
|-------|--------|-------------|
| /data-understand | Business context, star schema design | "Clean Sheets" approach (restructure source, not transform layer) |
| /data-explore | EDA report, quality issues | 37.5% shops CLOSED (filter out), 78% verbatims empty |
| /data-clean | 3 clean tables (dim_shops, fact_google_reviews, fact_sms_surveys) | MOBIS case mismatch fixed, language inferred from zip |
| /data-validate | Quality certificate (99.9%) | 24 dupe review_ids, 3 null ratings documented |

**Tables ready for BigQuery** (JSONL format - CSV had multiline parsing issues).

## Data Analyst Methodology (Proven on Orange CX)

### The 4-Phase Workflow

```
/data-understand → /data-explore → /data-clean → /data-validate
      ↓                 ↓                ↓              ↓
   Problem           EDA report      Clean tables   Certificate
   definition        + issues        + scripts      + gate
```

### Key Principles

| Principle | Implementation |
|-----------|----------------|
| **WHY before HOW** | Every phase reads `cookbook/philosophy.md` first |
| **Diagnose before treat** | EDA must complete before cleaning decisions |
| **Conservative cleaning** | Flag rather than delete when uncertain |
| **Validation gate** | 95% threshold per dimension blocks bad data |
| **Full audit trail** | Every operation logged with before/after counts |

### Output Structure

```
ai-docs/
├── data-understand-{project}.md   # Business context
├── data-explore-{project}.md      # EDA findings
├── data-clean-{project}.md        # Cleaning decisions
└── data-validate-{project}.md     # Quality certificate

cases/{project}/
├── eda_{project}.py               # EDA script
├── clean_{project}.py             # Cleaning pipeline
├── validate_{project}.py          # Validation gate
└── clean_output/
    ├── dim_*.csv/jsonl            # Dimension tables
    └── fact_*.csv/jsonl           # Fact tables
```

---

## Painpoints & Solutions (Orange CX Case Study)

### Painpoint 1: MOBIS Code Case Mismatch

**Problem**: id_business had `mobis467` (lowercase), SMS had `MOBIS467` (uppercase). Join only matched 30%.

**Solution**: Normalize to uppercase in cleaning script.
```python
dim_shops['mobis_code'] = dim_shops['mobis_code'].str.upper()
```
**Result**: Join improved from 30% → 64%.

---

### Painpoint 2: CSV Multiline Text Breaks BigQuery

**Problem**: Google Reviews verbatim field had embedded `\n` newlines. BigQuery CSV parser error: "too many errors, giving up".

**Solution**: Export as JSONL (JSON Lines) instead of CSV.
```python
df.to_json('table.jsonl', orient='records', lines=True)
```
**Result**: JSONL loads cleanly - newlines escaped as `\n` in JSON strings.

---

### Painpoint 3: Incomplete Shop Master

**Problem**: id_business had 161 shops, but SMS surveys referenced 28 additional MOBIS codes. 1,218 SMS records couldn't be mapped.

**Solution**: Accept partial coverage, flag with `is_mappable` boolean.
- 63.8% SMS → dim_shops (full context)
- 36.2% SMS kept with NULL shop_id (analyze by channel/MOBIS)

**Lesson**: Master data is rarely complete. Design for graceful degradation.

---

### Painpoint 4: Language Field 72% Empty

**Problem**: IAM-Language column sparse. Needed language for SQL agent prompts.

**Solution**: Infer from Belgian postal codes:
```python
def infer_language_from_zip(zipcode):
    if 1000 <= z <= 1299: return 'BI'  # Brussels bilingual
    if 4000 <= z <= 7999: return 'FR'  # Wallonia
    else: return 'NL'  # Flanders
```
**Result**: 100% language coverage.

---

### Painpoint 5: CLOSED Shops Polluting Master Data

**Problem**: full_shop_infos had 2,224 rows but 835 (37.5%) were Macro-Segment = "CLOSED" (defunct businesses).

**Solution**: Filter early in cleaning pipeline.
```python
shop_info_active = shop_info[shop_info['macro_segment'] != 'CLOSED']
```
**Lesson**: EDA reveals what "clean" means. CLOSED was a business status, not a flag error.

---

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
- **JSONL over CSV for BigQuery** - Multiline text fields break CSV parsing

## Gotchas

### General
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

### Data Analyst Specific
- **CSV multiline fields break BigQuery** → use JSONL format
- **MOBIS codes may have case variance** → always normalize to uppercase
- **Shop master data often incomplete** → design for NULL foreign keys
- **"CLOSED" in master data = defunct** → filter early, not an error flag
- **Belgian zip codes map to language** → 1000-1299=BI, 4000-7999=FR, else=NL
- **Validation gate catches cleaning misses** → 24 dupes, 3 nulls found post-clean
- **Temporal validation needs UTC** → `pd.to_datetime(..., utc=True)` for tz-aware comparison

## Next

- [x] Test data-analyst skill on real dataset (Orange CX Intelligence)
- [x] Complete /data-explore phase for Orange CX project
- [x] Complete /data-clean phase for Orange CX project
- [x] Complete /data-validate phase for Orange CX project
- [x] Export to JSONL for BigQuery (CSV had multiline issues)
- [ ] **Create `/data-llm` command** - Prepare LLM to understand data structure
  - Generate schema documentation for SQL agent
  - Include: table relationships, column meanings, join keys
  - Include: known data gaps (28 unmapped MOBIS, 36% SMS unlinked)
  - Include: query patterns (time filtering, shop aggregation)
  - Output: `ai-docs/data-llm-{project}.md` for agent context injection
- [ ] Load JSONL files to BigQuery and test queries
- [ ] Add data-analyst to examples/repo-template/
- [ ] Test repo-template in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
