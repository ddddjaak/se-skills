# SE Skills Package — Design Specification

## Package Overview

**Package name:** `se-skills`
**Target role:** Chip vendor SE (System Engineer / Application Architect)
**Target users:** Internal SE team; shareable across departments
**Design philosophy:** Mirrors the `agent-skills` pattern — each skill is a narrow, self-contained capability with explicit triggers, processes, outputs, and verification. Skills can be used independently or chained inline (one skill invokes another when upstream artifacts are missing).

---

## The SE Workflow Chain

```
PRD / Datasheet / Standard / Customer Requirement
    │
    ▼
┌──────────────────────────┐
│ requirements-decompose    │  ← can invoke interview-me
│ Raw → Structured SysReq  │
└──────────┬───────────────┘
           │ System Requirements (with traceability IDs)
           ▼
┌──────────────────────────┐
│ architecture-design       │  ← can invoke requirements-decompose,
│ SysReq → Module/IF design │      source-driven-development
└──────────┬───────────────┘
           │ Architecture Design (block diagram, module list, IF specs)
           ▼
┌──────────────────────────┐
│ spec-authoring            │  ← can invoke architecture-design,
│ Design → Formal specs    │      requirements-decompose
└──────────┬───────────────┘
           │ Software Outline Design, HW-SW IF Spec, Test Plan
           ▼
┌──────────────────────────┐
│ design-review             │  ← can invoke ANY upstream skill
│ Adversarial, cross-dept   │
└──────────┬───────────────┘
           │ Review report, action items
           ▼
┌──────────────────────────┐
│ traceability-matrix       │  ← runs across all artifacts
│ Req → Design → Test       │
└──────────────────────────┘
```

**Inline invocation pattern** (matching `agent-skills` style):

Each skill declares in its "Interaction with Other Skills" section which skills it can invoke and under what conditions. When a downstream skill detects missing or incomplete upstream artifacts, it does NOT silently proceed — it either invokes the upstream skill inline or surfaces the gap to the user.

---

## Skill 1: `requirements-decompose`

### Positioning

The entry point of the SE skill chain. Transforms raw, heterogeneous inputs (PRD, chip datasheet, industry standards, customer specs, competitive analysis) into a structured, traceable system requirements document that every downstream artifact can reference.

This skill is to SE what `interview-me` is to software development: it confronts ambiguity head-on before any design work begins.

### When to Use

- A new chip or product project kicks off and requirements exist only as a PRD or datasheet
- Multiple input sources exist (datasheet + standard + customer spec) and need consolidation
- Requirements are implicit, scattered across documents, or contradict each other
- You need to assign ownership (HW / SW / System / Mechanical) to each requirement
- A downstream skill (`architecture-design`, `spec-authoring`) detects incomplete requirements

**When NOT to use:**

- Requirements are already fully decomposed and traceable in a structured document
- The ask is a single-module change with no new system-level impact
- Pure information lookup ("what does the datasheet say about register X?")

### The Process

```
COLLECT ──→ CLASSIFY ──→ RESOLVE ──→ DERIVE ──→ ASSIGN ──→ VALIDATE
   │           │           │           │           │            │
   ▼           ▼           ▼           ▼           ▼            ▼
 Gather     Categorize  Resolve     Derive     Assign       Human
 all raw    by domain   conflicts   system-    ownership    review
 inputs     & type      & gaps      level reqs (HW/SW/SYS)  & sign-off
```

#### Step 1: COLLECT — Gather all raw inputs

Before any analysis, inventory every input source:

```
RAW INPUT INVENTORY:
1. PRD: [document name, version, date, owner]
2. Chip Datasheet: [chip name, revision, sections relevant]
3. Industry Standard: [standard name, version, mandatory/optional clauses]
4. Customer Specification: [customer, document ID, date]
5. Reference Design: [platform, version]
6. Legacy/Previous-gen Requirements: [project name, document ID]
→ Any other inputs I'm missing?
```

Surface the inventory to the user before proceeding. Missing inputs discovered during Step 3 (resolve) are expensive — this is the cheapest moment to catch them.

#### Step 2: CLASSIFY — Categorize by domain and type

Classify every extracted requirement across two axes:

**Domain axis (who owns this?):**
| Domain | Examples |
|--------|----------|
| HW | Pin assignments, voltage domains, clock trees, PCB constraints |
| SW | Driver interfaces, protocol stacks, RTOS requirements, memory maps |
| System | Power sequences, boot flow, safety states, cross-domain timing |
| Mechanical | Thermal envelope, form factor, connector placement |
| Compliance | Certification requirements (FCC, CE, safety standards) |

**Type axis (what kind of statement is this?):**
| Type | Marker words | Treatment |
|------|-------------|-----------|
| Functional | "shall support", "must provide" | Trace to design element |
| Performance | "within X μs", "≤ Y mW" | Trace to verification test |
| Constraint | "must not exceed", "only when" | Trace to design rule / DFM |
| Interface | "via I2C", "over SPI at Z MHz" | Trace to interface spec |
| Safety/Security | "must not", "shall isolate" | Trace to safety analysis |

**Output:** A classified requirement table:

```markdown
| ID    | Raw Requirement | Source | Domain | Type    | Status |
|-------|----------------|--------|--------|---------|--------|
| REQ-001 | "SPI flash must respond within 10ms" | Datasheet §3.2 | SW | Performance | Draft |
| REQ-002 | "Vcore ramp 0.6V→1.1V in ≤ 2ms" | PRD §4.1 | System | Performance | Draft |
| REQ-003 | "eSPI bus operates at 66MHz" | Standard §2 | HW | Interface | Draft |
```

#### Step 3: RESOLVE — Conflict detection and gap identification

This is the highest-value step. Cross-reference all classified requirements and surface:

**Conflicts:**
```
CONFLICT DETECTED:
REQ-012 (Datasheet §5.1): "I2C pull-up to 3.3V"
REQ-047 (PRD §3.2):     "All I2C buses operate at 1.8V"
→ These cannot both be true. Which source takes precedence?
```

**Gaps:**
```
GAP DETECTED:
PRD mentions "secure boot" but no requirements specify:
- Which authentication algorithm (RSA/ECDSA/other)?
- Key storage mechanism?
- Boot timeout behavior on verification failure?
→ These must be resolved before architecture design.
```

