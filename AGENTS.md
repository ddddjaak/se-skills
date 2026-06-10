# AGENTS.md

This file provides guidance to AI coding agents when working with the SE Skills repository.

## Repository Overview

SE Skills is a Claude Code plugin providing structured workflow skills for chip vendor System Engineers (Application Architects). It covers the full SE lifecycle: requirements decomposition → architecture design → specification authoring → cross-department review → traceability validation.

## Project Structure

```
se-skills/
├── skills/                  # 5 SE workflow skills + 1 meta-skill
│   ├── using-se-skills/     # Meta-skill: skill discovery and invocation
│   ├── requirements-decompose/
│   ├── architecture-design/
│   ├── spec-authoring/
│   ├── design-review/
│   └── traceability-matrix/
├── agents/                  # 5 professional review personas
│   ├── system-architect.md
│   ├── hw-domain-expert.md
│   ├── fw-domain-expert.md
│   ├── verification-engineer.md
│   └── compliance-reviewer.md
├── .claude/commands/        # 5 slash commands
├── docs/                    # Output templates and reference
├── CLAUDE.md                # Primary agent guidance (read this first)
└── README.md                # Project overview and quick start
```

## How to Work in This Repository

### Adding or Modifying Skills

1. Every skill is a directory under `skills/<kebab-case-name>/` with a `SKILL.md` file
2. SKILL.md must have YAML frontmatter: `name` (matches directory name) and `description` (third person, starts with what it does, followed by "Use when...")
3. Required sections: Overview, When to Use, Process, Common Rationalizations, Red Flags, Verification
4. Keep SKILL.md under 500 lines — use progressive disclosure (details in steps, not preamble)
5. Cross-reference other skills by their directory name (e.g., `architecture-design`)
6. Update `using-se-skills/SKILL.md` Quick Reference table when adding/removing skills

### Adding or Modifying Agents

1. Agents live in `agents/<role-name>.md`
2. Format: YAML frontmatter → role identity → review framework → output format → rules → composition
3. Update `agents/README.md` when adding/removing agents
4. Agents do NOT invoke other agents — orchestration belongs to slash commands

### Validation

Skills reference each other by name. When changing a skill name or adding new skills, verify:
- All cross-references in "Interaction with Other Skills" sections resolve to existing skills
- The `using-se-skills` meta-skill reflects the current skill set
- Slash command files reference the correct skill names

### Key Conventions

- **Every claim traces to something** — requirement IDs, interface IDs, constraint IDs
- **Numbers, not adjectives** — "≤ 500μs" not "fast"; "≤ 2W" not "low power"
- **Skills are workflows, not suggestions** — follow steps in order, don't skip verification
- **Verification is non-negotiable** — every skill ends with a checklist; "looks right" is never sufficient

## Package Independence

SE Skills is completely independent of AE Skills (ae-skills). There are no functional cross-dependencies between the two packages. The only cross-references are informational (each package's README and meta-skill mention the other for discoverability).

## Read Order

For new contributors or agents working in this repo, read in this order:
1. `README.md` — what this is and how to use it
2. `CLAUDE.md` — how to work in this codebase
3. `skills/using-se-skills/SKILL.md` — how skills are discovered and invoked
4. `agents/README.md` — how agent personas work
5. `CONTRIBUTING.md` — how to contribute
