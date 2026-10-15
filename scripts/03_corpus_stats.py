# -*- coding: utf-8 -*-
"""
Corpus statistics over the legacy-encoded text:
- Which byte values actually occur in the Gujarati text (so the mapping table
  only needs to cover these).
- Frequency, to prioritize verification of the most common glyphs.
Strips HTML, drops verse-number anchors and ASCII digits/punctuation that are
structural, keeping the <gujFont> body text.
"""
import sys, io, zipfile, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"

z = zipfile.ZipFile(APK)
html_names = [n for n in z.namelist()
              if n.startswith('assets/') and n.endswith('.html')
              and not n.startswith('assets/dexopt')]

tag_re = re.compile(r'<[^>]+>')
counter = collections.Counter()
n_files = 0
for n in html_names:
    try:
        raw = z.read(n).decode('latin-1')  # legacy bytes are latin-1
    except Exception:
        continue
    n_files += 1
    # isolate body, strip tags
    body = raw
    m = re.search(r'<body[^>]*>(.*)</body>', raw, re.S | re.I)
    if m:
        body = m.group(1)
    text = tag_re.sub('', body)
    for ch in text:
        counter[ch] += 1

print(f"files scanned: {n_files}")
print(f"distinct chars: {len(counter)}")
print()
print("All non-ASCII-letter chars by frequency (candidate Gujarati-glyph bytes):")
for ch, cnt in counter.most_common():
    cp = ord(ch)
    kind = 'ascii' if 0x20 <= cp < 0x7f else 'HIGH'
    disp = ch if ch.isprintable() else repr(ch)
    print(f"  {cp:#04x} {kind:5} {disp!r:6} {cnt}")