**Ambiguities:**
```
AMBIGUITY DETECTED:
REQ-023: "System shall boot quickly"
→ "Quickly" is not testable. Target: cold boot < 500ms? warm boot < 100ms?
```

For each conflict/gap/ambiguity, surface to the user with a concrete proposed resolution (GUESS pattern from `interview-me`). Do not silently pick one.

#### Step 4: DERIVE — Generate system-level requirements

Raw requirements often state *what* without *how*. Derive the system-level requirements that bridge the gap:

```
RAW:        "Chip supports S0/S3/S5 power states"
DERIVED:    SYS-REQ-001: "System shall transition S0→S3 when host asserts SLP_S3#"
            SYS-REQ-002: "System shall transition S3→S0 within 500μs of SLP_S3# de-assertion"
            SYS-REQ-003: "System shall sequence power rails S0→S3 per Table X (reverse order)"
            SYS-REQ-004: "System shall assert PWR_OK to host only after all rails stable in S0"
```

Derivation rules:
- Every derived requirement must trace back to at least one raw requirement
- Derived requirements must be testable (quantified, observable)
- If a derivation feels like an architectural decision rather than a requirement, flag it — it belongs in `architecture-design`, not here

#### Step 5: ASSIGN — Ownership assignment

Assign every requirement to the owning discipline:

```markdown
| ID          | Requirement | Owner | Verifier |
|-------------|-------------|-------|----------|
| SYS-REQ-001 | S0→S3 transition on SLP_S3# | System (SE) | HW Test |
| SYS-REQ-002 | S3→S0 within 500μs | SW (FW) | SW Test |
| HW-REQ-001  | I2C pull-up 3.3V ±5% | HW (EE) | HW Test |
```

Ownership assignment drives cross-department review. A requirement with no owner is a requirement that will be missed.

#### Step 6: VALIDATE — Human review and sign-off

Present the complete structured requirements document. Do not proceed to `architecture-design` until the user confirms.

### Output

A structured requirements document (saved to `docs/requirements/[project]-system-requirements.md` after confirmation):

```markdown
# System Requirements: [Project/Chip Name]

## Document Control
- Version: [1.0 draft]
- Date: [YYYY-MM-DD]
- Author: [SE name]
- Input Sources: [list with versions]

## Requirement Table
| ID | Requirement | Source | Domain | Type | Owner | Verifier | Status |
|----|-------------|--------|--------|------|-------|----------|--------|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Derived Requirements
| ID | Requirement | Derived From | Rationale |
|----|-------------|-------------|-----------|
| ... | ... | ... | ... |

## Conflict Resolution Log
| Conflict ID | Description | Resolution | Resolved By | Date |
|-------------|-------------|------------|-------------|------|
| ... | ... | ... | ... | ... |

## Open Items
| ID | Description | Blocker For | Owner | Due |
|----|-------------|-------------|-------|-----|
| ... | ... | ... | ... | ... |

## Traceability Matrix (initial)
| Raw Source | System Req ID | Design Element (TBD) | Test Case (TBD) |
|------------|--------------|----------------------|-----------------|
| ... | ... | (filled by architecture-design) | (filled by spec-authoring) |
```

### Interaction with Other Skills

- **`interview-me`** (from agent-skills): Invoked inline when a requirement is too vague to classify. Example: PRD says "system shall be robust" — invoke `interview-me` to extract what "robust" means.
- **`architecture-design`**: Downstream consumer. Hands off the structured requirements as input.
- **`traceability-matrix`**: Initializes the first column (Raw Source → System Req).

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The PRD is clear enough, let's just start designing" | PRDs state what marketing wants. System requirements state what engineering can verify. The gap between them is where projects fail. |
| "Conflicts will get caught in design review" | Catching a conflict during design review means rework. Catching it here costs a conversation. |
| "I can classify requirements while designing the architecture" | Classification and design are different cognitive modes. Switching between them produces shallow work in both. |
| "Derived requirements are just design decisions" | If it's testable and traces to a raw requirement, it's a requirement. If it's a "how" choice among valid alternatives, it's a design decision. Surface the boundary cases. |

### Red Flags

- Classifying requirements without first inventorying all input sources
- Accepting "TBD" or "as needed" as a requirement without chasing down the owner
- Silently resolving conflicts instead of surfacing them
- Deriving requirements that don't trace back to any raw source
- Proceeding to architecture design before ownership is assigned
- Skipping the human review gate (Step 6)

### Verification

- [ ] All raw input sources inventoried with versions and dates
- [ ] Every requirement classified by domain and type
- [ ] All conflicts, gaps, and ambiguities surfaced and resolved
- [ ] Every derived requirement traces to at least one raw requirement
- [ ] Every requirement has an assigned owner
- [ ] The human has explicitly confirmed the requirements document
- [ ] The document is saved to a version-controlled location

---

## Skill 2: `architecture-design`

### Positioning

Transforms structured system requirements into a concrete architecture: module decomposition, interface definitions, constraint analysis, and design trade-off decisions. This is the bridge between "what must the system do" and "how will we build it."

Analogous to `planning-and-task-breakdown` in agent-skills, but for hardware-software system architecture rather than software implementation tasks.

### When to Use

- Structured system requirements exist (output of `requirements-decompose`)
- Starting a new chip application design
- Adding a major subsystem to an existing design
- Evaluating architecture alternatives against requirements
- Downstream skill (`spec-authoring`) detects missing architecture decisions

**When NOT to use:**

- Requirements are not yet decomposed (run `requirements-decompose` first)
- The change is limited to a single module with no interface impact
- Pure implementation task ("implement this driver per existing architecture")

### The Process

```
DECOMPOSE ──→ INTERFACE ──→ CONSTRAINT ──→ TRADE-OFF ──→ DOCUMENT
    │             │             │              │              │
    ▼             ▼             ▼              ▼              ▼
  Module       Define        Analyze        Evaluate       Produce
  breakdown    all IFs       constraints    alternatives   architecture
                                                           document
```

#### Step 1: DECOMPOSE — Module breakdown

From the system requirements, identify the major functional blocks and their boundaries:

