# -*- coding: utf-8 -*-
"""
Polish-pass analysis. Categorize ALL remaining imperfections with examples:
  A) stray non-Gujarati letters (latin + latin-1 high bytes)  -> gopika byte + word
  B) suspicious double-matra / matra-after-virama sequences   -> example words
  C) the 'અનો'/'સર્જ' class (e-matra / reph in specific clusters)
For each stray gopika glyph we show raw bytes + a couple whole words so we can
decide the correct Unicode mapping.
"""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert, unswap_arpita
from html_extract import extract_verses

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
names = [n for n in z.namelist()
         if n.startswith('assets/') and n.endswith('.html')
         and not n.startswith('assets/dexopt')]

STRAY = re.compile(r'[^઀-૿\s\d.,;:?!()‘’“”।\-/]')
DBL = re.compile(r'[ાિીુૂૃૄેૈોૌ]{2}')
VIRMAT = re.compile(r'્[ાિીુૂૃૄેૈોૌ]')

stray_chars = collections.Counter()
stray_examples = collections.defaultdict(list)  # char -> list of (gopika_word, converted)
dbl = collections.Counter()
dbl_examples = collections.defaultdict(list)

for n in names:
    for _, raw in extract_verses(z.read(n)):
        out = convert(raw)
        # A: stray chars
        for m in STRAY.finditer(out):
            c = m.group()
            stray_chars[c] += 1
            if len(stray_examples[c]) < 3:
                # find the gopika word that produced it (approx: convert word-by-word)
                for w in raw.split():
                    cw = convert(w)
                    if c in cw:
                        stray_examples[c].append((w, cw))
                        break
        # B: double matra
        for m in DBL.finditer(out):
            seq = m.group()
            dbl[seq] += 1
            if len(dbl_examples[seq]) < 3:
                for w in raw.split():
                    if DBL.search(convert(w)) and seq in convert(w):
                        dbl_examples[seq].append((w, convert(w)))
                        break

print("=" * 70)
print("A) STRAY NON-GUJARATI CHARS (excluding spaces/digits/punct):")
print("=" * 70)
for c, cnt in stray_chars.most_common(30):
    exs = stray_examples[c]
    exstr = '  '.join(f'{g!r}->{u!r}' for g, u in exs)
    print(f"  {c!r} (U+{ord(c):04X})  x{cnt}")
    for g, u in exs:
        print(f"       {g!r:16} bytes={' '.join(f'{ord(ch):02x}' for ch in unswap_arpita(g))} -> {u}")
print()
print("=" * 70)
print("B) TOP DOUBLE-MATRA SEQUENCES:")
print("=" * 70)
for seq, cnt in dbl.most_common(15):
    exs = dbl_examples[seq]
    print(f"  {seq!r} x{cnt}: " + '  '.join(f'{g!r}->{u!r}' for g, u in exs[:2]))
