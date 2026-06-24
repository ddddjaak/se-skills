# AGENTS.md

This file provides guidance to AI coding agents when working with the SE Skills repository.

## Repository Overview

SE Skills is a Claude Code plugin providing structured workflow skills for chip vendor System Engineers (Application Architects). It covers the full SE lifecycle with 16 skills organized in a **Define → Design → Document → Verify → Validate** chain, supporting two work modes: **Pipeline Mode** (guided step-by-step) and **Goal Mode** (fully autonomous execution).

## Project Structure

```
se-skills/
├── skills/                        # 16 SE workflow skills
│   ├── using-se-skills/           # Pipeline conductor — phase detection + skill routing
│   ├── requirements-decompose/    # Define: raw inputs → structured requirements
│   ├── requirements-review/       # Verify: checklist-based requirements review
│   ├── architecture-design/       # Design: system-level module decomposition
│   ├── software-architecture-design/  # Design: firmware thread model, IPC, memory budget
│   ├── hardware-architecture-design/  # Design: pin assignments, voltage domains, SI analysis
│   ├── spec-authoring/            # Document: SOD, HW-SW IF Spec, Test Plan
│   ├── software-detailed-design/  # Document: function signatures, state machines, data structures
│   ├── hardware-detailed-design/  # Document: schematic guidance, BOM, PCB rules, PDN
│   ├── algorithm-design/          # Document: signal processing, control loops, calibration
│   ├── design-review/             # Verify: four-lens adversarial review (HW/SW/Test/System)
│   ├── code-static-review/        # Verify: coding standard compliance
│   ├── test-plan-review/          # Verify: test plan completeness
│   ├── test-report-review/        # Verify: test report correctness
│   ├── release-review/            # Verify: release readiness gate
│   └── traceability-matrix/       # Validate: cross-artifact gap analysis
├── agents/                        # 5 professional review personas
├── references/                    # 21 SE review checklists (loaded on demand)
├── .claude/commands/              # 6 slash commands
│   ├── se-goal.md                 # Autonomous: full-pipeline execution
│   ├── se-requirements.md
│   ├── se-architecture.md
│   ├── se-spec.md
│   ├── se-review.md
│   └── se-traceability.md
├── .claude-plugin/                # Plugin manifest
├── docs/                          # Output templates + versions.json (pipeline state)
├── CLAUDE.md                      # Primary agent guidance — Pipeline Mode + Goal Mode rules
├── README.md                      # Project overview and quick start
└── AGENTS.md                      # This file
```

## How to Work in This Repository

### Adding or Modifying Skills

1. Every skill is a directory under `skills/<kebab-case-name>/` with a `SKILL.md` file
2. SKILL.md must have YAML frontmatter: `name` and `description`
   - Description format: Chinese trigger phrase first, then English, then trigger conditions, then explicit NOT clauses to disambiguate from similar skills
3. Required sections: Overview, When to Use, Process, Common Rationalizations, Red Flags, Verification
4. Keep SKILL.md under 500 lines — use progressive disclosure
5. Every skill MUST include `## After This Skill` section declaring upstream/downstream connections
6. Cross-reference other skills by their directory name
7. Update `using-se-skills/SKILL.md` Quick Reference table when adding/removing skills

### Pipeline Rules (in CLAUDE.md)

CLAUDE.md is the authoritative source for:
- **Pipeline Mode**: trigger keywords, 3-step phase detection (directory + content quality), option presentation format, execution protocol
- **Goal Mode**: Plan→Act→Observe→Reflect loop, auto-skill selection rules, self-correction protocol (max 3 retries per phase), stop conditions
- **Cross-session resume**: reads `docs/versions.json` to recover pipeline state

When updating skills, agents, or commands, keep CLAUDE.md in sync — it is the runtime behavior definition.

### Adding or Modifying Agents

1. Agents live in `agents/<role-name>.md`
2. Format: YAML frontmatter → role identity → review framework → output format → rules → composition
3. Update `agents/README.md` when adding/removing agents
4. Agents do NOT invoke other agents — orchestration belongs to slash commands

### Validation

Skills reference each other by name. When changing a skill name or adding new skills, verify:
- All cross-references in "After This Skill" and "Interaction with Other Skills" sections resolve
- The `using-se-skills` meta-skill reflects the current skill set (Quick Reference + Pipeline Conduction)
- Slash command files reference the correct skill names
- CLAUDE.md phase detection logic maps to actual artifact directory names
- `docs/versions.json` artifact entries match current skill set

### Key Conventions

- **Every claim traces to something** — requirement IDs, interface IDs, constraint IDs
- **Numbers, not adjectives** — "≤ 500μs" not "fast"; "≤ 2W" not "low power"
- **Two work modes**: Pipeline Mode (guided) for step-by-step control, Goal Mode (autonomous) for full automation
- **Skills are workflows, not suggestions** — follow steps in order, don't skip verification
- **Verification is non-negotiable** — every skill ends with a checklist; "looks right" is never sufficient
- **After This Skill is required** — every skill declares what comes next

## Package Independence

SE Skills is completely independent of AE Skills (ae-skills). There are no functional cross-dependencies between the two packages.

## Read Order

For new contributors or agents working in this repo, read in this order:
1. `README.md` — what this is and how to use it (Pipeline Mode vs Goal Mode)
2. `CLAUDE.md` — runtime behavior: Pipeline Mode + Goal Mode + phase detection + execution protocol
3. `skills/using-se-skills/SKILL.md` — pipeline conductor: phase detection protocol + option generation
4. `agents/README.md` — how agent personas work
5. `CONTRIBUTING.md` — how to contribute