**Decomposition rules:**
1. Each module has a single, clearly defined responsibility
2. Module boundaries follow natural interfaces (buses, protocols, voltage domains)
3. Modules that change together stay together; modules that change for different reasons are separate
4. Hardware-dependent modules are isolated from hardware-independent logic

**Output — Module Definition Table:**

```markdown
| Module ID | Module Name | Responsibility | Depends On | Provides To |
|-----------|-------------|---------------|------------|-------------|
| MOD-01 | Power Sequencer | Power state machine (S0/S3/S5), rail sequencing | GPIO driver, Timer | SMCHost, Thermal |
| MOD-02 | SMCHost | Host interface (eSPI/LPC), Port 62/66, KCS | eSPI driver, Power Seq | Peripheral, Sensor |
| MOD-03 | Thermal Engine | Temperature monitoring, fan PID control | ADC driver, PWM driver | Power Seq (thermal shutdown) |
| MOD-04 | CABI Adapter | SPI-based IPC with MCU Core | SPI driver, DMA | All inter-core modules |
| ... | ... | ... | ... | ... |
```

#### Step 2: INTERFACE — Define all interfaces

For every dependency arrow in the module decomposition, define the interface precisely:

**Interface Definition Template:**

```markdown
### Interface: Power Sequencer ↔ SMCHost

| Property | Specification |
|----------|--------------|
| Type | Event-driven (k_event) + shared state (struct) |
| Direction | Bidirectional |
| Initiator | SMCHost (host commands), Power Seq (state change notifications) |
| Protocol | sysevent event bus (see system/sysevent.h) |
| Events IN | EVENT_HOST_SLP_S3, EVENT_HOST_SLP_S5, EVENT_HOST_PWRBTN |
| Events OUT | EVENT_PWR_STATE_CHANGE, EVENT_PWR_FAILURE |
| Shared State | `struct power_state` (protected by mutex power_state_lock) |
| Timing | State change notification within 100μs of rail stable |
| Error Handling | EVENT_PWR_FAILURE triggers thermal shutdown and host notification |
| Version | v1.0 |
```

**Interface checklist:**
- [ ] Data format and encoding defined
- [ ] Timing/performance bounds specified
- [ ] Error handling and failure modes defined
- [ ] Concurrency model (blocking, non-blocking, ISR context, thread context)
- [ ] Version compatibility strategy

#### Step 3: CONSTRAINT — Analyze system constraints

Extract and cross-reference all constraints from the requirements:

```markdown
| Constraint ID | Constraint | Source | Affected Modules | Verification |
|---------------|------------|--------|-----------------|--------------|
| CON-001 | Total boot time < 500ms cold, < 100ms warm | SYS-REQ-005 | MOD-01, MOD-02, MOD-04 | Integration test |
| CON-002 | SPI flash read ≥ 50MB/s sustained | HW-REQ-012 | MOD-04 | HW test |
| CON-003 | Total power < 2W in S0 (all rails active) | SYS-REQ-008 | MOD-01, MOD-03 | Power measurement |
| CON-004 | Memory budget: 256KB SRAM total, 128KB for FW | HW-REQ-015 | All SW modules | Static analysis |
```

Constraint conflicts should be surfaced immediately — these are often the hardest problems and earliest to catch:

```
CONSTRAINT CONFLICT:
CON-001 requires boot < 500ms, but CON-002 requires flash init + calibration
that takes 300ms alone, leaving 200ms for all other boot phases.
→ Relax CON-001 to 600ms, or optimize flash init (hardware change)?
```

#### Step 4: TRADE-OFF — Evaluate alternatives

For every non-trivial architecture decision, document the alternatives considered and the rationale:

```markdown
### Decision: Inter-Core Communication Protocol

**Context:** SIO Core (Cortex-M33) and MCU Core (Cortex-M4F) need bidirectional
communication over SPI at ≥ 10Mbps.

**Alternatives considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A. CABI (custom packet protocol) | Tailored to our use case, minimal overhead, already proven in gen-1 | Custom, no ecosystem tooling, team must maintain parser | ✅ SELECTED |
| B. OpenAMP (RPMsg over VirtIO) | Industry standard, Linux-compatible | Heavy (≥ 32KB code), complex init, overkill for dual-M-core | Rejected |
| C. Raw SPI with custom framing | Simplest hardware path | Re-inventing flow control, no multi-client support | Rejected |

**Rationale:** CABI provides the right balance of overhead vs. flexibility
for a dual-M-core system without an OS on either side. The maintenance
cost is acceptable given the team's familiarity from gen-1.
```

**Trade-off documentation rules:**
- Every architectural decision that had a credible alternative must be documented
- If only one option was considered, ask whether you've actually explored the space
- The rationale must reference specific requirements or constraints, not vague preferences

#### Step 5: DOCUMENT — Produce the architecture document

Assemble the complete architecture design document.

### Output

An architecture design document (saved to `docs/architecture/[project]-architecture-design.md` after confirmation):

```markdown
# Architecture Design: [Project/Chip Name]

## Document Control
- Version, Date, Author
- References: [System Requirements doc, Datasheet, Standards]

## System Block Diagram
[ASCII art or reference to diagram file]

## Module Definitions
[Module table from Step 1]

## Interface Specifications
[Per-interface definitions from Step 2 — every module dependency has an IF spec]

## Constraint Analysis
[Constraint table from Step 3, plus conflict resolutions]

## Design Decisions & Trade-offs
[Per-decision rationale from Step 4]

## Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| ... | High/Med/Low | High/Med/Low | ... | ... |

## Open Items
[Questions needing resolution before spec-authoring]
```

### Interaction with Other Skills

- **`requirements-decompose`**: Invoked inline if the input requirements document is incomplete or contains unresolved conflicts. Architecture design cannot proceed on unstable requirements.
- **`source-driven-development`** (from agent-skills): Invoked inline when the architecture references third-party IP, standard protocols, or framework constraints that need verification against official documentation.
- **`spec-authoring`**: Downstream consumer. Each module in the architecture becomes a section in the software outline design.
- **`design-review`**: Can review the architecture document for cross-department consistency.

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The architecture is obvious from the reference design" | Reference designs answer "what worked for the demo." Your product has different constraints, different peripherals, different cost targets. |
| "We'll define interfaces during implementation" | Interfaces defined during implementation are defined by the first person who writes code. Interfaces defined in architecture are designed for all consumers. |
| "Trade-off documentation is overhead" | Six months later, someone will ask "why didn't we use OpenAMP?" If you can't answer from the document, you'll re-litigate the decision. |
| "Constraints are the HW team's problem" | Every constraint that HW owns, SW inherits. Partitioning ownership is the SE's core job. |

