# Package development examples

These examples define the minimum useful behavior, not literal scripts to copy.

## Add a package

Input: “Package this upstream CLI for my package repository, flake, or overlay.”

Expected route: inspect the target's pinned nixpkgs context and search existing
expressions first; inspect upstream build and release metadata; choose a source or
release route; add a fixed derivation and preserve the target's package-facing
surface; build it and run `--version` or an equivalent safe call. Ask before
connecting it to a system or Home Manager consumer when that is not part of the task.

## Upgrade an existing derivation

Input: “Update the package from 1.2 to 1.3.”

Expected route: compare the changelog and lockfiles, verify the new tag/artifact,
refresh source and dependency hashes independently, inspect the diff, rebuild, and
report any changed runtime or desktop behavior. Do not assume a version-only edit is
safe.

## Integrate a package surface

Input: “Expose an existing package through the overlay or flake package for a module
consumer.”

Expected route: inspect the established attribute name, system matrix, overlay
contract, and consumer imports; change only the requested package-facing surface;
evaluate and build the package, then run the consumer's dry-build when in scope.
Do not activate the system as part of package validation.

## Repair a binary or desktop package

Input: “The AppImage builds but the launcher or Wayland startup is broken.”

Expected route: inspect the artifact type, ELF dependencies, wrapper, desktop entry,
icon, and runtime flags; fix the first failing boundary; rebuild and inspect the
output. Mark actual GUI/Wayland behavior as unverified until the user activates it
and performs the live test.

## Review without editing

Input: “Audit this derivation for Nix packaging problems.”

Expected route: collect the same evidence, report findings by severity and location,
and stop before edits unless the user explicitly approves a change.
