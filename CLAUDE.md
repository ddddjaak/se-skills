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

## SE Pipeline Mode — AUTOMATIC (Critical)

**This project contains 16 SE workflow skills organized in a Define → Design → Document → Verify → Validate chain.** When a user expresses SE work intent without naming a specific skill name, **you MUST enter Pipeline Mode automatically**. Do NOT ask "which skill do you want to use?" or dump a list of 16 skill names. Instead, guide the user through the workflow by detecting their current phase and presenting logical next-step options.

### Trigger Keywords

**Pipeline Mode triggers** — user wants guided, step-by-step help. Enter when message contains any of these patterns (but NOT Goal Mode patterns):

| Chinese Phrase Patterns | English Phrase Patterns |
|------------------------|------------------------|
| 帮我做需求 / 帮我分解需求 / 梳理需求 | "help me with requirements" / "structure the requirements" |
| 帮我做架构 / 帮我设计架构 / 模块怎么划分 | "help me design the architecture" / "how should I structure" |
| 帮我写规格 / 帮我写概要设计 / 生成接口文档 | "help me write the spec" / "generate the specification" |
| 帮我审查 / 帮我review / 帮我检查一下 | "help me review" / "can you check this" |
| 帮我做追溯 / 帮我检查覆盖 / 查一下缺口 | "help me with traceability" / "check coverage" |
| 下一步做什么 / 该用哪个技能 / 我现在在哪个阶段 | "what should I do next" / "which phase am I in" |
| 我有PRD / 我有需求文档 / 这是数据手册 | "I have a PRD" / "here is the datasheet" |

**Goal Mode triggers** — user wants fully autonomous execution. Enter when message contains any of these patterns:

| Chinese Phrase Patterns | English Phrase Patterns |
|------------------------|------------------------|
| 端到端做完 / 走完全流程 / 全部自动做 | "complete the full workflow" / "run through the entire pipeline" |
| 从需求到追溯全自动 / 一条龙 / 不用问我 | "end to end" / "fully autonomous" / "don't ask me" |
| 开干 / 直接开始 / go | "just do it" / "go ahead" / "run it all" |
| 自动完成...的SE流程 / 自动走完...全链路 | "auto-complete the SE process for" |

**Keyword-only triggers** (weaker signal — combine with context):

When a message contains at least TWO of these single-word signals without a specific skill name, it likely indicates SE intent: 需求, 架构, 规格, 审查, 追溯, requirements, architecture, specification, review, traceability.

### Phase Detection (scan docs/ before responding)

**Step 1 — Check directory structure.** Use Glob (`docs/*/`) to detect which artifact directories exist:

```
docs/requirements/   exists → Define phase at minimum (check content quality below)
docs/architecture/   exists → Design phase at minimum
docs/spec/           exists → Document phase at minimum
docs/reviews/        exists → Verify phase has run
docs/traceability/   exists → Validate phase has run
```

**Step 2 — Verify content quality (not just directory existence).** A directory being present does NOT mean the phase is complete. Check:

| Directory | Quality Check | How to Verify |
|-----------|--------------|---------------|
| `docs/requirements/` | Contains .md files with REQ-XXX IDs | Grep for `REQ-` in the directory |
| `docs/architecture/` | Contains .md files with MOD-XXX or IF-XXX IDs | Grep for `MOD-\|IF-` in the directory |
| `docs/spec/` | Contains .md files with spec content (not placeholder) | Check file size > 500 bytes |
| `docs/reviews/` | Contains review report .md files with findings | Grep for `## Findings` or `## Review Report` |
| `docs/traceability/` | Contains traceability matrix .md file | Check for `docs/traceability/*.md` |

**Step 3 — Determine true phase status:**

| Condition | Phase Status | What to offer |
|-----------|-------------|---------------|
| No `docs/requirements/` dir | **Define — not started** | Only `requirements-decompose` |
| `docs/requirements/` exists but empty or no REQ-XXX IDs | **Define — in progress (incomplete)** | Resume `requirements-decompose` or start fresh |
| `docs/requirements/` has REQ-XXX IDs, no `docs/architecture/` | **Design — ready to start** | Architecture options (system / SW / HW) |
| `docs/architecture/` exists but no MOD-XXX/IF-XXX IDs | **Design — in progress (incomplete)** | Resume architecture skill or review existing |
| `docs/architecture/` has IDs, no `docs/spec/` | **Document — ready to start** | Spec authoring options |
| `docs/spec/` has content (files > 500B) | **Verify — ready to start** | Review options matching artifact type present |
| `docs/reviews/` has review reports | **Validate** | `traceability-matrix` |

### Option Presentation Format

Present exactly 2-4 numbered options. Each option includes:
1. Number
2. What it produces (outcome — user cares about this)
3. Skill name in parentheses (for traceability)

