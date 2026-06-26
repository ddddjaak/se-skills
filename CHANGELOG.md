# Changelog

All notable changes to the SE Skills project will be documented in this file.

## [Unreleased]

### Added
（暂无 — 下一个版本的变更将在此记录）

## [2.0.0] — 2026-06-26

### Added

**MCP Server Integration (3 new servers via `.mcp.json`):**

- **draw.io MCP (`@drawio/mcp`)** — official jgraph MCP server for architecture diagram generation
  - Supports Mermaid.js, XML, and CSV input formats
  - Generates flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, and more
  - Auto-installs via `npx -y @drawio/mcp` on first use — no manual setup required
  - Resolved after two iterations: `drawio-mcp` v1.6.0 (Sujimoshi) crashed on Node.js 24 due to JSDOM `navigator` getter incompatibility; `diagram-master` was limited to flowchart type only; `@drawio/mcp` is the definitive solution

- **Visio MCP (`office-visio-mcp-server`)** — professional `.vsdx` diagram generation for user manuals
  - Supports: create/open `.vsdx` files, add shapes (rectangle, circle, diamond, etc.), connect shapes with dynamic/straight/curved connectors, add text to shapes, list shapes, export images
  - Portable entry point: `python -c "from visio_mcp_server.visio_server import main; main()"` — no hardcoded paths
  - Requires: Windows + Microsoft Visio installed + `pip install office-visio-mcp-server`
  - Use case: formal documentation deliverables (user manuals, datasheets) requiring Visio-format diagrams

- **Engineering Math MCP (`gnomon-mcp`)** — calculation engine for MCU datasheet work
  - `calc()`: Python math expressions (sqrt, sin, cos, log, pi, e, statistics functions)
  - `calc_convert()`: unit conversion via Pint (meter↔foot, Celsius↔Fahrenheit, voltage/current/power units)
  - `calendar()`: date math, business day calculations
  - `now()`: current date/time in multiple formats
  - Windows compatible: `mcp-mathematics` failed on Windows (`resource` module Unix-only); `gnomon-mcp` works cross-platform
  - Use cases: SNR calculation, power budget (P = V × I), thermal analysis (T_j = T_ambient + P × θ_JA), timing calculations, baud rate error, pull-up resistor sizing

**SessionStart Hook System:**

- `hooks/hooks.json`: SessionStart hook registration — mirrors ae-skills pattern
  - Triggers on every new Claude Code session (not `/reload-plugins`)
  - Executes `bash ${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh`
- `hooks/session-start.sh`: injects the `using-se-skills` meta-skill content at session start
  - Reads `skills/using-se-skills/SKILL.md` and outputs JSON with `priority: "IMPORTANT"`
  - Requires `jq` on PATH for JSON construction; graceful fallback with INFO message if missing
  - Result: every new session auto-activates the SE pipeline conductor (phase detection, guided workflow)
  - Verified: `2 hooks` in `/reload-plugins` output (1 ae-skills + 1 se-skills)

**4-Channel Document Preprocessing Pipeline:**

- `scripts/preprocess_pdf.py` (709 lines): PDF → structured text + tables + figures
  - Text extraction via PyMuPDF (fitz), OCR fallback via Tesseract
  - Table extraction with quality scoring, figure extraction with metadata
- `scripts/preprocess_xlsx.py` (575 lines): Excel → markdown tables
  - Sheet-by-sheet conversion, merged cell forward-fill, header row detection
- `scripts/preprocess_docx.py` (476 lines): Word → heading hierarchy + paragraph + table + image extraction
  - Preserves document structure (headings → outline), table border/style metadata
- `scripts/preprocess_pptx.py` (412 lines): PowerPoint → slide text + speaker notes + embedded images
  - Slide-by-slide extraction, shape type detection, notes preservation
- `scripts/extract_figures.py` (214 lines): Shared figure extraction with quality scoring
- `scripts/extract_tables.py` (206 lines): Shared table extraction with false-positive detection
- `scripts/requirements.txt` (26 lines): 10 Python dependencies (PyMuPDF, Pillow, pytesseract, openpyxl, python-docx, python-pptx, pandas, tabula-py, camelot-py, pdfplumber)
- All 4 channels include `--verify` mode for automated quality scoring:
  - Text density check, OCR quality assessment, garbled character detection, table false-positive filtering, empty slide detection
