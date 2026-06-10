# Changelog

All notable changes to the SE Skills project will be documented in this file.

## [Unreleased]

### Added
- 5 professional agent personas: system-architect, hw-domain-expert, fw-domain-expert, verification-engineer, compliance-reviewer
- Agents README with composition rules and usage patterns
- Cross-package reference note in using-se-skills (points to ae-skills)
- Core Operating Behaviors #7-9: Surface Assumptions, Push Back When Warranted, Maintain Scope Discipline
- Failure Mode #10: Silently resolving ambiguity
- Skill Rule #5: Verification is part of the work
- Lifecycle caveat: "Not every task needs every skill"
- AGENTS.md — standard agent instructions file
- CONTRIBUTING.md — contribution guidelines
- `.github/` — issue templates and PR template

### Changed
- Enhanced CLAUDE.md: added Skills by Phase, Conventions, Prerequisites, Boundaries
- Enhanced README.md: full rewrite matching ae-skills depth — commands, quick start, skills by phase, agent roles, how skills work, why SE Skills, contributing
- Enhanced using-se-skills meta-skill: 9 core behaviors (was 6), 10 failure modes (was 9), 5 skill rules (was 4)
- Updated plugin.json: agents path configured

### Fixed
- Decoupled from ae-skills: removed all cross-package functional dependencies, inlined vague-requirement handling and third-party IP verification guidance

## [1.0.0] — 2025

### Added
- Initial release with 5 SE workflow skills: requirements-decompose, architecture-design, spec-authoring, design-review, traceability-matrix
- Meta-skill: using-se-skills
- 5 slash commands: `/se-requirements`, `/se-architecture`, `/se-spec`, `/se-review`, `/se-traceability`
- Plugin manifest: plugin.json, marketplace.json
- CLAUDE.md with repository structure guide
- MIT License
