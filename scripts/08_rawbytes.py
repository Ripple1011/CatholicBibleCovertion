# -*- coding: utf-8 -*-
"""Pull the EXACT raw bytes of Genesis 1:1 verse-1 words straight from the APK,
so we debug reality, not a hand transcription."""
import sys, io, zipfile, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
APK = r"C:\Users\Admin\Downloads\gurjarvani_x\in.maxwellchristian.gurjarvani.apk"
z = zipfile.ZipFile(APK)
raw = z.read('assets/0/1/1.html').decode('latin-1')
m = re.search(r'name="v1".*?</a>(.*?)<a name="v2"', raw, re.S)
v1 = re.sub(r'<[^>]+>', '', m.group(1)).strip()
# split into words, dump bytes
for w in v1.split(' ')[:8]:
    print(f"{w!r:20} -> {' '.join(f'{ord(c):02x}' for c in w)}")
