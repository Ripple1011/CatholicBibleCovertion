# -*- coding: utf-8 -*-
"""For each stray Latin char, find the gopika byte and surrounding word so the
exact Unicode replacement can be decided. Focus on real-font strays (I,g,l,F),
and separately flag parser strays (p from &entities;, v from <a name>)."""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert, unswap_arpita

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
tag_re = re.compile(r'<[^>]+>')

names = [n for n in z.namelist()
         if n.startswith('assets/') and n.endswith('.html')
         and not n.startswith('assets/dexopt')]

want = set('IglF')
found = collections.defaultdict(list)
for n in names:
    raw = z.read(n).decode('utf-8', 'replace')
    m = re.search(r'<body[^>]*>(.*)</body>', raw, re.S | re.I)
    text = tag_re.sub('', m.group(1) if m else raw)
    for w in text.split():
        u = convert(w)
        for ch in want:
            if ch in u and len(found[ch]) < 4:
                found[ch].append((w, u))

for ch in 'IglF':
    print(f"=== stray {ch!r} ===")
    for gop, u in found[ch]:
        print(f"   gopika={gop!r}  bytes={' '.join(f'{ord(c):02x}' for c in gop)}")
        print(f"   unswap={unswap_arpita(gop)!r}")
        print(f"   -> {u}")
    print()
