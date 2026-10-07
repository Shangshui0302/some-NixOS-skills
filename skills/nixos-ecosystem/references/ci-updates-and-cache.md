# CI, updates, quality, and binary caches

Use this reference for repository checks, input/package updates, dependency impact,
large evaluations, and build acceleration.

## Baseline checks

Run cheap checks first, then builds. Inspect the flake's formatter before choosing
its non-mutating check flag: `nix fmt` forwards arguments to that formatter, and
not every formatter accepts `--check`. If the flake has no formatter, run the
repository's declared formatter directly with its documented check option:

```bash
# Only when formatter.<system> supports --check:
nix fmt --no-update-lock-file --no-write-lock-file -- --check
statix check
deadnix --fail
nix flake check --no-update-lock-file --no-write-lock-file
host=your-config-name
nixos-rebuild dry-build --flake ".#${host}" --no-update-lock-file --no-write-lock-file
```

Use `nixd` or `nil` in the editor with the same flake inputs. Do not make formatting
or linting an excuse to rewrite unrelated files.

## Updates and impact

Separate three operations:

1. update a package source/hash;
2. update a flake input lock;
3. migrate an expression to a changed nixpkgs/Home Manager API.

For packages, `nix-update` can automate known source and dependency-hash patterns,
but review its diff and run the package test. For nixpkgs changes, use
`nixpkgs-review` to build the changed package and affected dependents when the
dependency surface matters. Never let an updater commit or push unless that action
was explicitly requested.

For large flakes, `nix-eval-jobs` and `nix-fast-build` can parallelize evaluation and
builds; select the relevant outputs rather than building every platform by default.

## Caches and trust

Use the official cache first. Add Cachix, Attic, or Hydra only with a documented
substituter, public key, retention policy, and trust boundary. A cache hit proves a
store path was substituted, not that the current live service is healthy. Never put
signing keys or CI tokens in the flake or build logs.

## Reviewable automation

The repository's first-layer freshness workflow detects a candidate nixpkgs lock,
runs the flake checks/builds against it, and reports overdue documentation reviews
as warnings without failing the job. Invalid manifests, flake checks, and build
errors still fail normally. A local equivalent is
`python3 scripts/check-freshness.py`. It does not silently change skill
instructions, activate hosts, delete generations, commit, or
push credentials. A later update job may propose a branch/PR only after the same
evidence and checks are available. If a NixOS version deprecates an image or
deployment command, update the reference and its examples together; do not retain
stale instructions just because an old lock still evaluates.