### Red Flags

- Module decomposition that maps 1:1 to the chip's IP block list (that's a block diagram, not an architecture)
- Interfaces described only as "TBD" or "standard [protocol name]" without specifics (address, speed, IRQ, locking)
- Zero documented trade-offs (means either the design space wasn't explored, or decisions weren't recorded)
- Constraints listed without affected modules (constraints without impact analysis are trivia)
- Skipping interface error handling ("happy path only" architecture)

### Verification

- [ ] Every system requirement is addressed by at least one module or design decision
- [ ] Every module dependency has a defined interface specification
- [ ] All constraints are analyzed for conflicts and assigned to modules
- [ ] Every non-trivial design decision has documented alternatives and rationale
- [ ] Risk register covers key technical uncertainties
- [ ] The human has explicitly confirmed the architecture document
- [ ] The document is saved to a version-controlled location

---

## Skill 3: `spec-authoring`

### Positioning

Transforms architecture design and system requirements into formal specification documents: Software Outline Design (软件概要设计), Hardware-Software Interface Specification, and Test Plan (测试方案). This is the most document-heavy SE task and the one where structure and templates provide the most leverage.

Analogous to `spec-driven-development` in agent-skills, but for chip-vendor specification formats rather than software feature specs.

### When to Use

- Architecture design is complete and confirmed
- Need to produce formal Software Outline Design (软件概要设计)
- Need to produce Hardware-Software Interface Specification
- Need to produce Test Plan (测试方案) from requirements and architecture
- A specific specification document is requested

**When NOT to use:**

- Architecture is not yet designed (run `architecture-design` first)
- The document already exists and only needs a minor update
- Pure documentation formatting (the skill is about content generation, not template filling)

### The Process

```
SELECT ──→ GATHER ──→ GENERATE ──→ CROSS-CHECK ──→ FINALIZE
  │          │           │             │              │
  ▼          ▼           ▼             ▼              ▼
 Choose    Collect     Author       Verify          Human
 which     all input   the spec     internal        review &
 spec(s)   artifacts   content      consistency     sign-off
```

#### Step 1: SELECT — Choose which specification(s) to produce

The skill supports three specification types. The user may request one, two, or all three:

| Spec Type | Chinese Name | Primary Audience | Content Focus |
|-----------|-------------|-----------------|---------------|
| Software Outline Design | 软件概要设计 | SW team, FW developers | Module decomposition, data structures, APIs, state machines, thread model |
| HW-SW Interface Spec | 软硬件接口规格 | HW team, SW team, Validation | Pin assignments, register maps, timing diagrams, interrupt routing |
| Test Plan | 测试方案 | Test team, Validation | Test cases mapped to requirements, test environment, pass/fail criteria |

Ask the user which spec(s) to generate. If the answer is "all of them," generate sequentially (SOD → HW-SW IF → Test Plan) because later specs reference earlier ones.

#### Step 2: GATHER — Collect all input artifacts

Assemble the complete input set:

```
INPUT ARTIFACTS FOR [Spec Type]:
- System Requirements: [doc path, version]      ← from requirements-decompose
- Architecture Design: [doc path, version]       ← from architecture-design
- Chip Datasheet: [doc, revision, sections]
- Reference Manual: [doc, revision, sections]
- Company Template: [template path, version]
- Related Specs: [list of already-completed specs this one references]
→ Confirm: are these the right versions? Any additional inputs?
```

If any input artifact is missing or outdated, invoke the upstream skill (`requirements-decompose` or `architecture-design`) inline, or surface the gap to the user.

#### Step 3: GENERATE — Author the specification content

Each spec type has a defined structure. The skill generates content following these structures, referencing the input artifacts for every claim.

**Software Outline Design (SOD) Structure:**
```markdown
# Software Outline Design: [Module/System Name]

## 1. Document Control
- Version, Date, Author, Change History

## 2. Scope and References
- What this document covers and what it explicitly does NOT cover
- References: System Requirements, Architecture Design, Datasheet, Standards

## 3. Module Overview
- Module's role in the system (from architecture-design)
- One-paragraph summary of responsibility

## 4. Functional Description
### 4.1 Feature List
| Feature ID | Feature | Requirement Trace | Priority |
|------------|---------|-------------------|----------|
| ... | ... | SYS-REQ-XXX | P0/P1/P2 |

### 4.2 State Machine (if applicable)
[State diagram + state transition table with trigger conditions]

### 4.3 Data Flow
[Data flow diagram or description: inputs → processing → outputs]

## 5. Interface Specification
### 5.1 External Interfaces
[From architecture-design Step 2 — referenced with MOD-IDs]

### 5.2 Internal Data Structures
```c
// Key structs, enums, constants with field descriptions
typedef struct {
    uint32_t field;  // description, valid range
} module_state_t;
```

### 5.3 API / Function Signatures
| Function | Signature | Precondition | Postcondition | Caller | Context |
|----------|-----------|-------------|---------------|--------|---------|
| module_init | `int module_init(void)` | HW initialized | Module ready | app.c | Thread |
| ... | ... | ... | ... | ... | ... |

## 6. Design Constraints
### 6.1 Timing Constraints
| Constraint | Value | Source | Verification |
|------------|-------|--------|-------------|
| ... | ... | ... | ... |

### 6.2 Memory Constraints
| Region | Size | Purpose |
|--------|------|---------|
| ... | ... | ... |

### 6.3 Concurrency Model
- Thread assignment (if thread model)
- Locking strategy (mutexes, spinlocks, lock-free)
- ISR vs. thread context boundaries

## 7. Error Handling
| Error Condition | Detection | Response | Recovery |
|----------------|-----------|----------|----------|
| ... | ... | ... | ... |

## 8. Open Items
[Questions requiring resolution before detailed design / implementation]
```

