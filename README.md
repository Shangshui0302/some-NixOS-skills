# nix-ecosystem-skills

Composable agent skills for evidence-driven Nix and NixOS work. The repository
covers package derivations and the surrounding configuration, lifecycle,
deployment, testing, and recovery workflow.

This repository is currently local and intentionally has no remote or push. Each
`skills/<name>/` directory is a stable consumer interface; the flake discovers every
directory containing `SKILL.md`.

## Skills

| Skill | Use for |
| --- | --- |
| `nix-packaging` | Add, upgrade, repair, or review local Nix derivations and their build/runtime evidence. |
| `nixos-ecosystem` | Manage Nix, flakes, NixOS, Home Manager, hardware, secrets, services, VMs, deployment, CI, and cross-platform boundaries. |

The ecosystem skill is a workflow router, not an installer or a replacement for
version-matched Nix/NixOS documentation. Its references are loaded by task domain so
ordinary work does not require reading a large manual.

## Use

From the repository root:

```bash
nix flake check
nix build .#nix-packaging
nix build .#nixos-ecosystem
nix build .#all-skills

python3 skills/nix-packaging/scripts/validate-skill.py skills/nix-packaging
python3 skills/nix-packaging/scripts/validate-skill.py skills/nixos-ecosystem
```

The same structural checks, flake checks, and three package outputs run in
`.github/workflows/ci.yml` when this repository is connected to GitHub.

The per-skill outputs and `all-skills` contain complete trees under
`share/agent-skills/<name>/`. Copy or wire those directories into an agent runtime
only through the host's normal configuration mechanism. Adding a new skill requires
only a directory with `SKILL.md`, its resources, and at least three eval cases; the
flake and aggregate check discover it automatically.

## Freshness and updates

The skill is not a frozen prompt: each applicable task has a freshness gate that
reads the locked inputs and checks the version-matched official documentation before
using an unfamiliar option or API. The repository itself does not perform silent
background updates. A requested update is a reviewable change to the lock, references,
examples, and evals, followed by the same checks; a future scheduled CI job may
propose that change but must stop before merge, activation, commit, or push.

## Design choices

- Evidence comes before edits: locked inputs, version-matched interfaces, and
  immutable upstream facts are recorded before changing a package or system.
- Read-only diagnosis and preview are the default; activation, commit, push, and
  PR creation require an explicit user decision.
- Each short `SKILL.md` routes to domain references on demand instead of loading a
  large manual for every task.
- Flake outputs are explicit, auto-discovered, and testable through structural
  validation plus representative eval cases.
- Automatic freshness checks may propose a reviewable update, but must not silently
  rewrite instructions or mutate a user's system.

These principles were informed by public projects, not copied from their source:
[atvari-eu/nix-skills](https://github.com/atvari-eu/nix-skills),
[nhooey/nix-skills](https://github.com/nhooey/nix-skills),
[papercomputeco/flake-skills](https://github.com/papercomputeco/flake-skills),
[Kyure-A/agent-skills-nix](https://github.com/Kyure-A/agent-skills-nix), and
[michalzubkowicz/nixos-management-skill](https://github.com/michalzubkowicz/nixos-management-skill).
The extracted ideas and deliberate non-goals are recorded in
[`docs/research-notes.md`](docs/research-notes.md).

## Scope boundary

These are workflow skills, not a package registry, NixOS module, installer, or
replacement for official manuals. They record how an agent should gather evidence,
make the smallest change, preserve ownership and recovery boundaries, and state
exactly which validation layer passed. They never imply permission to run
`nixos-rebuild switch`, remote deployment, disk formatting, commit, or push.
