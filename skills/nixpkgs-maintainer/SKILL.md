---
name: nixpkgs-maintainer
description: >
  Evidence-led workflow for maintaining and contributing packages in the upstream
  NixOS/nixpkgs repository: triage, update, repair, new package, backport, review,
  adoption, and local-to-upstream work. Use only when the requested outcome is an
  upstream nixpkgs contribution or maintainer review; not for local overlays,
  standalone derivations, or NixOS/Home Manager configuration.
---

# Nixpkgs Maintainer

Use this skill when the target is a change to, or a review of, the upstream
NixOS/nixpkgs package collection. Do not assume the current directory is a
nixpkgs checkout: locate and verify the target repository first. For ordinary
local package development, use the generic nix-packaging skill instead.

The outcome is an evidence-backed, reviewable nixpkgs change or review with an
honest validation report. This skill does not install packages, run
nixos-rebuild, push, open a PR, force-push, remove maintainers/packages, or run
a broad automated sweep unless the user explicitly authorizes that exact action.

## Progress checklist

Keep this checklist in working notes or the response; do not create a tracking
file unless requested.

- [ ] Verify the target nixpkgs checkout or supplied PR/diff; record branch,
  revision, and clean/dirty scope when available.
- [ ] Assign a primary task type and any secondary type:
  UPDATE, BROKEN, NEW_PACKAGE, PATCH, DEPENDENCY_BREAKAGE, REVIEW, ADOPT, or
  LOCAL_TO_UPSTREAM.
- [ ] Build the evidence ledger before editing a derivation.
- [ ] Read the target package's anatomy and identify its consumers and tests.
- [ ] Reproduce the reported failure or verify the upstream change.
- [ ] Make the smallest change that fixes the demonstrated boundary.
- [ ] Run applicable validation levels and label all skipped levels.
- [ ] Prepare the PR packet; stop before external mutation without explicit approval.

Read the relevant detail only when needed:

- [Task triage and evidence](references/task-triage-and-evidence.md) for classification,
  repository discovery, and the evidence ledger.
- [Package anatomy](references/package-anatomy.md) before choosing a builder or
  editing an existing package.
- [Validation ladder](references/validation.md) before claiming a fix or review
  is complete.
- [Patch lifecycle](references/patch-lifecycle.md) for upstream fixes and
  backports.
- [PR packet](references/pr-packet.md) before committing or preparing a PR.

## Freshness gate

Nixpkgs interfaces, branch policy, CI policy, and package paths change. At task
time, inspect the target checkout and current official Nixpkgs guidance; do not
use this skill or memory as a substitute for the locked source. For GitHub
investigation use gh (gh pr view, gh pr diff, gh pr checks, gh release view, or
gh api when necessary). Do not use curl or hand-built GitHub API requests.

Before code changes, record:

1. The exact nixpkgs repository, base branch, HEAD, and relevant package path.
2. The current package version, source/revision, maintainer and metadata.
3. The official upstream release/tag/commit, changelog or issue, license, and
   build/runtime evidence relevant to the requested change.
4. The exact local failure or successful reproduction, including architecture
   and any sandbox, display, network, GPU, or hardware boundary.
5. For each flag, patch, disabled check, or unusual dependency: its reason,
   source, and removal condition.

If the repository, package identity, source provenance, or failure boundary is
unclear, stop and state the smallest read-only investigation needed.

## Workflow

1. **Classify.** A request may have multiple labels. Route REVIEW as
   read-only; route LOCAL_TO_UPSTREAM through upstream conventions rather than
   copying local machine-specific wiring.
2. **Investigate.** Search the target nixpkgs tree and upstream first. Compare
   the current package with release notes, lockfiles, upstream issues/commits,
   reverse dependencies, and existing CI/test evidence.
