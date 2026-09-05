# Freshness and evidence

Use this reference before selecting a builder, changing a hash, or claiming an
upstream interface is supported.

## 1. Establish the evaluation context

1. Find the target flake and read `flake.lock`.
2. Record the `nixpkgs` node's locked revision, nar hash, and URL.
3. Inspect that exact nixpkgs checkout for the builder, hook, or helper being used.
4. If no lock exists, state which explicit nixpkgs reference is being used and treat
   the result as provisional.

Useful checks include:

```bash
nix flake metadata --json path:. | jq '.locks.nodes.nixpkgs'
nix eval --impure --expr '
  let f = builtins.getFlake (toString ./.) in
  builtins.attrNames f.inputs
'
```

Do not use a registry or an unpinned channel as proof of the target flake's API.

## 2. Compare two documentation layers

For every non-trivial builder or hook, answer both questions:

- What does the locked nixpkgs source accept and do?
- What does the current official Nixpkgs manual or nix.dev packaging guide now
  recommend?

If the answers differ, classify the difference:

| Difference | Action |
| --- | --- |
| Documentation wording only | Record the current wording; keep the locked-compatible code. |
| New optional interface | Use it only after proving the lock exposes it. |
| Removed/renamed interface | Stop, report migration impact, and update the lock or expression deliberately. |
| Security or reproducibility guidance changed | Treat as a required review item, not a cosmetic note. |

The skill itself must not silently rewrite its rules in response to a newer page.

## 3. Collect upstream facts

Use `gh` for GitHub repositories, releases, tags, and file contents. Record:

- immutable tag or commit and its release date;
- the documented build command and the CI job that actually runs it;
- source archive or release artifact name, platform, and architecture;
- executable name and install layout;
- license files and bundled third-party notices;
- generated files or vendored dependencies that affect fixed-output hashes.

Prefer two independent signals, such as a release artifact plus CI, before making
an unusual packaging choice. A README claim alone is not enough for an ELF,
AppImage, Electron, or plugin package.

## 4. Write a small evidence record

Before editing, leave a short note in the task or review containing:

```text
nixpkgs: <locked revision> / <builder or hook>
upstream: <immutable tag or commit> / <source or artifact>
route: <source | binary | AppImage | Electron | data | plugin>
reason: <one sentence>
open questions: <unknowns and the check that will answer each>
```

Never substitute a guessed hash, guessed main program, or guessed license for an
open question; use a deliberate fake-hash iteration or mark the task blocked.
