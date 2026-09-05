---
name: nix-packaging
description: >
  Reproducible Nix packaging workflow for adding, upgrading, repairing, or reviewing
  packages and derivations from source, prebuilt binaries, AppImages, Electron/ASAR,
  fonts, themes, data, or plugins. Use when a user says “package for Nix”, “create,
  fix, or update a derivation”, “add a local package”, “wrap an AppImage”, “prefetch
  a hash”, “choose a nixpkgs builder”, or “verify a Nix package”, including NixOS and
  Home Manager integration. Investigates locked nixpkgs APIs, official docs, upstream
  release/build evidence, hashes, install layout, wrappers, and reproducible checks.
  Not for ordinary software installation, generic NixOS configuration, or an upstream
  PR review without a packaging task.
---

# Nix Packaging

IRON LAW: DO NOT CHANGE A DERIVATION UNTIL LOCKED NIXPKGS INTERFACES AND UPSTREAM
SOURCE/RELEASE EVIDENCE ARE RECORDED; A BUILD WITHOUT THAT EVIDENCE IS NOT A
REPRODUCIBLE PACKAGING RESULT.

Red flags — return to the evidence step if any appear:

- A builder was selected from a single marker file or memory alone.
- A floating channel, registry result, or “latest” URL is the only source evidence.
- A hash, wrapper, desktop entry, or runtime dependency is guessed.
- `nix develop` succeeds but the derivation, output layout, or executable was not built.
- A successful dry-build is reported as a deployed or live runtime test.

## Progress checklist

Copy this checklist into the working notes and mark it as the task advances:

- [ ] Step 0: Load repository policy and define scope ⚠️ REQUIRED
  - [ ] Find `AGENTS.md`, contribution rules, dirty files, consumers, and the requested observable behavior.
  - [ ] Classify the task as add, upgrade, repair, or review.
- [ ] Step 1: Pass the freshness gate ⛔ BLOCKING
  - [ ] Record the `nixpkgs` revision from `flake.lock`, or state the fallback when no lock exists.
  - [ ] Inspect the locked builder/helper interface and compare it with current official docs.
  - [ ] Report drift and migration impact; never silently apply a newer API to an older lock.
- [ ] Step 2: Gather source and package evidence ⚠️ REQUIRED
  - [ ] Search the pinned nixpkgs and the target repository for an existing package or helper.
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
  - [ ] Expose a stable flake package when the target repository uses flakes; follow its existing naming convention.
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

Load [references/validation.md](references/validation.md) for the package-type matrix and output checks. A
typical flake-backed package uses:

```bash
nix-instantiate --parse path/to/package.nix
nix flake check path:. --no-build
nix build path:.#pname -L --no-link --print-out-paths
git diff --check
```

If the package is wired into a NixOS/Home Manager configuration, also run:

```bash
nixos-rebuild dry-build --flake path:.
```

Use `scripts/validate-skill.py` to check this skill repository itself. It is a
deterministic lint, not a substitute for building the target package.

## Upgrades and freshness maintenance

Load [references/update-policy.md](references/update-policy.md) for repeat updates. Pin source and documentation
inputs, make update checks explicit, and keep automatic work read-only by default.
An automated job may open a reviewable update change after checks pass; it must not
silently rewrite a skill, switch a system, commit, or push.

## Three concrete request shapes

Load [references/examples.md](references/examples.md) when the request is ambiguous. The minimum supported
shapes are: add a missing local package from an upstream release; upgrade an existing
derivation and refresh source/dependency hashes; and repair a prebuilt/AppImage,
Electron, font/theme, or plugin package while proving its output and integration.

## Anti-patterns

- Do not use `nix develop` success as proof that `nix build` works.
- Do not choose a builder from `Cargo.toml`, `package.json`, or one guessed dependency alone.
- Do not fetch dependencies online during a sandboxed build (`cargo fetch`, `npm install`, `pip install`, and similar).
- Do not use floating source URLs, mutable branches, old-style hashes, or version literals duplicated across an expression.
- Do not hide missing libraries with `autoPatchelfIgnoreMissingDeps`, a default FHS wrapper, or an oversized `buildInputs` list.
- Do not claim desktop, IPC, playback, Wayland, or compositor behavior was tested when only the derivation built.
- Do not run `nixos-rebuild switch`, commit, push, delete files, or create a PR without explicit authorization.

## Delivery format

Return a compact evidence report:

1. **Scope and route** — task type, package type, and why this builder was chosen.
2. **Evidence** — locked nixpkgs revision/API, upstream revision/artifact/license, and relevant hashes.
3. **Changes** — derivation, flake output, consumers, and documentation.
4. **Verification** — parse, flake check, build, output/smoke, dry-build, and live status separately.
5. **Next action** — exact manual command or user decision still required.

Never call a package “done” while a required check is missing; label the blocker and
the smallest next experiment instead.
