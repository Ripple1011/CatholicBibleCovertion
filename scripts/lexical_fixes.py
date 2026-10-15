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
}

# precompile a word-boundary-ish pattern. Gujarati has no \b word boundary that
# works well, so we anchor on non-letter / string edges around the token.
_GUJ = r'઀-૿'
_patterns = [
    (re.compile(r'(?<![' + _GUJ + r'])' + re.escape(w) + r'(?![' + _GUJ + r'])'), r)
    for w, r in WORD_FIXES.items()
]


def apply_lexical_fixes(text):
    """Apply confirmed whole-word source-defect corrections to converted text."""
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