- Integration: `skills/requirements-decompose/SKILL.md` Step 0 PREPROCESS covers all 4 input types (~200 lines added)
- `references/`: 4 processing guides extracted from document-skills patterns:
  - `pdf-processing-guide.md` (222 lines)
  - `spreadsheet-processing-guide.md` (199 lines)
  - `docx-processing-guide.md` (195 lines)
  - `pptx-processing-guide.md` (176 lines)

### Changed

**`requirements-decompose` SKILL.md:**
- Added Step 0 PREPROCESS section (~200 lines): automatic document ingestion pipeline
  - PDF → requirements extraction with OCR fallback
  - DOCX → heading-structured requirement parsing
  - PPTX → slide-by-slide requirement identification
  - XLSX → sheet-based requirement matrix extraction
- Document preprocessing step runs before formal requirement decomposition

### Fixed

**16 findings from comprehensive project audit (4 review rounds):**

CRITICAL fixes (breaking Pipeline/Goal Mode phase detection):
- Output path unification: `docs/specs/` → `docs/spec/` across 6 files (4 spec-producing skills, 2 commands, traceability-matrix)
  - `spec-authoring/SKILL.md`, `hardware-detailed-design/SKILL.md`, `software-detailed-design/SKILL.md`, `algorithm-design/SKILL.md`
  - `.claude/commands/se-spec.md`, `skills/traceability-matrix/SKILL.md`
  - Root cause: skills wrote to `docs/specs/` but pipeline conductor checked `docs/spec/` — automatic phase detection silently skipped the Document phase

HIGH fixes:
- `design-review/SKILL.md`: filled empty "See Also" section with 4 reference checklists (system-design-review, hw-design-review, sw-design-review, testability-review)
- Added Pipeline Mode guidance text to 11 skills that were missing it (now 15/16 skills have guidance; `using-se-skills` is the conductor itself)
  - `requirements-decompose`, `architecture-design`, `software-architecture-design`, `hardware-architecture-design`
  - `spec-authoring`, `software-detailed-design`, `hardware-detailed-design`, `algorithm-design`
  - `design-review`, `requirements-review`, `code-static-review`, `test-plan-review`, `test-report-review`, `release-review`, `traceability-matrix`

MEDIUM fixes:
- `marketplace.json`: updated description from 5 skills (initial release) to all 16 skills with full lifecycle coverage
- `plugin.json` + `marketplace.json`: unified author name to `ddddjaak`
- `agents/README.md`: corrected persona count description (4 default review lenses + compliance-reviewer as independent)

Cross-package hygiene:
- Removed 7 ae-skills skill name references from 4 skills:
  - `architecture-design/SKILL.md`: removed `planning-and-task-breakdown` reference
  - `software-architecture-design/SKILL.md`: removed `spec-driven-development`, `doubt-driven-development`, `interview-me` references
  - `hardware-architecture-design/SKILL.md`: removed `spec-driven-development`, `doubt-driven-development`, `interview-me` references
  - `design-review/SKILL.md`: removed `doubt-driven-development` reference
- `CONTRIBUTING.md`: removed ae-skills script reference
- Preserved boundary declaration statements in `CLAUDE.md` and `AGENTS.md` (these are explicit policy, not cross-package coupling)

LOW fixes:
- `using-se-skills/SKILL.md`: skill count `15+` → `16` (exact count)
- Architecture output templates: added explicit Scope/Not-Covered sections to `architecture-design`, `software-architecture-design`, `hardware-architecture-design`

### Infrastructure

- `.gitignore`: added entries for draw.io test artifacts (`*.drawio`, `*.vsdx`)
- `.mcp.json`: 3 MCP servers configured with descriptions (drawio, visio, math)
  - Uses `${CLAUDE_PLUGIN_ROOT}` resolution for hooks; MCP commands are portable (npx/python/uvx)

## [1.0.0] — 2025

### Added

**Autonomous Goal Mode (`/se-goal`):**
- New slash command `.claude/commands/se-goal.md` — goal-driven full-pipeline execution
- CLAUDE.md: ~150 lines of Goal Mode rules — Plan→Act→Observe→Reflect loop, auto-skill selection by phase+domain, self-correction protocol (max 3 retries per phase), stop conditions (success/escalate/budget/pause), progress reporting format
- Pipeline Mode vs Goal Mode distinction: triggers, user interaction, failure handling

