---
name: nix-packaging
description: >
  Evidence-driven, reproducible Nix package development for adding, upgrading,
  repairing, reviewing, and integrating derivations across package repositories,
  flakes, overlays, and NixOS or Home Manager consumers. Use when a user asks to
  develop a Nix package, create or update a derivation, wrap an AppImage, prefetch a
  hash, choose a nixpkgs builder, or verify package output. Covers source, prebuilt
  binaries, AppImages, Electron/ASAR, fonts, themes, data, and plugins while
  checking locked nixpkgs APIs, upstream release/build evidence, hashes, install
  layout, wrappers, and reproducible checks. Use nixpkgs-maintainer for upstream
  nixpkgs maintenance classification, contributor workflow, maintainer ownership,
  or PR preparation. Not for ordinary software installation or generic NixOS
  configuration without a package task.
---

# Nix Package Development

IRON LAW: DO NOT CHANGE A PACKAGE EXPRESSION UNTIL THE TARGET NIXPKGS INTERFACES
AND UPSTREAM SOURCE/RELEASE EVIDENCE ARE RECORDED; A BUILD WITHOUT THAT EVIDENCE
IS NOT A REPRODUCIBLE PACKAGING RESULT.

Red flags — return to the evidence step if any appear:

- A builder was selected from a single marker file or memory alone.
- A floating channel, registry result, or “latest” URL is the only source evidence.
- A hash, wrapper, desktop entry, or runtime dependency is guessed.
- `nix develop` succeeds but the derivation, output layout, or executable was not built.
- A successful dry-build is reported as a deployed or live runtime test.

## Scope boundary

This skill owns the package expression, its build inputs, output contract, and
package-facing flake or overlay integration. Treat NixOS/Home Manager modules as
consumers: inspect their package interface and dry-build them when in scope, but
leave system configuration and activation to `nixos-ecosystem`.

When the request targets the upstream `NixOS/nixpkgs` maintenance process—such as
classifying an update or breakage, adopting a package, checking affected dependents,
or preparing a nixpkgs PR—use `nixpkgs-maintainer`. If both are involved, this skill
supplies derivation evidence and the maintainer skill owns the upstream workflow.

## Progress checklist

Copy this checklist into the working notes and mark it as the task advances:

- [ ] Step 0: Load repository policy and define scope ⚠️ REQUIRED
  - [ ] Find `AGENTS.md`, contribution rules, dirty files, package consumers, and the requested observable behavior.
  - [ ] Classify the task as add, upgrade, repair, or review.
  - [ ] Identify whether the expression lives in a package repository, standalone file, flake, overlay, or nixpkgs tree.
- [ ] Step 1: Pass the freshness gate ⛔ BLOCKING
  - [ ] Record the target's `nixpkgs` revision from `flake.lock`, a pinned package-repository input, or the nixpkgs checkout; state the fallback when none exists.
  - [ ] Inspect the locked builder/helper interface and compare it with current official docs.
  - [ ] Report drift and migration impact; never silently apply a newer API to an older lock.
- [ ] Step 2: Gather source and package evidence ⚠️ REQUIRED
  - [ ] Search the target tree, relevant nixpkgs input, overlays, and existing helpers for an existing package or implementation.
  - [ ] Verify upstream tag/commit, build commands, CI, license, platform, artifact, executable name, and install layout.
  - [ ] Choose the narrowest route: source, prebuilt ELF, AppImage, Electron/ASAR, data, font/theme, or plugin.
- [ ] Step 3: Present the minimal plan ⚠️ REQUIRED for non-trivial edits
  - [ ] State files, dependencies, risks, verification commands, and what will remain unverified.
  - [ ] Ask before destructive edits, installation, system activation, commit, push, or PR creation.
- [ ] Step 4: Implement the smallest derivation
  - [ ] Pin `pname`, `version`, source/revision, and SRI hashes; use `pname`/`version` consistently in URLs and filenames.
  - [ ] Use the narrowest nixpkgs builder and default phases; custom phases must run their matching hooks.
  - [ ] Separate build tools, link/runtime libraries, test tools, and wrapper-provided commands.
  - [ ] Complete GUI integration as one unit: wrapper, desktop entry, icon, `Exec`, and runtime flags.
  - [ ] Preserve or expose the target's existing package surface—flake output, overlay, or package attribute—only when it is in scope.
