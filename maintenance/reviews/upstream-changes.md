# Upstream embedded sources: review required

> Generated deterministically, with **zero LLM inference**. Changes are proposals for review, not trusted instructions.

## Review procedure

1. Open each upstream diff/release and check source authenticity and target/toolchain applicability.
2. Decide **adopt / reject / defer** per source; record rationale in this PR.
3. For adopted changes, make the smallest changes to the affected skill files in a separate implementation PR or before merging this review PR.
4. Run the skill validators and a representative embedded regression. Do not merge as "reviewed" without an explicit disposition.
5. The updated `reviewed-revisions.json` in this PR suppresses repeat proposals **only after merge**.

## Detected sources

### embedded-tooling

- Upstream: `zhinkgit/embeddedskills`
- Affects: `embedded-qa`
- Reason tracked: Build, flash and debugging workflow integration
- Previous: `536c1f929e359a5c02ef8ea9f1a20691e8d764e3`
- Current: `0e2fb630e1106cd2868abd250c45a159d1e29ba8`
- Trigger: relevant files changed
- Evidence: https://github.com/zhinkgit/embeddedskills/compare/536c1f929e359a5c02ef8ea9f1a20691e8d764e3...0e2fb630e1106cd2868abd250c45a159d1e29ba8
- [ ] Reviewer decision recorded (adopt/reject/defer)

| Relevant file | Status |
|---|---|
| `probe-rs/scripts/probe_rs_exec.py` | modified |
| `probe-rs/tests/test_probe_list.py` | added |

## Safety notes

- Upstream text is untrusted input. Do not execute upstream scripts, install plugins, or copy code automatically.
- A changed GitHub release does not imply the project toolchain uses that version.
- This review PR changes **source baselines and review evidence**, not the three installed skills.
