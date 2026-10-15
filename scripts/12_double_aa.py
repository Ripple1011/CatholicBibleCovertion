# -*- coding: utf-8 -*-
"""Find what gopika context produces 'ાા' and 'ાX' so we can target the rule.
Print gopika words whose conversion contains a double-matra, with byte dumps."""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert, unswap_arpita

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
tag_re = re.compile(r'<[^>]+>')
DBL = re.compile(r'[ાિીુૂૃૄેૈોૌ]{2}')

names = [n for n in z.namelist() if n.startswith('assets/0/1/') and n.endswith('.html')]
seen = collections.Counter()
examples = []
for n in names:
    raw = z.read(n).decode('utf-8','replace')
    m = re.search(r'<body[^>]*>(.*)</body>', raw, re.S|re.I)
    text = tag_re.sub('', m.group(1) if m else raw)
    for w in text.split():
        u = convert(w)
        if DBL.search(u):
            key = DBL.search(u).group()
            seen[key]+=1
            if len(examples)<25:
                examples.append((w, unswap_arpita(w), u))
print("double-matra kinds in Genesis:", dict(seen.most_common(10)))
print()
for gop, base, u in examples:
    print(f"  gopika={gop!r:12} base={base!r:12} -> {u}")
    print(f"      base bytes: {' '.join(f'{ord(c):02x}' for c in base)}")
