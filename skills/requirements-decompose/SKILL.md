---
name: requirements-decompose
description: Transforms raw, heterogeneous inputs (PRD, chip datasheet, industry standards, customer specs) into a structured, traceable system requirements document. Use when a new chip or product project kicks off and requirements exist only as scattered documents, when multiple input sources contradict each other, or when you need to assign ownership (HW/SW/System) to each requirement.
---

# Requirements Decompose

## Overview

Raw requirements arrive as a pile of heterogeneous documents — a PRD from marketing, a chip datasheet from the hardware team, an industry standard, a customer specification, a reference design. None of them speak the same language. None of them are structured for engineering traceability. None of them are complete on their own.

This skill transforms that pile into a single, structured system requirements document where every requirement is classified by domain and type, conflicts are resolved, gaps are identified, derived requirements are explicit, and ownership is assigned. Every downstream artifact — architecture, specifications, test plans — depends on this document. The quality of the entire project starts here.

This skill is to SE what `interview-me` is to software development: it confronts ambiguity head-on before any design work begins.

## When to Use

- A new chip or product project kicks off and requirements exist only as a PRD or datasheet
- Multiple input sources exist (datasheet + standard + customer spec) and need consolidation into one source of truth
- Requirements are implicit, scattered across documents, or contradict each other
- You need to assign ownership (HW / SW / System / Mechanical) to each requirement before design begins
- A downstream skill (`architecture-design`, `spec-authoring`) detects incomplete or ambiguous requirements and invokes this skill inline

**When NOT to use:**

- Requirements are already fully decomposed and traceable in a structured document with IDs
- The ask is a single-module change with no new system-level impact
- Pure information lookup ("what does the datasheet say about register X?")
- The user explicitly asks for a quick answer without formal decomposition

## The Process

```
COLLECT ──→ CLASSIFY ──→ RESOLVE ──→ DERIVE ──→ ASSIGN ──→ VALIDATE
   │           │           │           │           │            │
   ▼           ▼           ▼           ▼           ▼            ▼
 Gather     Categorize  Resolve     Derive     Assign       Human
 all raw    by domain   conflicts   system-    ownership    review
 inputs     & type      & gaps      level reqs (HW/SW/SYS)  & sign-off
```

### Step 1: COLLECT — Inventory all raw inputs

Before any analysis, inventory every input source and surface the list to the user:

```
RAW INPUT INVENTORY:
1. PRD:                 [document name, version, date, owner]
2. Chip Datasheet:      [chip name, revision, sections relevant]
3. Industry Standard:   [standard name, version, mandatory/optional clauses]
4. Customer Spec:       [customer name, document ID, date]
5. Reference Design:    [platform, version]
6. Legacy/Previous-gen: [project name, document ID]
→ Any other inputs I'm missing?
```

This is the cheapest moment to catch missing inputs. A missing source discovered during Step 3 ("resolve conflicts") means re-doing the classification.

### Step 2: CLASSIFY — Categorize every requirement

Extract every requirement from every source and classify it across two axes.

**Domain axis** — who owns this requirement?

| Domain | Examples |
|--------|----------|
| HW | Pin assignments, voltage domains, clock trees, PCB constraints, signal integrity |
| SW | Driver interfaces, protocol stacks, RTOS requirements, memory maps, boot flow |
| System | Power sequences, reset behavior, cross-domain timing, fault propagation |
| Mechanical | Thermal envelope, form factor, connector placement, mounting |
| Compliance | Certification (FCC, CE, UL), safety standards, security requirements |

**Type axis** — what kind of statement is this?

| Type | Marker words | Treatment |
|------|-------------|-----------|
| Functional | "shall support", "must provide", "is responsible for" | Trace to design element |
| Performance | "within X μs", "≤ Y mW", "≥ Z Mbps" | Trace to verification test |
| Constraint | "must not exceed", "only when", "limited to" | Trace to design rule / DFM |
| Interface | "via I2C", "over SPI at Z MHz", "through GPIO" | Trace to interface specification |
| Safety/Security | "must not result in", "shall isolate", "shall authenticate" | Trace to safety analysis |

**Output after Step 2:** A classified requirement table:

```markdown
| ID    | Raw Requirement | Source | Domain | Type    | Status |
|-------|----------------|--------|--------|---------|--------|
| REQ-001 | "SPI flash must respond within 10ms" | Datasheet §3.2 | SW | Performance | Draft |
| REQ-002 | "Vcore ramp 0.6V→1.1V in ≤ 2ms" | PRD §4.1 | System | Performance | Draft |
| REQ-003 | "eSPI bus operates at 66MHz" | Standard §2 | HW | Interface | Draft |
| REQ-004 | "System shall support S0/S3/S5 states" | PRD §2 | System | Functional | Draft |
```

