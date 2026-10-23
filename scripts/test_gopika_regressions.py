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
    # expanded જો ligature family (Bible Pass-1): òu + various consonants -> જો
    ('òuíkkt',       'જોતાં',     'jotaan'),
    ('òufu',         'જોકે',      'joke'),
    ('òuze',         'જોડી',      'jodi'),
    ('òu¾{',         'જોખમ',      'jokham'),
    ('òuþu',         'જોશે',      'joshe'),
    ('f{òuh',        'કમજોર',     'kamjor'),
    # but these must STAY જે (critical guardrail)
    ('òuðwt',        'જેવું',     'jevu - òu+ð stays je'),
    ('òu{',          'જેમ',       'jem - òu+{ stays je'),
    ('òuðk',         'જેવા',      'jeva'),
    # reph on a half-form-led conjunct (ત્ય): reph rides the FIRST consonant
    ('ðíÞkuo',       'વર્ત્યો',   'vartyo - reph on ત of ત્ય (was વત્ર્યો)'),
    ('{íÞo',         'મર્ત્ય',    'martya'),
    ('yÃÞko',        'અર્પ્યા',   'arpya'),
    ('ð»kko',        'વર્ષા',     'varshaa - reph on ષ (lone cons, વ untouched)'),
    # short-i hops a 2-char conjunct core atomically (Òt = ન્ન)
    ('MkkrÒkæÞ',     'સાન્નિધ્ય', 'saannidhya - short-i past ન્ન core'),
    ('MkkrÒkæÞ{kt',  'સાન્નિધ્યમાં', 'saannidhyamaan'),
    # reph crosses the vocalic-r matra ']'(ૃ)
    ('Ëwð]or¥kykuLku', 'દુર્વૃત્તિઓને', 'durvruttione - reph over ૃ'),
    # conjunct core (જ્ઞ/ન્ન) + o-matra: must keep ો, not lose it to ે
    ('Þ¿kku',         'યજ્ઞો',     'yajno - જ્ઞ + o-matra'),
    ('Þ¿kkuLke',      'યજ્ઞોની',   'yajnoni'),
    ('ík¥ð¿kku',      'તત્ત્વજ્ઞો', 'tattvagno'),
    ('WÒkku',         'ઉન્નો',     'unno - ન્ન + o-matra'),
    # the e/aa contrasts for the same cores MUST be preserved
    ('Þ¿ku',          'યજ્ઞે',     'yajne - જ્ઞ + e stays ે'),
    ('Þ¿kk',          'યજ્ઞા',     'yajnaa - જ્ઞ + aa stays ા'),
    # Š reph+short-i before a FULL consonant ({=મ, ð=વ): ר्+C+િ
    ('ÄkŠ{f',         'ધાર્મિક',   'dharmik - Š before full મ (was ધામરિક)'),
    ('ÄŠ{c',          'ધર્મિષ્ઠ',  'dharmishth'),
    ('økŠðc',         'ગર્વિષ્ઠ',  'garvishth - Š before full વ'),
    ('rLkŠððkË',      'નિર્વિવાદ', 'nirvivad'),
    # reph crossing an already-reordered ordinary short-i 'r'
    ('Äkr{of',        'ધાર્મિક',   'dharmik - reph over reordered short-i (was ધામિર્ક)'),
    ('Mk{rÃkoík',     'સમર્પિત',   'samarpit'),
    # controls: valid િર્ sequences must NOT be disturbed by the r-in-reph change
    ('rLkËkuo»k',     'નિર્દોષ',   'nirdosh - control'),
    ('ßÞkurík{oÞ',    'જ્યોતિર્મય', 'jyotirmay - control'),
    ('ríkMkko',       'તિર્સા',    'tirsa - control'),
    # full-consonant Š reph+short-i over an Arpita-SWAPPED carrier: raw Ë=દ (not
    # the base-font સ). Callback must unswap the matched carrier before lookup.
    ('MkkŠËMk',       'સાર્દિસ',   'Sardis - raw ŠË -> ર્દિ (was સાર્સિસ)'),
    ('MkkŠËMkLkk',    'સાર્દિસના', 'Sardis-na'),
    ('MkkŠËMk{kt',    'સાર્દિસમાં', 'Sardis-maan'),
    ('rLkŠËü',        'નિર્દિષ્ટ', 'nirdisht - preface/trace control for ŠË'),
    # raw/base contrast guards for the swapped carriers
    ('økŠŒc',         'ગર્તિષ્ઠ',  'raw ŠŒ -> ર્તિ (Œ=ત) contrast guard'),
    # HALF-form + kkì = candra-o ૉ (first k completes half-form, kì=candra-o).
    # Must NOT be eaten by the generic HALF+kk->aa branch.
    ('MkkìLku',       'સૉને',      'Sone (candra-o) - was સાૅને'),
    ('Mkì',           'સૅ',        'single-k candra-e stays ૅ (NOT candra-o)'),
    ('MxkìEf',        'સ્ટૉઈક',    'stoik - full-cons + kì candra-o (control)'),
    ('{kìh',          'મૉર',       'mor - full-cons + kì candra-o (control)'),
    # Pass 12: raw U(0x55) glyph = e-matra + anusvara (ેં), NOT nasal-only.
    # Bounded to the ખેંચ- (¾U[) and ફેંક- (VUf) stems.
    ('¾U[eLku',       'ખેંચીને',   'khenchine - raw U carries e-matra (was ખંચીને)'),
    ('¾U[u',          'ખેંચે',     'khenche'),
    ('¾U[u÷k',        'ખેંચેલા',   'khenchela'),
    ('¾U[íkku',       'ખેંચતો',    'khenchto'),
    ('VUfeLku',       'ફેંકીને',   'phenkine - V U f stem'),
    # conjunct inflections of the SAME two stems (¾U/VU anchor, ચ્ય/ક્ય follower)
    ('¾UåÞwt',        'ખેંચ્યું',  'khenchyu - ¾U + ચ્ય conjunct'),
    ('¾UåÞku',        'ખેંચ્યો',   'khenchyo'),
    ('VUõâwt',        'ફેંક્યું',  'phenkyu - VU + ક્ય conjunct'),
    ('VUõâku',        'ફેંક્યો',   'phenkyo'),
    # negatives/controls for Pass 12: these must NOT change
    ('¾t[kðwt',       'ખંચાવું',   'khanchavu - plain raw t (NO U); stays nasal-only'),
    ('MkkUÃkðkLkwt',  'સાંપવાનું',  'aa+U family held outside bounded release (unchanged)'),
    ('ÃknkU[e',       'પહાંચી',    'pahanchi - FROZEN form, bounded must not touch'),
    # Š = reph ર્ + short-i િ as a pre-base unit riding the next consonant
    ('{qŠík',        'મૂર્તિ',    'murti - Š reph+short-i -> ર્ on ત'),
    ('feŠík',        'કીર્તિ',    'kirti'),
    ('Mk{ŠÃkík',     'સમર્પિત',   'samarpit'),
    ('ÃkkŠÚkð',      'પાર્થિવ',   'parthiv'),
    ('ynŠLkþ',       'અહર્નિશ',   'aharnish'),
    # short-i hopping a C+્ર post-base-ra cluster (ખ્રિસ્ત = Christ!)
    ('r¾úMík',       'ખ્રિસ્ત',   'khrist - short-i hops ખ્ર (C+્ર)'),
    ('rÃkúÞ',        'પ્રિય',     'priya - half-form પ્ + ્ર'),
    ('økkrçkúÞu÷',   'ગાબ્રિયેલ', 'gabriel'),
    ('yrøkúÃÃkk',    'અગ્રિપ્પા', 'agrippa'),
    # Pass 22: decoder must stay FAITHFUL to both half-ka and full-ka (the fix is
    # lexical, NOT a decoder change). õ=ક્ half-form, f=ક full.
    ('{kuõÕÞku',     'મોક્લ્યો',  'mok­lyo - source half-ka õ (lexically fixed later)'),
    ('{kufÕÞku',     'મોકલ્યો',   'moklyo - correct full-ka f control'),
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

