# -*- coding: utf-8 -*-
"""List multi-char gopika keys and flag those composed only of low-ASCII
(which can collide across glyph boundaries) vs those with high bytes/virama."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_table import load_pairs

PAIRS = load_pairs()
G2U = {}
for uni, gop in PAIRS:
    if gop not in G2U:
        G2U[gop] = uni

print("Multi-char gopika keys:")
for gop in sorted(G2U, key=len, reverse=True):
    if len(gop) > 1:
        bytes_ = ' '.join(f'{ord(c):02x}' for c in gop)
        low_only = all(0x20 <= ord(c) < 0x7f for c in gop)
        flag = 'LOW-ASCII(risky)' if low_only else 'has-high-byte(safe)'
        print(f"  {gop!r:8} -> {G2U[gop]!r:8}  [{bytes_}] {flag}")
