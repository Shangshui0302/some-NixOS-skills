# System lifecycle and recovery

Use this reference before a rebuild, activation, generation cleanup, or recovery.

## State machine

Treat each stage as a separate claim:

```text
source edit → parse → eval → dry-build → build/VM → dry-activate → approved test → approved switch → observe
```

Replace `host` with the intended `nixosConfigurations` attribute; `--flake .`
omits explicit output selection. Evaluation and dry-build are not
filesystem-read-only guarantees. `--no-build` suppresses flake check builds, but
import-from-derivation may still build during evaluation; use
`--option allow-import-from-derivation false` when that must be forbidden.
`--no-update-lock-file` rejects required lock changes, and `--no-write-lock-file`
prevents writing a generated lock.

| Stage | Typical command | Side effect |
| --- | --- | --- |
| Parse | `nix-instantiate --parse <file.nix>` | parses only; no activation |
| Evaluation | `nix flake check --no-build --no-update-lock-file --no-write-lock-file` | validates flake outputs without building checks or activating |
| Build plan | `nixos-rebuild dry-build --flake .#host --no-update-lock-file --no-write-lock-file` | plans system outputs; no activation; evaluation may fetch inputs or write store/cache data |
| VM build | `nixos-rebuild build-vm --flake .#host --no-update-lock-file --no-write-lock-file` | builds a launcher; launch `./result/bin/run-*-vm` separately before claiming VM runtime evidence; guest disk state persists |
| Dry activation | `nixos-rebuild dry-activate --flake .#host --no-update-lock-file --no-write-lock-file` | builds the system and previews activation; the preview may be incomplete and dry-compatible activation snippets are executed |
| Test activation | `sudo nixos-rebuild test --flake .#host --no-update-lock-file --no-write-lock-file` | builds and activates the running system; boot default unchanged |
| Switch | `sudo nixos-rebuild switch --flake .#host --no-update-lock-file --no-write-lock-file` | changes the running system and boot target |
| Rollback | `sudo nixos-rebuild switch --rollback` or select a generation in the boot menu | rolls the system profile back and activates it as the boot default; boot-menu selection is a separate recovery path |

Do not run `test`, `boot`, `switch`, or rollback automatically. Before any
activation, record the current generation, expected service changes, and a tested
recovery command.

## Runtime evidence

After an approved activation, check the specific boundary that changed:

```bash
systemctl --failed
systemctl status <unit>
journalctl -b -u <unit> --no-pager
readlink /run/current-system
nixos-rebuild list-generations
```

For user services run `systemctl --user` and
`journalctl --user -b -u <unit> --no-pager` as the intended user. For graphical
sessions inspect the session environment and compositor/session logs. A healthy
generation can still contain a failed service or an unusable user configuration.

## Recovery ladder

1. Stop or isolate the failing service without deleting state.
2. Boot or switch to the previous generation.
3. Use an out-of-band console or rescue environment if the host cannot boot or
   network access is lost; use a VM to reproduce the failure when useful.
4. Only after recovery, inspect the failing diff and add a regression test.

Garbage collection is not a rollback strategy. Keep at least one known-good
generation until the new one has passed the live checks.