3. **Reproduce.** For BROKEN or DEPENDENCY_BREAKAGE, identify whether the first
   failure is upstream, the nix expression, a dependency/toolchain change,
   sandbox/network, or a host-only runtime condition. Fix the root boundary,
   not just the named symptom.
4. **Inspect anatomy.** Determine the source kind, builder/hooks, dependency
   lock or vendor hash, outputs/install layout, wrappers, patches, checks,
   update path, metadata, and downstream impact before selecting a change.
5. **Edit minimally.** Follow current nixpkgs conventions, preserve unrelated
   work, and document special choices in code or patch names. Do not add a
   broad dependency set, speculative abstraction, or unproved test skip.
6. **Validate in layers.** Use the L0-L5 ladder in
   [references/validation.md](references/validation.md); a lower level never
   proves a higher-level runtime claim.
7. **Package the result.** Prepare the evidence and PR packet, including branch,
   maintainers, tests, rebuild impact, patch expiry, and AI disclosure details.
8. **Stop at the boundary.** Ask before commit, push, PR creation, force-push,
   deletion, system activation, or any other external/state-changing action.

## Validation

Use the smallest applicable check at each level and report pass, fail, or
not run with a reason:

- **L0 — parse/evaluate:** parse the expression and evaluate the target
  attribute with the target nixpkgs checkout.
- **L1 — build:** build the changed package in the nixpkgs sandbox and retain
  the log/output path.
- **L2 — package tests:** run checkPhase, passthru.tests, relevant global
  package tests, or linked NixOS module tests.
- **L3 — binary smoke:** inspect the output and run each relevant executable,
  normally at least --version or --help, in a safe temporary environment.
- **L4 — nixpkgs integration:** run nixpkgs-review for the PR/WIP and inspect
  affected dependents when applicable.
- **L5 — real-world scenario:** exercise the requested platform or environment
  such as Wayland/X11, network parsing, GPU, plugins, or hardware, and record
  the exact machine/session. This is not implied by a successful build.

L0-L2 are the structural baseline for package changes; L3 is expected when a
binary exists; L4 is expected for a contribution with downstream impact or a
PR review; L5 is conditional on the package and the user's stated scenario.

## Anti-patterns

- Treating a local overlay, Home Manager package, or standalone derivation as an
  upstream nixpkgs contribution.
- Assuming the current checkout, branch, API, package path, version, hash, or
  builder without checking it.
- Changing version and a hash without inspecting upstream changes, lockfiles,
  metadata, tests, and consumers.
- Using doCheck = false, broad skips, unexplained flags, or extra libraries to
  conceal an unknown failure.
- Calling a dry-build, evaluation, or nixpkgs-review invocation proof of live
  GUI, network, playback, Wayland, GPU, plugin, or hardware behavior.
- Adding overrideAttrs in nixpkgs to hide a dependency change, or retaining a
  patch without a purpose and expiry condition.
- Fetching a patch from an unstable open PR when a stable upstream commit or a
  justified vendored patch is available.
- Running a maintainer sweep that edits packages, commits, pushes, or opens PRs
  without per-package evidence and explicit authorization.

## Delivery format

Return a compact packet with:

1. **Route:** primary/secondary task type, target repository/branch/revision,
   package attribute/path, and why the route fits.
2. **Evidence:** current nixpkgs state, upstream release/commit/license,
   failure/reproduction, maintainers, consumers, and any inference clearly
   marked as such.
3. **Anatomy and change:** source/build/lock/test/patch/output facts and the
   minimal files changed, with reasons for non-default choices.
4. **Validation:** L0-L5 results per architecture/environment, with commands,
   logs or output paths, and explicit unverified boundaries.
5. **PR readiness:** commit/branch suggestion, rebuild or release-note impact,
   maintainer notification, patch removal condition, package/CI checklist, and
   required responsible-person/AI disclosure.
6. **Next action:** one exact manual command or decision; name the blocker when
   the packet is not ready.

Never call the package or PR “done” when a required level or evidence item is
missing.
