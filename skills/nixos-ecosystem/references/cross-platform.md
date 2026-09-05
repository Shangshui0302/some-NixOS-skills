# Cross-platform boundaries

Use this reference for nix-darwin, Nix-on-Droid, non-NixOS Linux, macOS workstations,
or flakes that expose several systems.

## Portable layer

Keep packages, pure libraries, dev shells, most Home Manager modules, and flake
metadata portable where practical. Pass `system`, `pkgs`, and explicit feature flags
instead of reading host state during evaluation.

## Platform adapters

| Platform | Owns | Do not assume |
| --- | --- | --- |
| NixOS | boot, kernel, systemd, hardware, system users, firewall | it exists on macOS/Android |
| nix-darwin | macOS system defaults, launchd, users, Darwin services | NixOS options or Linux paths |
| Home Manager | user files, packages, user services | root-only system state |
| Nix-on-Droid | Android proot/module environment | full NixOS boot or systemd |
| non-NixOS Linux | Nix profile and Home Manager layers | `nixos-rebuild` or NixOS modules |

Select the correct flake output and activation command for the platform. Do not
reuse a Linux `systemd` unit, `/etc` path, boot option, or `nixos-rebuild` command on
a platform that does not provide it.

## Multi-system checks

Evaluate each supported output explicitly, but build only the systems the task needs.
Record unsupported systems rather than silently dropping them. A portable module can
still depend on platform-specific packages; expose that dependency in the module
interface and test one representative host per platform.
