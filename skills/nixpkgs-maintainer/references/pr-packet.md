# PR packet

Prepare this packet before asking for a commit, push, or pull request. Re-read
the current upstream `CONTRIBUTING.md`, `pkgs/README.md`, and PR template because
their branch names, checkboxes, and automation policy can change.

```text
Package / attribute / path:
Primary + secondary task type:
Target repository / base branch / revision:

Changes:
- <minimal expression, metadata, test, or patch change>

Upstream:
- release/commit: <immutable ref>
- changelog/issue/PR: <link>
- license/platform/install evidence: <summary>

Failure or motivation:
- <reproduction or reason; label inference separately>

Validation:
- L0: <pass/fail/not run + command>
- L1: <pass/fail/not run + command/output>
- L2: <tests and result>
- L3: <binary smoke result>
- L4: <nixpkgs-review and affected dependents>
- L5: <real-world scenario or why not applicable>

Patch and maintenance:
- <source, reason, and removal condition>
- <maintainer/ownership or adoption decision>

Commit / PR:
- <current nixpkgs commit convention and proposed summary>
- <rebuild, release-note, and README impact>
- <responsible-person review and required AI/automation disclosure>

Next action:
- <one exact manual command or decision>
```

The upstream PR template currently asks for platforms, applicable tests,
`nixpkgs-review`, basic binary functionality, release notes, relevant README
conventions, and the automation/AI policy. Fill only what was actually run;
mark the rest as not applicable or not run with a reason.

For non-trivial LLM or automation output, the responsible contributor must
understand and review the change. Re-check the current automation/AI policy for
the required disclosure format; when it requires a commit trailer, use the
specified `Assisted-by:` form rather than treating `Co-authored-by:` as a
substitute. This skill prepares text but does not submit it.

Stop before `git commit`, `git push`, PR creation, force-push, maintainer/package
deletion, or other external mutation unless the user has explicitly authorized
that exact action.
