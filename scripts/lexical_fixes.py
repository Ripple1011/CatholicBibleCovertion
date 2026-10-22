# -*- coding: utf-8 -*-
"""
Output-level lexical corrections for CONFIRMED source-data defects — applied
AFTER the structural converter (gopika_decode.convert). Kept separate and
explicit so every correction is auditable.

ONLY add entries here for defects proven to be in the SOURCE BYTES themselves
(not converter bugs). Each entry must be a whole-word, unambiguous fix.

Current entries:
  * સજ્યાં / સજ્યું -> સર્જ્યાં / સર્જ્યું
    Reason: the source encodes 'MkßÞ...' = જ્ય with NO reph glyph (verified:
    ßÞ=જ્ય occurs 539x and is correct elsewhere e.g. જ્યોતિ/રાજ્યમાં; reph,
    when present, uses the 'o' marker as in MksoLk=સર્જન). So these specific
    'create' forms are missing their reph in the app's own data. The decoder
    must not invent bytes, so the fix lives here. Occurrences: સજ્યાં x6,
    સજ્યું x2 (whole corpus sample).
"""
import re

# Verified phrase-level corrections for specific source defects (stranded lone
# matras etc.). Applied as plain substring replacements (order before WORD_FIXES).
# Each verified against the raw bytes + full-verse context.
PHRASE_FIXES = {
    # Bible Pass 15 — 2 Timothy 4:20 (NT/16/chapters/4/20). SOURCE-LEVEL
    # person/place transposition: the source attaches the object marker ને to
    # Miletus (a place) and the locative માં to Trophimus (a person). Both names
    # decode correctly everywhere and are retained verbatim; only their
    # grammatical slots are swapped. Same-edition controls: Acts 21:29 ત્રોફિમસને
    # (Trophimus is a person), Acts 20:17 મિલેતસથી (Miletus is a place). Full,
    # exact verse so NO name/suffix is replaced globally and it cannot half-apply.
    'અરાસ્તસ કરિંથ રહી પડ્યો હતો, અને મિલેતસને હું ત્રોફિમસમાં માંદો મૂકી આવ્યો હતો.':
        'અરાસ્તસ કરિંથ રહી પડ્યો હતો, અને ત્રોફિમસને હું મિલેતસમાં માંદો મૂકી આવ્યો હતો.',
    # Bible Pass 17 — Ephraim census figure inside grouped Numbers 2:24
    # (OT/4/chapters/2/24, the figure is conventionally Numbers 2:19). SOURCE
    # DEFECT: raw '45,500' (34 35 2c 35 30 30) faithfully decodes to ૪૫,૫૦૦, but
    # it must be ૪૦,૫૦૦: the value's OWN stated subtotal ૧,૦૮,૧૦૦ (108100) only
    # reconciles with 40500 (40500+32200+35400=108100; 45500 gives 113100), and
    # Numbers 1:33 reads ૪૦,૫૦૦ for Ephraim. One full-value overlay; grouping and
    # all other numbers (incl. Gad ૪૫,૬૫૦ and the 26:18 ૪૦,૫૦૦) untouched.
    '“પશ્ચિમ બાજુએ એફ્રાઈમના વંશની સેનાના ધ્વજ હેઠળના લોકોએ નીચેના આગેવાનો હેઠળ ટુકડીવાર છાવણી નાખવી : એફ્રાઈમના વંશજેના આગેવાન એલિશામા બિન અમિહુદની આગેવાની હેઠળ ૪૫,૫૦૦ માણસો. એના પછી મનાશાના વંશજેના આગેવાન ગમલિયેલ બિન પદાહસોરની આગેવાની હેઠળ ૩૨,૨૦૦ માણસો. બિન્યામીનના વંશજેના આગેવાન અબિદાન બિન ગિદોનીની આગેવાની હેઠળ ૩૫,૪૦૦ માણસો. એફ્રાઈમના વંશજેની છાવણીના માણસોની કુલ સંખ્યા ૧,૦૮,૧૦૦ . કૂચ કરતી વખતે તેઓ ત્રીજે સ્થાને રહે.':
        '“પશ્ચિમ બાજુએ એફ્રાઈમના વંશની સેનાના ધ્વજ હેઠળના લોકોએ નીચેના આગેવાનો હેઠળ ટુકડીવાર છાવણી નાખવી : એફ્રાઈમના વંશજેના આગેવાન એલિશામા બિન અમિહુદની આગેવાની હેઠળ ૪૦,૫૦૦ માણસો. એના પછી મનાશાના વંશજેના આગેવાન ગમલિયેલ બિન પદાહસોરની આગેવાની હેઠળ ૩૨,૨૦૦ માણસો. બિન્યામીનના વંશજેના આગેવાન અબિદાન બિન ગિદોનીની આગેવાની હેઠળ ૩૫,૪૦૦ માણસો. એફ્રાઈમના વંશજેની છાવણીના માણસોની કુલ સંખ્યા ૧,૦૮,૧૦૦ . કૂચ કરતી વખતે તેઓ ત્રીજે સ્થાને રહે.',
    # Matthew 5:19: stray lone ે after કોઈ -> drop (verb is just કોઈ)
    'જે કોઈે આજ્ઞાઓનું': 'જે કોઈ આજ્ઞાઓનું',
    # Kirtansagar #103: જ્યાં િ છનવાયે -> જ્યાં નિજ છવાયે (confirmed)
    'જ્યાંિ છનવાયે': 'જ્યાં નિજ છવાયે',
    'જ્યાં િ છનવાયે': 'જ્યાં નિજ છવાયે',
    'જ્યાં છિનવાયે': 'જ્યાં નિજ છવાયે',
    # Kirtansagar #267: 'પુત્ર વની મને' -> 'પુત્ર વિના મને' (વની=without; the
    # token વની is valid elsewhere e.g. દેવની, so fix only this phrase).
    'પુત્ર વની મને': 'પુત્ર વિના મને',
    # --- Pass-4 remaining-review (verified vs raw + native reading) ---
    # Song 2: જેજે = જે જે (two separate words) — runs BEFORE the જેજે->જોજે
    # whole-word rule below so this context wins.
    'જેજે કરશે': 'જે જે કરશે',
    # Song 239: મશાંતિ -> ને શાંતિ (liturgical 'glory ... and peace')
    'મહિમા ! મશાંતિ': 'મહિમા ! ને શાંતિ',
    'મહિમા! મશાંતિ': 'મહિમા! ને શાંતિ',
    # Song 518: આર્જતના -> અરજ તણા ('hearer of our petitions')
    'અમ આર્જતના સુણનારા': 'અમ અરજ તણા સુણનારા',
    # Bible Pass-5 phrase-scoped (whole-word would hit valid forms elsewhere):
    # Jeremiah 31:13 'આનંદ માણશો' -> 'આનંદ માણશે' (3rd-person; Isaiah 55:2
    # 'મોજ માણશો' 2nd-person is valid and untouched).
    'આનંદ માણશો.': 'આનંદ માણશે.',
    # Sirach 19:5 stray standalone ચ between two sentences.
    'લેવી. ચ જે ભોગવિલાસ': 'લેવી. જે ભોગવિલાસ',
    # --- Stations-of-the-Cross ordinal headings (Songs 283/284) ---
    # Source renders digits as consonants + stray spaces before the ordinal
    # suffix. Normalize each 'N<space>suffix સ્થાન' heading. Scoped to the exact
    # 'સ્થાન' heading context so standalone ર/પ/જું/મું elsewhere are untouched.
    '૧ લું સ્થાન': '૧લું સ્થાન',
    'ર જું સ્થાન': '૨જું સ્થાન',
    '૩ જું સ્થાન': '૩જું સ્થાન',
    '૪ થું સ્થાન': '૪થું સ્થાન',
    'પ મું સ્થાન': '૫મું સ્થાન',
    '૬ ઠ્ઠું સ્થાન': '૬ઠ્ઠું સ્થાન',
    '૬ ઠું સ્થાન': '૬ઠ્ઠું સ્થાન',
    '૭ મું સ્થાન': '૭મું સ્થાન',
    '૮ મું સ્થાન': '૮મું સ્થાન',
    '૯ મું સ્થાન': '૯મું સ્થાન',
    '૧૦ મું સ્થાન': '૧૦મું સ્થાન',
    '૧૧ મું સ્થાન': '૧૧મું સ્થાન',
    '૧ર મું સ્થાન': '૧૨મું સ્થાન',
    '૧૩ મું સ્થાન': '૧૩મું સ્થાન',
    '૧૪ મું સ્થાન': '૧૪મું સ્થાન',
}