**HW-SW Interface Spec Structure:**
```markdown
# Hardware-Software Interface Specification: [System/Subsystem Name]

## 1. Document Control

## 2. Scope and References

## 3. Pin / Signal Assignment
| Signal Name | GPIO / Pin | Direction | Voltage Domain | Pull | Initial State | SW Access |
|-------------|-----------|-----------|---------------|------|---------------|-----------|
| PWRBTN_IN   | GPIOA_3   | Input     | 3.3V           | PU   | High          | gpio_read() |
| ... | ... | ... | ... | ... | ... | ... |

## 4. Register Map
| Address | Register Name | Bit(s) | Access | Reset Value | Description |
|---------|--------------|--------|--------|-------------|-------------|
| 0x4000_1000 | CTRL_REG | [0] | R/W | 0x0 | Enable bit |
| ... | ... | ... | ... | ... | ... |

## 5. Interrupt Map
| IRQ # | Source | Priority | Handler | Latency Budget |
|-------|--------|----------|---------|---------------|
| ... | ... | ... | ... | ... |

## 6. Timing Diagrams
[For critical sequences: power-on, reset, bus transactions]
[ASCII art or reference to waveform documents]

## 7. Power Domain Crossings
[Signals crossing between independently-powered domains]
| Signal | From Domain | To Domain | Level Shifter | Isolation |
|--------|------------|-----------|---------------|-----------|
| ... | ... | ... | ... | ... |

## 8. Open Items
```

**Test Plan Structure:**
```markdown
# Test Plan: [System/Module Name]

## 1. Document Control

## 2. Scope and References
- What is tested, what is explicitly excluded
- Environment assumptions

## 3. Test Environment
### 3.1 Hardware Requirements
| Equipment | Purpose | Quantity |
|-----------|---------|----------|
| ... | ... | ... |

### 3.2 Software Requirements
| Tool | Version | Purpose |
|------|---------|---------|
| ... | ... | ... |

### 3.3 Test Setup
[Block diagram of test setup]

## 4. Test Case Matrix
| TC-ID | Requirement Trace | Test Description | Input / Stimulus | Expected Output | Pass Criteria | Priority | Automated? |
|-------|-------------------|-----------------|------------------|-----------------|---------------|----------|-----------|
| TC-001 | SYS-REQ-001 | Verify S0→S3 transition on SLP_S3# | Assert SLP_S3# low | Sequence per power table | All rails off in order, ≤ 10ms | P0 | Yes |
| ... | ... | ... | ... | ... | ... | ... | ... |

## 5. Test Procedures
### TC-001: S0→S3 Transition Test
1. Precondition: System in S0, all rails stable
2. Step 1: Assert SLP_S3# low via test fixture
3. Step 2: Monitor rail sequence on oscilloscope
4. Step 3: Verify sequence matches Table X
5. Step 4: Verify all rails off within 10ms
6. Postcondition: System in S3

## 6. Coverage Analysis
| Requirement ID | Covered By (TC-ID) | Coverage |
|----------------|-------------------|----------|
| SYS-REQ-001 | TC-001 | Full |
| SYS-REQ-002 | TC-002, TC-003 | Full |
| SYS-REQ-003 | — | **GAP** ← flagged for resolution |

## 7. Open Items
```

#### Step 4: CROSS-CHECK — Internal consistency verification

Before presenting to the user, verify internal consistency:

- Every requirement referenced in the spec actually exists in the requirements document
- Every interface described matches the architecture design interface spec
- Every test case traces to at least one requirement
- No "orphan" content (design elements with no requirement trace)
- Version references match across all linked documents

```
CROSS-CHECK RESULTS:
✅ 23/23 requirements have corresponding design elements
⚠️  TC-015 references SYS-REQ-099 which does not exist in requirements doc v1.2
❌ Interface MOD-03→MOD-04 described here but missing from architecture design §5.3
→ Fix these before finalizing.
```

#### Step 5: FINALIZE — Human review and sign-off

Present the complete specification. Do not proceed until the user confirms. This is a formal document that will be referenced by multiple departments — errors here propagate.

### Output

One or more specification documents, saved to `docs/specs/[project]-[spec-type].md` after confirmation.

### Interaction with Other Skills

- **`architecture-design`**: Invoked inline if architecture decisions required for the spec are missing or ambiguous.
- **`requirements-decompose`**: Invoked inline if requirement references in the spec don't resolve.
- **`design-review`**: After the spec is finalized, can be invoked to adversarially review it before distribution.
- **`traceability-matrix`**: Populates the Design Element and Test Case columns.

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The spec is just the architecture doc with more detail" | The architecture doc answers "how does the system fit together." The spec answers "how do I implement this module." Different audiences, different granularity. |
| "I'll write the spec after implementation" | That's documentation, not specification. The spec's value is forcing design clarity before coding starts. |
| "The template is boilerplate — content matters" | Structure communicates. A spec that skips error handling or concurrency model sections implicitly says "these weren't designed." |
| "Test cases can be derived later by the test team" | If the SE doesn't know how to test a requirement, the requirement isn't testable. Testability is a requirement quality, not a test-team responsibility. |

### Red Flags

- Generating spec content that doesn't reference specific requirement IDs
- Interface specifications without timing or error handling
- Test cases without quantified pass/fail criteria
- Skipping cross-check (Step 4) — internal inconsistency in specs erodes trust across departments
- "TBD" used as a placeholder for critical parameters without an owner and deadline

### Verification

- [ ] Spec type(s) explicitly confirmed by user before generation
- [ ] All input artifacts referenced with correct versions
- [ ] Every spec section populated (no empty sections retained from template)
- [ ] Every claim in the spec traces to a requirement or architecture decision
- [ ] Cross-check passed with no unresolved issues
- [ ] Test plan covers every P0 requirement
- [ ] The human has explicitly confirmed the specification document(s)
- [ ] Documents saved to version-controlled location

---

## Skill 4: `design-review`

### Positioning

Adversarial, cross-department review of any SE artifact (requirements document, architecture design, specification). Runs fresh-context reviewers through department-specific lenses (HW, SW, Test, System) to catch gaps, inconsistencies, and unstated assumptions before artifacts are distributed.

