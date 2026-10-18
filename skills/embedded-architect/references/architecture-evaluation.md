# Architecture evaluation matrix and decision evidence

A rated matrix is a reasoning aid, **not** a substitute for measurable acceptance criteria. Reject options that violate hard constraints before scoring preferences. Never hide Unknown as Good.

| Criterion | Questions for defensible assessment | Typical evidence |
|---|---|---|
| Hardware efficiency | CPU and DMA load, RAM/flash, IO bandwidth, wake/idle costs | Target datasheets, measured traces, resource estimates |
| Complexity | Number of stateful parts, coupling, boot sequencing, communication paths | Component/dependency diagram, error-path count |
| Maintainability | Test boundaries, coupling, observability, replaceability | Interface contracts, repository conventions, test seams |
| Real-time behavior | Worst-case blocking, ISR budget, deadlines/jitter, priority inversion | Timing budget, scheduling analysis, on-target timing plan |
| Safety/robustness | Failsafe behavior, timeouts, watchdog, brownout/reboot recovery | Failure-mode table, injection tests, recovery invariants |

Use `Good`, `Trade-off`, `Problem`, or `Unknown` for each option/criterion, with one evidence-based sentence for the rating. Add power, lifecycle cost, security or compliance as columns/rows when required by product constraints. Avoid arbitrary aggregate scores if options violate non-negotiable timing, power or safety gates.

### Decision policy

- **Proceed** if an option satisfies every known hard constraint and remaining Unknowns have a bounded validation plan.
- **Revise** if material concerns can be corrected, or necessary evidence is missing to authorize production implementation.
- **Reject** if no viable option satisfies a hard constraint, or risks cannot be made acceptable in scope.

Explicitly distinguish proposed architecture from evidence already demonstrated. Record accepted alternatives and rationale in a short ADR when the decision is long-lived.

### Example (illustrative only; not a target benchmark)

| Option | Hardware efficiency | Complexity | Maintainability | Real-time | Safety/robustness |
|---|---|---|---|---|---|
| Event-driven bare-metal | Good: no scheduler overhead | Good: one state machine | Trade-off: scale limits | Unknown: needs worst-case timing | Unknown: reset/recovery not tested |
| Small RTOS | Trade-off: task stacks | Trade-off: synchronization | Good: clear responsibilities | Trade-off: priority analysis | Good: task supervision possible |

Do not reuse example ratings without project-specific reasoning.
