# -*- coding: utf-8 -*-
"""
Locate every remaining anomaly occurrence with FULL VERSE CONTEXT + book/chapter
/verse reference, so each can be manually verified before a lexical fix.
Excludes the known-good 'word-final virama' class and the intentional Daniel '='.
"""
import sys, io, json, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data\output"
FILES = ['bible.json', 'kirtansagar.json', 'holi_gito.json', 'natal_garba.json']

MATRA = r'ાિીુૂૃૄેૈોૌ'
ANUS = r'ંઁ'
# the real-bug anomaly patterns (exclude word-final virama + non-Gujarati '=')
PATS = [
    ('two matras',          re.compile(r'[' + MATRA + r'][' + MATRA + r']')),
    ('matra after anusvara', re.compile(r'[' + ANUS + r'ઃ][' + MATRA + r']')),
    ('independent V + matra', re.compile(r'[અ-ઔ][' + MATRA + r']')),
    ('orphan mark (space)',  re.compile(r'[઀-૿]\s+[' + MATRA + ANUS + r'્]')),
]

BOOKS = json.load(open(os.path.join(ROOT, '..', 'book_names.json'), encoding='utf-8')) \
    if os.path.exists(os.path.join(ROOT, '..', 'book_names.json')) else {}


def book_name(testament, bid):
    try:
        return BOOKS[testament][bid]['name']
    except Exception:
        return f"{testament} book{bid}"


seen = set()
hits = []


def scan_bible(data):
    for tst, books in data.items():
        for bid, bk in books.items():
            name = bk.get('name', f'{tst} {bid}')
            for ch, verses in bk['chapters'].items():
                for v, text in verses.items():
                    for label, rx in PATS:
                        m = rx.search(text)
                        if m:
                            key = (name, ch, v)
                            if key in seen:
                                continue
                            seen.add(key)
                            frag = text[max(0, m.start()-4):m.start()+6]
                            hits.append((f"{name} {ch}:{v}", label, frag, text))


def scan_songs(data, corpus):
    for sid, entry in data.items():
        text = entry.get('text', '')
        for label, rx in PATS:
            m = rx.search(text)
            if m:
                key = (corpus, sid)
                if key in seen:
                    continue
                seen.add(key)
                frag = text[max(0, m.start()-4):m.start()+6]
                hits.append((f"{corpus} #{sid}", label, frag, text))


for fn in FILES:
    data = json.load(open(os.path.join(ROOT, fn), encoding='utf-8'))
    if fn == 'bible.json':
        scan_bible(data)
    else:
        scan_songs(data, fn.replace('.json', ''))

print(f"{len(hits)} occurrences with context:\n")
for ref, label, frag, text in hits:
    print(f"### [{ref}]  ({label})  flagged near: {frag!r}")
    print(f"    {text}\n")
