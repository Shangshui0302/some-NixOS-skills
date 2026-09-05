# Builder routing

Choose the narrowest route supported by the evidence. Read only the section for the
package type under investigation.

## Source packages

| Upstream signal | Starting point | Verify next |
| --- | --- | --- |
| Autotools/Make | `stdenv.mkDerivation` | default configure/build/install phases |
| CMake | `cmake` in `nativeBuildInputs` | feature flags and install output |
| Meson/Ninja | `meson`, `ninja` | project options and tests |
| Rust | `rustPlatform.buildRustPackage` | `cargoHash`/lock mode and workspace targets |
| Go | `buildGoModule` | `vendorHash`, `subPackages`, version flags |
| Python app | `buildPythonApplication` | build backend, runtime dependencies, imports |
| Node/npm | `buildNpmPackage` | lockfile, `npmDepsHash`, offline build, wrapper |

Use default phases first. If a phase is replaced, run its matching `pre` and `post`
hooks. Put tools used while building in `nativeBuildInputs`, libraries needed by the
result in `buildInputs`, and test-only programs in `nativeCheckInputs`.

## Prebuilt ELF

Start with `fetchurl` plus `autoPatchelfHook` only when the artifact is a native
release. Before adding libraries, inspect `file`, `readelf -h`, the interpreter, and
dynamic `NEEDED` entries. If the program invokes external commands by name, provide
them with a wrapper or store path; merely listing them as a build input is not a
runtime contract.

Record `sourceProvenance` for native binary code and inspect bundled licenses. Move
to a manual patch only when the failure is understood; use an FHS wrapper as a last
resort, not as a default escape hatch.

## AppImage and Electron

Confirm the AppImage type and whether source packaging is practical before using
`appimageTools`. If desktop resources are extracted, install them explicitly and
test their `Exec`, `Icon`, and wrapper paths.

For Electron/ASAR, prefer a reproducible source build when available. Otherwise pin
the ASAR/resource bundle, use the nixpkgs Electron runtime, and document every
Wayland, sandbox, or keyring flag that survives into the wrapper.

## Fonts, themes, data, and plugins

Use `stdenvNoCC` for data-only outputs. Install fonts under `share/fonts`, themes
under `share/themes`, and check the expected files and permissions. Use `fc-scan`
for fonts.

For compositor plugins, match the source commit to the compositor ABI exposed by
the locked nixpkgs. A successful `.so` build is not proof of live loading; reserve
IPC/log inspection for post-activation validation.

## Metadata and integration

At minimum, verify `pname`, `version`, description, homepage, license, platforms,
and `mainProgram` where applicable. Use SRI `hash` values and interpolate version
variables rather than duplicating literals. Desktop integration is complete only
when the wrapper, desktop file, icon, and executable agree.
