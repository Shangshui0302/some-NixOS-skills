# Validation layers

Run the smallest check that proves each claim, and label the layer in the final
report.

## Required command sequence

```bash
nix-instantiate --parse path/to/package.nix
nix flake check path:. --no-build
nix build path:.#pname -L --no-link --print-out-paths
git diff --check
```

Use `nix log path:.#pname` after a failed build. Do not replace a sandbox build with
an interactive `nix develop` session.

## Output checks by package type

| Type | Inspect | Safe smoke test |
| --- | --- | --- |
| CLI | `$out/bin`, wrapper `PATH`, interpreter | `--version` or `--help` |
| Native binary | architecture, interpreter, `NEEDED` | `--version` with a minimal fixture |
| AppImage/Electron | wrapper, desktop file, icon, resource paths | `--version`/headless startup when supported |
| Font | `share/fonts`, metadata | `fc-scan` on one font |
| Theme/data | expected files, permissions, paths | list/read one expected asset |
| Plugin | expected `.so`, ABI metadata | post-activation plugin listing |

Check that a wrapper does not refer to `/usr/bin`, that versioned URLs and hashes
agree, and that no placeholder or fake hash remains.

## Integration boundary

Run `nixos-rebuild dry-build --flake path:.` only when the package is wired into a
NixOS or Home Manager configuration. This proves evaluation and build planning, not
activation. Keep these states separate:

1. **Derivation build** — the store output was produced.
2. **Un-deployed smoke** — the output was inspected or safely invoked.
3. **System dry-build** — the configuration can include the package.
4. **Live test** — a user applied the configuration and observed the real service,
   desktop, IPC, media, or Wayland behavior.

Never promote one state to another in prose.

## Failure routing

Locate the first failing phase: unpack, patch, configure, build, check, install, or
fixup. Fix that cause before changing dependencies. For fixed-output failures, use a
deliberate fake hash, copy the reported `got` value, and rebuild; never disable the
check to make the output green.
