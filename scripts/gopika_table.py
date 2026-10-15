# -*- coding: utf-8 -*-
"""
Extract the Unicode<->Gopika pair table directly from the upstream myExpr.js
(RahulThakor/GujaratiFontConverter) so we never hand-transcribe ~150 entries.

array_one is a flat JS array of alternating "unicode", "gopika" string literals.
We parse those pairs. Direction in file is Unicode -> Gopika; we invert for decode.
"""
import re, os

JS_PATH = os.path.join(os.path.dirname(__file__), '..', 'source_assets', 'myExpr.js')


def load_pairs():
    with open(JS_PATH, encoding='utf-8') as f:
        src = f.read()
    # isolate the array_one = new Array( ... ) block
    m = re.search(r'array_one\s*=\s*new Array\((.*?)\)\s*var array_one_length', src, re.S)
    block = m.group(1)
    # strip // line comments and /* */ block comments
    block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
    block = re.sub(r'//[^\n]*', '', block)
    # grab all double-quoted string literals in order
    lits = re.findall(r'"((?:[^"\\]|\\.)*)"', block)
    # unescape minimal
    lits = [l.encode().decode('unicode_escape') if '\\' in l else l for l in lits]
    # pair them up: (unicode, gopika)
    pairs = []
    for i in range(0, len(lits) - 1, 2):
        uni, gop = lits[i], lits[i + 1]
        if uni == '' and gop == '':
            continue
        pairs.append((uni, gop))
    return pairs


if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    pairs = load_pairs()
    print(f"parsed {len(pairs)} pairs")
    for uni, gop in pairs[:40]:
        print(f"  {uni!r:12} <-> {gop!r:8}  gop_bytes={' '.join(f'{ord(c):02x}' for c in gop)}")