# whole-word replacements: {wrong: right}
# NOTE: these fire only as STANDALONE words (Gujarati-letter boundaries), so a
# short token like 'તં' will never match inside a larger correct word.
WORD_FIXES = {
    'સજ્યાં': 'સર્જ્યાં',
    'સજ્યું': 'સર્જ્યું',
    # Bible Pass 13 — Psalm 119:172 (OT/46/119/172). SOURCE DEFECT: the raw token
    # yk¿kyku lacks the extra k that carries the long-ā after જ્ઞ. Correctly
    # encoded yk¿kkyku -> આજ્ઞાઓ already decodes right (no entry needed); the
    # decoder must NOT invent the missing byte, so this is lexical. Same-chapter
    # 119:176 uses the correct plural as an internal control. (×1 in corpus.)
    'આજ્ઞઓ': 'આજ્ઞાઓ',
    # Bible Pass 14 — SOURCE DEFECT: source wrote half-dha æ(e6, ધ્) where this
    # word family needs half-gha Î(ce, ઘ્). Decoder is faithful to both glyphs, so
    # this is lexical, not a converter remap (remapping æ would corrupt every real
    # ધ્ word). Same-edition control f]íkÎLkeyku -> કૃતઘ્નીઓ (Luke 6:35) already
    # decodes correctly. Each deficient form occurs once in the live Bible.
    'કૃતધ્નતા': 'કૃતઘ્નતા',  # Wisdom 14:26 (OT/25/14/26); f]íkæLkíkk
    'કૃતધ્ની': 'કૃતઘ્ની',    # 2 Timothy 3:2 (NT/16/3/2);  f]íkæLke
    # 1st/2nd person pronouns {U / íkU. NOTE (Pass 12): the GopikaTWO_N glyph
    # evidence shows raw U actually encodes ે+ં, so these ARE decoder-level ેં
    # words, not an exception. They stay here only because the Pass-12 decoder
    # fix is deliberately bounded to the ખ+U/ફ+U stems (a global U->ut would
    # cross frozen boundaries like પહાંચ-). If/when the global U mapping is
    # approved, these two standalone pronouns should move into the decoder and
    # be removed here. See BIBLE_AUDIT_PASS12_RESOLUTION.md.
    'તં': 'તેં',    # 'you did' (íkU ×305)
    'મં': 'મેં',    # 'I/me'    ({U ×291)
    # FULL-consonant + k spurious-aa that is lexical (same ambiguity as સવાર):
    'હાવા': 'હવા',      # air/wind (nkðk)
    'હાવાને': 'હવાને',
    'હાવામાં': 'હવામાં',
    # --- Kirtansagar Pass-1 audit (verified against raw bytes) ---
    # Source defects: reph genuinely absent/misplaced in the source bytes
    # (same class as સજ્યાં). Decoder must not invent the reph.
    'સજ્ર્યો': 'સર્જ્યો',   # MkßÞkuo (×2) - 'created'
    'અપ્ર્યો': 'અર્પ્યો',   # yÃÞkuo (×1) - 'offered'
    # Source spelling: standard Gujarati is મબલખ (source literally has ક = f).
    'મબલક': 'મબલખ',        # {çk÷f (×4) - 'abundant'
    # 'ò'+z ligature for જોડ not caught by the òu[EÞ] rule; single rare word.
    'અજેડ': 'અજોડ',        # yòuz (×1) - 'matchless'
    # Digit-for-consonant source typo: ૫(5) used for પ.
    '૫ણ': 'પણ',            # '૫ણ' -> 'પણ' (but)
    # --- Kirtansagar Pass-2 (verified against raw bytes) ---
    # Source defects: reph genuinely MISSING in the source bytes (no reph glyph)
    'ઉતાયું': 'ઉતાર્યું',   # WíkkÞwO (×5) - 'lifted/saved'
    'તાયું': 'તાર્યું',     # standalone (×1) - 'saved'
    'નિમ્ર્યો': 'નિર્મ્યો', # rLkBÞkuo (×2) - reph-order on મ્ cluster
    'અપ્રિત': 'અર્પિત',     # (×1) stray - 'offered' (reph order)
    # Digit-for-consonant: ૫ used for પ
    '૫ાપનો': 'પાપનો',       # (×1)
    # Phrase: Song 267 only (દેવની elsewhere is correct, untouched)
    # --- Kirtansagar Pass-3 source defects (verified vs raw bytes) ---
    'શ્રધ્ધા': 'શ્રદ્ધા',   # ©æÄk - source has ધ્ધ; standard દ્ધ
    'આતમા': 'આત્મા',        # ykík{k - source wrote આતમ (no conjunct)
    'તારૂં': 'તારું',       # íkkYt - source used રૂ(long); standard ું
    'મારૂં': 'મારું',       # {kYt
    'કરૂણા': 'કરુણા',       # fYýk - long ૂ -> short ુ
    'હૈયુ': 'હૈયું',         # niÞw - missing anusvara
    'જયારે': 'જ્યારે',      # sÞkhu - source જય, standard જ્ય
    'ત્યા': 'ત્યાં',        # missing anusvara (Song 57; whole-word only)
    'પરણામ': 'પ્રણામ',      # Ãkhýk{ - source પરણ, standard પ્રણ
    'મત્યુને': 'મૃત્યુને',  # {íÞwLku - missing ૃ
    'ઠયાં': 'થયાં',         # XÞkO - source ઠ for થ
    'યિજ્ઞક': 'યજ્ઞક',      # Þkr¿kf - stray short-i
    # --- Pass-4 remaining-review whole words (verified vs raw + native) ---
    'જેજે': 'જોજે',         # òusu/òuòu - ò ligature જો ('look/see'); Song 2 'જે જે'
                            #   handled by the phrase fix above (runs first).
    'જેજન': 'જોજન',         # òusLk - 'yojan' (distance measure)
    'જેજનો': 'જોજનો',       # òusLkku
    'સંથે': 'કંઠે',         # MkUÚku - 'around the neck' (dew-pearl necklace)
    'ચકરઈ': 'ચકરાઈ',        # [fhE - missing ા
    'તાજપ': 'તાજગી',        # íkksÃk - 'freshness'
    'મહાત': 'માત',          # {nkík - 'defeated' (Song 236)
    'મિરિયમ': 'મરિયમ',      # r{rhÞ{ - Mary; book standard is મરિયમ
    'મિરિયમની': 'મરિયમની',
    # --- Bible Pass-1 stragglers (òu{=મ kept as જે; su=જે ligature cases) ---
    'તેજેમય': 'તેજોમય',     # íkuòu{Þ - 'radiant' (òu{ ambiguous, lexical)
    'જેરકડી': 'જોરકડી',     # suhfze - 'forcibly'
    'જેરોજ': 'જોરોજ',
    # òu+r(short-i) stragglers -> જો (twins etc.)
    'જેડિયો': 'જોડિયો', 'જેડિયા': 'જોડિયા', 'જેડિયાં': 'જોડિયાં',
    'ઝંજેડી': 'ઝંઝોડી',
    # Source defect: missing reph (no ર byte), like સજ્યાં
    'વિચાયું': 'વિચાર્યું',  # rð[kÞwO (×40) - 'thought'
    # --- Bible Pass-2 source defects (verified vs raw) ---
    'ક્હ્યું': 'કહ્યું',     # õÌkwt (×2) - source ક્હ instead of કહ
    'તેમણ': 'તેમણે',        # íku{ý (×1) - missing final ે (Mark 5:39)
    'જઈશ્વરનું': 'ઈશ્વરનું', # sEïhLkwt (×1) - stray leading જ (Luke 20:19)
    'ંબધા': 'બધા',          # tçkÄk (×1) - stray leading anusvara (Joshua 20:9)
    '૫ારેવાનાં': 'પારેવાનાં',# digit ૫ for પ (Leviticus 14:30)
    'ઇસા્રયલીઓનાં': 'ઇસ્રાયલીઓનાં',  # RMkkúÞ - aa before ્ર (×1)
    # stray leading ચ ([ byte) before an otherwise complete word (Sirach cluster)
    'ચઅને': 'અને', 'ચઅભિમાની': 'અભિમાની', 'ચતેણે': 'તેણે',
    'ચપ્રભુ': 'પ્રભુ', 'ચપ્રભુથી': 'પ્રભુથી', 'ચપણ': 'પણ',
    'ચમારા': 'મારા', 'ચજ્યારે': 'જ્યારે', 'ચપહેલા': 'પહેલા',
    'ચપહેલાં': 'પહેલાં',
    # --- Bible Pass-3 source defects (verified vs raw) ---
    'વતું': 'વર્તું',       # ðíkwO (×2) - source missing reph
    'માશે': 'માયે',         # {kþu (×1) - source શ for ય (Luke 1:14)
    'તેણો': 'તેણે',         # íkuýku (×1) - ણો for ણે (Genesis 24:67)
    'તેમન': 'તેમને',        # íku{Lk (×1) - missing ે (Mark 10:13)
    'કરીન': 'કરીને',        # fheLk (×1) - missing ે (Genesis 18:2)
    'હુ': 'હું',            # nw (×2) - missing anusvara (whole-word only)
    'એવુ': 'એવું',          # yuðw (×1) - missing anusvara
    'સાંપ્યુ': 'સાંપ્યું',  # MkkUÃÞw (×1) - missing anusvara
    # damaged section headings
    'નિયમા': 'નિયમો',       # rLkÞ{k (×3) - heading 'rules'
    'અન્નબલિઆ': 'અન્નબલિ',  # heading fragment, stray trailing આ (Lev 6:6)
    # --- Bible Pass-4 source defects (missing reph / consonant typo) ---
    'મયું': 'મર્યું',       # {ÞwO - 'died' (source missing reph)
    'નયું': 'નર્યું',       # LkÞwO - 'sheer/pure'
    'ઠયું': 'થયું',         # XÞwO - source ઠ for થ
    # malformed join in 1 Sam 29:2 source
    'માણસાપલિસ્તીઓએ': 'માણસો; પલિસ્તીઓએ',
    # --- Bible Pass-5 source defects (verified vs raw) ---
    'ચગુસ્સે': 'ગુસ્સે',    # [økwMMku - stray leading ચ (Sirach 19:18)
    'ચ"હું': '"હું',        # ["nwt - stray leading ચ (Sirach 19:21)
    'મંન': 'મન',            # {tLk - extra anusvara (Psalms 119:32)
    'થથરતો': 'થરથરતો',      # ÚkÚkhíkku - duplicated syllable (2 Macc 3:17)
    'અંતને': 'અંતના',       # ytíkLku - wrong ending (Daniel 11:40)
    'માણસેને': 'માણસોને',   # {kýMkukLku - wrong ending (1 Chr 19:3)
    'કેવે': 'કેવા',         # fuðu - agreement (1 Cor 15:35)
}