# Lexical-layer cases (apply_lexical_fixes), with Gujarati word-boundary guards.
# (input, expected). These test the WORD_FIXES/PHRASE_FIXES overlay, NOT decode.
LEX_CASES = [
    # Bible Pass 13: source-defect plural of આજ્ઞા (Psalm 119:172). Whole word only.
    ('આજ્ઞઓ', 'આજ્ઞાઓ'),
    ('તારી આજ્ઞઓ મહીં', 'તારી આજ્ઞાઓ મહીં'),   # in situ (the verse context)
    # NEGATIVE boundary controls: correctly-encoded forms must pass THROUGH.
    ('આજ્ઞાઓ', 'આજ્ઞાઓ'),                        # already correct (×249 in corpus)
    ('આજ્ઞાઓનું', 'આજ્ઞાઓનું'),                  # correct + suffix
    ('આજ્ઞા', 'આજ્ઞા'),                           # singular
    ('યજ્ઞો', 'યજ્ઞો'), ('જ્ઞાન', 'જ્ઞાન'),       # unrelated જ્ઞ words
    ('કોઈઆજ્ઞઓ', 'કોઈઆજ્ઞઓ'),                    # Gujarati prefix -> NO whole-word match
    # Bible Pass 14: source half-dha ધ્ -> half-gha ઘ્ (ingratitude family).
    ('કૃતધ્નતા', 'કૃતઘ્નતા'),                     # Wisdom 14:26
    ('કૃતધ્ની', 'કૃતઘ્ની'),                        # 2 Timothy 3:2
    ('સારા માણસોની વ્યગ્રતા, કૃતધ્નતા, અંતરની',
     'સારા માણસોની વ્યગ્રતા, કૃતઘ્નતા, અંતરની'),   # in situ (Wisdom 14:26)
    # NEGATIVE / idempotence controls for Pass 14
    ('કૃતઘ્નીઓ', 'કૃતઘ્નીઓ'),                      # Luke 6:35 control - unchanged
    ('કૃતઘ્નતા', 'કૃતઘ્નતા'),                      # already correct - idempotent
    ('કૃતઘ્ની', 'કૃતઘ્ની'),
    ('મધ્ય', 'મધ્ય'), ('ધ્યાન', 'ધ્યાન'), ('અધ્યક્ષ', 'અધ્યક્ષ'),  # no generic ધ replace
    ('કૃતધ્નીઓ', 'કૃતધ્નીઓ'),                      # Gujarati suffix -> NO whole-word match
    # Bible Pass 15 — 2 Timothy 4:20 person/place transposition (full-verse phrase).
    ('અરાસ્તસ કરિંથ રહી પડ્યો હતો, અને મિલેતસને હું ત્રોફિમસમાં માંદો મૂકી આવ્યો હતો.',
     'અરાસ્તસ કરિંથ રહી પડ્યો હતો, અને ત્રોફિમસને હું મિલેતસમાં માંદો મૂકી આવ્યો હતો.'),
    # idempotence: the corrected verse passes through unchanged
    ('અરાસ્તસ કરિંથ રહી પડ્યો હતો, અને ત્રોફિમસને હું મિલેતસમાં માંદો મૂકી આવ્યો હતો.',
     'અરાસ્તસ કરિંથ રહી પડ્યો હતો, અને ત્રોફિમસને હું મિલેતસમાં માંદો મૂકી આવ્યો હતો.'),
    # NEGATIVE: the two names appearing SEPARATELY must NOT be swapped (Acts controls)
    ('એફેસસના ત્રોફિમસને પાઉલ', 'એફેસસના ત્રોફિમસને પાઉલ'),
    ('મિલેતસથી તેણે એફેસસ', 'મિલેતસથી તેણે એફેસસ'),
    ('મિલેતસને', 'મિલેતસને'),            # bare token, not the phrase -> unchanged
    ('ત્રોફિમસમાં', 'ત્રોફિમસમાં'),        # bare token, not the phrase -> unchanged
    # Bible Pass 17 — Numbers 2:24 Ephraim census ૪૫,૫૦૦ -> ૪૦,૫૦૦ (full value).
    # NEGATIVE: a bare ૪૫,૫૦૦ number alone must NOT be changed (no WORD_FIXES entry;
    # only the exact full grouped value matches).
    ('૪૫,૫૦૦', '૪૫,૫૦૦'),
    # protected numbers that must never be touched
    ('૪૫,૬૫૦', '૪૫,૬૫૦'),                  # Gad, Numbers 2 southern camp
    ('૪૦,૫૦૦', '૪૦,૫૦૦'),                  # Gad, Numbers 26:18 (different census)
    # Bible Pass 19 — Genesis 14:22 truncated oath: add missing ે (ક -> કે).
    # Uses the decode-stage “મં (PHRASE_FIXES runs before the મં->મેં WORD_FIX);
    # the WORD_FIX then also turns “મં into “મેં within the same call.
    ('પણ અબ્રામે જવાબ આપ્યો, “મં પૃથ્વી અને આકાશના સર્જનહાર પ્રભુ પરમેશ્વર આગળ સોગંદ લીધા છે ક',
     'પણ અબ્રામે જવાબ આપ્યો, “મેં પૃથ્વી અને આકાશના સર્જનહાર પ્રભુ પરમેશ્વર આગળ સોગંદ લીધા છે કે'),
    # NEGATIVE: a bare ક in any other context must NOT be touched (full-value key).
    ('એક', 'એક'), ('ક ', 'ક '), ('તેઓ ક ખરા', 'તેઓ ક ખરા'),
    # Bible Pass 21 — Job 38:7 reversed u-vowel lengths ખાતમૂહુર્ત -> ખાતમુહૂર્ત.
    ('ખાતમૂહુર્ત', 'ખાતમુહૂર્ત'),
    ('એનું ખાતમૂહુર્ત કોણે', 'એનું ખાતમુહૂર્ત કોણે'),   # in situ
    # NEGATIVE / idempotence
    ('ખાતમુહૂર્ત', 'ખાતમુહૂર્ત'),       # already correct
    ('મુહૂર્ત', 'મુહૂર્ત'),             # Sirach 14:12 control root - unchanged
    ('મૂહુર્ત', 'મૂહુર્ત'),             # bare reversed root (not the compound) -> no match
    # Bible Pass 22 — John 10:36 extra half-ka મોક્લ્યો -> મોકલ્યો (remove 1st virama).
    ('મોક્લ્યો', 'મોકલ્યો'),
    ('જગતમાં મોક્લ્યો છે', 'જગતમાં મોકલ્યો છે'),       # in situ
    # NEGATIVE / idempotence / boundary (from the handoff's required fixtures)
    ('મોકલ્યો', 'મોકલ્યો'),           # control form - unchanged
    ('અમોક્લ્યો', 'અમોક્લ્યો'),        # Gujarati prefix -> no whole-word match
    ('મોક્લ્યોમાં', 'મોક્લ્યોમાં'),    # Gujarati suffix -> no whole-word match
    # preservation: related/legit forms must NOT change
    ('મોકલ્યા', 'મોકલ્યા'), ('મોકલ્યું', 'મોકલ્યું'),
    ('ક્લેશ', 'ક્લેશ'),               # genuine ક્લ conjunct stays
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
    # lexical-layer cases
    print("  -- apply_lexical_fixes --")
    from lexical_fixes import apply_lexical_fixes
    for src, good in LEX_CASES:
        got = apply_lexical_fixes(src)
        ok = (got == good)
        if not ok:
            fails += 1
        print(f"{'OK' if ok else '!!'} {src!r:18} -> {got!r:18} exp={good!r}")
    total = len(CASES) + len(FIX_CASES) + len(LEX_CASES)
    print(f"\n{total - fails}/{total} pass")
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
