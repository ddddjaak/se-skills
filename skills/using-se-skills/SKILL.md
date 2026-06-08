---
name: using-se-skills
description: Discovers and invokes SE skills. Use when starting an SE session or when you need to discover which SE skill applies to the current task. This is the meta-skill that governs how all other SE skills are discovered and invoked.
---

# Using SE Skills

## Overview

SE Skills is a collection of workflow skills for chip vendor System Engineers (Application Architects), organized by the SE workflow phase. Each skill encodes a specific process that senior SEs follow — from raw requirements decomposition through architecture design, formal specification authoring, cross-department review, and traceability validation.

This meta-skill helps you discover and apply the right skill for your current SE task.

## When to Use

- Starting a new chip application project and unsure which skill to apply first
- You know the SE workflow exists but don't know which phase you're in
- A task spans multiple SE phases and you need to know the correct sequence
- A colleague asks "which SE skill should I use for this?"
- You want a quick reference for the full SE skill lifecycle

**When NOT to use:**

- You already know exactly which skill to invoke (just invoke it directly)
- The task is not SE-related (e.g., pure software implementation, hardware design, mechanical engineering)

## Skill Discovery

When an SE task arrives, identify the phase and apply the corresponding skill:

```
SE Task arrives
    │
    ├── Raw requirements exist as scattered docs? ──→ requirements-decompose
    │   (PRD + Datasheet + Standards + Customer Spec)
    │
    ├── Have structured requirements, need architecture? ──→ architecture-design
    │   (Module decomposition, interface specs, constraints, trade-offs)
    │
    ├── Architecture is confirmed, need formal specs? ──→ spec-authoring
    │   ├── Firmware team needs implementation spec? ──→ Software Outline Design (软件概要设计)
    │   ├── HW-SW boundary needs definition? ──→ HW-SW Interface Spec (软硬件接口规格)
    │   └── Validation team needs test procedures? ──→ Test Plan (测试方案)
    │
    ├── An artifact is ready for cross-dept review? ──→ design-review
    │   (Four-lens adversarial review: HW, SW, Test, System)
    │
    ├── Need to verify cross-artifact integrity? ──→ traceability-matrix
    │   (Req → Design → Test gap analysis and coverage report)
    │
    └── Not sure what the stakeholder actually wants? ──→ interview-me (from agent-skills)
        (Clarify vague inputs before starting requirements decomposition)
```

## The SE Workflow Chain

For a complete chip application project, the typical skill sequence is:

```
1. interview-me               → Extract what the stakeholder actually wants
    (from agent-skills)         (used when input requirements are vague)

2. requirements-decompose     → Raw inputs → Structured system requirements
                                 with domain classification, ownership assignment,
                                 conflict resolution, and traceability IDs

3. architecture-design        → Requirements → Module decomposition,
                                 interface definitions, constraint analysis,
                                 trade-off decisions

4. spec-authoring             → Architecture + Requirements → Formal specs:
                                 SOD, HW-SW IF Spec, Test Plan

5. design-review              → Adversarial cross-department review through
                                 four lenses before artifact distribution

6. traceability-matrix        → Cross-artifact validation:
                                 coverage gaps, orphans, action items
```

**Note:** `traceability-matrix` can (and should) be run after every artifact is produced, not just at the end. It is the quality check that runs across the chain.

## Core Operating Behaviors

These behaviors apply across all SE skills. They are non-negotiable.

### 1. Every Claim Traces to Something

Every design element, specification section, and test case must reference a requirement ID, architecture interface ID, or constraint ID. Content without a trace is opinion, not engineering. When you write a specification sentence, ask: "which requirement does this satisfy?"

### 2. Numbers, Not Adjectives

"Fast" is not a requirement. "≤ 500μs" is. "Robust" is not a requirement. "Survives 1000 transitions without state corruption" is. Replace every qualitative adjective with a quantified, testable statement. If you cannot quantify it, flag it as an ambiguity for the stakeholder.

### 3. Surface Conflicts Immediately

