# -*- coding: utf-8 -*-
"""Report every leftover Latin char after conversion, with full verse context,
using the robust shared extractor (entities decoded, gujFont-scoped)."""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert
from html_extract import extract_verses

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
OUT = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data\residue_report.txt"
z = zipfile.ZipFile(APK)
LATIN = re.compile(r'[A-Za-z]')


def label_for(name):
    parts = name.split('/')
    if len(parts) == 4:
        coll, book, chap = parts[1], parts[2], parts[3].replace('.html', '')
        testament = {'0': 'OT', '1': 'NT'}.get(coll, coll)
        return f"{testament} book{book} ch{chap}"
    if len(parts) == 3:
        return f"{parts[1]} #{parts[2].replace('.html','')}"
    return name


names = [n for n in z.namelist()
         if n.startswith('assets/') and n.endswith('.html')
         and not n.startswith('assets/dexopt')]

records = []
char_counter = collections.Counter()
for n in names:
    loc = label_for(n)
    for vlabel, raw_text in extract_verses(z.read(n)):
        out = convert(raw_text)
        strays = LATIN.findall(out)
        if strays:
            for c in strays:
                char_counter[c] += 1
            marked = LATIN.sub(lambda m: f'>>>{m.group()}<<<', out)
            records.append((loc, vlabel, raw_text, marked, ''.join(sorted(set(strays)))))

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write("RESIDUE REPORT — leftover Latin characters after Gopika->Unicode conversion\n")
    f.write("=" * 78 + "\n")
    f.write(f"Total occurrences: {sum(char_counter.values())}\n")
    f.write(f"Distinct stray chars: {dict(char_counter.most_common())}\n")
    f.write(f"Verses affected: {len(records)}\n")
    f.write("=" * 78 + "\n\n")
    for loc, vlabel, raw_text, marked, chars in records:
        f.write(f"[{loc} : {vlabel}]  stray={chars}\n")
        f.write(f"  GOPIKA : {raw_text}\n")
        f.write(f"  UNICODE: {marked}\n\n")

print(f"wrote {OUT}")
print(f"total stray Latin occurrences: {sum(char_counter.values())}")
print(f"distinct: {dict(char_counter.most_common())}")
print(f"verses affected: {len(records)}")
