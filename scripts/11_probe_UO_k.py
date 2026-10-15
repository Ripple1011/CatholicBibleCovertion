# -*- coding: utf-8 -*-
"""Probe: contexts of leftover 'U','O','o','r' and the 'ાX' double-matra, to
decide correct rules. Show real gopika snippets (UTF-8 decoded) around them."""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
tag_re = re.compile(r'<[^>]+>')

def text_of(n):
    raw = z.read(n).decode('utf-8','replace')
    m = re.search(r'<body[^>]*>(.*)</body>', raw, re.S|re.I)
    return tag_re.sub('', m.group(1) if m else raw)

# gather words containing specific gopika bytes
targets = {'U':0x55,'O':0x4f,'o':0x6f,'r':0x72}
examples = {k:[] for k in targets}
names = [n for n in z.namelist() if n.startswith('assets/0/') and n.endswith('.html')]
for n in names[:60]:
    for w in text_of(n).split():
        for ch,by in targets.items():
            if ch in w and len(examples[ch])<6:
                examples[ch].append(w)

for ch, ws in examples.items():
    print(f"=== gopika words containing {ch!r} (0x{targets[ch]:02x}) ===")
    for w in ws:
        print("   ", w, '=>', ' '.join(f'{ord(c):02x}' for c in w))
    print()
