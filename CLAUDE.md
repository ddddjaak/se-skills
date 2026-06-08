# SE Skills

Chip vendor SE (System Engineer / Application Architect) workflow skills for Claude Code.

## Overview

This plugin provides a collection of structured workflow skills for chip vendor System Engineers. Each skill encodes a specific process that senior SEs follow — from raw requirements decomposition through architecture design, formal specification authoring, cross-department review, and traceability validation.

Skills can be used independently or chained end-to-end for a complete project workflow.

## Skills

| Skill | Slash Command | Description |
|-------|--------------|-------------|
| using-se-skills | — (auto) | Meta-skill: discover and invoke the right SE skill |
| requirements-decompose | `/se-requirements` | Raw inputs → structured system requirements |
| architecture-design | `/se-architecture` | Requirements → modules, interfaces, constraints |
| spec-authoring | `/se-spec` | Architecture → SOD, HW-SW IF Spec, Test Plan |
| design-review | `/se-review` | Four-lens adversarial review of any SE artifact |
| traceability-matrix | `/se-traceability` | Cross-artifact gap analysis and coverage |

## Quick Start

### Full Project Workflow

```
/se-requirements  →  /se-architecture  →  /se-spec  →  /se-review  →  /se-traceability
```

### Individual Skill Usage

- **Just need to review a colleague's architecture?** → `/se-review`
- **Need a test plan from existing requirements?** → `/se-spec`
- **Need to verify coverage before milestone review?** → `/se-traceability`

### Prerequisites

- Claude Code with plugin support
- Works with existing `agent-skills` plugin — SE skills can invoke agent skills inline when needed

## Directory Structure

```
se-skills/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .claude/
│   └── commands/           # Slash command definitions
│       ├── se-requirements.md
│       ├── se-architecture.md
│       ├── se-spec.md
│       ├── se-review.md
│       └── se-traceability.md
├── skills/
│   ├── using-se-skills/    # Meta-skill
│   ├── requirements-decompose/
│   ├── architecture-design/
│   ├── spec-authoring/
│   ├── design-review/
│   └── traceability-matrix/
├── SE-SKILLS-DESIGN.md     # Full design specification
└── CLAUDE.md               # This file
```
