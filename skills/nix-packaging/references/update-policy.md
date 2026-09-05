# Update policy

This skill has an explicit freshness mechanism, not silent background mutation.

## Manual update

For a package upgrade, re-check the upstream changelog/release, immutable revision,
artifact layout, license, build files, lockfiles, and every fixed-output hash. Re-run
the full validation sequence even when the expression change looks mechanical.

## Reviewable automated update

A future CI job may run on a schedule and create a reviewable branch or pull request
only when all of these are true:

1. the upstream revision is resolved reproducibly;
2. the generated diff is limited to version/source/hash metadata and known updates;
3. parse, flake checks, build checks, and package-specific smoke checks pass;
4. the job records the old and new revisions and the documentation snapshot used.

The job must never silently edit the skill, activate a system, commit to a user's
branch, or push without an explicit repository policy allowing that action.

## Documentation drift

At the start of a packaging task, compare locked nixpkgs behavior with current
official docs. If a process or API changed, open a small maintenance change that
updates the relevant reference and its examples together. Keep the old lock
compatible until a deliberate flake update is approved.

## Update scripts

Add `passthru.updateScript` only after at least two successful, deterministic manual
updates demonstrate the same source discovery, version extraction, hash refresh, and
validation path. A script that guesses release assets or mutates a working tree is
not an update mechanism.
