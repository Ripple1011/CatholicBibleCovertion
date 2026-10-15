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
    # Matthew 5:19: stray lone ે after કોઈ -> drop (verb is just કોઈ)
    'જે કોઈે આજ્ઞાઓનું': 'જે કોઈ આજ્ઞાઓનું',
    # Kirtansagar #103: જ્યાં િ છનવાયે -> જ્યાં નિજ છવાયે (confirmed)
    'જ્યાંિ છનવાયે': 'જ્યાં નિજ છવાયે',
    'જ્યાં િ છનવાયે': 'જ્યાં નિજ છવાયે',
    'જ્યાં છિનવાયે': 'જ્યાં નિજ છવાયે',
    # Kirtansagar #267: 'પુત્ર વની મને' -> 'પુત્ર વિના મને' (વની=without; the
    # token વની is valid elsewhere e.g. દેવની, so fix only this phrase).
    'પુત્ર વની મને': 'પુત્ર વિના મને',
}

# whole-word replacements: {wrong: right}
# NOTE: these fire only as STANDALONE words (Gujarati-letter boundaries), so a
# short token like 'તં' will never match inside a larger correct word.
WORD_FIXES = {
    'સજ્યાં': 'સર્જ્યાં',
    'સજ્યું': 'સર્જ્યું',
    # 1st/2nd person pronouns: source byte U(0x55) is anusvara ં in most words
    # (નોંધ, પહોંચી...) but these two pronouns need ેં. Fixing the decoder would
    # corrupt the anusvara words, so correct the two pronouns here.
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
