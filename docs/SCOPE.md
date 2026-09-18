# Future package scope

Decision recorded 2026-09-18. This is a future release boundary, not an API change.
The code baseline for these audits is Commit 2,
`71a7fbcbe7a731779e042c711eb6677354694217`; later working-tree experiments are
preserved separately. Existing guides may still describe the broader prototype.

## Purpose

Lightweight, width-aware typesetting of mathematical optimization notation and
models while preserving ordinary LaTeX mathematics. Authors supply the mathematics
and explicit breaks; the package arranges measured components within local width.

## Core

- One mixed notation block for sets, parameters and literal variable declarations.
- One lightweight model environment with a minimization/maximization objective
  and explicitly separated constraint rows.
- Local width-aware placement of index domains, with explicit author overrides.
- Responsive equation-tag placement and a conventional right-position override.
- Small optional helpers: membership `\for` and indexed `\Sum`, including raw
  starred escapes; native LaTeX remains usable.
- Standard `\label`, `\ref`, `\eqref` and row `\notag`, respecting numbering mode.

## Boundaries

No solver, symbolic algebra, mathematical-correctness checking, semantic inference,
complete modeling DSL, natural-language parser, or replacement for amsmath.
No automatic font shrinking, margin invasion, or rewriting of arbitrary math.
The current bounded `in`, `>=`, `<=` and summation `where` conveniences are
explicit input adapters, not general mathematical interpretation.

Postpone the public structured adapter for the first release (see
[API recommendation](API-AUDIT.md#structured-api-decision)). Review redundant
loaders, implicit variable types and margin-extension keys for removal. Preserve
useful shared internals; do not expand scope merely to retain a prototype feature.

## Feature freeze

Feature development is temporarily frozen until CTAN remediation is complete.
New public syntax needs a recorded justification: a real bug, compatibility,
actual manuscript usage, or implementation simplification. An exception is not
automatic approval; assess its maintenance cost and existing LaTeX alternatives.

`\var[domain={[0,M]}]{t_i}{...}` is **not approved**. Bounded time variables have
a genuine train-model use case, but the syntax decision awaits manuscript evidence.
Existing uncommitted custom-domain/type code and train fixtures remain intact and
outside Commit 3. No rename, API removal, new syntax, CTAN submission or release
is performed here. Commit 4 requires the maintainer's explicit name choice;
implementation simplification belongs to Commit 5.
