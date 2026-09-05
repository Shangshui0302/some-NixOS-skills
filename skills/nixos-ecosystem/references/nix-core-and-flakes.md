# Nix core and flakes

Use this reference for Nix language, flakes, inputs, lock files, dev shells, and
version-specific option lookup.

## Establish the source of truth

1. Locate the repository root and read `flake.lock` before changing inputs.
2. Record the locked `nixpkgs`, Home Manager, and other module revisions.
3. Inspect the locked source or evaluate the exact output before relying on an API.
4. Compare current `nix.dev`, Nixpkgs, and NixOS manuals to detect process drift.

Flakes are a reproducibility boundary, not a guarantee that every output is portable.
Inputs can diverge unless `follows` is deliberate, and outputs still need an explicit
system. Do not update a lock file merely to make an unfamiliar option evaluate.

## Inspect without mutation

```bash
nix flake metadata --json path:.
nix flake show path:.
nix eval --json path:.#nixosConfigurations.<host>.config.system.stateVersion
nix repl path:.
```

For an option that is not obvious, use the target's `nixos-option`, `nix eval`, the
version-matched manual, or `nixd` backed by the same inputs. Never invent option names
from a blog post written for another release.

## Output conventions

Follow the existing flake's conventions for `nixosConfigurations`, `homeConfigurations`,
`packages`, `devShells`, `checks`, `formatter`, and image outputs. Add a new abstraction
only when it removes repeated, tested behavior. Keep `flake.nix` thin: put reusable
logic in modules or functions with a clear owner.

## Change classification

| Change | First proof | Do not claim yet |
| --- | --- | --- |
| Nix expression | parse/eval | runtime behavior |
| Flake input | lock diff and eval | cache availability |
| Package | build and output inspection | service or GUI health |
| NixOS module | dry-build or VM test | live activation |
| Home Manager file | activation build | that no manual file will be overwritten |

`nix develop` is a development environment, not proof that a package, module, or
system configuration builds in its intended sandbox.
