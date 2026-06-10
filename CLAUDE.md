# SE Skills

This is the se-skills project — a collection of structured workflow skills for chip vendor System Engineers (Application Architects).

## Project Structure

```
skills/              → Core skills (SKILL.md per directory)
agents/              → Reusable agent personas (system-architect, hw-domain-expert, fw-domain-expert, verification-engineer, compliance-reviewer)
.claude/commands/    → Slash commands (/se-requirements, /se-architecture, /se-spec, /se-review, /se-traceability)
.claude-plugin/      → Plugin manifest (plugin.json, marketplace.json)
```

## Skills by Phase

| Phase | Skill | Description |
|-------|-------|-------------|
| **Define** | requirements-decompose | Raw inputs → structured, traceable system requirements with ownership |
| **Design** | architecture-design | Requirements → modules, interfaces, constraints, trade-off decisions |
| **Document** | spec-authoring | Architecture + Requirements → SOD, HW-SW IF Spec, Test Plan |
| **Verify** | design-review | Four-lens (HW/SW/Test/System) adversarial review of any SE artifact |
| **Validate** | traceability-matrix | Cross-artifact gap analysis: orphans, coverage gaps, action items |

The skills chain naturally: Define → Design → Document → Verify → Validate. Each skill can also be used independently.

## Conventions

- Every skill lives in `skills/<name>/SKILL.md`
- YAML frontmatter with `name` and `description` fields
- Description starts with what the skill does (third person), followed by trigger conditions ("Use when...")
- Every skill has: Overview, When to Use, Process, Common Rationalizations, Red Flags, Verification
- Skills reference each other by name (`requirements-decompose`, `architecture-design`, etc.)
- The meta-skill `using-se-skills` governs skill discovery and invocation
- Each skill's output is a document saved to `docs/<type>/` (e.g., `docs/requirements/`, `docs/architecture/`)

## Prerequisites

- All skills in the SE workflow require upstream artifacts. `architecture-design` requires structured requirements. `spec-authoring` requires confirmed architecture. `design-review` requires a completed artifact. If prerequisites are missing, skills invoke the upstream skill inline.

## Boundaries

- Always: Follow the skill anatomy format (Overview → When to Use → Process → Rationalizations → Red Flags → Verification)
- Always: Every claim must trace to a requirement ID, interface ID, or constraint ID
- Always: Quantify — "≤ 500μs" not "fast"; "≤ 2W" not "low power"
- Never: Add skills that are vague advice instead of actionable processes
- Never: Duplicate content between skills — reference other skills instead
- Never: Proceed to downstream work before upstream artifacts are confirmed
- Never: This package is independent of ae-skills — no cross-package references
