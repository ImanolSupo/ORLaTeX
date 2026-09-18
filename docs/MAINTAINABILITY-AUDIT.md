# Maintainability audit

Baseline Commit 2 (`71a7fbc`), 2026-09-18. Ratings are internal qualitative
judgments, not statements that the maintainer has mastered the code. Tests below
are existing evidence locations, not proof of all publisher/engine compatibility.
`S` = `orlatex.sty`; `I` = `orlatex-input.code.tex`. Test names refer to
`testfiles/<name>.lvt`; visual files are under `examples/`.

| Subsystem / location | Complexity | Why / likely failures | Existing evidence | Simplification opportunity |
| --- | --- | --- | --- | --- |
| Loader: S header/tail, wrappers | LOW | Requires amsmath/input module; missing installed module or conflicting names. | Five alias regressions, `scripts/check_aliases.py` | Remove redundant wrappers after name decision. |
| Configuration/key system: S `__orlatex_apply_layer:`, `__orlatex_resolve_layer:`, `__orlatex_element_begin:nn` | MEDIUM | Defaults/setup/style/environment/row cascade; density precedence, style restrictions and grouping can leak or disagree. | `cascade`, `diagnostics`, `tags` | Reduce style/row overrides and margin keys if unsupported by manuscripts. |
| Seven-field record/storage: S `__orlatex_store:n`; I attach helper | MEDIUM | Unexpanded tokens, property-list snapshots and field order; accidental expansion, incorrect field replacement or stale row settings. | `semantics`, `input`, `sums` | Preserve one record path; document invariant, avoid extra domain fields. |
| Notation input adapters: S set/parameter collectors; I `\orvar`, `\orsetdef`, `\orfor` | MEDIUM | Context validation and last-record mutation; representation conflicts, duplicate domains, altered tokens. | `semantics`, `input`, `diagnostics` | One mixed block and literal variable path; review duplicate set helper. |
| Model body/row parser: I `__orlatex_input_model:n`, `__orlatex_input_row:n`, `__orlatex_input_scan:` | HIGH | Recursive token capture and dual syntax detection; macro-generated structure, groups/manual breaks, missing labels/domains, wrong objective classification. | `input-numbering`, `robustness`, `input` | Remove structured fallback; retain explicit top-level row boundary and grouped/raw escapes. |
| Membership scanner: I `__orlatex_input_domain:nN`, `__orlatex_domain_scan:`, `__orlatex_domain_clause:` | HIGH | Brace opacity, parenthesis depth and comma/membership delimiters; malformed tuples, unsupported raw syntax, accidental expansion. | `input`, `sums`, `robustness` | Keep bounded grammar and raw star; do not broaden arbitrary-math parsing. |
| `where` handling: I `__orlatex_sum_spec:nN` | MEDIUM | Space-delimited single filter with group opacity; repeated/empty keyword, misplaced membership or protected literal text. | `sums` | Native condition math/raw subscript already limits required grammar. |
| Summation scope: I `\orsum`, local `\Sum` binding | MEDIUM | Group-local scanner state must end before operator/summand; nested sums or alias restoration can break. | `sums`, `load-scope`, alias support | One operator implementation; preserve scoped alias and native `\sum` alternative. |
| Notation renderer: S `__orlatex_description_row:nnnnnnn`, `__orlatex_notation_output:nn` | HIGH | Single line, hanging prose and stacked/below-domain paths with boxes/paragraph settings; baselines, overflows, indentation and page-boundary failures. | `flow`, `fonts`, `robustness`, examples 10–12 | Remove unused overrides, retain independent rows; inspect real prose/math widths. |
| Model renderer: S `__orlatex_prepare_model:`, `__orlatex_model_row:nnnnnnn` | HIGH | Cached math boxes, multi-pass dimensions, title pagination and vtop/hbox composition; side effects evaluated twice, register reuse, inconsistent baselines/counters. | `tags`, `responsive`, `robustness`, `fonts`, examples 14–15, 19–22 | Preserve single renderer; simplify supported presentation variants before algorithms. |
| Domain measurement/layout: S `__orlatex_choose_domain:`, `__orlatex_fit_tagged_row:` | HIGH | Joint fit with marker/tag reserves and gap minima; a domain may stack or overflow incorrectly at narrow local widths. | `responsive`, `tags`, fixtures `responsive-model`, `tag-target` | Keep component placement, explicit breaks and warnings; no automatic scaling. |
| Equation-tag measurement/anchor: S `__orlatex_measure_columns:nnnnnnn`, `__orlatex_prepare_row:nnnnnnn`, `__orlatex_choose_tag_anchor:` | HIGH | Predicted tag widths, upper-middle extent/outlier cap, exact gaps and suppressed rows interact; counter-format transition or one long row can disturb all tags. | `tags`, `numbering`, `input-numbering`, examples 19–21 | Keep one auto strategy plus conventional right override; resist more heuristics. |
| Numbering/labels: S `__orlatex_model_numbering:`, `__orlatex_model_row:nnnnnnn`; I label/notag capture | HIGH | Grouped measurement must not create real labels/anchors; row/model/none and first unsuppressed row affect counters. | `numbering`, `input-numbering`, `tags`, `diagnostics` | Keep ordinary equation counter and labels; avoid a custom reference registry. |
| Lightweight public bindings: I environments | MEDIUM | Alias restoration and reserved literal markers; mixed input styles and macro-generated structure are limited. | `input`, `load-scope`, `sums` | Single documented input path and local short names. |
| Structured API: S typed/objective/constraint collectors and separate environments; I fallback | MEDIUM | Shared renderer but distinct semantic input contracts; implicit types, per-row metadata and two command sets create divergent diagnostics. | `semantics`, `cascade`, `diagnostics` plus shared tests | Postpone public adapter; retain only internals needed by lightweight path (API audit). |
| l3build regression workflow: `build.lua`, testfiles | MEDIUM | Three engines/two passes and normalized expected logs; platform font/log wrapping differences or casually regenerated expectations can mask regressions. | 18 tests, engine-specific diagnostic expectations | Preserve behavioral assertions; consolidate duplicate loader tests only after loader decision. |
| Visual fixtures/examples | MEDIUM | Shared sources, full/narrow/two-column widths and pagination need visual judgment; log-only checks can miss poor spacing. | `scripts/compile.py`, comparison sources, examples 05–07, 14–15, 19–22 | Curate representative fixtures; keep stress cases outside CTAN, add manuscript evidence later. |
| Manual extraction/build: `docs/orlatex.tex`, `scripts/check_manual.py`, `prepare_assets.py`, `build.lua` | MEDIUM | Verbatim/rendered/fixture duplication and source fingerprints; stale guide, missing dependency, newline-sensitive extraction/hash. | Extracted examples; fixture equality and asset checks | One source per example; reduce advanced sections and generated preview obligations. |
| Release scripts: `scripts/release.py`, `test_release.py`, `release.json`, manifest | MEDIUM | Broad extension-based inclusion and several consistency gates; unintended artifacts, stale fingerprints or inaccurate inventory. | Release-gate unit tests, extracted-install loader smoke | Separate minimal explicit CTAN file allowlist from repository packaging; no change here. |
| CI: `.github/workflows/ci.yml` | MEDIUM | Three-engine Ubuntu apt TeX Live jobs; installed distro age, platform line endings, missing diagnostics/dependencies can differ from MiKTeX. | Workflow runs regressions, examples, extraction and release gates | Verify actual hosted results; record exact TeX Live version, do not equate apt install with current TeX Live. |