**Example for Design phase:**
```
Based on your requirements document, the next step is architecture design. Which level?

1. System-level module decomposition — modules, interfaces, constraints, trade-offs (architecture-design)
2. Software/firmware architecture — RTOS threads, memory budget, IPC, data flows (software-architecture-design)
3. Hardware architecture — pin assignments, voltage domains, PCB constraints (hardware-architecture-design)
4. Something else — tell me what you need
```

**Example for Verify phase (when docs/spec/ exists):**
```
Your specification is ready. What would you like to review?

1. Cross-department adversarial review — HW/SW/Test/System lenses (design-review)
2. Requirements document review — checklist-based completeness check (requirements-review)
3. Source code static analysis — coding standard compliance (code-static-review)
4. Something else — tell me what artifact you want reviewed
```

### Execution Protocol

1. **Detect** the phase:
   - First, check if `docs/versions.json` exists — if so, use it as the authoritative phase state
   - Otherwise, scan `docs/` directories (use Glob: `docs/*/`) and verify content quality per the quality checks above
   - Distinguish between "phase not started", "phase in progress (incomplete)", and "phase complete"
2. **Present** 2-4 numbered options in the format above — always include "Something else" as the last option
3. **Execute** the chosen skill via the Skill tool with the fully-qualified name (e.g., `se-skills:requirements-decompose`)
4. **Record** — after the skill completes, update `docs/versions.json`:
   - Add the produced file path to the artifact's `files` array
   - Set `status` to `produced`
   - Update `pipeline.last_updated` and `pipeline.current_phase`
   - Check off the relevant `phase_checkpoints` entry
5. **Loop** — return to step 1: re-scan state, present the next logical options
6. **Stop** when the user says "done", "stop", or when `traceability-matrix` has been run and `phase_checkpoints.validate_complete` is true

### Cross-Session Resume

When starting a new session, check `docs/versions.json` first:
- If it exists and has `produced` artifacts → resume from the highest completed phase; present the next logical options
- If it does not exist or has no produced artifacts → run full phase detection from directory scan
- If the user mentions a specific artifact → cross-reference against `versions.json` to determine which phase they are in

### Never (Pipeline Anti-Patterns)

- ❌ Ask "which of these 16 skills do you want?" — overwhelming and unhelpful
- ❌ Say "use `requirements-decompose` for requirements" — the user doesn't need to know skill names
- ❌ Skip phase detection — always check `docs/` first
- ❌ Jump downstream when upstream artifacts are missing — if `docs/requirements/` is empty, do NOT offer architecture design
- ❌ Run multiple skills in parallel without asking — each phase gates on the previous one's output

## SE Autonomous Goal Mode — GOAL-DRIVEN (Critical)

**This is the fully autonomous mode.** When the user gives a clear end-goal — not "help me with X" but "complete the full SE workflow for X" — you run the entire Define → Design → Document → Verify → Validate chain autonomously. You do NOT ask per-phase questions. You self-correct when reviews fail. You only escalate when genuinely stuck.

### Trigger (enter Goal Mode instead of Pipeline Mode)

Pipeline Mode presents options and waits for user choice. Goal Mode executes autonomously. Enter Goal Mode when:

| Trigger | Example |
|---------|---------|
| `/se-goal` command | `/se-goal 完成温度传感器方案的SE全流程` |
| Explicit completion language | "端到端做完", "走完全流程", "自动完成...的SE", "complete the full SE workflow for", "run through the entire pipeline" |
| Clear end-state declared | "从PRD到追溯矩阵全部自动做", "from requirements to traceability, go" |
| User says "go" / "开干" after Pipeline Mode shows the first option | "直接开始，不用问我" |

**If uncertain whether the user wants Pipeline Mode or Goal Mode, default to Pipeline Mode (ask).** Only enter Goal Mode when the intent is unambiguous.

### Goal Execution Protocol (Plan → Act → Observe → Reflect)

```
GOAL RECEIVED
    │
    ▼
┌─────────────────────────────────────────────┐
│  PLAN: Parse goal, detect inputs, set path   │
│  · What are we building?                     │
│  · What inputs exist? (PRD, datasheet, etc.) │
│  · What's the target endpoint?               │
│  · Report the planned chain to user ONCE     │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│  ACT: Execute the next skill in chain        │
│  · Auto-select skill based on phase + domain │
│  · Run skill to completion                   │
│  · Record output in versions.json            │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│  OBSERVE: Run verification checklist         │
│  · Every skill has a verification section    │
│  · Check every checkbox with evidence        │
│  · Record pass/fail per checklist item       │
└────────────────────┬────────────────────────┘
                     ▼
              ┌──────┴──────┐
              │             │
           ALL PASS     SOME FAIL
              │             │
              ▼             ▼
    ┌─────────────┐  ┌──────────────────┐
    │ Next Phase  │  │ REFLECT: Fix      │
    │ (continue)  │  │ · Identify root   │
    └─────────────┘  │   cause           │
                     │ · Retry same      │
                     │   skill (max 3)   │
                     │ · If 3 failures:  │
                     │   ESCALATE        │
                     └────────┬─────────┘
                              │
                     ┌────────┴─────────┐
                     │                  │
                  FIXABLE          GENUINELY STUCK
                     │                  │
                     ▼                  ▼
               Retry skill        ESCALATE to user
               (go to ACT)        with specific
                                  blocker + options
```

