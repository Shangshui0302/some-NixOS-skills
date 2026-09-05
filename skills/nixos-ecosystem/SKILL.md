---
name: nixos-ecosystem
description: >
  Evidence-driven Nix and NixOS ecosystem management. Use when a user asks to design,
  inspect, configure, migrate, test, install, deploy, roll back, recover, or review
  Nix, NixOS, Home Manager, flakes, modules, services, hardware, disks, secrets,
  desktops, VMs, containers, CI, binary caches, nix-darwin, or Nix-on-Droid. Trigger
  on phrases such as “fix my NixOS config”, “add a NixOS module”, “rebuild safely”,
  “deploy this host”, “set up Home Manager”, “partition with disko”, “manage secrets”,
  “test in a VM”, “rollback”, “update flake inputs”, or “why did this service fail”.
  Routes to current, version-aware references and keeps diagnosis, build, activation,
  and live runtime evidence separate. Not a replacement for the Nix/NixOS manuals,
  and not an excuse to run destructive or privileged actions without approval.
---

# NixOS Ecosystem

IRON LAW: NEVER APPLY A NIXOS CHANGE UNTIL THE TARGET, LOCKED VERSION, SIDE EFFECTS,
RECOVERY PATH, AND VALIDATION LAYER ARE EXPLICIT.

Red flags — return to context and evidence collection if any appear:

- The host, user, remote target, or execution environment is unclear.
- An option or command was recalled from memory instead of checked against the active version.
- A successful evaluation is being called a successful activation or live test.
- A disk, bootloader, secret, firewall, network, or remote deployment action lacks a rollback path.
- A mutable state directory, secret, or generated file is being treated as declarative source.

## Routing map

Load only the reference matching the task:

| Task signal | Load | Main result |
| --- | --- | --- |
| Nix language, flake, input, lock, dev shell | [references/nix-core-and-flakes.md](references/nix-core-and-flakes.md) | Version-aware evaluation and input plan |
| NixOS modules, Home Manager, profiles | [references/configuration-and-home.md](references/configuration-and-home.md) | Correct ownership and module composition |
| rebuild, test, switch, generation, rollback, recovery | [references/system-lifecycle.md](references/system-lifecycle.md) | Safe state transition plan |
| hardware, boot, disk, persistence, encryption, secrets | [references/hardware-storage-secrets.md](references/hardware-storage-secrets.md) | Preflight and recovery-aware system design |
| service, systemd, desktop, graphics, network | [references/services-and-desktop.md](references/services-and-desktop.md) | Declarative service and runtime diagnosis |
| installation, remote host, fleet, VM, container | [references/deployment-and-testing.md](references/deployment-and-testing.md) | Targeted deployment or isolated test |
| CI, cache, update, formatter, lint, review | [references/ci-updates-and-cache.md](references/ci-updates-and-cache.md) | Reproducible maintenance pipeline |
| Darwin, Android, or another non-NixOS host | [references/cross-platform.md](references/cross-platform.md) | Platform-specific boundary and fallback |

## Progress checklist

Copy this checklist into the task notes:

- [ ] Step 0: Establish context ⛔ BLOCKING
  - [ ] Identify the repository, current branch, dirty files, host platform, target machine, and privilege boundary.
  - [ ] Read repository `AGENTS.md`/contribution rules and preserve unrelated edits.
- [ ] Step 1: Establish version and source evidence ⚠️ REQUIRED
  - [ ] Read `flake.lock`, record the relevant nixpkgs/Home Manager/module revisions, and inspect their actual interfaces.
  - [ ] Check current official documentation for changes; report lock/API drift instead of silently mixing versions.
  - [ ] Use the exact option/module/tool source for non-trivial claims.
- [ ] Step 2: Classify the change
  - [ ] Decide whether it belongs to Nix code, a NixOS module, Home Manager, host hardware, mutable state, deployment, or a test.
  - [ ] Decide whether native NixOS service, package, container, VM, or external tool is the narrowest fit.
- [ ] Step 3: Produce a read-only plan ⚠️ REQUIRED for non-trivial or privileged work
  - [ ] Show affected files, dependency edges, expected generations, side effects, recovery path, and checks.
  - [ ] Ask before writing files, formatting, changing locks, installing, rebuilding, deploying, deleting, or pushing.
- [ ] Step 4: Validate the plan
  - [ ] Parse and evaluate the intended output.
  - [ ] Dry-build the system or package; run a VM/integration test when the behavior crosses system boundaries.
  - [ ] Inspect logs, generated units, closure changes, and secrets/state ownership.
- [ ] Step 5: Apply only the approved action ⚠️ REQUIRED
  - [ ] Prefer `test`, `dry-activate`, VM, canary, or a scoped remote target before `switch`.
  - [ ] Keep an explicit previous generation or deployment revision available.
- [ ] Step 6: Observe and report
  - [ ] Separate written configuration, evaluated/buildable output, activated generation, and live behavior.
  - [ ] Report rollback command, remaining uncertainty, and the exact manual next step.

## Context gate