**Pipeline Mode (automatic phase detection and guidance):**
- CLAUDE.md: ~60 lines of Pipeline Mode rules — phrase-level trigger keywords (Chinese/English), 3-step phase detection (directory scan → content quality verification → true phase status), option presentation templates, execution protocol with loop
- using-se-skills: ~80 lines of Pipeline Conduction section — phase detection protocol, per-phase option generation with exact wording templates, special artifact routing
- Cross-session resume: reads `docs/versions.json` on session start to recover pipeline state

**Skill chain fully connected:**
- All 16 skills: `## After This Skill` section declaring upstream dependencies, downstream consumers, alternative paths, and traceability checkpoint
- Pipeline graph from islands to directed graph — any requirement traceable through full chain

**Artifact traceability and state persistence:**
- `docs/versions.json` — 15 artifact entries, 14 dependency links, 5 phase checkpoints, cross-session state persistence
- CLAUDE.md execution protocol: Record step updates versions.json after each skill completes

**Skill description optimization:**
- All 16 skill YAML descriptions rewritten: Chinese trigger phrases first, unique first sentences, explicit NOT clauses for disambiguation
- Review family (7 skills) disambiguated: unique identifiers replace shared "review" opening
- Architecture family (5 skills) disambiguated: "Transforms...into..." pattern eliminated

**Documentation:**
- README.md: `/se-goal` added to command table, Pipeline vs Goal Mode comparison table, skill count 15→16
- docs/README.md: full directory structure, versions.json documentation, work mode reference
- AGENTS.md: complete rewrite reflecting 16 skills, 6 commands, Pipeline Mode + Goal Mode, versions.json

### Changed

**Reference checklist simplification (21 files):**
- Tables reduced from 4–9 columns to 1–2 columns (ID + check content only)
- Removed: 修订记录, 适用范围, 参考文件, CHIPSEA CONFIDENTIAL markers
- Removed: 目的(Objectives) sections, **评估**: YES/NO inline markers
- Cleaned: template placeholder values (OK→[待评估], No→[待评估])
- Total: ~2500+ lines → 1210 lines (~50% reduction)

**using-se-skills meta-skill:**
- Added Pipeline Conduction section with phase detection protocol and option generation
- Added After This Skill section declaring conductor role
- Enhanced Quick Reference to include all 16 skills

**CLAUDE.md:**
- Added Pipeline Mode rules (trigger keywords, phase detection, execution protocol)
- Added Goal Mode rules (Plan→Act→Observe→Reflect, auto-selection, self-correction)
- Added cross-session resume protocol
- Updated slash command routing table
- Refined trigger keywords from single-word to phrase-level patterns

**README.md:**
- Command table restructured with mode badges (自主式/引导式)
- Added Pipeline Mode vs Goal Mode 4-dimension comparison
- Command count 5→6, skill count 15→16
- using-se-skills description updated to pipeline conductor
- Project structure updated with se-goal.md

**docs/README.md:**
- Complete directory structure including all artifact subdirectories
- versions.json documentation
- Work mode reference table

**AGENTS.md:**
- Full rewrite: 16 skills, 6 commands, pipeline architecture, validation rules

### Fixed

- Skill descriptions: eliminated ambiguity between 7 review skills and 5 architecture skills
- Phase detection: upgraded from binary directory check to 3-step quality verification
- Cross-session state: added versions.json to persist pipeline progress across sessions

## [0.1.0] — 2025

### Added
- Initial release with 5 SE workflow skills: requirements-decompose, architecture-design, spec-authoring, design-review, traceability-matrix
- Meta-skill: using-se-skills
- 5 professional agent personas: system-architect, hw-domain-expert, fw-domain-expert, verification-engineer, compliance-reviewer
- 5 slash commands: `/se-requirements`, `/se-architecture`, `/se-spec`, `/se-review`, `/se-traceability`
- Plugin manifest: plugin.json, marketplace.json
- CLAUDE.md with repository structure guide
- AGENTS.md, CONTRIBUTING.md, README.md
- `.github/` — issue templates and PR template
- MIT License