### Auto-Skill Selection Rules

When in Goal Mode, do NOT present options. Select automatically:

| Phase | Condition | Auto-Selected Skill |
|-------|-----------|-------------------|
| **Define** | Always | `requirements-decompose` |
| **Design** | No prior architecture | `architecture-design` (system-level first) |
| **Design** | System arch exists, user mentioned HW | `hardware-architecture-design` |
| **Design** | System arch exists, user mentioned SW/firmware | `software-architecture-design` |
| **Document** | System arch exists | `spec-authoring` |
| **Document** | SW arch exists | `software-detailed-design` |
| **Document** | HW arch exists | `hardware-detailed-design` |
| **Document** | Algorithm requirements present | `algorithm-design` |
| **Verify** | Spec documents exist | `design-review` (four-lens adversarial) |
| **Verify** | Requirements doc only | `requirements-review` |
| **Verify** | Source code exists | `code-static-review` |
| **Verify** | Test plan doc exists | `test-plan-review` |
| **Verify** | Test report exists | `test-report-review` |
| **Verify** | Release package exists | `release-review` |
| **Validate** | Reviews exist | `traceability-matrix` |

**Domain inference from user's goal statement:**
- "温度传感器" / "power management" / "motor control" → system-level (architecture-design)
- "固件" / "firmware" / "RTOS" / "驱动" → SW path (software-architecture-design)
- "PCB" / "原理图" / "schematic" / "layout" → HW path (hardware-architecture-design)

### Self-Correction Protocol

When a verification checklist fails:

1. **Identify** which checklist items failed
2. **Classify** the failure:
   - **Missing content**: Skill didn't produce required output → re-run the same skill with explicit instruction to address the gap
   - **Quality issue**: Output exists but doesn't meet quantified metrics → re-run with tighter constraints
   - **Traceability gap**: Missing REQ/MOD/IF/TC IDs → re-run with explicit tracing instruction
   - **Ambiguity**: Requirement/constraint is genuinely ambiguous → ESCALATE (don't guess)
3. **Retry** the skill (max 3 attempts per phase). On retry, pass the specific failure items as context.
4. **If 3 retries exhausted**: ESCALATE with:
   - What was attempted (3 times)
   - What checklist items still fail
   - Recommended path forward (options for the user)

### Stop Conditions

| Condition | Action |
|-----------|--------|
| `traceability-matrix` passes all checks AND finds zero gaps | **SUCCESS** — report completion with artifact summary |
| Same phase fails 3 consecutive retries | **ESCALATE** — present specific blocker and options to user |
| Total skill executions exceed 20 | **STOP** — report progress so far, ask whether to continue |
| User interrupts with "stop" / "pause" / "wait" | **PAUSE** — report current phase, completed artifacts, next steps |
| Contradictory requirements or constraints detected | **ESCALATE** — surface the contradiction with specific REQ-XXX IDs |

### Progress Reporting (Goal Mode)

After each phase completes successfully, report ONE concise status line:

```
✅ Define  complete — 23 requirements (REQ-001 ~ REQ-023), 3 domains
✅ Design  complete — 5 modules (MOD-01 ~ MOD-05), 12 interfaces
✅ Document complete — SOD v1.0, HW-SW IF Spec v1.0, Test Plan v1.0
⏳ Verify  in progress — running design-review (attempt 1)…
```

Do NOT ask "ready to proceed?" between phases in Goal Mode. Just report and continue.

### Goal Mode vs Pipeline Mode

| Dimension | Pipeline Mode | Goal Mode |
|-----------|--------------|-----------|
| Trigger | Any SE-related request | Explicit completion intent |
| Phase transitions | User picks from options | Auto-selected by rules |
| Verification failures | Reported to user | Auto-retried (max 3x) |
| User interaction | Every phase | Only on escalation or completion |
| Stop | User says "done" | Goal achieved or stuck |

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
| `/se-goal` | **Autonomous Goal Mode** — full Define→Design→Document→Verify→Validate chain, auto-correcting, human only on escalation |
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
