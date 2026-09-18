# Name candidates and package landscape

Research date: 2026-09-18. **No name selected.** Display names are proposals;
Commit 4 requires an explicit maintainer choice and fresh collision checks.

## Official naming guidance

The current [CTAN upload addendum](https://ctan.org/file/help/ctan/CTAN-upload-addendum)
requires lowercase ids, no initial digit, and portable filenames; it recommends
at least four characters. Hyphens are preferred over underscores. `l3` and
`ltx-` prefixes are reserved for the LaTeX Project. Third-party expl3 packages
may use `lt3...`, but need not. Avoid `tex` suffixes, author-based names and
cryptic ids; communicate purpose. Display-name case variants are accepted, with
matching id/name preferred. Package ids uniquely identify catalogue entries;
runtime filenames should be unique, including case-insensitive comparisons.
The [upload guide](https://ctan.org/help/upload-pkg) favors a browsing-friendly
flat package directory for small distributions, a README and user documentation.

## Collision method and ORmath assessment

Queried the official [complete catalogue](https://ctan.org/json/2.0/packages),
`https://ctan.org/json/2.0/pkg/<id>` for all eleven ids below, and
`https://ctan.org/search?ext=false&FILES=on&phrase=<id>.sty` for every candidate.
Every candidate API lookup returned HTTP 404 with `Not found`; every file search
returned HTTP 200 with no matching documents. The full catalogue likewise has
none of these ids. General CTAN search for `ormath` returned no matches; web
searches for `ormath` with LaTeX/TeX and exact `ormath.sty` exposed no obvious
external TeX collision. These are dated negative checks, not name reservations.

`ormath` is provisionally viable: six lowercase letters, no reserved prefix or
`tex` suffix. `ORmath` suggests Operations Research mathematics to an informed
reader, but OR is ambiguous and “math” is broad; the name alone does not communicate
optimization-model typesetting. Always pair it with an explicit subtitle.
There **is already a local `ormath.sty` compatibility loader** in this project;
it is not an external collision and must be reconciled deliberately in a future
rename. No unrelated mathematical package with this exact id was found.
An additional attempt to read TeX Live's SVN `ls-R` failed TLS negotiation:
independent complete TeX Live filename validation remains unverified. CTAN
catalogue/file searches and web searches do not cover private or pending packages.

## Finalists

For every finalist, CTAN collision = none found in the dated catalogue/API
checks; external filename collision = none found in official CTAN file search.

| Package id | Display name | Meaning / strengths | Risks or confusion / filename qualification |
| --- | --- | --- | --- |
| `ormath` | ORmath | Operations Research mathematics; maintainer's strong preference, compact, covers notation and models. | Broad “math”, ambiguous OR; needs “Optimization notation and model typesetting” subtitle; project's own alias exists. |
| `optnotation` | OptNotation | Optimization notation; descriptive and emphasizes writing mathematics. | Model layout not explicit; “opt” can mean optional/optical; `optnotation.sty` not found externally or locally. |
| `optmodel` | OptModel | Optimization model notation/layout; concise recognizable subject. | Can sound like a solver/modeling system; subtitle must say typesetting; `optmodel.sty` not found externally or locally. |
| `optlayout` | OptLayout | Layout for optimization mathematics; directly signals typography. | Can mean optimizing page layout; notation declarations underrepresented; `optlayout.sty` not found externally or locally. |
| `or-notation` | OR Notation | Operations Research notation; descriptive alternative to ORmath. | OR abbreviation remains ambiguous; less direct about models; `or-notation.sty` not found externally or locally. |

## Ten alternatives considered

| Id | Assessment (same dated negative CTAN id/file checks) |
| --- | --- |
| `optnotation`, `optmodel`, `optlayout`, `or-notation` | Finalists above. |
| `optimodel` | Optimization models, but contraction is less readable and sounds like a modeling application. |
| `optmath` | Too broad; weaker purpose signal than `optnotation`. |
| `or-model` | Operations Research model; ambiguous abbreviation and solver implication. |
| `mathopt` | Mathematical optimization; reads like an optimization software library, not a typesetting tool. |
| `optform` | Optimization formulations; can mean web forms or general formatting. |
| `mpnotation` | Mathematical-programming notation; MP is cryptic and also evokes unrelated TeX tooling. |

No candidate ends in `tex`. There is lexical proximity to `optidef` among `opt...`
names, but no identity or compatibility claim; avoid a name/subtitle implying an
extension or replacement of that package.

## Relevant existing packages

This is a limited primary-source landscape review, not a ranking or novelty claim.
“Not documented” means the reviewed sources establish no such feature, not a
proof that every version or user extension lacks it. Syntax examples below are
short interface identifiers, not quotations of manuals.

| Package / source | Main function and syntax | Notation definitions | Width response / numbering / domains | Scope implication and naming risk |
| --- | --- | --- | --- | --- |
| [optidef](https://ctan.org/pkg/optidef), [v3.1 manual](https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/optidef/optidef.pdf) | Optimization displays; `mini`, `maxi`, `argmini`, `argmaxi` families with objective arguments and `\addConstraint{lhs}{rhs}`; an optional third braced component supplies extra aligned material. | No set/parameter/variable description blocks documented; variable argument identifies optimization variables. | Aligned constraint layouts; whole-model, individual-equation or no references; optional extra alignment and explicit objective/page breaks. Local measured domain relocation/shared compact responsive tag anchor are not documented in the reviewed manual. | Considerable overlap in model display and references. A defensible focus is mixed notation plus measured local component placement, pending manuscripts. Similar `opt...` names need clear descriptions. |
| [multiobjective](https://ctan.org/pkg/multiobjective) | Operators for multiobjective optimization and multicriteria work; mathematical operator macros rather than model row environments. | Specialized mathematical symbols, not description blocks. | Responsive model layout, model numbering and index-domain placement not established by catalogue description. | Related subject, different task. Avoid implying provision of a multiobjective operator vocabulary. |
| [amsmath](https://ctan.org/pkg/amsmath), [mathtools](https://ctan.org/pkg/mathtools) | General math displays (`align`, `aligned`), explicit alignment/breaks; mathtools adds symbols, display building blocks and tag controls. | Not dedicated optimization notation declarations. | General equation numbering/references and author-arranged domains; reviewed catalogue documents no optimization-specific local domain/tag fitting. | Foundation and alternative for manual author control, not something this package replaces. Broad “math” names risk implying similar breadth. |
| [breqn](https://ctan.org/pkg/breqn) | Automatic displayed-equation line breaking (`dmath` family), with supporting formula-processing changes. | No optimization notation blocks established by catalogue. | Width-sensitive formula breaking, unlike the proposed component-placement scope; detailed model/domain numbering not evaluated here. | Automatic arbitrary formula rewriting/breaking stays outside this package's scope. |
| [nomencl](https://ctan.org/pkg/nomencl), [author repository](https://github.com/borisveytsman/nomencl) | Symbol lists using `\nomenclature{symbol}{description}` and MakeIndex. | Yes: general symbol/description lists, not typed optimization declarations. | Not a model renderer; optimization domains/equation tags not established by catalogue. | Description-list overlap makes a clear optimization/local-layout purpose necessary. No exact candidate-name collision found. |
