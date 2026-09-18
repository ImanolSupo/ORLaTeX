# CTAN review notes

Recorded 2026-09-18 from the maintainer's supplied review summary. The rejected
submission was `orlatex` 0.1.0; it was never installed as a CTAN package.

| Review point | Required response |
| --- | --- |
| `orlatex` is unacceptable as a new package id because of its `tex` suffix. | Research a purpose-related id; choose it explicitly before renaming. |
| A substantially revised package may be submitted under an acceptable new name. | Complete remediation before considering another submission. |
| Simplify the distribution. | Separate the repository from a small, explicitly allowlisted CTAN archive. |
| Test current TeX Live and MiKTeX. | Obtain evidence from both distributions; one distribution with three engines is insufficient. |
| Gain experience in actual manuscripts. | Record manuscript needs, failures and author interventions; demonstration fixtures alone do not establish this. |
| The maintainer must understand, diagnose, modify and maintain the implementation. | Personally study parser, measurement/layout, LaTeX internals, regression tests and bug-report workflows. |

These are technical maintenance obligations. This record makes no claim about
reviewer motives, general CTAN policy on AI, implementation provenance, or the
maintainer's present mastery.

Commit 3 defines scope and records audits only. [Scope](SCOPE.md),
[API](API-AUDIT.md), [distribution](DISTRIBUTION-AUDIT.md),
[names and landscape](NAME-CANDIDATES.md), and
[maintenance](MAINTAINABILITY-AUDIT.md) provide the decisions and evidence.
