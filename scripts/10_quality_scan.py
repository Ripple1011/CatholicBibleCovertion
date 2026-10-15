# -*- coding: utf-8 -*-
"""Whole-corpus quality using the REAL pipeline (html_extract + convert)."""
import sys, io, zipfile, collections, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert
from html_extract import extract_verses

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
names = [n for n in z.namelist()
         if n.startswith('assets/') and n.endswith('.html')
         and not n.startswith('assets/dexopt')]

GUJ = lambda c: 0x0A80 <= ord(c) <= 0x0AFF
LATIN = lambda c: ('a' <= c <= 'z') or ('A' <= c <= 'Z')
DBL = re.compile(r'[ાિીુૂૃૄેૈોૌ]{2}')

guj = lat = other = 0
leftover = collections.Counter()
dbl = collections.Counter()
for n in names:
    for _, raw in extract_verses(z.read(n)):
        out = convert(raw)
        for c in out:
            if GUJ(c): guj += 1
            elif LATIN(c): lat += 1; leftover[c] += 1
            else: other += 1
        for m in DBL.finditer(out):
            dbl[m.group()] += 1

total = guj + lat + other
print(f"gujarati: {guj} ({100*guj/total:.3f}%)  leftover-latin: {lat} ({100*lat/total:.4f}%)  other: {other}")
print("leftover latin:", dict(leftover.most_common()))
print("top double-matra (spurious-aa indicator):")
for s, c in dbl.most_common(8):
    print(f"   {s!r} {c}")
