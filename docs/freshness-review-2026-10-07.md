# Documentation freshness review: 2026-10-07

Reviewed all 13 unique references mapped by `freshness-sources.json`, the relevant skill
instructions, and the repository's installation examples. These are source/API
and documentation findings. They do not establish a successful host activation or
prove that every external packaging example builds.

## Sources and conclusions

- **nixpkgs-locked-api:** compared locked
  `0968519e14f7aa7d3e9b389682bd74d2b51c8ce8` with current master
  `2878f09f4e746af44c016c9a0b71f8cc5f9e2a43` and the rendered unstable manual
  `26.11pre1026231.65179426c83b`. Checked builder/input APIs, font/theme layouts,
  binary metadata, Electron ABI guidance, and the five maintainer references.
  Corrected packaging details; the existing maintainer process remains compatible.
  The two source revisions' CONTRIBUTING, PR template, and by-name README match.
- **home-manager-locked-api:** inspected locked
  `693e8ce0fb240a73c116a03cfd7b19269c87af88` for
  `homeManagerConfiguration`, `activationPackage`, directory `home.file` links,
  and `home.stateVersion = "25.11"`. The repository's module API is compatible.
  Added the missing `extraSpecialArgs` prerequisite to the README example.
- **nix-manual:** checked the current Nix manual (2.35.2) for flake inspection,
  lock options and arbitrary node labels/follows, evaluation/build boundaries,
  formatter argument forwarding, and import-from-derivation. Guarded checkout/lock
  inspection examples, clarified system-keyed outputs, and made host selection
  explicit.
- **nixos-manual:** checked the current unstable manual (26.11), locked
  `nixos-rebuild-ng`, activation code, and testing interfaces. Corrected lifecycle
  side effects, incomplete dry-activation previews, VM build versus runtime
  evidence, remote flake selection, recovery guidance, and user-service logs.
- **home-manager-manual:** reviewed the current 26.11 unstable manual's standalone,
  NixOS, and nix-darwin installation guidance. Its exact publication commit was
  not established. Clarified integration modes, activation-service checks, and
  the links produced after activation.

All five sources were reviewed on 2026-10-07. The 30-day intervals are unchanged,
so their next review date is 2026-11-06. `flake.lock` is unchanged. The corrections
above are inaccuracies found during review, not demonstrated new upstream breaking
changes or a reason to migrate the lock.

## Source-first exceptions

The current rendered Nixpkgs manual includes older AppImage `name` and executable
rename examples, and older Rust `cargoSha256`/vendor-tarball wording. The locked
and compared current source use `pname`/`version` for AppImage extraction and
`cargoHash` or explicit lock/vendor modes for Rust. Keep inspecting those source
interfaces rather than copying the older manual examples. The skills' existing
generic AppImage and `cargoHash`/lock routes remain compatible.

## Evidence

- [Locked builder definitions](https://github.com/NixOS/nixpkgs/tree/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/pkgs/build-support),
  [locked font installer](https://github.com/NixOS/nixpkgs/blob/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/pkgs/by-name/in/installFonts/install-fonts.sh),
  [locked contribution guide](https://github.com/NixOS/nixpkgs/blob/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/CONTRIBUTING.md),
  [compared current contribution guide](https://github.com/NixOS/nixpkgs/blob/2878f09f4e746af44c016c9a0b71f8cc5f9e2a43/CONTRIBUTING.md)
- [Nix flake check](https://nix.dev/manual/nix/2.35/command-ref/new-cli/nix3-flake-check),
  [Nix import-from-derivation](https://nix.dev/manual/nix/2.35/language/import-from-derivation.html),
  [NixOS manual](https://nixos.org/manual/nixos/unstable/)
- [Locked rebuild manual](https://github.com/NixOS/nixpkgs/blob/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/pkgs/by-name/ni/nixos-rebuild-ng/nixos-rebuild.8.scd),
  [locked activation implementation](https://github.com/NixOS/nixpkgs/blob/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/nixos/modules/system/activation/activation-script.nix)
- [Locked Home Manager flake guidance](https://github.com/nix-community/home-manager/blob/693e8ce0fb240a73c116a03cfd7b19269c87af88/docs/manual/nix-flakes/nixos.md),
  [current Home Manager NixOS integration](https://nix-community.github.io/home-manager/nix-flakes/nixos.html),
  [Home Manager installation](https://nix-community.github.io/home-manager/installation.html)
- [Electron native modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules)
- [Locked AppImage implementation](https://github.com/NixOS/nixpkgs/blob/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/pkgs/build-support/appimage/default.nix),
  [locked Rust builder](https://github.com/NixOS/nixpkgs/blob/0968519e14f7aa7d3e9b389682bd74d2b51c8ce8/pkgs/build-support/rust/build-rust-package/default.nix)

## Verification boundaries

The freshness warning regression suite and all three skill structural checks run
locally. Full flake/build results are tracked separately by the PR's CI. No NixOS
activation, remote deployment, VM boot, or lock update was performed for this
review. External deployment and developer-tool guidance was checked against its
official documentation; those tools are not all pinned by this repository.
