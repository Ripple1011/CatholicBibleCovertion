# -*- coding: utf-8 -*-
"""
Build the final structured JSON for the Gurjarvani Bible + songbooks.

Outputs (under Gurjarvani_Data/output/):
  bible.json        - {testament: {book_id: {name, chapters: {chap: {verse: text}}}}}
  kirtansagar.json  - {song_id: {title?, text}}
  holi_gito.json
  natal_garba.json
  manifest.json     - counts + the book name map

All Gujarati text is Unicode (converted from Gopika Two). English book names
come from the source <title>, with known corrections applied.
"""
import sys, io, zipfile, re, json, os, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert as _convert
from html_extract import extract_verses
from lexical_fixes import apply_lexical_fixes


import re as _re

# A dangling combining mark split from its word by a stray source space
# ('હુ ં' -> 'હું', 'પ ોતાનાં' -> 'પોતાનાં') rejoins to the PRECEDING letter.
# EXCEPTION: a lone pre-base short-i 'િ' as its own token belongs to the
# FOLLOWING word (it is stored before its consonant), so it is handled
# separately below and excluded here.
_ORPHAN_MARK = _re.compile(r'([઀-૿])\s+([ંઁાીુૂૃૄેૈોૌ્])')  # note: no 'િ'
# A lone short-i token ' િ ' (space both sides) -> prefix the next word, where
# it becomes that word's pre-base short-i (વચાળે િ નજનું -> વચાળે નિજનું).
_LONE_SHORT_I = _re.compile(r'\sિ\s+(\S)')


def convert(text):
    """Structural decode + orphan combining-mark rejoin + lexical corrections."""
    out = _convert(text)
    prev = None
    while prev != out:
        prev = out
        out = _ORPHAN_MARK.sub(r'\1\2', out)
    # lone short-i joins the following word's first consonant
    out = _LONE_SHORT_I.sub(r' \1િ', out)
    return apply_lexical_fixes(out)

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
OUTDIR = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data\output"
os.makedirs(OUTDIR, exist_ok=True)
z = zipfile.ZipFile(APK)

# known source-title corrections
NAME_FIX = {
    ('0', 46): 'Psalms',              # titled 'Genesis', 150 chapters
    ('0', 45): 'Song of Songs',       # 'Centicle of Canticles'
    ('0', 25): 'Wisdom',              # 'Wisdom 2'
}


def title_of(coll, book):
    for chap in range(1, 4):
        n = f'assets/{coll}/{book}/{chap}.html'
        try:
            raw = z.read(n).decode('utf-8', 'replace')
        except KeyError:
            continue
        m = re.search(r'<title>(.*?)</title>', raw, re.S | re.I)
        if m:
            t = re.sub(r'\s*-\s*Chapter.*$', '', m.group(1), flags=re.I).strip()
            return t
    return None


# CONFIRMED source verse-boundary defects (coll, book, chap, verse) where the
# verse body has a leaked inline OWN-number marker and the text after it is the
# real (missing) next verse. Verified individually against the source HTML; a
# general rule is unsafe (cross-refs, numbers, the deuterocanonical Esther-5
# embedded numbering). Only these exact locations are recovered.
#   Isaiah 27:2 -> text before '૨' is a duplicate of v1 (discard); after = real v2
#   Ezekiel 31:5 -> text before '૫' is v4 spillover (keep v5 only, after marker)
#   1 Samuel 29:2 -> after '૨' is the missing verse 3
_VERSE_RECOVERY = {
    ('0', 27, 27, '2'): ('drop_before', 2),   # Isaiah 27:2 duplicate of v1
    ('0', 31, 31, '5'): ('drop_before', 5),   # Ezekiel 31:5 v4 spillover
    ('0', 9, 29, '2'): ('recover_after', 3),  # 1 Samuel 29:2 -> recover v3
}
_G2I = {ord(c): str(i) for i, c in enumerate('૦૧૨૩૪૫૬૭૮૯')}


def build_bible():
    bible = {}
    for coll, testament in [('0', 'OT'), ('1', 'NT')]:
        books = collections.defaultdict(lambda: collections.defaultdict(dict))
        for n in z.namelist():
            m = re.match(rf'assets/{coll}/(\d+)/(\d+)\.html$', n)
            if not m:
                continue
            book, chap = int(m.group(1)), int(m.group(2))
            for vlabel, raw in extract_verses(z.read(n)):
                vnum = vlabel[1:] if vlabel.startswith('v') else vlabel
                text = convert(raw)
                key = (coll, book, chap, vnum)
                if key in _VERSE_RECOVERY:
                    mode, newv = _VERSE_RECOVERY[key]
                    # split at the inline OWN-number (gujarati digits == vnum)
                    mm = re.search(r'(?<=[.!?”’])\s*(' +
                                   ''.join('૦૧૨૩૪૫૬૭૮૯'[int(d)] for d in vnum) +
                                   r')(?=[઀-૿])', text)
                    if mm:
                        before, after = text[:mm.start()].strip(), text[mm.end():].strip()
                        if mode == 'drop_before':
                            text = after            # keep real verse, drop dup/spill
                        elif mode == 'recover_after':
                            text = before            # this verse keeps its own text
                            books[book][chap][str(newv)] = after  # recovered verse
                books[book][chap][vnum] = text
        bible[testament] = {}
        for book in sorted(books):
            name = NAME_FIX.get((coll, book)) or title_of(coll, book)
            chapters = {str(c): dict(books[book][c]) for c in sorted(books[book])}
            bible[testament][str(book)] = {'name': name, 'chapters': chapters}
    return bible


def build_songbook(coll):
    songs = {}
    entries = []
    for n in z.namelist():
        m = re.match(rf'assets/{coll}/(\d+)\.html$', n)
        if m:
            entries.append((int(m.group(1)), n))
    for sid, n in sorted(entries):
        verses = extract_verses(z.read(n))
        text = '\n'.join(t for _, t in verses)
        songs[str(sid)] = {'text': convert(text)} if False else {'text': text and convert(text)}
    return songs


bible = build_bible()
with io.open(os.path.join(OUTDIR, 'bible.json'), 'w', encoding='utf-8') as f:
    json.dump(bible, f, ensure_ascii=False, indent=1)

songbooks = {}
for coll in ['kirtansagar', 'holi_gito', 'natal_garba']:
    sb = build_songbook(coll)
    songbooks[coll] = len(sb)
    with io.open(os.path.join(OUTDIR, f'{coll}.json'), 'w', encoding='utf-8') as f:
        json.dump(sb, f, ensure_ascii=False, indent=1)

# manifest
manifest = {
    'source': 'in.maxwellchristian.gurjarvani v1.0.3',
    'encoding': 'Gopika Two (Arpita) -> Unicode Gujarati',
    'bible': {t: {b: {'name': d['name'], 'chapters': len(d['chapters'])}
                  for b, d in books.items()}
              for t, books in bible.items()},
    'songbooks': songbooks,
}
with io.open(os.path.join(OUTDIR, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# summary
ot = sum(len(d['chapters']) for d in bible['OT'].values())
nt = sum(len(d['chapters']) for d in bible['NT'].values())
print(f"Bible: OT {len(bible['OT'])} books / {ot} chapters ; NT {len(bible['NT'])} books / {nt} chapters")
print(f"Songbooks: {songbooks}")
print(f"wrote JSON to {OUTDIR}")
