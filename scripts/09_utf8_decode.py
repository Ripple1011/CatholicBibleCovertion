# -*- coding: utf-8 -*-
"""Correct pipeline: HTML is UTF-8. Decode UTF-8 -> recover true Gopika (latin-1)
chars -> Arpita unswap -> table decode. Verify against Genesis 1:1 words."""
import sys, io, zipfile, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_table import load_pairs

PAIRS = load_pairs()
G2U = {}
for uni, gop in PAIRS:
    if gop not in G2U:
        G2U[gop] = uni
GOP_KEYS = sorted([k for k in G2U if k], key=len, reverse=True)

def decode(s):
    out=[]; i=0; n=len(s)
    while i<n:
        hit=None
        for k in GOP_KEYS:
            if s.startswith(k,i): hit=k; break
        if hit: out.append(G2U[hit]); i+=len(hit)
        else: out.append(s[i]); i+=1
    return ''.join(out)

def unswap(s):
    s = s.replace('k','\x00').replace('t','k').replace('\x00','t')
    s = s.replace('Œ','\x01').replace('Ë','Œ').replace('\x01','‚')
    return s

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
# READ AS UTF-8 now
raw = z.read('assets/0/1/1.html').decode('utf-8')
m = re.search(r'name="v1".*?</a>(.*?)<a name="v2"', raw, re.S)
v1 = re.sub(r'<[^>]+>', '', m.group(1)).strip()
print("Full verse 1 decode:")
print("  raw gopika:", v1)
print("  UNSWAP+decode:", decode(unswap(v1)))
print()
for w in v1.split(' ')[:8]:
    print(f"  {w!r:14} bytes={' '.join(f'{ord(c):02x}' for c in w)} -> {decode(unswap(w))}")
