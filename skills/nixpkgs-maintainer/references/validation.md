# Nixpkgs validation ladder

Run the smallest applicable check at each level and retain the command, target
revision, platform, result, and output path. A lower level never proves a
higher-level claim.

| Level | Proves | Typical evidence |
| --- | --- | --- |
| L0 parse/evaluate | the expression and target attribute evaluate in the target nixpkgs tree | parser/evaluator output |
| L1 build | the changed package builds in the sandbox | build log and store path |
| L2 package tests | declared package and relevant integration tests pass | `checkPhase`, `passthru.tests`, package/global or linked NixOS tests |
| L3 binary smoke | installed executables have the expected basic behavior | `./result/bin/* --version`/`--help`, output inspection |
| L4 nixpkgs integration | affected dependents and the PR/WIP build set remain viable | `nixpkgs-review` result and affected attributes |
| L5 real world | the requested display, network, GPU, plugin, hardware, or other scenario works | named machine/session and observed behavior |

Use the target checkout and its current documented commands. Examples are
deliberately adaptable:

```bash
nix-instantiate --parse pkgs/by-name/xx/example/package.nix
nix eval --raw .#example.version
nix build .#example -L --no-link --print-out-paths
nix log .#example
nixpkgs-review wip
```

For a non-flake nixpkgs checkout, use the package-set commands documented by the
current `pkgs/README.md` and `nixpkgs-review` documentation. Do not invent a
second flake output merely to make a check convenient.

At L2, run only tests applicable to the changed package and platform, but do
not silently omit an existing relevant test. At L4, inspect rebuild impact and
reverse dependencies when the change can affect them. At L5, keep display,
network, credentials, GPU, and hardware prerequisites explicit; a sandbox build
does not provide them.

Report skipped levels as `not run` with a reason. If a level fails, record the
first failing boundary and stop broadening the change until its cause is
understood. Never use `doCheck = false` or a blanket test skip as a substitute
for diagnosis.
