# Research notes: ideas, not source

The repository started as a packaging skill and now contains a small Nix/NixOS
ecosystem skill set. Public projects and official documentation were used as design
evidence; no implementation text was copied. These notes record decisions useful for
an independent, reviewable workflow.

## Ideas adopted

1. **Composable directories with stable paths.** A skill lives in its own directory
   and long material is loaded from references only when the task reaches that
   domain. The path is treated as a consumer-facing interface.
2. **Explicit trigger metadata.** The frontmatter names concrete actions and object
   types, including the cases the skill intentionally excludes.
3. **Read-only preview before mutation.** A default command or inspection path is
   safe; installation and other writes have an explicit entry point and confirmation
   boundary.
4. **Declarative distribution.** A flake exposes an immutable package containing the
   complete skill tree. Consumers can pin the repository in their own lock file.
5. **Small behavior evaluations.** `evals/evals.json` describes representative
   request shapes and the safety properties an implementation must preserve.
6. **Layered update review.** Source revisions and docs are pinned or recorded, an
   update produces a reviewable diff, and checks run before a human merges it.
7. **Context-aware execution.** Before commands are suggested, the workflow checks
   which machine and repository policy will execute them.

## Ecosystem ideas adopted

1. **Router plus progressive references.** `nixos-ecosystem/SKILL.md` owns triggers,
   safety gates, and decision order; domain references hold only the material needed
   for the current task.
2. **Version-aware source of truth.** Read `flake.lock`, inspect the locked source,
   and compare version-matched manuals before relying on an option or API. A current
   web page must not silently override a locked interface.
3. **Lifecycle state machine.** Treat parse/eval, dry-build, VM or integration test,
   activation, and live observation as separate claims with separate evidence.
4. **Ownership and recovery.** Decide whether NixOS, Home Manager, a package, a
   service, or mutable state owns each concern; high-risk work records a target,
   backup/recovery path, and rollback generation before applying it.
5. **Declarative state boundaries.** Handle disks, persistence, secrets, hardware,
   desktop services, caches, and deployment as explicit boundaries rather than
   treating generated state as source.
6. **Smallest safe target.** Prefer local evaluation, dry-builds, VM tests, and a
   single canary before remote or fleet deployment. Tools such as nixos-anywhere,
   disko, deploy-rs, and Colmena inform selection, not implicit authorization.
7. **Cross-platform adapters.** Keep portable Nix and Home Manager code separate
   from NixOS, nix-darwin, Nix-on-Droid, and non-NixOS activation assumptions.
8. **Reviewable maintenance.** Keep format/lint, input updates, package updates,
   cache changes, and CI automation independently reviewable; freshness may propose
   an update but never mutates a user system silently.

## Ideas deliberately not adopted

- No broad skill marketplace or automatic installer; this repository provides a
  small, local skill set and should not replace a host's skill manager.
- No automatic replacement of an existing skill directory; user-authored files must
  remain safe.
- No large Nix framework dependency just to enumerate systems or discover one skill.
- No workflow that commits, pushes, switches a system, or opens a pull request as an
  implicit side effect.
- No claim that a successful derivation build proves GUI, compositor, media, or
  post-activation behavior.

## References inspected

- [atvari-eu/nix-skills](https://github.com/atvari-eu/nix-skills): focused Nix skills,
  stable skill directories, and lightweight eval cases.
- [nhooey/nix-skills](https://github.com/nhooey/nix-skills): per-skill packaging,
  read-only preview versus explicit installation, and flake aggregation.
- [papercomputeco/flake-skills](https://github.com/papercomputeco/flake-skills):
  composition, local-over-upstream precedence, pinning, and stale-content cleanup.
- [Kyure-A/agent-skills-nix](https://github.com/Kyure-A/agent-skills-nix): source
  registries, lock snapshots, ownership markers, and safety-oriented checks.
- [michalzubkowicz/nixos-management-skill](https://github.com/michalzubkowicz/nixos-management-skill):
  progressive references, execution-context checks, and version-specific option
  verification.

Domain references used for the ecosystem workflow:

- [Nix ecosystem wiki](https://wiki.nixos.org/wiki/Nix_Ecosystem) and the
  [NixOS manual](https://nixos.org/manual/nixos/stable/) for the lifecycle and
  system/module boundaries.
- [Home Manager](https://github.com/nix-community/home-manager) for standalone
  versus NixOS-module ownership and version alignment.
- [nixos-anywhere](https://github.com/nix-community/nixos-anywhere) and
  [disko](https://github.com/nix-community/disko) for installation and destructive
  disk preflight boundaries.
- [sops-nix](https://github.com/Mic92/sops-nix),
  [agenix](https://github.com/ryantm/agenix), and
  [impermanence](https://github.com/nix-community/impermanence) for secret and
  persistent-state ownership.
- [nixos-hardware](https://github.com/NixOS/nixos-hardware),
  [deploy-rs](https://github.com/serokell/deploy-rs), and
  [Colmena](https://github.com/zhaofengli/colmena) for hardware and deployment
  selection, canaries, and recovery considerations.
- [NixOS VM tests](https://nixos.org/manual/nixos/stable/#sec-nixos-tests),
  [microvm.nix](https://github.com/microvm-nix/microvm.nix),
  [nix-eval-jobs](https://github.com/NixOS/nix-eval-jobs), and
  [nix-fast-build](https://github.com/Mic92/nix-fast-build) for isolated testing
  and scalable evaluation/build workflows.
- [nixfmt](https://github.com/NixOS/nixfmt),
  [statix](https://github.com/oppiliappan/statix),
  [deadnix](https://github.com/astro/deadnix),
  [Cachix](https://docs.cachix.org/), and
  [Attic](https://github.com/zhaofengli/attic) for reviewable quality and cache
  maintenance.

The independent content in `skills/nix-packaging/` combines those principles with
packaging-specific evidence and validation. `skills/nixos-ecosystem/` applies the
same boundaries to NixOS management without pretending that a build proves live
runtime health.
