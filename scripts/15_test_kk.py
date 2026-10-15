# -*- coding: utf-8 -*-
"""Test hypothesis: collapsing runs of raw 'k'(0x6b) to a single k fixes the
spurious aa-matra without breaking genuine aa (માં, આકાશ).
We insert the collapse BEFORE unswap and compare."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import gopika_decode as gd

def convert_collapsed(text):
    text = re.sub(r'k{2,}', 'k', text)   # collapse kk.. -> k  (raw 0x6b runs)
    return gd.convert(text)

cases = {
    'માં (expect)': '{kt',
    'આકાશ (expect)': 'ykfkþ',
    'પાણી->પાણી (expect પાણી=પ+ા+ણ+ી)': 'Ãkkýe',
    'પછી?': 'ÃkAe',
    'દિવસ': 'rËðMk',
    'કર્યો': 'fÞkuo',
    'Genesis1:1': '«kht¼{kt Eïhu ykfkþ yLku Ãk]Úðe MkßÞkO.',
    'હતી (níke)': 'níke',
    'સારો (Mkkhku)': 'Mkkhku',
}
for label, g in cases.items():
    print(f"{label}")
    print(f"   current : {gd.convert(g)}")
    print(f"   collapsed: {convert_collapsed(g)}")
