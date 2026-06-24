# Changelog

All notable changes to the SE Skills project will be documented in this file.

## [Unreleased]

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