Before suggesting commands, answer: where is the repository, where does evaluation
run, where does activation run, and which user owns each side effect? A local NixOS
host, remote NixOS target, macOS workstation, CI runner, rescue shell, and disposable
VM have different command availability and risk. If any answer is missing, stop at
read-only inspection.

## Version-aware option lookup

Load [references/nix-core-and-flakes.md](references/nix-core-and-flakes.md) before using an unfamiliar option or API. Do
not invent `services.*`, `systemd.*`, Home Manager, or flake output names. Prefer the
locked source, `nix eval`, `nixos-option` on the target host, version-matched manuals,
or a language server backed by the same inputs. Record the version that supports the
answer.

## Configuration ownership

Load [references/configuration-and-home.md](references/configuration-and-home.md) when a change could fit both system and
user scope. Keep one owner for each package, file, service, environment variable,
and desktop integration. A shared module may be imported by multiple hosts, but a
host-specific workaround must not leak into the common layer without evidence.

## Lifecycle and recovery

Load [references/system-lifecycle.md](references/system-lifecycle.md) before building or activating a system. Use
`parse → eval → dry-build → test/VM → activate → observe` as separate claims. Treat
boot, kernel, display, network, firewall, secrets, disk, and remote deployment as
high-risk changes with explicit rollback and rescue procedures.

## State, secrets, and destructive operations

Load [references/hardware-storage-secrets.md](references/hardware-storage-secrets.md) for disks, persistence, encryption,
impermanence, agenix, or sops-nix. Never print secret contents or put them in Nix
evaluation output. Never run a disk formatter or unattended installer until the
target identity, backup state, exact disk, and destructive effect have been confirmed.

## Services and runtime proof

Load [references/services-and-desktop.md](references/services-and-desktop.md) for systemd, desktop sessions, graphics,
audio, input, networking, or user services. Prefer the native module when it exists,
but verify generated units, ordering, permissions, environment, and logs. A dry-build
does not prove that a compositor plugin, Wayland session, media player, or service is
healthy after activation.

## Deployment and isolated tests

Load [references/deployment-and-testing.md](references/deployment-and-testing.md) for `nixos-anywhere`, disko, deploy-rs,
Colmena, NixOS VM tests, containers, or microVMs. Select the smallest safe target:
local VM, disposable host, canary, one remote node, then fleet. Do not treat a
parallel deployment tool as permission to deploy.

## CI, updates, and caches

Load [references/ci-updates-and-cache.md](references/ci-updates-and-cache.md) for format/lint checks, flake input updates,
package update scripts, dependency impact, Hydra/Cachix/Attic, or large evaluations.
Keep updates reviewable: detect, propose, check, then merge. Do not silently update
the skill or mutate a user's system.

## Cross-platform boundary

Load [references/cross-platform.md](references/cross-platform.md) for nix-darwin, Nix-on-Droid, non-NixOS Linux,
or mixed-host flakes. Separate portable Nix/Home Manager code from platform modules;
do not assume `nixos-rebuild`, systemd, or Linux paths exist everywhere.

## Pre-delivery checklist

- [ ] Target host, execution context, and privilege boundary are stated.
- [ ] Relevant lock revisions and version-specific option/API evidence are recorded.
- [ ] Every changed file has one clear owner and no duplicate declaration was introduced.
- [ ] Parse/eval, dry-build/build, and any VM or runtime test are reported separately.
- [ ] Secrets, disks, boot, network, and deployment actions have explicit safety gates.
- [ ] A rollback or recovery command is documented for every high-risk change.
- [ ] No unapproved `switch`, remote deployment, destructive command, commit, or push occurred.

## Freshness gate

Before relying on an option, command, module interface, or deployment tool:

1. Read the repository's locked inputs and record the relevant revisions.
2. Check the version-matched manual or upstream source for the behavior in question.
3. Mark claims as locked-source evidence, current documentation, or an inference.
4. If sources disagree, stop at diagnosis and report the drift instead of silently
   updating the lock or inventing a compatibility shim.

## Validation

Use the smallest check that proves the current claim, and report layers separately:

- parse/evaluate the changed expression and flake output;
- dry-build the package or system;
- run a VM/integration test for system boundaries when available;
- activate only after approval, then inspect the active generation, units, logs, and
  user-visible behavior.

An exit-0 build is evidence about evaluation and derivations only. It is not proof
of bootability, service health, secrets access, network behavior, or desktop runtime.

## Anti-patterns

- Guessing an option, module argument, output name, or command from memory.
- Mixing an unlocked or current online interface with a different locked input.
- Editing generated state, `/etc`, a secret, or a disk directly when the declarative
  owner is in the repository.
- Running `sudo nixos-rebuild switch`, remote deployment, disk formatting, garbage
  collection, commit, or push without an explicit user decision.
- Declaring a dry-build, VM build, or evaluation to be live runtime proof.
- Adding duplicate package, service, desktop, or secret ownership across modules.

## Delivery format

Report, in this order:

1. target repository/host, execution context, branch, and privilege boundary;
2. locked revisions and the evidence used for non-trivial interfaces;
3. files changed and ownership decisions;
4. parse/eval, dry-build, VM/integration, activation, and live-runtime results,
   clearly separated;
5. recovery command, remaining uncertainty, and the exact manual next step.
