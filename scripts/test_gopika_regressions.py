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
    ('hkrºk',        'રાત્રિ',    'raatri - short-i hops the ત્ર conjunct core'),
    ('MksoLknkh',    'સર્જનહાર',  'sarjanhaar - reph via o marker'),
    ('ðíkuo',        'વર્તે',     'varte - reph on a half-form consonant'),
    ('ð»kuo',        'વર્ષે',     'varshe - reph'),
    ('{køkuo',       'માર્ગે',    'maarge - reph'),
    ('hÌkku',        'રહ્યો',     'rahyo - EXTRA core હ્ય + o-matra (not રહ્યે)'),
    ('{kufÕÞtw',     'મોકલ્યું',  'moklyu - anusvara+u order -> u+anusvara'),
    ('¾uuuz',        'ખેડ',       'khed - repeated e-matra collapse'),
    ('¼uuxku',       'ભેટો',      'bheto - repeated e-matra collapse'),
    # NOTE: 'MkßÞkO' decodes to સજ્યાં (not સર્જ્યાં) because the SOURCE bytes
    # lack the reph (ßÞ = જ્ય, no reph glyph); this is a source-data defect, not
    # a converter bug. Left for an output-level lexical correction if desired.
    # --- double-virama must NOT appear ---
    ('{qõâkt',       'મૂક્યાં',   'no duplicate virama (was મૂક્્યાં)'),
    # --- anomaly-scan-derived (matra order / repeats / reph-at-end) ---
    ('Au]',          'છે',        'chhe - spurious trailing ૃ dropped'),
    ('yk¿kk',        'આજ્ઞા',     'aajnaa - જ્ઞ conjunct keeps its aa'),
    ('yk¿kkyku',     'આજ્ઞાઓ',    'aajnaao'),
    # જોવું family: 'ò'+'u'+letter = જો ligature (not જે)
    ('òuE',          'જોઈ',       'joi - ò ligature jo, not je'),
    ('òuÞku',        'જોયો',      'joyo'),
    ('òuÞwt',        'જોયું',     'joyu'),
    ('òuELku',       'જોઈને',     'joine'),
    # but bare òu at word end stays જે
    ('çkeòu',        'બીજે',      'bije - bare òu word-final stays je'),
    ('fhòu',         'કરજે',      'karje'),
]

# Unicode-level fix_unicode() cases (post-decode normalization), from the
# systematic anomaly scan. Each left side is an INVALID sequence that must
# normalize to the right side.
FIX_CASES = [
    ('તંે', 'તેં'), ('મંે', 'મેં'), ('ખંેચી', 'ખેંચી'), ('વહંેચતો', 'વહેંચતો'),
    ('ક્યાંં', 'ક્યાં'), ('તારુંં', 'તારું'), ('લીધુું', 'લીધું'), ('વૃૃૃ', 'વૃ'),
    ('કીતિર્', 'કીર્તિ'), ('પરિપૂતિર્', 'પરિપૂર્તિ'), ('છેૃ', 'છે'),
    ('મોકલ્યંુ', 'મોકલ્યું'),
]


def main():
    from gopika_decode import fix_unicode
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
    # fix_unicode normalization cases
    print("  -- fix_unicode normalization --")
    for bad, good in FIX_CASES:
        got = fix_unicode(bad)
        ok = (got == good)
        if not ok:
            fails += 1
        print(f"{'OK' if ok else '!!'} {bad!r:14} -> {got!r:14} exp={good!r}")
    total = len(CASES) + len(FIX_CASES)
    print(f"\n{total - fails}/{total} pass")
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
