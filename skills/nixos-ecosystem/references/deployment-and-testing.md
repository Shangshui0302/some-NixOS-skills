# Deployment and isolated testing

Use this reference for installation, remote rebuilds, fleets, NixOS tests,
containers, and microVMs.

## Choose the smallest target

1. Evaluate and dry-build locally.
2. Run a focused NixOS VM test or `build-vm` when the behavior crosses systemd,
   boot, networking, or user-session boundaries.
3. Test on a disposable host or one canary.
4. Deploy one remote node, observe, then expand to a fleet.

Do not use a fleet tool to skip the canary or confirmation step.

## Installation and disks

`nixos-anywhere` plus `disko` is suitable for repeatable commissioning, but the
target may be repartitioned and overwritten. Confirm hostname, SSH identity, disk
serial/path, backups, encryption recovery, and the exact flake output before running
it. Never aim an unattended install at an unverified production host.

## Remote deployment

For a small number of hosts, start with `nixos-rebuild --target-host` and explicit
`--flake host` selection. For multiple hosts, compare deploy-rs and Colmena:

- deploy-rs exposes deployment checks and can roll back successful peers when a
  multi-target deployment fails;
- Colmena is a stateless wrapper around Nix operations and supports parallel deploys.

In either case, record the source revision, target set, previous generation, SSH
user, activation mode, and post-deploy health checks. Keep secrets and host keys out
of command logs.

## Tests

Use `pkgs.testers.runNixOSTest` or the current NixOS test framework for declarative
multi-node tests. Test the invariant, not an implementation detail: a service is
reachable, a unit is ordered correctly, a user can log in, or a secret is mounted
with the intended permissions. Use containers for fast service tests and VMs when
kernel, boot, graphical, setuid, or isolation behavior matters.

MicroVMs are a useful middle layer for repeatable service isolation, but their
network, state, and hypervisor assumptions must be included in the test plan.