# Word-INITIAL prefix normalizations. Fire only at the start of a word
# (Gujarati-letter boundary before). Each verified that EVERY corpus word with
# this prefix should take the replacement.
PREFIX_FIXES = {
    # Source alternates સરજ-/સર્જ- for the 'create' root; normalize to સર્જ-
    # (the standard form, already present in the same book). All ~28 inflections
    # (સરજનહાર, સરજ્યો, સરજાશે, સરજેલી, …) are the create-root -> સર્જ-.
    'સરજ': 'સર્જ',
    # Same pattern for the 'offer' root: source alternates અરપ-/અર્પ-; the book
    # overwhelmingly uses અર્પ- (અર્પણ ×41 etc.). All અરપ- forms (અરપું/અરપે/
    # અરપી/અરપો) are the offer-root. Guarded word-initial.
    'અરપ': 'અર્પ',
    # Source byte U(0x55)=anusvara in most words, but the 'distribute' root needs
    # ેં: વહંચ- -> વહેંચ- (all ~155 inflections are the distribute root).
    'વહંચ': 'વહેંચ',
}

# precompile a word-boundary-ish pattern. Gujarati has no \b word boundary that
# works well, so we anchor on non-letter / string edges around the token.
_GUJ = r'઀-૿'
_patterns = [
    (re.compile(r'(?<![' + _GUJ + r'])' + re.escape(w) + r'(?![' + _GUJ + r'])'), r)
    for w, r in WORD_FIXES.items()
]
# word-initial prefix: Gujarati letter boundary before, letter-continuation after
_prefix_patterns = [
    (re.compile(r'(?<![' + _GUJ + r'])' + re.escape(p) + r'(?=[' + _GUJ + r'])'), r)
    for p, r in PREFIX_FIXES.items()
]


def apply_lexical_fixes(text):
    """Apply confirmed phrase + whole-word + prefix source-defect corrections."""
    for wrong, right in PHRASE_FIXES.items():
        text = text.replace(wrong, right)
    for pat, repl in _prefix_patterns:
        text = pat.sub(repl, text)
    for pat, repl in _patterns:
        text = pat.sub(repl, text)
    return text


if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    tests = [
        'આકાશ અને પૃથ્વી સજ્યાં.',
        'ઈશ્વરે આ બધું સજ્યું.',
        'સજ્યાંત',   # must NOT fire (not a standalone word)
    ]
    for t in tests:
        print(f"{t!r} -> {apply_lexical_fixes(t)!r}")
