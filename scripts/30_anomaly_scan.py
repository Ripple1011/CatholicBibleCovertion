# -*- coding: utf-8 -*-
"""
Systematic anomaly scanner for the converted Unicode Gujarati JSON.

Instead of spot-checking words by eye, flag every sequence that is
ORTHOGRAPHICALLY INVALID or SUSPICIOUS in Gujarati. Almost all conversion bugs
leave such a signature. For each anomaly class we report the count and a few
example words (whole token containing the bad sequence) so they can be traced
to raw bytes and fixed at the converter level.

Gujarati block:
  consonants      ક–હ   U+0A95–U+0AB9  (+ ળ U+0AB3)
  independent V   અ–ઔ   U+0A85–U+0A94 (+ ઋ ...)
  dependent matra ા–ૌ   U+0ABE–U+0ACC
  anusvara ં U+0A82, candrabindu ઁ U+0A81, visarga ઃ U+0A83
  virama ્ U+0ACD
  nukta ઼ U+0ABC
"""
import sys, io, json, os, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data"
FILES = ['bible.json', 'kirtansagar.json', 'holi_gito.json', 'natal_garba.json']

CONS = r'ક-હળ'          # ક–હ + ળ
MATRA = r'ા-ૌ'              # ા–ૌ (dependent vowels)
BELOW = r'ુૂ'              # ુ ૂ
VIRAMA = '્'
ANUS = r'ઁં'               # candrabindu, anusvara
VISARGA = 'ઃ'
INDEP = r'અ-ઔ'            # independent vowels
NONGUJ = r'[^઀-૿\s\d.,;:?!()‘’“”।/\-–—"\']'

# anomaly patterns: (name, compiled regex that matches the BAD sequence)
CHECKS = [
    # two dependent vowel signs in a row (only one allowed per consonant)
    ('two matras in a row', re.compile(r'[' + MATRA + r'][' + MATRA + r']')),
    # same matra repeated (font artifact)  e.g. ેે
    ('repeated same matra', re.compile(r'([' + MATRA + r'])\1')),
    # virama followed by a dependent vowel (virama should precede a consonant)
    ('virama + matra', re.compile(VIRAMA + r'[' + MATRA + r']')),
    # duplicate virama
    ('duplicate virama', re.compile(VIRAMA + VIRAMA)),
    # anusvara/candrabindu BEFORE a below vowel (wrong order: should be ુ/ૂ then ં)
    ('anusvara before ુ/ૂ', re.compile(r'[' + ANUS + r'][' + BELOW + r']')),
    # matra immediately after anusvara/visarga (nothing should attach after them)
    ('matra after anusvara', re.compile(r'[' + ANUS + VISARGA + r'][' + MATRA + r']')),
    # independent vowel carrying a dependent matra (should be a consonant)
    ('independent V + matra', re.compile(r'[' + INDEP + r'][' + MATRA + r']')),
    # virama at end of a word (orphan half-form) -> token ends in ્
    ('word-final virama', re.compile(VIRAMA + r'(?=\s|$|[.,;:?!)’”])')),
    # a vowel sign directly after a word boundary / space (orphan matra)
    ('orphan leading matra', re.compile(r'(?:^|\s)[' + MATRA + ANUS + VIRAMA + r']')),
    # leftover Latin / non-Gujarati letter inside Gujarati text
    ('non-Gujarati char', re.compile(NONGUJ)),
    # anusvara + anusvara, or visarga + visarga
    ('double anusvara', re.compile(r'[' + ANUS + r']{2}')),
    # reph signature: a bare 'ર્' NOT followed by a consonant (reph should sit on
    # the next consonant). 'ર્' at word end or before a matra/space.
    ('reph ર્ not on consonant', re.compile(r'ર' + VIRAMA + r'(?=\s|$|[' + MATRA + ANUS + r'])')),
]


def tokens_with(text, rx):
    out = []
    for m in rx.finditer(text):
        # grab the surrounding whitespace-delimited token
        s = text.rfind(' ', 0, m.start()) + 1
        e = text.find(' ', m.end())
        if e == -1:
            e = len(text)
        out.append(text[s:e].strip('.,;:?!()‘’“”"'))
    return out


def walk(o, cb):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'name':
                continue
            walk(v, cb)
    elif isinstance(o, str):
        cb(o)


counts = collections.Counter()
examples = collections.defaultdict(collections.Counter)
for fn in FILES:
    path = os.path.join(OUT, 'output', fn)
    data = json.load(open(path, encoding='utf-8'))

    def cb(text):
        for name, rx in CHECKS:
            toks = tokens_with(text, rx)
            if toks:
                counts[name] += len(toks)
                for t in toks:
                    examples[name][t] += 1
    walk(data, cb)

print("=" * 70)
print("ANOMALY SCAN — invalid/suspicious Gujarati sequences (all corpora)")
print("=" * 70)
for name, _ in CHECKS:
    c = counts[name]
    top = examples[name].most_common(6)
    print(f"\n[{c:6}] {name}")
    for tok, n in top:
        print(f"         {n:5}  {tok}")
