# -*- coding: utf-8 -*-
"""
Before/after comparison of the converter fix.
Compares output_old/*.json (pre-fix) vs output/*.json (post-fix):
  - changed verse/song count
  - most frequent word-level before->after changes
  - suspicious-pattern frequencies before vs after
  - new Latin / duplicate-virama checks
Writes reports/<name>_before_after.md for each corpus.
"""
import sys, io, json, os, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data"
OLD = os.path.join(ROOT, 'output_old')
NEW = os.path.join(ROOT, 'output')
REP = os.path.join(ROOT, 'reports')
os.makedirs(REP, exist_ok=True)

SUSPICIOUS = ['જના', 'દુર્જના', 'પાંથ', 'નાભ', 'નાભમંડળ', 'અડગા', 'ગાઢ',
              'ક્્યાં', 'ક્્યારે', 'અનો']
LATIN = re.compile(r'[A-Za-z]')
DUP_VIRAMA = re.compile(r'્્')


def strings_of(obj):
    if isinstance(obj, dict):
        # bible: skip the 'name' (English) fields
        for k, v in obj.items():
            if k == 'name':
                continue
            yield from strings_of(v)
    elif isinstance(obj, str):
        yield obj


def flatten_verses(path):
    """Return ordered list of (key, text) leaf strings, key = path to leaf."""
    data = json.load(open(path, encoding='utf-8'))
    out = []

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'name':
                    continue
                walk(v, p + '/' + str(k))
        elif isinstance(o, str):
            out.append((p, o))
    walk(data, '')
    return out


def report(name):
    oldp = os.path.join(OLD, name)
    newp = os.path.join(NEW, name)
    if not (os.path.exists(oldp) and os.path.exists(newp)):
        return None
    old = dict(flatten_verses(oldp))
    new = dict(flatten_verses(newp))
    keys = sorted(set(old) | set(new))
    changed = 0
    word_changes = collections.Counter()
    for k in keys:
        o, n = old.get(k, ''), new.get(k, '')
        if o != n:
            changed += 1
            ow, nw = o.split(), n.split()
            if len(ow) == len(nw):
                for a, b in zip(ow, nw):
                    if a != b:
                        word_changes[(a, b)] += 1

    def susp(d):
        c = collections.Counter()
        for t in d.values():
            for s in SUSPICIOUS:
                c[s] += t.count(s)
            c['<LATIN letters>'] += len(LATIN.findall(t))
            c['<DUP virama ્્>'] += len(DUP_VIRAMA.findall(t))
        return c
    so, sn = susp(old), susp(new)

    lines = [f"# {name} — before/after\n",
             f"- leaves compared: {len(keys)}",
             f"- changed: {changed} ({100*changed/max(1,len(keys)):.1f}%)\n",
             "## Top word changes (before -> after)"]
    for (a, b), c in word_changes.most_common(40):
        lines.append(f"- {c:5}  `{a}` -> `{b}`")
    lines.append("\n## Suspicious patterns (before -> after)")
    for s in SUSPICIOUS + ['<LATIN letters>', '<DUP virama ્્>']:
        lines.append(f"- `{s}` : {so[s]} -> {sn[s]}")
    open(os.path.join(REP, name.replace('.json', '_before_after.md')), 'w',
         encoding='utf-8').write('\n'.join(lines))
    return name, changed, len(keys), so, sn, word_changes


for nm in ['kirtansagar.json', 'bible.json', 'holi_gito.json', 'natal_garba.json']:
    r = report(nm)
    if not r:
        print(f"{nm}: (missing old or new)")
        continue
    name, changed, total, so, sn, wc = r
    print(f"=== {name}: {changed}/{total} leaves changed ===")
    print("  suspicious:", {s: f"{so[s]}->{sn[s]}" for s in SUSPICIOUS
                            if so[s] or sn[s]})
    print(f"  LATIN: {so['<LATIN letters>']}->{sn['<LATIN letters>']}  "
          f"DUP-virama: {so['<DUP virama ્્>']}->{sn['<DUP virama ્્>']}")
    print("  top 8 word changes:",
          [f"{a}->{b} x{c}" for (a, b), c in wc.most_common(8)])
    print()