Analogous to `doubt-driven-development` in agent-skills — shares the same adversarial posture and fresh-context reviewer pattern — but adapted for multi-discipline hardware-software system design rather than pure software implementation.

### When to Use

- An SE artifact (requirements, architecture, spec) is ready for cross-department distribution
- Before a formal design review meeting — to catch issues in advance
- When integrating across department boundaries
- After a significant design change that may have ripple effects
- A downstream consumer of the artifact reports inconsistency or ambiguity

**When NOT to use:**

- The artifact is a draft that hasn't been self-reviewed yet
- Typos, formatting, or mechanical corrections (use a simpler review)
- The user explicitly wants speed over thoroughness for a low-risk artifact

### The Process

```
SCOPE ──→ LENS-REVIEW ──→ RECONCILE ──→ REPORT
   │           │               │            │
   ▼           ▼               ▼            ▼
 Define    Review through   Classify      Produce
 artifact  4 department     findings      review
 & depth   lenses           by severity   report
```

#### Step 1: SCOPE — Define the review scope

Clarify what is being reviewed and at what depth:

```
REVIEW SCOPE:
Artifact: [type] — [document name] v[X.Y]
Depth: Quick scan (major issues only) / Standard / Exhaustive
Focus areas: [user-specified, or "all"]
Review lenses: HW / SW / Test / System (all default)
→ Confirm scope before proceeding.
```

If the artifact is large (>20 pages), ask the user to specify focus areas. An exhaustive review of a 50-page architecture doc is expensive; a targeted review of the 5 pages most likely to have issues is often higher value.

#### Step 2: LENS-REVIEW — Review through department lenses

Spawn independent fresh-context reviewers, each with a department-specific adversarial prompt. Each reviewer receives the ARTIFACT only (not the author's reasoning, not the CLAIM — matching `doubt-driven-development`'s pattern).

**Four lens prompts:**

**HW Lens:**
```
You are a hardware engineer reviewing this SE artifact. Find issues:

- Are pin assignments, voltage domains, and timing constraints
  specified unambiguously?
- Can the hardware team implement from this spec without
  follow-up questions?
- Are power sequencing, reset, and clock requirements complete?
- Are there assumptions about PCB layout, signal integrity,
  or thermal that should be explicit but aren't?
- Are any HW requirements specified in a way that constrains
  component selection unnecessarily?

Find issues or state that you cannot find any after thorough examination.
```

**SW Lens:**
```
You are a firmware engineer reviewing this SE artifact. Find issues:

- Are register maps, memory maps, and interrupt assignments complete?
- Are API signatures and data structures defined precisely enough
  to implement against?
- Are concurrency, ISR context, and locking requirements specified?
- Are timing budgets realistic given the RTOS and CPU constraints?
- Are error handling and edge cases covered for every interface?

Find issues or state that you cannot find any after thorough examination.
```

**Test Lens:**
```
You are a validation engineer reviewing this SE artifact. Find issues:

- Is every requirement testable with quantified pass/fail criteria?
- Are test environments and equipment specified for non-trivial tests?
- Are there requirements that can only be tested in a specific
  system state that isn't reachable with the proposed test setup?
- Are any requirements inherently untestable (e.g., "shall be robust")?
- Do test cases cover failure modes, not just happy paths?

Find issues or state that you cannot find any after thorough examination.
```

**System Lens:**
```
You are a systems engineer reviewing this SE artifact. Find issues:

- Do cross-domain interactions (HW↔SW, power↔thermal, boot↔security)
  have defined handshake protocols?
- Are there unstated assumptions about system state during
  transitions (boot, shutdown, fault recovery)?
- Do any requirements or design decisions conflict across domains?
- Are failure propagation paths analyzed? (If module A fails,
  what happens to B, C, D?)
- Is the integration sequence (what gets brought up in what order)
  implicit or explicit?

Find issues or state that you cannot find any after thorough examination.
```

**Review orchestration:** All four lens reviews run in parallel. Each returns structured findings.

#### Step 3: RECONCILE — Classify findings

Consolidate findings from all four lenses. For each finding, classify using the `doubt-driven-development` precedence (first matching class wins):

1. **Artifact misread** — reviewer flagged something because the artifact was unclear. Fix the artifact text, not the design.
2. **Valid + actionable** — real issue requiring a design or spec change.
3. **Valid trade-off** — issue is real but cost of fixing exceeds cost of accepting. Document the trade-off.
4. **Noise** — reviewer flagged something correct under context the reviewer didn't have.

**Cross-lens synthesis:** When the same issue is flagged by multiple lenses, it's a high-confidence finding. When lenses contradict each other (HW says "too constrained," SW says "not constrained enough"), surface the tension explicitly — these are the most valuable insights.

#### Step 4: REPORT — Produce the review report

### Output

A design review report (saved to `docs/reviews/[project]-[artifact]-review-[date].md`):

```markdown
# Design Review Report: [Artifact Name] v[X.Y]

## Review Summary
- Date: [YYYY-MM-DD]
- Reviewers: HW Lens, SW Lens, Test Lens, System Lens
- Scope: [Standard / Exhaustive / Focused on §X-Y]
- Findings: [N] total — [A] actionable, [B] trade-off, [C] informational

## Actionable Findings (Must Fix)
| ID | Lens | Severity | Description | Affected Section | Proposed Fix |
|----|------|----------|-------------|-----------------|-------------|
| DR-001 | SW + System | Critical | Boot sequence assumes SPI flash ready at t=0; actual ready time is 300ms | Arch §4.2, SOD §6.1 | Add flash-init phase to boot sequence; update timing budget |
| DR-002 | Test | High | SYS-REQ-008 (power < 2W) has no test procedure; current measurement setup undefined | Test Plan §4 | Add power measurement procedure with equipment list |
| ... | ... | ... | ... | ... | ... |

## Trade-off Findings (Accept or Escalate)
| ID | Lens | Description | Cost to Fix | Cost to Accept | Recommendation |
|----|------|-------------|-------------|---------------|---------------|
| ... | ... | ... | ... | ... | ... |

## Cross-Lens Tensions
| Tension | Lenses | Description |
|---------|--------|-------------|
| ... | HW vs SW | ... |

## Informational Notes
| ID | Lens | Note |
|----|------|------|
| ... | ... | ... |

## Review Status
- [ ] All actionable findings resolved or assigned owners
- [ ] Trade-offs escalated to project lead for decision
- [ ] Artifact version bumped to reflect changes
```