## Evidence gaps and recorded risks

Manuscript necessity for structured-only metadata is not established. Train
fixtures are development evidence, not a demonstrated full manuscript workflow.
Current TeX Live validation and maintainer technical ownership remain remediation
work. No concrete runtime bug was established by this audit; risks above are
plausible failure modes, not claims of observed defects. Baseline asset fingerprints
are byte-sensitive across checkout line endings; the working tree already holds
a prospective fix, kept outside this commit. The historical local review describes
an older test count and is not suitable as present validation evidence.

## First personal study targets

| Target / source and important macros | Questions the maintainer should answer |
| --- | --- |
| Membership grammar — I `__orlatex_domain_scan:`, `__orlatex_domain_clause:`, `__orlatex_input_domain:nN` | Why does `(i,j) in A` avoid a clause split? What changes when `\for*` bypasses scanning, and how are groups/macros protected? |
| Model capture — I `__orlatex_input_model:n`, `__orlatex_input_row:n`, `__orlatex_input_scan:` | How are top-level `\\` distinguished from grouped aligned breaks? Why does a leading literal objective choose the input path, and what happens to `\label`/`\notag`? |
| Responsive domain fit — S `__orlatex_choose_domain:`, `__orlatex_fit_tagged_row:`, `__orlatex_prepare_row:nnnnnnn` | Which measured widths and minimum gaps force a domain below? Why is local `\linewidth` the basis, and how do exact author gaps differ from `auto`? |
| Tag anchor and reference safety — S `__orlatex_measure_columns:nnnnnnn`, `__orlatex_choose_tag_anchor:`, `__orlatex_model_row:nnnnnnn` | Why does one outlier not stretch all tags, including the special two-row case? How do suppressed rows and counter-sensitive math remain consistent between measurement and actual labels? |
| Regression diagnosis — `build.lua`, `testfiles/{input,tags,numbering,sums}.lvt` and expected `.tlg` | How does one run a failing test on all three engines and distinguish a platform log difference from behavior? What independent evidence is required before changing an expectation? |

## Commit 3 sanity validation

Commit 2 baseline: `l3build check` passed in an isolated HEAD export with MiKTeX
25.4 on Windows, 18 tests × pdftex/xetex/luatex × two passes (108 TeX passes).
Engines identify as MiKTeX-pdfTeX 4.21, MiKTeX-XeTeX 4.15 and LuaHBTeX 1.22.0.
The exact staged export must pass the same check before commit; runtime, build
configuration, regression inputs and expectations must be byte-identical to
Commit 2. Local TeX Live was not run; later validation must use current TeX Live.
