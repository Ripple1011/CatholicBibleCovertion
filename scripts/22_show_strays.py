# -*- coding: utf-8 -*-
"""Show full verses that still contain stray (non-Gujarati, non-punctuation)
characters, with the stray wrapped in >>><<< and its location."""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert
from html_extract import extract_verses

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)

# stray = anything not Gujarati block, not whitespace/digits, not normal punctuation/quotes
STRAY = re.compile(r'[^઀-૿\s\d.,;:?!()‘’“”।\-/–—"\x27]')


def label_for(name):
    p = name.split('/')
    if len(p) == 4:
        return f"{ {'0':'OT','1':'NT'}.get(p[1],p[1]) } book{p[2]} ch{p[3].replace('.html','')}"
    if len(p) == 3:
        return f"{p[1]} #{p[2].replace('.html','')}"
    return name


names = [n for n in z.namelist()
         if n.startswith('assets/') and n.endswith('.html')
         and not n.startswith('assets/dexopt')]

by_char = collections.defaultdict(list)   # stray char -> list of (loc, vlabel, marked)
for n in names:
    loc = label_for(n)
    for vlabel, raw in extract_verses(z.read(n)):
        out = convert(raw)
        strays = set(STRAY.findall(out))
        if strays:
            marked = STRAY.sub(lambda m: f'>>>{m.group()}<<<', out)
            for c in strays:
                if len(by_char[c]) < 3:
                    by_char[c].append((loc, vlabel, marked))

# print a few examples per distinct stray char, prioritising most interesting
order = sorted(by_char, key=lambda c: -sum(1 for _ in by_char[c]))
for c in order:
    print(f"\n########## stray {c!r} (U+{ord(c):04X}) ##########")
    for loc, vlabel, marked in by_char[c]:
        print(f"[{loc} : {vlabel}]")
        print(f"  {marked}")
