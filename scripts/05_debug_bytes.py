# -*- coding: utf-8 -*-
"""Debug: show, for each Genesis 1:1 byte (after Arpita unswap), the raw table hit,
with NO reorder rules, to see the true per-byte mapping."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import unswap_arpita, G2U, GOP_KEYS

gen_bytes = bytes([0xab,0x6b,0x68,0x74,0xbc,0x7b,0x6b,0x74,0x20,
                   0x45,0xef,0x68,0x75,0x20,
                   0x79,0x6b,0x66,0x6b,0xfe,0x20,
                   0x79,0x4c,0x6b,0x75,0x20,
                   0xc3,0x6b,0x5d,0xda,0xf0,0x65,0x20,
                   0x4d,0x6b,0xdf,0xde,0x6b,0x4f,0x2e])
legacy = gen_bytes.decode('cp1252')
base = unswap_arpita(legacy)
print("orig  bytes:", ' '.join(f'{ord(c):02x}' for c in legacy))
print("unswap base:", ' '.join(f'{ord(c):02x}' for c in base))
print()
# greedy decode with trace, no reorder
i=0; n=len(base)
while i<n:
    hit=None
    for k in GOP_KEYS:
        if k and base.startswith(k,i):
            hit=k; break
    if hit:
        print(f"  pos {i:2} byte {ord(base[i]):02x} key={hit!r} -> {G2U[hit]!r}")
        i+=len(hit)
    else:
        print(f"  pos {i:2} byte {ord(base[i]):02x} char={base[i]!r} -> PASSTHROUGH")
        i+=1