### Interaction with Other Skills

- **`requirements-decompose`**: If review finds fundamental requirement gaps, invoke to re-decompose.
- **`architecture-design`**: If review finds architecture-level issues, invoke to redesign affected modules.
- **`spec-authoring`**: If review finds spec issues, invoke to regenerate affected sections.
- **`traceability-matrix`**: After review resolution, re-run to verify traceability is intact.
- **`doubt-driven-development`** (from agent-skills): The philosophical parent. Design-review is doubt-driven-development specialized for SE artifacts.

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The cross-department review meeting will catch issues" | Meetings catch what people notice during meetings. Fresh-context adversarial review catches what people miss when reading for approval. |
| "Four lenses is overkill for a small spec" | Small specs have small blast radii — reduce depth, not lenses. A 5-minute per-lens scan still catches things a single-lens read misses. |
| "The reviewers don't have enough context" | That's the point. If your artifact only makes sense to someone who already knows what you meant, it's not a specification — it's a memory aid. |
| "I can just ask the HW team to review the HW parts" | They will, at the formal review. This skill catches issues *before* the formal review, so the meeting is about decisions, not discovery. |

### Red Flags

- Reviewing an artifact the author hasn't self-reviewed first
- Feeding the reviewer the CLAIM or author's reasoning (biases toward agreement)
- Classifying findings without re-reading the artifact text against each one
- Treating all lens outputs as equally actionable (cross-lens agreement multiplies confidence)
- Skipping the System lens ("it's just HW and SW") — system-level integration issues are the most expensive to fix

### Verification

- [ ] Review scope (artifact, depth, focus areas) confirmed with user
- [ ] All four lens reviews completed with adversarial prompts
- [ ] Every finding classified using the precedence order
- [ ] Cross-lens tensions explicitly surfaced
- [ ] Actionable findings have proposed fixes
- [ ] Review report saved and shared
- [ ] Artifact version updated to reflect review

---

## Skill 5: `traceability-matrix`

### Positioning

Maintains the traceability chain across all SE artifacts: Raw Requirements → System Requirements → Design Elements → Test Cases. Identifies coverage gaps, orphaned design elements, and untested requirements. Runs across artifacts rather than producing one — it's the "lint" of the SE skill chain.

### When to Use

- After completing any SE artifact — to verify coverage
- Before a milestone review (requirements freeze, design freeze, test readiness)
- When scope changes — to assess impact on existing artifacts
- A downstream artifact is complete and needs validation against upstream
- Auditing or certification requires formal traceability

**When NOT to use:**

- No artifacts exist yet (run the upstream skills first)
- The change is purely editorial (typo fixes, reformatting)

### The Process

```
LINK ──→ COVERAGE ──→ GAP-ANALYSIS ──→ REPORT
  │          │             │              │
  ▼          ▼             ▼              ▼
 Build     Calculate     Identify       Produce
 trace     coverage      orphans       traceability
 chains    metrics       & gaps        report
```

#### Step 1: LINK — Build traceability chains

Extract all IDs from every artifact and build the link graph:

```
Raw Source → System Req → Architecture Element → Design Element → Test Case
    │             │               │                    │               │
 PRD §3.1    SYS-REQ-001     MOD-01 (Power Seq)    SOD §4.2         TC-001
                                                        │           TC-002
                                                        └───────────TC-003
```

**Extraction rules:**
- Requirements document: extract SYS-REQ-XXX, HW-REQ-XXX, SW-REQ-XXX
- Architecture document: extract MOD-XXX, CON-XXX, IF-XXX
- SOD: extract feature references to requirements
- Test Plan: extract TC-XXX references to requirements

#### Step 2: COVERAGE — Calculate coverage metrics

```markdown
## Coverage Summary

| From | To | Coverage | Detail |
|------|----|----------|--------|
| System Requirements | Architecture Elements | 23/25 (92%) | 2 requirements not addressed by any module |
| System Requirements | Test Cases | 21/25 (84%) | 4 requirements with no test coverage |
| Architecture Elements | Test Cases | 18/23 (78%) | 5 modules with no dedicated test cases |
| Test Cases | Requirements | 30/30 (100%) | All test cases trace to requirements (no orphan tests) |
```

#### Step 3: GAP-ANALYSIS — Identify orphans and gaps

**Orphan detection:**
```
ORPHAN DETECTED:
MOD-07 (Debug UART) — defined in architecture §3.7 but traces to zero requirements.
→ Either this module is unnecessary (remove it) or the requirement is missing (add it).
```

**Gap detection:**
```
COVERAGE GAP:
SYS-REQ-014 ("System shall enter deep sleep when idle > 5s") — no test case.
→ Add test case for deep sleep entry condition and timing.
```

**Over-coverage:**
```
OVER-COVERAGE:
TC-042 tests behavior ("SPI CRC error recovery") not required by any specification.
→ Either this is undocumented required behavior (add requirement) or unnecessary testing (remove test case).
```

#### Step 4: REPORT — Produce the traceability report

### Output

A traceability report (saved to `docs/traceability/[project]-traceability-[date].md`):

```markdown
# Traceability Report: [Project Name]

## Report Metadata
- Date: [YYYY-MM-DD]
- Artifacts Analyzed: [list with versions]
- Generated By: traceability-matrix skill

## Traceability Matrix
| Raw Source | System Req | Arch Element | Design Element | Test Case(s) | Status |
|------------|-----------|-------------|---------------|-------------|--------|
| PRD §3.1 | SYS-REQ-001 | MOD-01 | SOD §4.2 | TC-001, TC-002, TC-003 | ✅ Complete |
| PRD §3.2 | SYS-REQ-002 | MOD-01, MOD-02 | SOD §4.3, §5.1 | TC-004 | ⚠️ Partial (no SW test) |
| Datasheet §5 | HW-REQ-003 | — | — | — | ❌ No trace (orphan) |
| — | — | MOD-07 | SOD §8 | — | ❌ No trace (orphan) |

## Coverage Summary
[From Step 2]

## Gap Analysis
### Requirements Without Design
| Req ID | Description | Impact | Recommendation |
|--------|-------------|--------|---------------|
| ... | ... | ... | ... |

### Requirements Without Tests
| Req ID | Description | Priority | Recommendation |
|--------|-------------|----------|---------------|
| ... | ... | ... | ... |

### Orphaned Design Elements
| Element | Location | Recommendation |
|---------|----------|---------------|
| ... | ... | ... |

## Action Items
| ID | Description | Owner | Due |
|----|-------------|-------|-----|
| ... | ... | ... | ... |
```

