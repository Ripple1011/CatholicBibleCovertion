# -*- coding: utf-8 -*-
"""Extract the English book name for each OT/NT book folder from the <title>
of its chapter 1 file (format: 'Genesis - Chapter 1'). Also count chapters."""
import sys, io, zipfile, re, json, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)

def chapters_for(coll):
    books = collections.defaultdict(set)
    for n in z.namelist():
        m = re.match(rf'assets/{coll}/(\d+)/(\d+)\.html$', n)
        if m:
            books[int(m.group(1))].add(int(m.group(2)))
    return books

def title_of(coll, book, chap=1):
    name = f'assets/{coll}/{book}/{chap}.html'
    try:
        raw = z.read(name).decode('utf-8','replace')
    except KeyError:
        return None
    m = re.search(r'<title>(.*?)</title>', raw, re.S|re.I)
    if not m: return None
    t = m.group(1).strip()
    t = re.sub(r'\s*-\s*Chapter.*$', '', t, flags=re.I).strip()
    return t

result = {}
for coll, label in [('0','OT'), ('1','NT')]:
    books = chapters_for(coll)
    result[label] = {}
    for book in sorted(books):
        chaps = sorted(books[book])
        # title from first available chapter
        t = title_of(coll, book, chaps[0])
        result[label][book] = {'name': t, 'chapters': len(chaps),
                               'chapter_ids': [chaps[0], chaps[-1]]}
        print(f"{label} book{book:2}: {t!r:28} chapters={len(chaps)} range={chaps[0]}-{chaps[-1]}")

with io.open(r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data\book_names.json",'w',encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("\nwrote book_names.json")
