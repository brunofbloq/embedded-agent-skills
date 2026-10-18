# Upstream source review policy

**Goal:** open draft review PRs for changes relevant to three embedded skills without Git submodules, background LLM inference or copying third-party code automatically.

## What triggers a PR

- `files`: a valid new upstream commit changes at least one configured path, including renamed paths; or GitHub's comparison is incomplete/unavailable. Non-matching changes are ignored.
- `release`: GitHub's `/releases/latest` stable release tag differs from the approved baseline. This intentionally ignores prereleases and commits not included in an approved release.

The monitor is scheduled weekly and can be dispatched manually. Third-party repositories cannot push webhook notifications into this repository without upstream cooperation. Schedule execution can be delayed or skipped by GitHub. The workflow checks current state rather than assuming every intermediate commit was seen.

## Governance

1. The generated PR is **draft**, with the upstream diff/release and impacted skill names.
2. Reviewer must record a disposition (adopt / reject / defer) for every item, confirming if it affects any actual target/compiler/board. Never treat repository popularity or changed descriptions as authoritative engineering correctness.
3. When adopting, implement a separate patch (or append one on a review-controlled branch), run skill validation and relevant firmware regression, and record source/version. When rejecting, give a short reason.
4. Only merge the baseline-advance PR after the dispositions are explicitly recorded. Merging an untouched draft merely records a revision as reviewed; it does **not** improve the skill.
5. Keep the generated `automation/upstream-source-review` branch bot-owned: manual edits there may be overwritten by a later scheduled run. Use a separate PR for authored changes and link it in the review discussion.

## Limitations

- The GitHub Compare API provides a bounded changed-file list. When 300 files are returned, >100 commits are reported, comparison status is unexpected, or the API fails, classify the result as **incomplete**, create a draft PR, and require human inspection. Conservatively flagging results may produce false-positive reviews, but avoids false negatives due to pagination/truncation.
- A compare can miss changes after rewritten history. Any comparison failure becomes a review request rather than silently updating the baseline.
- Unrelated branch commits are intentionally not checkpointed if no PR is created. Long-running repositories may occasionally need a manual new reviewed baseline.
- GitHub outages, expired permissions, repository deletion or private access changes fail the job. No change detector can guarantee instantaneous or complete notification under all outage conditions.
- GitHub API is rate-limited; a GH_TOKEN grants higher authenticated limits but must never appear in logs.
- A 404 for a stable GitHub release is an error; if a source stops publishing releases, change its monitor mode explicitly after review.
- This system does **not** detect edits to vendor PDF datasheets or off-GitHub documentation. Verify device datasheet/errata at firmware execution time.
- GitHub Actions default `GITHUB_TOKEN` cannot automatically trigger another CI run by pushing/creating its own PR. The upstream workflow runs its own safety checks first.

## Backfill / bootstrap

Baseline values in `reviewed-revisions.json` correspond to observed public GitHub revisions as of 2026-10-18. If a source is added, set its baseline explicitly from the public API and document what was reviewed; never auto-bootstrap to whatever HEAD happens to be and silently label it reviewed. To check source changes without writing anything, use `python scripts/check_upstream.py --dry-run`.
