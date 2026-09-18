# Distribution and development-artifact audit

Baseline Commit 2: 113 tracked files (651,031 bytes), plus 25 modified files and
14 nonignored untracked files at audit start. `git ls-files`, status, top-level
listing, release selection and recursive artifact/path searches were inspected.
Destinations below describe the **future** distribution, not today's packaging.

| Top-level item / major directory | Classification | Future destination and reason |
| --- | --- | --- |
| `orlatex.sty`, `orlatex-input.code.tex` | RUNTIME | Both, under the chosen future name; handwritten runtime source. |
| `ormath.sty`, `ortex.sty` | REDUNDANT | Neither after a deliberate compatibility decision; preserve now. No CTAN installation needs loader migration. |
| `.github/` (4 tracked files) | DEVELOPMENT ONLY | GitHub: workflow, two issue templates, PR template. |
| `.editorconfig`, `.gitattributes`, `.gitignore` | DEVELOPMENT ONLY | GitHub: editor/Git settings. |
| `API-COMPARISON.md` | DEVELOPMENT ONLY | GitHub: evidence for adapter choice; consolidate if stale. |
| `ARCHITECTURE.md` | DEVELOPMENT ONLY | GitHub: implementation map; update after simplification. |
| `CHANGELOG.md` | USER DOCUMENTATION | Both: retain accurate release/development history. |
| `CITATION.md` | USER DOCUMENTATION | Both if needed; preferably merge short citation guidance into README. |
| `CONTRIBUTING.md` | DEVELOPMENT ONLY | GitHub: contributor workflow. |
| `DESIGN-NOTES.md` | DEVELOPMENT ONLY | GitHub: consolidate design decisions into architecture where duplicated. |
| `LICENSE`, `NOTICE.md` | SOURCE/BUILD | Both: license grant and maintenance/ownership notice. |
| `MANIFEST.txt` | SOURCE/BUILD | Both, with separately scoped inventories or an archive-only manifest; current repository inventory must not define CTAN scope. |
| `README.md` | USER DOCUMENTATION | Both: concise purpose, installation, usage, license and maintainer contact. |
| `RELEASE-CHECKLIST.md` | DEVELOPMENT ONLY | GitHub: consolidate release procedure. |
| `RELEASE-NOTES.md` | REDUNDANT | Neither as a separate file after merging relevant facts into changelog. |
| `TEST-RESULTS.md` | DEVELOPMENT ONLY | GitHub: concise evidence, not sprawling execution history. |
| `build.lua` | SOURCE/BUILD | GitHub; include in CTAN only if necessary for the retained user-document build. Current configuration also drives regressions. |
| `release.json` | SOURCE/BUILD | GitHub: release-tool metadata; public version/license facts also live in runtime/README. |
| `docs/` (5 tracked before these audits) | USER DOCUMENTATION / DEVELOPMENT ONLY / GENERATED | Split: manual `.tex`/`.pdf` in both; required manual fixtures also in both. Preview source/image and `assets.json` for GitHub build/README. These six audit documents are GitHub only. |
| `examples/` (35 tracked; 7 untracked) | USER DOCUMENTATION / TEST | GitHub retains useful cases; CTAN gets only 2–4 self-contained examples and essential manual fixtures. Comparison triplicates/stress cases stay on GitHub. |
| `scripts/` (8 tracked) | SOURCE/BUILD / DEVELOPMENT ONLY | GitHub: compile, extraction, comparison, asset, loader and release tools. CTAN only a minimal build helper if the manual cannot otherwise be rebuilt. |
| `testfiles/` (39 tracked; 6 untracked) | TEST | GitHub: 18 baseline `.lvt`, expectations including engine variants, one support source; exclude from ordinary CTAN archive. |
| `docs/MODEL-TYPOGRAPHY-BENCHMARK.md` (untracked) | DEVELOPMENT ONLY | GitHub if curated as evidence; CTAN excluded. |
| `LOCAL-REVIEW.md` (ignored) | DEVELOPMENT ONLY | Neither: historical local report; not current release evidence. |
| `build/`, `output/`, `tmp/` (ignored) | GENERATED / DEVELOPMENT ONLY | Neither: logs, compiled examples, release bundles, scratch snapshots, patches and local reports. |
| `.ocs/` (ignored) | GENERATED | Neither: local PDF output. |
| `.git/` | DEVELOPMENT ONLY | Neither in any file archive: Git's own metadata/history transport. |
| Nested `__pycache__/`, `*.pyc` (ignored) | GENERATED | Neither: Python caches. |

The existing release tool includes editor files, `.github/`, every permitted
example/test/script, and many engineering reports: it packages a development
repository rather than a minimal user distribution. Its directory selection is
extension-based, not an explicit per-file CTAN allowlist. The uncommitted change
to admit all `docs/*.md` would widen it further. Commit 3 changes neither tool nor
manifest. A future CTAN allowlist must explicitly select required source/manual
dependencies and exclude development artifacts regardless of Git tracking state.

## Artifact findings

| Finding | Tracking state | GitHub? | CTAN? |
| --- | --- | --- | --- |
| `AGENTS.md`, `agent.md`, `CLAUDE.md`, `CODEX.md`, `.claude/`, `.codex/`, `.cursor/`, prompt/task/chat transcript names | None found in this repository, including ignored-name search. | No accidental addition identified. | Exclude any future local copies. |
| Architecture, design, API comparison, test/release reports and new benchmark | Existing tracked reports; benchmark untracked | Yes if maintained and concise; names do not establish authorship/provenance. | Exclude engineering/process reports. |
| `LOCAL-REVIEW.md` | Untracked and ignored | No | Must exclude. |
| `tmp/commit1-{postcommit,staged}.patch`, `tmp/commit2-{postcommit,staged}.patch`, `tmp/pre-commit{1,2,3}-full.patch` | Untracked and ignored | No | Must exclude; retained as local preservation evidence. |
| Local logs/reports/scripts/snapshots under `tmp/`; PDFs/logs under `output/`, `build/`, `.ocs/` | Untracked and ignored | No | Must exclude; no deletion needed. |
| Literal user-home paths (`C:\Users\`, `/home/`) | No hits in tracked/nonignored untracked text; 120 matching ignored files: 107 output, 1 build, 12 tmp (scan before writing these audits). | Generated local evidence only; do not publish. | Must exclude generated files. |

No history rewrite or cleanup is authorized by these findings. The full initial
tracked diff, status and content hashes are retained in ignored `tmp/pre-commit3-*`;
hash verification covers existing tracked and nonignored untracked files.

## Simplification estimates (not quotas)

| Measure | Current | Plausible future |
| --- | --- | --- |
| Tracked repository files | 113 before Commit 3; 119 after six audit files | About 85–105, depending on consolidation, retained experiments and shared regression coverage. |
| Runtime files | 4: main style, input module, two wrappers | 2 (one loader/implementation plus input module); 1 only if consolidation improves readability. |
| CTAN archive files | Existing selector covers 113 baseline files plus generated `MANIFEST.json` | About 12–18: 2 runtime, README/license/notice/changelog/manifest, manual source/PDF, 2–4 examples and 1–3 essential manual/build dependencies. |
| CTAN payload size | Baseline repository payload about 636 KiB | Roughly 430–550 KiB unpacked / 300–400 KiB ZIP, dominated by the manual PDF. An illustrative 10-file subset is 435,928 bytes before required fixtures and new naming. |

These estimates assume a rebuilt concise manual and removal of redundant loaders;
they are not a packaging implementation or a reason to discard valuable tests.
