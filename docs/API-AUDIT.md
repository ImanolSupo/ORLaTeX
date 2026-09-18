# Public API audit

Baseline: Commit 2 (`71a7fbc`), inspected in `orlatex.sty` (907 lines),
`orlatex-input.code.tex` (289 lines), and both seven-line wrappers.
Classification is a recommendation; every current API remains unchanged.
CORE = scope essential; JUSTIFIED ADVANCED = bounded author control;
QUESTIONABLE = evidence/cost review; REDUNDANT = duplicate interface;
INTERNAL-CANDIDATE = useful mechanism without a demonstrated public need;
REMOVE-CANDIDATE = postpone or remove from the first release.

## Commands, environments and loaders

| Public item | Actual baseline behavior / signature | Class and reason |
| --- | --- | --- |
| `ornotation[options]` | Mixed notation collection; locally binds `\set`, `\setdef`, `\param`, `\var`, `\for`. | CORE: single notation entry point. |
| `\set[options]{symbol}{description}` / `\orset` | Identical set collector; representations are mutually exclusive. | CORE: set definitions; namespaced spelling prevents short-name dependence. |
| `\setdef{symbol}{definition}{description}` / `\orsetdef` | Calls `\orset[definition=...]`; short spelling only in `ornotation`. | REDUNDANT: convenient duplicate of one key. |
| `\param[options]{math}{description}` / `\orparameter` | Literal parameter collector; short spelling in `ornotation`. | CORE: parameter notation. |
| `\var[options]{complete math}{description}` / `\orvar` | Literal variable collector; only top-level `>=`, `<=` normalized; **no generated type**. | CORE: ordinary variable declarations. |
| `\for{memberships}`, `\for*{raw math}` / `\orfor`, `\orfor*` | Trailing domain attaches to previous record; lightweight model parser captures it per row. Short binding in `ornotation` and `ormodel`; namespaced command requires an active package environment and preceding record. | CORE: explicit index-domain helper and raw escape. |
| `ormodel[options]` | Body capture; literal leading `\minimize`/`\maximize` selects lightweight mode, otherwise executes structured collection. Locally binds all model short commands. | CORE: model layout; dual dispatch is a simplification candidate. |
| `\minimize`, `\maximize` | Argumentless literal objective markers at the start of a lightweight model/row. | CORE: objective direction. |
| `\st` | Optional leading constraint marker after the objective. | CORE: model readability. |
| `\subjectto` | Local alias for `\st`. | REDUNDANT: second spelling. |
| `\Sum{spec}`, `\Sum*{raw subscript}` | Local alias for `\orsum` throughout `ormodel`, including structured bodies. | CORE: compact optional helper; external meanings restored on exit. |
| `\orsum{spec}`, `\orsum*{raw subscript}` | Global mathematical operator; one native `\sum` per call, summand follows as ordinary math. | CORE: scoped implementation also usable in ordinary mathematics. |
| `\orlatexsetup{keys}` | Group-scoped setup layer, parsed through configuration keys. | CORE: document defaults. |
| `\orlatexstyle{name}{visual keys}` and `style=name` | User-defined named styles; no shipped named styles; nested `style=` forbidden. | QUESTIONABLE: extra cascade and validation; retain publicly only with manuscript need. |
| `orsets`, `orparameters`, `orvariables` (all `[options]`) | Separate structured blocks bind `\set`, `\parameter`, `\variable` respectively. | REMOVE-CANDIDATE: mixed notation covers ordinary use. |
| `\parameter[options]{math}{description}` | Local structured alias for `\orparameter` in `orparameters`. | REDUNDANT: duplicate of `\param`. |
| `\variable[options]{symbol}{description}` / `\orvariable` | Structured variable collector, implicit `type=continuous`; short binding in `orvariables`; namespaced collector also allowed in mixed notation. | REMOVE-CANDIDATE: implicit domain semantics and second variable path. |
| `\objective[min or max,keys]{math}` / `\orobjective` | Structured objective, default `min`; exactly one sense and one objective required. Short binding in `ormodel`. | REMOVE-CANDIDATE: alternative model syntax. |
| `\constraint[keys]{math}` / `\orconstraint` | Structured constraint with per-row keys; short binding in `ormodel`. | REMOVE-CANDIDATE: alternative model syntax. |
| `orlatex.sty` | Canonical loader; LaTeX format minimum 2022-06-01; requires amsmath and input module. | CORE: current runtime entry point, future name undecided. |
| `ormath.sty`, `ortex.sty` | Thin compatibility loaders requiring `orlatex`; no separate functionality. | REMOVE-CANDIDATE: two extra names for a package never installed on CTAN. |
| `\label{...}`, `\ref{...}`, `\eqref{...}`, `\notag` | Existing LaTeX/amsmath commands, not new public definitions. Parser captures row label/notag; refs use ordinary labels. Row labels require `numbering=rows`; `\notag` rejects model numbering. | CORE: standard reference integration. |
| Top-level `\\`, grouped math breaks, `in`, `>=`, `<=`, single summation `where` | Explicit row separators and bounded literal token conventions; brace groups/macros remain opaque. `where` applies only to summation specifications. | JUSTIFIED ADVANCED: documented convenience, raw/native escapes retained. |

