# -*- coding: utf-8 -*-
"""Compare decode WITH vs WITHOUT Arpita unswap, per word, no reorder.
Goal: find the variant + matching strategy that yields readable Gujarati."""
import sys, io
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

words_bytes = [
    ('word0', [0xab,0x6b,0x68,0x74,0xbc,0x7b,0x6b,0x74]),
    ('ઈશ્વરે', [0x45,0xef,0x68,0x75]),
    ('આકાશ',  [0x79,0x6b,0x66,0x6b,0xfe]),
    ('અને',   [0x79,0x4c,0x6b,0x75]),
    ('પૃથ્વી',[0xc3,0x6b,0x5d,0xda,0xf0,0x65]),
    ('સર્જ્યાં',[0x4d,0x6b,0xdf,0xde,0x6b,0x4f]),
]
for name, bs in words_bytes:
    s = bytes(bs).decode('cp1252')
    print(f"--- {name} : bytes {' '.join(f'{b:02x}' for b in bs)}")
    print(f"    NOSWAP : {decode(s)}")
    print(f"    UNSWAP : {decode(unswap(s))}")