### Step 3: RESOLVE — Conflict detection and gap identification

This is the highest-value step. Cross-reference all classified requirements and surface three categories of issues.

**Conflicts** — two sources say different things about the same requirement:

```
CONFLICT DETECTED:
REQ-012 (Datasheet §5.1): "I2C pull-up to 3.3V"
REQ-047 (PRD §3.2):      "All I2C buses operate at 1.8V"
→ These cannot both be true. Which source takes precedence?
→ GUESS: Datasheet takes precedence for electrical specs. PRD may be stale.
```

**Gaps** — a requirement is mentioned but not specified:

```
GAP DETECTED:
PRD mentions "secure boot" but no requirements specify:
- Which authentication algorithm (RSA / ECDSA / other)?
- Key storage mechanism (OTP / eFuse / external secure element)?
- Boot timeout behavior on verification failure?
→ These must be resolved before architecture design can proceed.
```

**Ambiguities** — a requirement exists but is not testable:

```
AMBIGUITY DETECTED:
REQ-023: "System shall boot quickly"
→ "Quickly" is not testable. Target: cold boot < 500ms? warm boot < 100ms?
→ GUESS: cold boot < 500ms based on competitive analysis. Confirm?
```

For every conflict, gap, and ambiguity, attach a GUESS with your reasoning — following the `interview-me` pattern. Reacting to a wrong guess is faster for the user than generating an answer from scratch.

### Step 4: DERIVE — Generate system-level requirements

Raw requirements often state *what* without *how*. Derive system-level requirements that bridge the gap between market intent and engineering specification:

```
RAW (from PRD):
  "Chip supports S0/S3/S5 power states"

DERIVED:
  SYS-REQ-001: "System shall transition S0→S3 when host asserts SLP_S3#"
  SYS-REQ-002: "System shall transition S3→S0 within 500μs of SLP_S3# de-assertion"
  SYS-REQ-003: "System shall sequence power rails S0→S3 per Table X (reverse order)"
  SYS-REQ-004: "System shall assert PWR_OK to host only after all rails stable in S0"
  SYS-REQ-005: "System shall enter S5 on SLP_S5# assertion regardless of S3 state"
```

**Derivation rules:**
- Every derived requirement must trace back to at least one raw requirement
- Every derived requirement must be testable — quantified, observable, with a clear pass/fail condition
- If a derivation feels like an architectural decision ("how" choice among valid alternatives) rather than a requirement ("what" must be true), flag it — it belongs in `architecture-design`, not here
- If you can't derive a requirement without guessing the architecture, surface the ambiguity: *"This derivation assumes a single-rail-sequencer design. If a multi-sequencer design is chosen, this splits into N requirements."*

### Step 5: ASSIGN — Ownership assignment

Assign every requirement to the owning discipline and the verifying discipline:

```markdown
| ID          | Requirement | Owner | Verifier |
|-------------|-------------|-------|----------|
| SYS-REQ-001 | S0→S3 transition on SLP_S3# | System (SE) | HW Test |
| SYS-REQ-002 | S3→S0 within 500μs | SW (FW) | SW Test |
| HW-REQ-001  | I2C pull-up 3.3V ±5% | HW (EE) | HW Test |
| SW-REQ-001  | SPI driver supports DMA chaining | SW (FW) | SW Test |
```

**Ownership rules:**
- A requirement with no owner is a requirement that will not be implemented
- Owner ≠ Verifier. The owner implements; the verifier confirms independently
- If ownership is unclear ("this could be HW or SW"), surface it: the decision is an architectural one

### Step 6: VALIDATE — Human review and sign-off

Present the complete structured requirements document. Do not proceed to `architecture-design` until the user confirms.

Ask explicitly:

```
Here's the complete system requirements document with [N] requirements
across [M] domains. [X] conflicts resolved, [Y] gaps identified and
addressed, [Z] requirements derived.

Does this capture everything? Anything to add, change, or remove?
```

The gate is an explicit confirmation. "Looks fine" is not confirmation — ask "anything to refine?" Silence is not confirmation — neither is "sure, let's move on."

## Output

A structured system requirements document saved to `docs/requirements/[project]-system-requirements.md` after user confirmation:

```markdown
# System Requirements: [Project/Chip Name]

## Document Control
- Version: [1.0 draft]
- Date: [YYYY-MM-DD]
- Author: [SE name]
- Input Sources: [list with document names, versions, dates]

## Requirement Table
| ID | Requirement | Source | Domain | Type | Owner | Verifier | Status |
|----|-------------|--------|--------|------|-------|----------|--------|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Derived Requirements
| ID | Requirement | Derived From | Rationale |
|----|-------------|-------------|-----------|
| ... | ... | ... | ... |

## Conflict Resolution Log
| Conflict ID | Description | Sources | Resolution | Resolved By | Date |
|-------------|-------------|---------|------------|-------------|------|
| ... | ... | ... | ... | ... | ... |

## Gap Log
| Gap ID | Description | Impact | Resolution | Owner | Due |
|--------|-------------|--------|------------|-------|-----|
| ... | ... | ... | ... | ... | ... |

## Traceability Seed (for traceability-matrix skill)
| Raw Source | System Req ID | Design Element | Test Case |
|------------|--------------|----------------|-----------|
| ... | ... | (filled by architecture-design) | (filled by spec-authoring) |
```

## Interaction with Other Skills

- **`interview-me`** (from agent-skills): Invoked inline when a requirement is too vague to classify. When the user says "system shall be robust" or "must be high-performance," invoke `interview-me` to extract what those words actually mean in measurable terms.
- **`architecture-design`**: Downstream consumer. The structured requirements document is the primary input to architecture design. Each REQ-ID becomes a constraint that architecture must satisfy.
- **`spec-authoring`**: Two hops downstream. Requirements are referenced by specification sections and test case definitions.
- **`traceability-matrix`**: Populates the first column of the matrix (Raw Source → System Requirement). The traceability seed table in this document's output is the starting point for the full matrix.
- **`design-review`**: Can review the requirements document for completeness before it feeds downstream. A requirements gap caught here costs a conversation; caught during architecture design costs rework.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The PRD is clear enough — let's just start designing" | PRDs state what marketing wants. System requirements state what engineering can verify. The gap between them is where projects ship late. |
| "Conflicts will get caught in the design review meeting" | Catching a conflict during design review means redesigning architecture. Catching it here costs a conversation. |
| "I can classify requirements while designing the architecture" | Classification and design are different cognitive modes. Switching between them produces shallow work in both. |
| "Derived requirements are just design decisions — leave them for architecture" | If it is testable and traces to a raw requirement, it is a requirement. If it is a "how" choice among valid alternatives, it is a design decision. Surface the boundary cases rather than silently categorizing. |
| "We don't need formal requirement IDs — everyone knows what REQ-001 means" | "Everyone" changes over the life of a project. New team members, handoffs, and audits all need explicit traceability. The IDs cost nothing; the ambiguity costs everything. |
| "The customer spec is the requirement — we don't need to re-write it" | Customer specs are written for the customer's procurement process, not for your engineering process. They mix requirements, preferences, and aspirational language. Decomposition separates these. |

## Red Flags

- Classifying requirements without first inventorying all input sources with versions
- Accepting "TBD" or "as needed" as a terminal requirement state without an owner and deadline
- Silently resolving conflicts instead of surfacing them to the user with a proposed resolution
- Deriving requirements that do not trace back to any raw source (unmoored requirements)
- Deriving requirements that are actually architecture decisions (jumping to "how" before "what" is complete)
- Proceeding to architecture design before ownership is assigned — unowned requirements will be orphaned
- Skipping the human review gate (Step 6) because "the classification looks complete"
- A requirement whose type and domain are both unclear — revisit Step 2 before moving on

## Verification

After completing requirements decomposition:

- [ ] All raw input sources inventoried with names, versions, dates, and owners
- [ ] Every requirement extracted and classified by both domain and type
- [ ] All conflicts have explicit resolutions with source precedence documented
- [ ] All gaps have owners and due dates for resolution
- [ ] All ambiguities have been chased down to quantified, testable statements
- [ ] Every derived requirement traces to at least one raw requirement
- [ ] Every derived requirement is testable (quantified, observable, clear pass/fail)
- [ ] Every requirement has an assigned owner AND a verifier (not the same person)
- [ ] The traceability seed table is populated (Raw Source → System Req ID)
- [ ] The human has explicitly confirmed the requirements document (not "looks fine," not "sure")
- [ ] The document is saved to a version-controlled location under `docs/requirements/`