### Interaction with Other Skills

- **`requirements-decompose`**: Invoked if orphan requirements are found (missing trace source).
- **`architecture-design`**: Invoked if orphan architecture elements are found.
- **`spec-authoring`**: Invoked if test gaps require new test cases.
- **`design-review`**: Traceability gaps should be resolved before design review, not discovered during it.

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Traceability is just paperwork for auditors" | Traceability is the only way to answer "if we change X, what breaks?" without reading every document. |
| "100% coverage is impossible, don't bother" | 100% is not the goal. Knowing *which* 15% is uncovered is the goal. |
| "I'll trace manually in a spreadsheet" | Manual traceability drifts. Every artifact update breaks links. Automated re-extraction catches drift immediately. |

### Red Flags

- Running traceability without version-pinning all input artifacts
- Reporting coverage percentages without listing what's NOT covered
- Orphan detection finding items that are "probably fine" — every orphan should be resolved or explicitly waived
- Generating action items without owners

### Verification

- [ ] All input artifacts referenced with exact versions
- [ ] Every requirement ID extracted and linked
- [ ] Coverage metrics calculated for all traceability dimensions
- [ ] Every orphan and gap documented with a recommendation
- [ ] Action items assigned owners
- [ ] Report saved to version-controlled location

---

## Skill Interaction Map

```
                    ┌─────────────────────┐
                    │   interview-me       │  (from agent-skills)
                    │   (preamble: clarify │
                    │    vague inputs)      │
                    └──────────┬──────────┘
                               │ invoked by requirements-decompose
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      requirements-decompose                       │
│  Raw Inputs → Structured System Requirements                     │
│  Output: System Requirements Document (with traceability IDs)     │
└──────────┬───────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      architecture-design                          │
│  System Reqs → Module Decomposition, IF Specs, Constraints        │
│  Output: Architecture Design Document                             │
│  Can invoke: requirements-decompose, source-driven-development    │
└──────────┬───────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      spec-authoring                               │
│  Architecture + Reqs → SOD, HW-SW IF Spec, Test Plan              │
│  Output: Formal Specification Documents                           │
│  Can invoke: architecture-design, requirements-decompose          │
└──────────┬───────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      design-review                                │
│  Adversarial cross-dept review of any SE artifact                 │
│  Output: Review Report with classified findings                   │
│  Can invoke: ANY upstream skill to fix issues found               │
└──────────────────────────────────────────────────────────────────┘

                         ┌──────────────────────────┐
                         │   traceability-matrix     │  (runs across all artifacts)
                         │   Req → Design → Test     │
                         │   Output: Trace Report    │
                         │   Can invoke: any skill   │
                         │   to fill gaps            │
                         └──────────────────────────┘
```

**Invocation rules:**
1. Each skill checks whether its required upstream artifact exists before proceeding. If missing, it either invokes the upstream skill inline (with user confirmation) or surfaces the gap.
2. Skills invoked inline run with the same `se-skills` persona context — they share the SE's domain knowledge and document conventions.
3. Skills can invoke `agent-skills` skills (`interview-me`, `source-driven-development`, `doubt-driven-development`) but the reverse is not true — `agent-skills` does not know about `se-skills`.

---

## Design Decisions

### Why 5 skills instead of 1?

| Approach | Pros | Cons |
|----------|------|------|
| 1 monolithic `se-workflow` skill | Simple invocation, linear flow | Can't use one part without running the whole chain; hard to update one step; can't compose with other skills mid-flow |
| 5 independent skills with inline invocation | Granular, composable, matches agent-skills UX | More files, must design interaction contracts carefully |
| → **5 skills (chosen)** | SE can invoke just `spec-authoring` with existing requirements and architecture; or just `design-review` on a colleague's artifact; or run the full chain when starting fresh |

### Why department-lens review instead of generic review?

A generic "review this design" prompt produces generic feedback. The HW engineer, FW engineer, and test engineer read the same document looking for different things. The lens structure forces each perspective to be exercised explicitly. Cross-lens tensions are the highest-value output — they represent exactly the integration issues that SEs exist to resolve.

### Why traceability as a separate skill?

Traceability is inherently cross-artifact. It doesn't produce a primary artifact of its own — it validates the relationships between artifacts. Embedding it in `spec-authoring` or `design-review` would couple it to a specific workflow step. As a standalone skill, it can be run at any point: after requirements (to verify completeness), after architecture (to verify coverage), after test plan (to verify every requirement is tested), or before a milestone review (to produce the formal traceability report).

---

## File Layout

Following the `agent-skills` directory convention:

```
skills/
├── se-skills/
│   ├── README.md                          # This design document
│   ├── requirements-decompose/
│   │   └── SKILL.md
│   ├── architecture-design/
│   │   └── SKILL.md
│   ├── spec-authoring/
│   │   └── SKILL.md
│   ├── design-review/
│   │   └── SKILL.md
│   └── traceability-matrix/
│       └── SKILL.md
```

Each `SKILL.md` follows the exact format of `agent-skills`: YAML frontmatter (name, description), Overview, When to Use, Process (numbered steps), Output, Interaction with Other Skills, Common Rationalizations, Red Flags, Verification checklist.

---

## Next Steps

1. **Review this design** — confirm the skill set, scope, and interaction model match what you need
2. **Prioritize** — which skill to implement first? (Recommendation: `requirements-decompose` — it's the entry point and has the most inline-invocation dependencies)
3. **Write the SKILL.md files** — following this design doc as the spec
4. **Test on a real project** — run the chain end-to-end on an actual chip application project
5. **Iterate** — adjust based on what works and what doesn't in practice

---

*Design authored for review. No SKILL.md files written yet — confirm the design before implementation.*
