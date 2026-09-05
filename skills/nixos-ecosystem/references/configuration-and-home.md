# NixOS modules and Home Manager

Use this reference when a change could belong to system configuration, user
configuration, a shared module, or a package consumer.

## One owner per concern

| Concern | Default owner | Questions |
| --- | --- | --- |
| Kernel, boot, hardware, network, system daemon | NixOS host module | Does it need root, boot-time ordering, or system-wide state? |
| Shell, editor, user service, dotfile, desktop preference | Home Manager | Is it per-user and safe to activate without changing the host? |
| Package derivation | package module/flake output | Does another consumer need the same output? |
| Shared policy | reusable module | Are its options typed, documented, and safe for every importer? |
| Mutable runtime state | service/data boundary | Can it be backed up and restored independently of the generation? |

Search existing imports and consumers before adding a declaration. A package should
not be installed once in `environment.systemPackages` and again in `home.packages`
without a reason. A desktop entry, wrapper, or generated config should have one
authoritative owner.

## Module design

- Give a module one logical responsibility and a namespaced option surface.
- Use typed options and defaults that are safe when the module is disabled.
- Keep host-specific hardware quirks at the host boundary; do not hide them in a
  shared module without a compatibility check.
- Prefer existing NixOS/Home Manager modules over hand-written service scripts.
- Treat `system.stateVersion` and `home.stateVersion` as compatibility contracts, not
  routine version bumps.

## Home Manager modes

Choose explicitly between standalone activation and Home Manager as a NixOS module.
The module form can activate system and user changes together; standalone mode gives
the user an independent generation and may be appropriate on non-NixOS systems.
Check the chosen mode's activation command and ownership before editing files that
may already be managed manually.

## Review questions

Ask: who owns this file after activation? Can two modules define the same option or
consumer? What happens when the option is disabled? Which state survives rollback?
These questions expose duplicate declarations and accidental coupling earlier than a
large dry-build.
