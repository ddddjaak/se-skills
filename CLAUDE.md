# SE Skills

This is the se-skills project — a collection of structured workflow skills for chip vendor System Engineers (Application Architects).

## Project Structure

```
skills/              → Core skills (SKILL.md per directory)
agents/              → Reusable agent personas (system-architect, hw-domain-expert, fw-domain-expert, verification-engineer, compliance-reviewer)
.claude/commands/    → Slash commands (/se-requirements, /se-architecture, /se-spec, /se-review, /se-traceability)
.claude-plugin/      → Plugin manifest (plugin.json, marketplace.json)
references/          → Detailed SE review checklists (loaded on demand via skill "See Also" sections)
```

## Skills by Phase

| Phase | Skill | Domain | Description |
|-------|-------|--------|-------------|
| **Define** | `requirements-decompose` | System | Raw inputs → structured, traceable system requirements with ownership |
| **Design** | `architecture-design` | System | Requirements → module decomposition, interfaces, constraints, trade-offs |
| **Design** | `software-architecture-design` | SW | System arch → firmware thread model, IPC design, memory budget, data flows |
| **Design** | `hardware-architecture-design` | HW | System arch → pin assignments, voltage domains, PCB constraints, component selection |
| **Document** | `spec-authoring` | System | Architecture + Requirements → SOD, HW-SW IF Spec, Test Plan |
| **Document** | `software-detailed-design` | SW | SW arch → function signatures, data structures, state machines, error handling |
| **Document** | `hardware-detailed-design` | HW | HW arch → schematic guidance, PCB rules, PDN design, thermal analysis |
| **Document** | `algorithm-design` | Algorithm | Algorithm reqs → signal processing, control loops, calibration, filter design |
| **Verify** | `design-review` | System | Four-lens (HW/SW/Test/System) adversarial review of architecture or spec artifacts |
| **Verify** | `requirements-review` | Requirements | Checklist-based review of requirements documents for completeness and traceability |
| **Verify** | `code-static-review` | SW | Static analysis of source code against company coding standards |
| **Verify** | `test-plan-review` | Test | Completeness and compliance review of test plan documents |
| **Verify** | `test-report-review` | Test | Review of test reports for correctness, completeness, and traceability |
| **Verify** | `release-review` | Release | Release readiness review (binaries, release notes, version manifest, test reports) |
| **Validate** | `traceability-matrix` | Cross-cutting | Cross-artifact gap analysis: orphans, coverage gaps, action items |

The meta-skill `using-se-skills` routes to the correct skill based on artifact type and phase. Skills chain naturally: Define → Design → Document → Verify → Validate. Each skill can also be used independently.

### Slash Command Routing

| Command | Routes to |
|---------|----------|
| `/se-requirements` | `requirements-decompose` |
| `/se-architecture` | `architecture-design` → `software-architecture-design` or `hardware-architecture-design` |
| `/se-spec` | `spec-authoring` → `software-detailed-design`, `hardware-detailed-design`, or `algorithm-design` |
| `/se-review` | `design-review`, `requirements-review`, `code-static-review`, `test-plan-review`, `test-report-review`, or `release-review` |
| `/se-traceability` | `traceability-matrix` |

## Anti-Hallucination Design

Every skill incorporates these mechanisms:

| Mechanism | How it manifests |
|-----------|-----------------|
| **Input gates** | Step 1 of every skill verifies input artifacts exist with exact versions before proceeding |
| **Requirement traceability** | Every claim, function, pin, and constraint must cite a requirement ID (REQ-XXX), interface ID (IF-XXX), or constraint ID (CON-XXX) |
| **Quantified metrics** | "≤ 500μs" not "fast"; "≤ 2W" not "low power"; T_j = T_ambient + P × θ_JA must be calculated, not estimated |
| **Stop-and-ask gates** | "If uncertain, surface and stop — do NOT guess" at every critical decision point (component selection, voltage tolerance, timing bound, error recovery strategy) |
| **Context boundaries** | Each skill explicitly declares what it reads and does NOT read (e.g., software-detailed-design reads ONLY the software architecture — not hardware specs, not test plans) |
| **TBD management** | Every TBD must have an owner and due date; naked TBDs are a verification failure |
| **Version discipline** | Every artifact references its inputs with exact version numbers; version mismatches between artifacts are surfaced as CRITICAL findings |
| **Checkpoint verification** | Every skill ends with a verification checklist; the skill is not complete until every checkbox is ticked with evidence |

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
