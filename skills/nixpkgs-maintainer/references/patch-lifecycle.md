# Patch lifecycle

Every non-trivial patch must have a source, a reason, and a removal condition.
Use this priority order:

1. The current upstream release already contains the fix: remove the patch.
2. Upstream merged a stable commit that is not released yet: backport that
   immutable commit and record the next release or commit that removes it.
3. Upstream has only an open pull request: use it only when the failure and
   proposed fix are clear, the source is immutable, and the risk is accepted;
   prefer a stable commit whenever possible.
4. The behavior is Nixpkgs-specific: keep a small local patch with a reason and
   a condition for reevaluation.
5. A workaround or hack is a last resort. Explain the known ceiling and the
   experiment that can replace it.

Record each patch in the evidence ledger or code comment:

```text
patch: <name or file>
source: <upstream URL and immutable commit/PR>
reason: <first failing boundary and why this patch fixes it>
introduced: <nixpkgs revision or package version>
remove when: <release/commit or condition>
validation: <levels and platforms run>
```

When updating a package, actively check whether every existing patch has landed
upstream. Remove obsolete patches instead of carrying them forward. If a patch
changes generated files, dependencies, or tests, re-check the upstream source
and lock data before assuming it still applies.

Do not fetch mutable branches, tags that can be retargeted, or an unexplained
commit. Do not hide an unresolved patch conflict with `postPatch` substitutions,
an override, or disabled tests.
