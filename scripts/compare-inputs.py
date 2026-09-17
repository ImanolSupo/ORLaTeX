# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Generate equivalent local comparison fixtures and count their actual source.

Run with --write-fixtures after intentional model changes. Otherwise read the
checked-in fixtures; report character and token counts, never estimated savings.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'examples' / 'comparison'

# kind, mathematical declaration, prose, index domain
MODELS = {
    'bin-packing': ([
        ('set', 'I', 'Items', ''), ('set', 'B', 'Candidate bins', ''),
        ('param', r'w_i', 'Item weight', r'i\in I'),
        ('param', 'C', 'Bin capacity', ''),
        ('var', r'x_{ib}\in\{0,1\}', 'Assignment', r'i\in I,b\in B'),
        ('var', r'y_b\in\{0,1\}', 'Bin used', r'b\in B'),
    ], [
        r'\sum_{b\in B}y_b',
        (r'\sum_{b\in B}x_{ib}=1', r'i\in I'),
        (r'\sum_{i\in I}w_i x_{ib}\leq C y_b', r'b\in B'),
        (r'x_{ib}\in\{0,1\}', r'i\in I,b\in B'),
        (r'y_b\in\{0,1\}', r'b\in B'),
    ]),
    'facility-location': ([
        ('set', 'I', 'Customers', ''), ('set', 'J', 'Candidate facilities', ''),
        ('param', r'd_i', 'Demand', r'i\in I'),
        ('param', r'c_{ij}', 'Service cost', r'i\in I,j\in J'),
        ('param', r'f_j,U_j', 'Opening cost and capacity', r'j\in J'),
        ('var', r'x_{ij}\geq0', 'Quantity served', r'i\in I,j\in J'),
        ('var', r'y_j\in\{0,1\}', 'Facility opened', r'j\in J'),
    ], [
        r'\sum_{j\in J}f_j y_j+\sum_{i\in I,j\in J}c_{ij}x_{ij}',
        (r'\sum_{j\in J}x_{ij}=d_i', r'i\in I'),
        (r'\sum_{i\in I}x_{ij}\leq U_j y_j', r'j\in J'),
        (r'x_{ij}\geq0', r'i\in I,j\in J'),
        (r'y_j\in\{0,1\}', r'j\in J'),
    ]),
    'planning': ([
        ('set', 'J', 'Jobs', ''), ('set', 'T', 'Periods', ''),
        ('param', r'd_{jt}', 'Demand', r'j\in J,t\in T'),
        ('param', r'c_{jt},f_{jt},h_{jt}', 'Production, setup, and holding costs', r'j\in J,t\in T'),
        ('param', r'B_t', 'Shared capacity', r't\in T'),
        ('param', r'a_j,U_{jt},S_j', 'Resource use, production bound, and storage capacity', r'j\in J,t\in T'),
        ('param', r's_j^{\mathrm{init}},s_j^{\mathrm{target}}', 'Initial inventory and required final inventory', r'j\in J'),
        ('param', r'q_{ijt}', 'Shipment cost', r'i\in J,j\in J,t\in T'),
        ('var', r'x_{jt}\geq0', 'Production', r'j\in J,t\in T'),
        ('var', r's_{jt}\geq0', 'Ending inventory', r'j\in J,t\in T'),
        ('var', r'z_{ijt}\in\mathrm Z', 'Shipment quantity', r'i\in J,j\in J,t\in T'),
        ('var', r'y_{jt}\in\{0,1\}', 'Setup indicator', r'j\in J,t\in T'),
    ], [
        r'{\sum_{j\in J,t\in T}(c_{jt}x_{jt}+f_{jt}y_{jt}+h_{jt}s_{jt})'
        r'\\{}+\sum_{i\in J,j\in J,t\in T}q_{ijt}z_{ijt}}',
        (r'x_{jt}+s_{j,t-1}-s_{jt}=d_{jt}', r'j\in J,t\in T'),
        (r'x_{jt}\leq U_{jt}y_{jt}', r'j\in J,t\in T'),
        (r'\sum_{j\in J}a_j x_{jt}\leq B_t', r't\in T'),
        (r's_{jt}\leq S_j', r'j\in J,t\in T'),
        (r's_{j0}=s_j^{\mathrm{init}}', r'j\in J'),
        (r's_{jT}\geq s_j^{\mathrm{target}}', r'j\in J'),
        (r'\sum_{i\in J}z_{ijt}\leq d_{jt}', r'j\in J,t\in T'),
        (r'z_{ijt}\leq U_{it}y_{it}', r'i\in J,j\in J,t\in T'),
        (r'x_{jt},s_{jt}\geq0', r'j\in J,t\in T'),
        (r'z_{ijt}\in\mathrm Z', r'i\in J,j\in J,t\in T'),
        (r'y_{jt}\in\{0,1\}', r'j\in J,t\in T'),
    ]),
}

def easy_math(s):
    return s.replace(r'\geq', '>=').replace(r'\leq', '<=')