The global namespaced collectors check context, rather than creating standalone
notation. Short commands are local aliases/markers, not globally installed APIs.
No runtime `\DeclareOption`/`\ProcessOptions` interface exists: keys are passed
to setup/styles/environments/declarations, not as package-loading options.

## Every public key family

Config keys are accepted by setup, named styles and environments. Declaration
keys are narrower; inherited visual keys are explicitly listed below.

| Key and accepted values | Scope | Class and reason |
| --- | --- | --- |
| `layout=auto,wide,stacked` | Config | CORE (`auto`); JUSTIFIED ADVANCED (overrides): author-directed component layout. |
| `density=relaxed,normal,compact,dense` | Config; presets, not named styles | CORE: bounded spacing presets; explicit same-layer keys win. |
| `font-size=auto,normal,small,footnotesize,scriptsize` | Config, element | JUSTIFIED ADVANCED: explicit selection; `auto` inherits, never shrinks to fit. |
| `numbering=rows,model,none` | Config | CORE: standard equation reference modes. |
| `domain-position=auto,right,below` | Config, element | CORE/ JUSTIFIED ADVANCED: local placement and overrides; oversize math can still warn. |
| `domain-gap=auto` or nonnegative dimension | Config, element | CORE/ JUSTIFIED ADVANCED: density-based notation gap, bounded model gap or exact override. |
| `domain-separator={math tokens}` (default `;`, empty allowed) | Config, element | JUSTIFIED ADVANCED: model expression/domain punctuation. |
| `tag-gap=auto` or nonnegative dimension | Config, element | CORE/ JUSTIFIED ADVANCED: responsive or exact tag separation. |
| `tag-position=auto,right` | Config, element | CORE/ JUSTIFIED ADVANCED: responsive anchor or conventional right placement. |
| `row-gap`, `space-before`, `space-after` (nonnegative dimensions) | Config; only `row-gap` also element | JUSTIFIED ADVANCED: ordinary vertical spacing. |
| `extend-left`, `extend-right` (nonnegative dimensions) | Config | REMOVE-CANDIDATE: explicit margin invasion conflicts with narrow local-width purpose. |
| `subject-to={text}` | Config | JUSTIFIED ADVANCED: conventional marker wording. |
| `style={name}` | Config, element | QUESTIONABLE: named-style cascade; element styles only permit consumed row visual keys. |
| `title={text}` | Environment | JUSTIFIED ADVANCED: heading kept with first row. |
| `label={name}` | Environment, element | CORE: environment model label; element row label; notation labels are rejected when rendered. |
| `for={raw index math}` | Element (therefore all declaration families) | REDUNDANT: key alternative to trailing `\for*`; no membership normalization here. |
| `size={n}`, `elements={math list}`, `definition={math}` | Set plus element keys | JUSTIFIED ADVANCED: explicit set construction; only one nonempty representation allowed. |
| `type=continuous,nonnegative,integer,binary` | Structured variable plus element keys | REMOVE-CANDIDATE: generated domain can be written as ordinary math. Not accepted by baseline `\var`. |
| Bare `min`, `max` | Structured objective plus element keys | REMOVE-CANDIDATE: alternative objective direction keys. |

Element visual keys: `font-size`, `row-gap`, `domain-gap`, `domain-separator`,
`domain-position`, `tag-gap`, `tag-position`, `style`. Set/variable/objective
families inherit this exact list plus `for` and `label`. Parameter, literal
variable and constraint use the element family directly. Unknown keys diagnose.
`suppress-tag` is private stored metadata (INTERNAL-CANDIDATE), not an accepted
public key. Bare variable type keys and custom `domain=` are uncommitted
experiments, absent from this baseline. No additional public keys were found.

## Structured API decision

**D. POSTPONE/REMOVE FROM FIRST PUBLIC RELEASE**, to be implemented in Commit 5.

| Question | Evidence / consequence |
| --- | --- |
| What problem does it solve? | Separate notation sections, typed-variable construction, explicit row metadata/style overrides, and command-assembled model rows. |
| Does lightweight cover it? | Mixed notation, complete variable math, row labels/notag and trailing domains cover ordinary manuscripts. Per-row visual overrides and macro-assembled rows are not fully equivalent; no real manuscript requiring them is established by the supplied evidence. |
| Runtime cost? | About 60–90 directly associated lines (typed variable/objective/constraint collectors, dedicated keys, separate environments/bindings and fallback dispatch) out of 1,210 runtime lines. Shared set/parameter collectors, element keys, records and renderers cannot simply be removed. This is a source-span estimate, not a measured deletion patch. |
| Test/document cost? | 10 of 18 `.lvt` files, 13 of 35 example/fixture sources and the manual reference structured declarations/environments (literal source scan). These contain mixed/shared coverage, not 10 disposable tests. The advanced manual section has one executable verbatim block plus rendered duplication. |
| Second semantic path? | Yes at input: implicit continuous type, raw `for=` and explicit metadata vs literal variable math and parsed domains. Both feed the same seven-field records and renderers; there is no second layout engine. |
| Real need and simplification? | Repository demonstrations/comparisons are not manuscript validation. Postponement reduces public contracts, implicit type semantics and dual dispatch, though most measured-layout complexity remains. Reconsider a reduced subset only when manuscript evidence justifies it. |