- [ ] Step 5: Verify in layers ⚠️ REQUIRED
  - [ ] Parse, evaluate/check, build, inspect the store output, and run one safe smoke test.
  - [ ] Run system dry-build only when the package is integrated into NixOS/Home Manager.
  - [ ] Keep build, smoke, dry-build, and post-activation/live status separate.
- [ ] Step 6: Report and maintain
  - [ ] Report evidence, changed files, hashes, checks, blockers, and the exact manual next step.
  - [ ] For upgrades, re-check changelog, lockfiles, license, artifact layout, and all hashes.
  - [ ] Add an update script only after the update path is proven stable and deterministic.

## Freshness gate

Load [references/freshness-and-evidence.md](references/freshness-and-evidence.md) before selecting a builder or writing a
new hash. Use `gh` for GitHub investigations. Prefer the locked `nixpkgs` source for
API facts, and use current official Nixpkgs/nix.dev documentation to detect process
changes. When they disagree, pause and explain whether the change is lock-compatible,
requires a lock update, or should remain a documented exception.

## Builder and implementation routing

Load only the relevant section of [references/builder-routing.md](references/builder-routing.md) after the evidence
step. Do not add a broad dependency set to hide an unknown phase failure. Prefer a
source build when it is maintainable; use a release binary or AppImage only when the
upstream source route is unavailable or materially less reliable.

For custom `buildPhase`, `checkPhase`, or `installPhase`, preserve the corresponding
`runHook preX` and `runHook postX`. For prebuilt native code, record provenance and
inspect architecture, interpreter, `NEEDED` libraries, and bundled component licenses.

## Validation

Load [references/validation.md](references/validation.md) for the package-type matrix and output checks. Adapt the
following checks to the target's package surface:

```bash
nix-instantiate --parse path/to/package.nix
nix flake check path:. --no-build       # when the target exposes a flake
nix build path:.#pname -L --no-link --print-out-paths  # use the target output name
git diff --check
```

If the package is wired into a NixOS/Home Manager configuration, also run:

```bash
nixos-rebuild dry-build --flake path:.
```

Use `scripts/validate-skill.py` to check this skill repository itself. It is a
deterministic lint, not a substitute for building the target package.

When the user asks to “run validation” without naming a consumer, default to
package evaluation, build, output inspection, and a safe smoke test. Add a
NixOS/Home Manager or other consumer dry-build only when that consumer is in
scope.

## Upgrades and freshness maintenance

Load [references/update-policy.md](references/update-policy.md) for repeat updates. Pin source and documentation
inputs, make update checks explicit, and keep automatic work read-only by default.
An automated job may open a reviewable update change after checks pass; it must not
silently rewrite a skill, switch a system, commit, or push.

## Four concrete request shapes

Load [references/examples.md](references/examples.md) when the request is ambiguous. The supported
shapes are: add a package to a package repository, standalone expression, flake, or
overlay; upgrade an existing derivation and refresh source/dependency hashes; repair
a prebuilt/AppImage, Electron, font/theme, or plugin package; and integrate a package
through an existing flake or overlay for a consumer.

## Anti-patterns

- Do not use `nix develop` success as proof that `nix build` works.
- Do not choose a builder from `Cargo.toml`, `package.json`, or one guessed dependency alone.
- Do not fetch dependencies online during a sandboxed build (`cargo fetch`, `npm install`, `pip install`, and similar).
- Do not use floating source URLs, mutable branches, old-style hashes, or version literals duplicated across an expression.
- Do not hide missing libraries with `autoPatchelfIgnoreMissingDeps`, a default FHS wrapper, or an oversized `buildInputs` list.
- Do not claim desktop, IPC, playback, Wayland, or compositor behavior was tested when only the derivation built.
- Do not treat package-expression checks as nixpkgs integration or PR review; use `nixpkgs-maintainer` for that upstream workflow.
- Do not run `nixos-rebuild switch`, commit, push, delete files, or create a PR without explicit authorization.

## Delivery format

Return a compact evidence report:

1. **Scope and route** — target repository/public surface, task type, package type, and why this builder was chosen.
2. **Evidence** — locked nixpkgs revision/API, upstream revision/artifact/license, and relevant hashes.
3. **Changes** — package expression, flake or overlay surface, consumers, and documentation.
4. **Verification** — parse, flake check, build, output/smoke, dry-build, and live status separately.
5. **Next action** — exact manual command or user decision still required.

Never call a package “done” while a required check is missing; label the blocker and
the smallest next experiment instead.
