# Bounded task QA contracts

Use during task segmentation, before creating implementation and verification
work items. Revisit only affected contracts when requirements or inputs change.
This is a planning aid, not a new council, test framework or approval layer.

## Refine with the user and specialists

1. Extract observable delivery criteria, deferred behavior, physical permissions
   and time/cost constraints from the user and authoritative project decisions.
2. Reuse existing specialist findings. Label inputs **verified** (with a source),
   **proposed**, or **unknown**; agent summaries alone are not verified evidence.
3. Ask only consequential unresolved questions. Delegated reversible decisions
   may proceed within their stated authority. Specialist suggestions do not
   silently add requirements or reduce acceptance criteria.
4. Map each criterion to implementation and verification owners. Parallelize
   disjoint outputs; keep one owner for shared integration files and fixtures.
5. Return contracts and unresolved decisions, not another large design dossier.

## Per-task contract

Record this in the work item or the project's existing planning format:

- **Outcome:** observable behavior and explicit non-goals.
- **Inputs:** frozen source revision plus uncommitted/new-file manifest when
  applicable; toolchain/configuration, approved interfaces, missing prerequisites.
- **Owner/scope:** writable files, interfaces, shared resources and collaborators.
- **Deliverables:** source changes and all new files, dependency configuration
  and applicable licence notices, image if built, hashes and evidence locations.
- **Integration:** build inclusion, stable ID/registry, actual implementation
  invocation, boot/resume hooks and user-facing selection where applicable.
- **Checks:** exact existing commands, fixtures, assertions and one executor per
  check. Include negative/error cleanup checks relevant to the change.
- **Reuse:** previous result IDs and their input/configuration identity; list
  changes that invalidate them. Reuse evidence, not unverified PASS summaries.
- **Bounds:** executable stages, command timeouts, checkpoint destination and one
  bounded correction attempt. Estimate from actual stages, not a universal call
  count. A small isolated defect need not acquire a formal multi-agent workflow.
- **Stop:** missing source, confirmed blocker, exhausted cost/time budget or owner
  cancellation. A retry requires new evidence or a materially changed plan.
- **Verdict:** PASS/FAIL/NOT_RUN/INCOMPLETE by evidence level; separate physical
  acceptance from software completion. Completing a review can mean REVISE.
- **Consumer:** downstream task and exact artifact it consumes.

For storage exclusivity, test both competing entry points: recorder claim while
raw access is active, and raw-write refusal while recording/mounted. Test safe
release after failure. For standby, registration alone is insufficient: account
for platform operations and boot/reset continuation, not a NOT_RUN placeholder.
These are risk examples, not requirements for every embedded feature.

## QA entry gate: source-complete, frozen and recoverable

Before starting an expensive matrix, verify that the consumer can extract the
bundle from its durable destination and match declared hashes. A committed
revision may provide existing source; include all additional uncommitted/new
source, configuration, dependency and licence files needed to reproduce it.
Objects, an ELF, or a summary alone cannot replace missing source. Do not create
an empty stub to satisfy a file-list or registry check.

An optional portable hash checker is provided:

```text
python skills/embedded-qa/scripts/verify_handoff.py --root <extracted-bundle> --manifest <manifest.json>
```

The JSON format is deliberately small:

```json
{
  "schema_version": 1,
  "required_paths": ["src/session.c", "config/storage.h"],
  "artifacts": [
    {"path": "src/session.c", "sha256": "<64 lowercase hex digits>", "role": "source"},
    {"path": "config/storage.h", "sha256": "<64 lowercase hex digits>", "role": "config"}
  ]
}
```

The placeholder hashes above must be replaced with real values. Paths are
relative to the extracted root; declare required source/config/licence paths
from the actual build/dependency inventory, not just whatever files survived.
At least one source artifact is required. Other roles: `license`, `evidence`,
`firmware`. The checker rejects missing/changed files, duplicate paths, traversal,
symlinks and malformed manifests. It does **not** discover omitted dependencies,
validate licences, prove a build, validate a test verdict, or enforce integration.
A manifest can be self-consistent but incomplete: the entry gate still requires
comparison against the authoritative build/feature inventory. Run the checker on
the retrieved durable copy, not only on the producer workspace.

## Execute once; review independently

- Builder: run affected unit/build checks and preserve machine-readable results.
- QA: independently verify the agreed candidate/claims at the cheapest faithful
  evidence level; define its oracle independently, not from current output.
- Reviewer: consume same-input QA evidence and examine code/interfaces/safety.
  Repeat a test only for changed inputs, disputed results or uncovered risk;
  state the reason. Independence does not require duplicating every matrix.
- Findings: publish the shortest reproduction and REVISE once confirmed blockers
  suffice. Do not keep expanding checks merely to polish a report.
- Hardware: absent probes, missing flash permission or pending physical timing
  become explicit bench gaps; close the software activity without inventing PASS.
  Do not reduce a real release requirement to a caveat to obtain approval.

## Stop the retry and publication loops

Preserve a done/remaining checkpoint after the first useful stage, before long
commands, and on cancellation. A runtime budget is a limit, not proof of useful
progress. Generic exit code 1 is not a transport diagnosis. Inspect logs and
artifacts before deciding whether a retry is justified; wall-clock and iteration
budgets are different and runtime-specific. Do not raise either speculatively.

If an operational choice is reconsidered twice without new evidence, use the
known supported method once or report a precise tooling blocker. For artifacts,
use the runtime's direct local-file attachment/upload operation; do not route
base64 blobs through model context. Verify remote readback and stored hashes.
If no durable storage is available, report that and retain local source; do not
claim publication or permit workspace cleanup. Stop/cost-stop instructions end
new checks and automatic retries, while retaining existing evidence. Check the
actual worker/scheduler state: a posted instruction is not proof it was received.
