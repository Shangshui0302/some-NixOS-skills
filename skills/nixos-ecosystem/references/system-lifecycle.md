# System lifecycle and recovery

Use this reference before a rebuild, activation, generation cleanup, or recovery.

## State machine

Treat each stage as a separate claim:

```text
source edit → parse → eval → dry-build → test/VM → dry-activate → switch → observe
```

| Stage | Typical command | Side effect |
| --- | --- | --- |
| Parse/eval | `nix-instantiate --parse`, `nix flake check` | none |
| Build plan | `nixos-rebuild dry-build --flake .` | none |
| Test activation | `nixos-rebuild test --flake .` | current session may change; boot default unchanged |
| Dry activation | `nixos-rebuild dry-activate --flake .` | reports planned activation |
| VM | `nixos-rebuild build-vm --flake .` | produces an isolated test system |
| Switch | `sudo nixos-rebuild switch --flake .` | changes the running system and boot target |
| Rollback | `nixos-rebuild switch --rollback` or select a generation | changes active generation |

Do not run `switch` automatically. Before any activation, record the current
generation, expected service changes, and a tested recovery command.

## Runtime evidence

After an approved activation, check the specific boundary that changed:

```bash
systemctl --failed
systemctl status <unit>
journalctl -b -u <unit> --no-pager
readlink /run/current-system
nixos-rebuild list-generations
```

For user services use `systemctl --user`; for graphical sessions inspect the session
environment and compositor/session logs. A healthy generation can still contain a
failed service or an unusable user configuration.

## Recovery ladder

1. Stop or isolate the failing service without deleting state.
2. Boot or switch to the previous generation.
3. Use a VM or rescue environment if the host cannot boot or network access is lost.
4. Only after recovery, inspect the failing diff and add a regression test.

Garbage collection is not a rollback strategy. Keep at least one known-good
generation until the new one has passed the live checks.