When two requirements contradict, two constraints cannot both be satisfied, or two departments have incompatible expectations, surface the conflict with a proposed resolution and reasoning. Silent resolution is the SE's most expensive mistake — it turns a conversation-cost problem into a rework-cost problem.

### 4. Ownership is Non-Negotiable

Every requirement must have an owner. Every action item must have an owner and a due date. Every TBD must have an owner and a due date. Items without owners are risks, not tasks.

### 5. Verification is Part of the Process

Every skill includes a verification checklist. A skill is not complete until the checklist is satisfied. "Looks right" is never sufficient — there must be explicit confirmation against each checklist item.

### 6. Version Discipline

Every artifact references its inputs with exact version numbers. When an input changes version, all dependent artifacts must be checked for consistency. Version skew between artifacts is a primary source of integration errors.

## Failure Modes to Avoid

1. Jumping to architecture design before requirements are decomposed and confirmed (architecture on unstable requirements is guessing)
2. Defining interfaces without timing, error handling, and concurrency models ("I2C" is not an interface specification)
3. Generating specifications with empty sections (a blank section communicates "not designed," not "not applicable")
4. Accepting TBDs without owners and due dates (an unowned TBD is a project risk)
5. Reviewing your own artifact without fresh-context adversarial reviewers (you will see what you expect to see)
6. Running traceability only at the end (gaps found late cost more to fix; run after every artifact)
7. Being sycophantic — "of course!" to a bad architecture decision that will cost months of rework
8. Classifying requirements without inventorying all input sources (missing sources discovered later invalidate the classification)

## Skill Rules

1. **Check prerequisites before invoking a skill.** Architecture design requires structured requirements. Spec authoring requires architecture. Design review requires a completed artifact. If prerequisites are missing, invoke the upstream skill inline.

2. **Skills are workflows, not suggestions.** Follow the steps in order. Do not skip verification steps. The process was designed to catch errors at the cheapest possible moment.

3. **Multiple skills chain naturally.** A complete SE workflow chains: `requirements-decompose` → `architecture-design` → `spec-authoring` → `design-review` → `traceability-matrix`. But skills can also be used independently — run just `design-review` on a colleague's artifact, or just `traceability-matrix` before a milestone review.

4. **When in doubt, start with requirements.** If requirements are not yet structured and traceable, begin with `requirements-decompose`. Everything downstream depends on it.

5. **SE skills and agent-skills coexist.** SE skills can invoke agent-skills inline when needed:
   - `requirements-decompose` invokes `interview-me` for vague inputs
   - `architecture-design` invokes `source-driven-development` for IP/standard verification
   - `design-review` is built on `doubt-driven-development`'s adversarial pattern

## Quick Reference

| Phase | Skill | One-Line Summary |
|-------|-------|-----------------|
| Define | requirements-decompose | Raw inputs → structured, traceable system requirements with ownership |
| Design | architecture-design | Requirements → modules, interfaces, constraints, trade-off decisions |
| Document | spec-authoring | Architecture + Requirements → SOD, HW-SW IF Spec, Test Plan |
| Verify | design-review | Four-lens (HW/SW/Test/System) adversarial review of any SE artifact |
| Validate | traceability-matrix | Cross-artifact gap analysis: orphans, coverage gaps, action items |

## Interaction with Agent Skills

SE skills are designed to work alongside agent-skills. The relationship:

| SE Skill | Can Invoke (agent-skills) | Relationship |
|----------|--------------------------|-------------|
| requirements-decompose | `interview-me` | Clarify vague stakeholder inputs before decomposition |
| architecture-design | `source-driven-development` | Verify third-party IP, standard protocols against official docs |
| design-review | `doubt-driven-development` | Philosophical parent — same adversarial fresh-context pattern |
| spec-authoring | `spec-driven-development` | Complementary — SE spec defines what; software spec defines how in code |

Agent skills are loaded alongside SE skills. When an SE skill needs to clarify, verify, or cross-examine, it invokes the relevant agent skill inline.
