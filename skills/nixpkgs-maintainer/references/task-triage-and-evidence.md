# Task triage and evidence

Use this reference at the start of every upstream nixpkgs task. It is a routing
and investigation aid, not a generic Nix tutorial.

## Classify the request

Apply one primary type and any secondary types; for example, an old desktop
package may be LOCAL_TO_UPSTREAM + BROKEN + UPDATE + PATCH.

| Type | Entry condition | First question | Typical output |
| --- | --- | --- | --- |
| UPDATE | An existing package should follow an upstream release or commit | What changed besides the version and source hash? | Minimal update with changelog, lockfile, metadata and binary evidence |
| BROKEN | Evaluation, build, test, or runtime is broken | What is the first reproducible failing boundary? | Root-cause fix or a documented blocker |
| NEW_PACKAGE | No suitable nixpkgs package exists | Is the upstream project usable, licensed, maintained and worth the maintenance cost? | Package in the current preferred layout with metadata, maintainer and tests |
| PATCH | An upstream or packaging fix must land before a release | Is there a stable upstream commit, and when can this patch disappear? | Fetch or vendor a documented patch, then prove and track expiry |
| DEPENDENCY_BREAKAGE | A dependency/toolchain update breaks this package or its consumers | Which edge changed, and what reverse dependencies are affected? | Compatibility fix with downstream validation |
| REVIEW | The user asks to assess a nixpkgs diff/PR | What does the diff claim, and what evidence is missing? | Findings by location; no edits unless separately authorized |
| ADOPT | A package needs a maintainer or the user wants to assume ownership | Is the maintainer-list and package metadata change appropriate? | Separate maintainer change and package change when required |
| LOCAL_TO_UPSTREAM | A local derivation/overlay is being proposed for nixpkgs | Which local assumptions must be removed or justified? | Upstream-shaped derivation, not a copied machine workaround |

Do not turn a request into a repository-wide update bot. A requested inventory
or sweep is read-only until each proposed change has its own evidence and the
user authorizes mutation.

## Verify the target

Do not infer that the current workspace is nixpkgs. Resolve the path supplied by
the user (or ask for one), then check:

~~~bash
git -C /path/to/nixpkgs rev-parse --show-toplevel
git -C /path/to/nixpkgs status --short
git -C /path/to/nixpkgs branch --show-current
git -C /path/to/nixpkgs rev-parse HEAD
test -f /path/to/nixpkgs/CONTRIBUTING.md
test -d /path/to/nixpkgs/pkgs
~~~

Record dirty files before editing and preserve unrelated changes. A supplied
diff or PR can be reviewed without a local checkout, but package builds and
consumer checks require a target checkout; state that boundary instead of
substituting a different nixpkgs revision.

For GitHub facts, use the gh CLI with an explicit repository, for example:

~~~bash
gh repo view NixOS/nixpkgs
gh pr view 12345 --repo NixOS/nixpkgs
gh pr diff 12345 --repo NixOS/nixpkgs
gh pr checks 12345 --repo NixOS/nixpkgs
gh release view v1.2.3 --repo OWNER/PROJECT
gh issue view 12345 --repo OWNER/PROJECT
~~~

Use gh api only when a higher-level gh command cannot provide a needed field.
Do not use curl, hand-built GitHub API URLs, mutable latest pages, or
unverified search snippets as release/source evidence.

## Evidence ledger

Make the following table before changing a derivation. It may remain in working
notes, a review comment, or the delivery packet.

~~~text
Package / attribute / path:
Primary and secondary task types:
Target repo / branch / revision:
Current nixpkgs version, source and status:
Upstream official project / release or commit / changelog:
License and maintainer evidence:
Failure or requested behavior / exact reproduction:
Package anatomy and affected consumers:
Patch, flag, disabled check, or override / reason / expiry:
Validation planned and not applicable levels:
Open contradictions or blockers:
~~~

Classify each entry as one of:

- **Source fact:** pinned nixpkgs file, official upstream release/commit/issue,
  official CI log, or current project documentation.
- **Local observation:** command, build log, output inspection, or runtime test
  performed on a named architecture/session.
- **Inference:** a reasoned conclusion derived from facts; state the reasoning
  and do not present it as upstream confirmation.

If two sources disagree, preserve both, identify which revision each describes,
and stop before choosing a patch or compatibility flag. An unknown hash,
builder, license, or failure cause is a blocker, not permission to guess.

## Official starting points

Recheck these files at task time because the upstream process evolves:

- [CONTRIBUTING.md](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md)
  for branches, review, PRs, backports, commit conventions and the automation/AI policy.
- [pkgs/README.md](https://github.com/NixOS/nixpkgs/blob/master/pkgs/README.md)
  for package conventions, sources, patches, tests, updates and package review.
- [pkgs/by-name/README.md](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/README.md)
  for the preferred layout and its limitations.
- [maintainers/README.md](https://github.com/NixOS/nixpkgs/blob/master/maintainers/README.md)
  for maintainer responsibilities and adoption.
