# -*- coding: utf-8 -*-
"""
Export a RAW-TRACE table so a proofreading agent with ONLY the GitHub repo (no
APK) can still trace any converted word back to its source Gopika bytes and the
intermediate conversion stages. This is what lets the agent tell a CONVERTER BUG
apart from REAL SOURCE TEXT.

Output: reports/raw_trace.jsonl  (one JSON object per DISTINCT converted word)
  {
    "u":   "<final Unicode word>",
    "raw": "<raw gopika token, UTF-8 recovered latin-1 chars>",
    "hex": "6e 6b ...",        # raw byte/codepoint values
    "unswap": "<after arpita unswap>",
    "n":   <corpus frequency>,
    "refs": ["OT Genesis 1:1", ...]   # up to 3 example locations
  }
Only distinct (converted-word) rows are emitted, so the file stays compact.
"""
import sys, io, zipfile, re, json, collections, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from html_extract import extract_verses
import gopika_decode as gd

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
OUT = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data\reports\raw_trace.jsonl"
BOOKS = json.load(open(os.path.join(os.path.dirname(OUT), '..', 'book_names.json'),
                      encoding='utf-8'))
z = zipfile.ZipFile(APK)


def ref_for(name):
    parts = name.split('/')
    if len(parts) == 4:
        coll, book, chap = parts[1], parts[2], parts[3].replace('.html', '')
        tst = {'0': 'OT', '1': 'NT'}.get(coll, coll)
        try:
            bn = BOOKS[tst][book]['name']
        except Exception:
            bn = f'{tst} {book}'
        return f'{bn} {chap}'
    if len(parts) == 3:
        return f'{parts[1]} #{parts[2].replace(".html", "")}'
    return name


rows = {}   # converted-word -> dict
freq = collections.Counter()
for n in z.namelist():
    if not n.endswith('.html') or n.startswith('assets/dexopt'):
        continue
    ref = ref_for(n)
    for _, raw in extract_verses(z.read(n)):
        for w in raw.split():
            w2 = re.sub(r'[^\x20-￿]', '', w).strip('.,;:?!“”‘’()-"')
            if not w2:
                continue
            u = gd.convert(w2)
            if not u.strip():
                continue
            freq[u] += 1
            if u not in rows:
                rows[u] = {
                    'u': u, 'raw': w2,
                    'hex': ' '.join(f'{ord(c):02x}' for c in w2),
                    'unswap': gd.unswap_arpita(w2),
                    'refs': [],
                }
            if len(rows[u]['refs']) < 3 and ref not in rows[u]['refs']:
                rows[u]['refs'].append(ref)

with io.open(OUT, 'w', encoding='utf-8') as f:
    for u, r in sorted(rows.items(), key=lambda kv: -freq[kv[0]]):
        r['n'] = freq[u]
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print(f"wrote {OUT}")
print(f"distinct converted words: {len(rows)}")
print(f"total word occurrences:   {sum(freq.values())}")
