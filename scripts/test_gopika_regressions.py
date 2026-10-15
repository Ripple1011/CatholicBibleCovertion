# -*- coding: utf-8 -*-
"""
Regression tests for the Gopika Two -> Unicode converter.

Each case maps a RAW gopika token (as it appears in the app HTML, UTF-8 decoded)
to its EXPECTED Unicode Gujarati. Raw forms were captured from the real corpus.

Run:  PYTHONIOENCODING=utf-8 python test_gopika_regressions.py
Exit code 0 = all pass; 1 = failures (prints a table).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gopika_decode import convert

# (raw_gopika, expected_unicode, note)
CASES = [
    # --- spurious-aa family (HALF-form + single k must DROP the aa) ---
    ('sLk',          'જન',        'half-na final k -> drop'),
    ('ð[Lk',         'વચન',       'vachan'),
    ('SðLk',         'જીવન',      'jivan'),
    ('{Lk',          'મન',        'man'),
    ('ÃktÚk',        'પંથ',       'panth'),
    ('yzøk',         'અડગ',       'adag'),
    ('økkZ',         'ગાઢ',       'gaadh - HALF ga + kk = real aa (ગાઢ, valid word)'),
    # --- genuine aa (FULL consonant + k = real ā) must be KEPT ---
    ('{khk',         'મારા',      'maaraa'),
    ('íkkhk',        'તારા',      'taaraa'),
    ('Ëefhk',        'દીકરા',     'dikaraa'),
    ('Ãkqhk',        'પૂરા',      'puraa'),
    ('Mkkhk',        'સારા',      'saaraa'),
    ('hkò',          'રાજા',      'raajaa'),
    ('rÃkíkk',       'પિતા',      'pitaa'),
    ('{kíkk',        'માતા',      'maataa'),
    ('níkk',         'હતા',       'hataa'),
    # --- 'and' family ---
    ('yLku',         'અને',       'ane'),
    ('íku',          'તે',        'te'),
    ('íkku',         'તો',        'to'),
    # --- Genesis 1:1 words (verified good) ---
    ('«kht¼{kt',     'પ્રારંભમાં', 'in-the-beginning'),
    ('Eïhu',         'ઈશ્વરે',    'God(erg)'),
    ('ykfkþ',        'આકાશ',      'sky'),
    ('Ãk]Úðe',       'પૃથ્વી',    'earth'),
    # --- conjunct short-i / reph / clusters (previously fixed) ---
    ('rËðMk',        'દિવસ',      'divas'),
    ('fÞkuo',        'કર્યો',     'karyo (reph)'),
    ('þÂõík',        'શક્તિ',     'shakti'),
    ('ð]rØ',         'વૃદ્ધિ',    'vruddhi'),
    # --- double-virama must NOT appear ---
    ('{qõâkt',       'મૂક્યાં',   'no duplicate virama (was મૂક્્યાં)'),
]


def main():
    rows = []
    fails = 0
    for raw, exp, note in CASES:
        got = convert(raw)
        ok = (got == exp)
        if not ok:
            fails += 1
        rows.append((ok, raw, got, exp, note))
    for ok, raw, got, exp, note in rows:
        mark = 'OK' if ok else '!!'
        print(f"{mark} {raw!r:16} got={got!r:14} exp={exp!r:14} {note}")
    print(f"\n{len(CASES) - fails}/{len(CASES)} pass")
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
