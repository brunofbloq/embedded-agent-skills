# Two-phase engineering reasoning and approval workflow

Use this file only for substantial architecture work, formal architecture reviews, or user-requested staged implementation. This preserves the original `embedded-systems-architect` process while separating architectural authority from implementation and independent QA.

## Phase 1: Architecture review & evaluation (before consequential code changes)

1. **System context.** Capture product goal, acceptance criteria, named target/board and revision, SDK/OS, existing modules, physical connections, resources, failure behavior and verified constraints. Explicitly label estimates and uncertainties.
2. **System topology.** Draw a compact diagram showing processors and system boundaries, who owns hardware, ISR/task/process placements, major flows, persistent state and the relevant interconnect. Represent *actual* silicon: do not render an A-core/M-core or RPMsg topology unless it exists.
3. **Proposed architecture.** Define boundaries, dependency directions and lifecycles; choose protocols/interfaces, message versions, data ownership, concurrency, boot/update, safety and recovery strategy. Include preliminary public contracts and resource budgets. Write down realistic alternatives and why they were declined.
4. **Five-axis evaluation.** For each viable option use Good / Trade-off / Problem / Unknown with evidence: hardware efficiency, complexity, maintainability, real-time constraints, safety/robustness. Add axes only where decisive. Load [architecture-evaluation.md](architecture-evaluation.md) via its direct link from the SKILL.md.
5. **Formal decision.** State **Proceed**, **Revise**, or **Reject** with the reason; spell out required corrections and missing evidence. If Proceed, specify interface-first, low-dependency-first module order and verification gates.
6. **Architecture approval.** Present the plan and ask for explicit approval before Phase 2. Accept a documented approval for the same plan revision; when requirements, hardware or risks change materially, reopen the decision. Until approval, do not implement substantive design-dependent modules. Isolated exploratory PoCs may be prepared if explicitly permitted and labeled non-production.

### Compact output template

```text
Architecture Plan: <feature> | revision: <id>
Context: requirements, hard constraints, verified board and assumptions
Topology: compact component and data/control flow
Interfaces: inputs, outputs, ownership, error and timing contracts
Options/evaluation: Good | Trade-off | Problem | Unknown, with justification
Decision: Proceed | Revise | Reject; outstanding blockers
Module order: M1 -> M2 -> M3 (dependencies)
Evidence: build/tests/simulation/HIL needed and unavailable evidence
Approval: requested | approved (<source/revision>) | superseded
```

## Phase 2: Module-by-module implementation and checkpoints

Enter only after the Phase 1 plan is approved (or the user has explicitly approved that exact design in advance).

For each module in dependency order:

1. **Interface first:** establish `.h` public APIs, protocol schema, sysfs contract or service endpoint only if the target architecture calls for it. Include lifetime, error, ownership, timing and compatibility behavior.
2. **Implementation:** delegate implementation to `embedded-developer`, or implement using its engineering conventions when appropriate. Limit edits to the approved component and shared contracts.
3. **Validation:** delegate independent acceptance tests to `embedded-qa`; run the cheapest credible backend. Require actual build, unit, integration, simulation or HIL evidence appropriate to risk. Do not imply a virtual peripheral proves physical behavior.
4. **Checkpoint:** record files changed, public interface, dependencies, observed test results, limitations, missing hardware evidence and changes relative to the approved architecture. Default to asking permission to proceed to the next module.
5. **Deviation handling:** if an interface breaks assumptions, timing budgets or system partitioning, **stop and revise Phase 1**. Do not silently redesign in implementation.

A user may explicitly authorize *batch continuation* within a specified approved architecture; in that case log the same module checkpoints but avoid repeated pauses. Do not interpret time pressure or an unanswered question as approval. Never request per-module approval for tiny tasks routed to the fast path.

### Checkpoint template

```text
Module: <name> [index/total] | Approved plan: <revision>
Interface: <public contracts and owners>
Changed files: <paths>
Dependency status: <blocking/nonblocking>
Observed evidence: <commands, pass/fail, scope>
Known gaps: <unverified hardware/timing/risks>
Next module: <name> | Approval: needed / batch-authorized
```

## Approval boundaries

Approval to evaluate architecture is not permission to flash hardware, change OTP/fuses/secure boot, publish artifacts, edit production cloud resources or perform irreversible actions. Obtain explicit authorization for those operations independently.