def easy_domain(s):
    return s.replace(r'\in ', ' in ')

def notation(rows, syntax):
    out = []
    if syntax == 'light':
        out.append(r'\begin{ornotation}')
        for kind, math, prose, domain in rows:
            line = rf'  \{kind}{{{easy_math(math)}}}{{{prose}}}'
            if domain:
                line += rf'\for{{{easy_domain(domain)}}}'
            out.append(line)
        out.append(r'\end{ornotation}')
    elif syntax == 'structured':
        for kind, env, cmd in [('set','orsets','set'), ('param','orparameters','parameter'), ('var','orvariables','variable')]:
            out.append(rf'\begin{{{env}}}')
            for k, math, prose, domain in rows:
                if k != kind:
                    continue
                options = []
                if kind == 'var':
                    for suffix, variable_type in [(r'\geq0', 'nonnegative'),
                                                  (r'\in\{0,1\}', 'binary'),
                                                  (r'\in\mathrm Z', 'integer')]:
                        if math.endswith(suffix):
                            math = math[:-len(suffix)]
                            options.append(f'type={variable_type}')
                            break
                if domain:
                    options.append(f'for={{{domain}}}')
                actual_cmd = cmd
                opt = f'[{",".join(options)}]' if options else ''
                out.append(rf'  \{actual_cmd}{opt}{{{math}}}{{{prose}}}')
            out.append(rf'\end{{{env}}}')
    else:
        for _, math, prose, domain in rows:
            tail = rf' $\forall\,{domain}$' if domain else ''
            out.append(rf'\noindent ${math}$: {prose}{tail}\par')
    return '\n'.join(out)

def model(rows, syntax, key):
    out = [rf'\begin{{{"align" if syntax == "raw" else "ormodel"}}}']
    for i, entry in enumerate(rows):
        math, domain = (entry, '') if i == 0 else entry
        label = f'{key}:{i}'
        if syntax == 'light':
            prefix = r'\minimize ' if i == 0 else (r'\st ' if i == 1 else '')
            tail = rf' \for{{{easy_domain(domain)}}}' if domain else ''
            line = '  ' + prefix + easy_math(math) + tail + rf' \label{{{label}}}'
        elif syntax == 'structured':
            opt = f'{"min," if i == 0 else ""}label={label}'
            if domain:
                opt += f',for={{{domain}}}'
            line = rf'  \{"objective" if i == 0 else "constraint"}[{opt}]{{{math}}}'
        else:
            prefix = r'\min\quad &' if i == 0 else (r'\text{s.t.}\quad &' if i == 1 else '&')
            # Explicit nested aligned is necessary for a multiline objective.
            if r'\\' in math:
                math = rf'\begin{{aligned}}{math[1:-1]}\end{{aligned}}'
            tail = rf' &&\forall\,{domain}' if domain else ' &&'
            line = '  ' + prefix + math + tail + rf' \label{{{label}}}'
        if syntax != 'structured' and i + 1 < len(rows):
            line += r' \\'
        out.append(line)
    out.append(rf'\end{{{"align" if syntax == "raw" else "ormodel"}}}')
    return '\n'.join(out)

if '--write-fixtures' in sys.argv:
    TARGET.mkdir(parents=True, exist_ok=True)
    for name, (defs, rows) in MODELS.items():
        for syntax in ['raw', 'structured', 'light']:
            (TARGET / f'{name}-{syntax}.tex').write_text(
                '% Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.\n'
                '% See NOTICE.md and MANIFEST.txt for work scope and maintenance.\n\n'
                + notation(defs, syntax) + '\n' + model(rows, syntax, name) + '\n', encoding='utf-8')

header = '| Model | Input | Characters | Structural commands | Braces | Option brackets | Alignment tokens | Lines |'
report = [header, '|---|---|---:|---:|---:|---:|---:|---:|']
structural = r'\\(?:begin|end|noindent|par|set|setdef|param|parameter|var|orvar|variable|objective|constraint|minimize|maximize|st|for|label|notag)\b'
for name in MODELS:
    for syntax in ['raw', 'structured', 'light']:
        path = TARGET / f'{name}-{syntax}.tex'
        source = path.read_text(encoding='utf-8')
        # Identical legal boilerplate is not mathematical-input typing cost.
        source = source.removeprefix(
            '% Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.\n'
            '% See NOTICE.md and MANIFEST.txt for work scope and maintenance.\n\n')
        if '--model-only' in sys.argv:
            begin = r'\begin{align}' if syntax == 'raw' else r'\begin{ormodel}'
            source = source[source.index(begin):]
        report.append(f'| {name} | {syntax} | {len(source)} | {len(re.findall(structural,source))} | '
                      f'{source.count("{")+source.count("}")} | {source.count("[")+source.count("]")} | '
                      f'{source.count("&")+source.count(chr(92)*2)} | {len(source.splitlines())} |')
print('\n'.join(report))
