---
name: embedded-qa
description: Design, implement and execute embedded firmware verification across host unit/mocks, static analysis, Renode or QEMU simulation, hardware-in-the-loop, J-Link/ST-Link/OpenOCD, UART/RTT, and physical measurement. Use for test strategy, regression, fault injection, acceptance gates, timing/stack/resource evidence and CI test automation on bare-metal, RTOS and embedded Linux targets. Select the cheapest credible test backend and clearly separate virtual-model evidence from real hardware qualification.
---

# Embedded QA

Deliver evidence-based, reproducible tests without claiming capabilities that the test environment cannot demonstrate. Choose one or more backends appropriate to the feature and its failure modes, not a prescribed test pyramid for every change.

## Planning and execution boundaries

During task segmentation, use [task-qa-contracts.md](references/task-qa-contracts.md)
to refine acceptance criteria with the user and existing specialist evidence.
Before execution, require a frozen, source-complete handoff and named affected
checks. Separate bench acceptance from software results; reuse same-input
evidence instead of automatically repeating another verifier's full matrix.
Publish confirmed blockers promptly, preserve partial progress, and stop on an
owner cost-stop. Budget exhaustion requires diagnosis, not an identical retry.

## Test workflow

1. **Inspect:** Identify actual firmware target, board/silicon revision, toolchain, current test infrastructure, requirements, safety/power/timing constraints, build artifacts and available host/emulator/probe hardware. Reuse existing tests and tooling before introducing a framework.
2. **Define the test oracle independently:** Translate requirements into observable positive, negative, boundary, fault, and recovery assertions. Verify expected values against specs and test vectors rather than blindly reproducing implementation outputs.
3. **Choose the lowest-cost faithful backend:** Host test portable state machines and protocols. Use Renode only if its CPU, interrupts, memory and peripherals needed by each claim are adequately modeled; otherwise mark `BLOCKED_BY_MODEL` and use mocks, model work, or HIL. Use real board/probe measurements for electrical, power, DMA/cache, timing and reset behavior.
4. **Build and run:** Capture exact firmware image/revision, model version, scripts, stimuli, exit statuses and bounded timeouts. Run targeted checks before wider regression. Isolate test resources, port numbers and teardown; never flash/erase real hardware without authorization.
5. **Report by evidence level:** Host, static, simulated, HIL and physical measurement each receive their own PASS/FAIL/NOT_RUN/INCOMPLETE outcome. Mark missing model coverage and test coverage separately. Preserve useful machine-readable logs, not verbose transcripts in the LLM context.
6. **Follow up:** Provide the shortest actionable failure reproduction, root-cause evidence or scope limitations. Add stable tests alongside fixes if appropriate.

## Conditional references

- [host-testing.md](references/host-testing.md) for mocks, sanitizers, property and fault tests.
- [renode-workflow.md](references/renode-workflow.md) for `.resc`/`.repl`, Robot Framework, UART and CI.
- [simulation-coverage.md](references/simulation-coverage.md) for precise Renode feasibility and evidence gating.
- [hil-testing.md](references/hil-testing.md) for ST-Link, J-Link, OpenOCD, serial/RTT and real-board instrumentation.

Use `scripts/summarize_robot.py` to summarize Robot `output.xml` (when produced). Do not invent Renode MCP integrations: verify a real installed adapter before relying on it. Protect shared debug probes, UART sockets, and power equipment from concurrent tests.

**Deliver:** test environment and constraints; commands executed; assertions/results with evidence location; simulated-versus-physical coverage; remaining risks.
