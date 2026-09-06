# Package anatomy

Read this reference before selecting a builder or editing an existing nixpkgs
package. The goal is to identify the package's contracts before changing its
expression.

| Area | Inspect | Record |
| --- | --- | --- |
| Location | attribute path, current preferred layout, imports | why this path is correct for the target revision |
| Source | fetcher, tag/commit, generated files, submodules | immutable source and provenance |
| Builder | `stdenv` helper, language builder, hooks, cross-compilation behavior | locked nixpkgs interface and why it fits |
| Dependencies | build, host, runtime, test, and propagated inputs | which phase and output needs each input |
| Lock data | `Cargo.lock`, `go.sum`, npm lockfile, Gradle dependencies, vendored tree | fixed-output hash and refresh method |
| Patches | local patches, `fetchpatch`, downstream substitutions, flags | reason, source, and expiry condition |
| Outputs | binaries, libraries, data, desktop files, wrappers, permissions | stable output contract and `meta.mainProgram` when applicable |
| Tests | `checkPhase`, `passthru.tests`, package/global tests, NixOS tests | applicable tests and missing coverage |
| Consumers | reverse dependencies, modules, overlays, aliases, platform users | affected graph and rebuild risk |
| Maintenance | update script, release cadence, maintainers, known issues | who owns the next update and what automation is safe |

For a new package, check the current `pkgs/README.md` and
`pkgs/by-name/README.md` before choosing a path or fetcher. Prefer the current
nixpkgs convention over copying a nearby package that is being migrated.

For an update, compare the old and new upstream build files and lock data, not
just `version` and `hash`. Re-check license, supported platforms, install layout,
patch applicability, and reverse dependencies.

For a breakage, identify the first failing phase or runtime boundary. Do not
add dependencies, overrides, `meta.broken`, or disabled tests until the failure
is reproduced and its scope is known.

For local-to-upstream work, remove machine-specific paths, implicit network
access, user configuration, and consumer-only wrappers. Keep only behavior that
belongs in the package expression or an explicitly requested nixpkgs interface.
