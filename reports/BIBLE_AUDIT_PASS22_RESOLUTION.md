# Resolution of Bible Spelling Audit — Pass 22

## Family A — extra half-ka in the sent-verb form (FIXED, lexical)

One bounded **source-defect** correction: `મોક્લ્યો` → `મોકલ્યો` at **John 10:36**
(NT/4/chapters/10/36). The source uses half-form ka ક્ where the verb needs full
ka ક.

### Raw-byte proof
    deficient  {kuõÕÞku  (hex 7b 6b 75 f5 d5 de 6b 75) -> મોક્લ્યો   (õ=f5=ક્ half-ka)
    control    {kufÕÞku  (hex 7b 6b 75 66 d5 de 6b 75) -> મોકલ્યો   (f=66=ક  full-ka)
    differ at ONE position: õ(ક્) vs f(ક); both keep ÕÞ = લ્ય conjunct

The decoder is FAITHFUL to both glyphs (verified: õ->ક્, f->ક). The source word
simply carries an extra half-form. A global õ->f or ક્->ક remap would destroy
genuine conjuncts, so this is a LEXICAL whole-word correction removing only the
FIRST virama (after ક); the valid લ્ય conjunct is retained:

    current:  મ ો ક ્ લ ્ ય ો   (two viramas)
    expected: મ ો ક   લ ્ ય ો   (one virama — the લ્ય)

### Same-edition controls
John 3:17 and John 17:18 (same Gospel, same "sent into the world" construction)
use the correct મોકલ્યો. The correct form appears 203× in the corpus; the
deficient મોક્લ્યો appears exactly once. GujaratiLexicon / internal usage support
the standard spelling (not another translation).

## Implementation
One WORD_FIXES entry in scripts/lexical_fixes.py with the existing Gujarati
boundary guard:

    'મોક્લ્યો': 'મોકલ્યો',  # John 10:36

No decoder/table/source/trace change; no õ->f remap; no prefix rule; no PHRASE
entry; no direct JSON patch.

## Verification (full rebuild)
- Complete Bible vs post-Pass-21 baseline: **exactly 1 verse value changed**
  (NT/4/10/36), length 184 -> 183 (one U+0ACD virama removed at offset 82, as the
  handoff predicted). No other value/key/metadata change.
- Deficient મોક્લ્યો removed from the ENTIRE corpus (1 -> 0); correct મોકલ્યો
  203 -> 204. John 3:17 & 17:18 controls unchanged.
- Preserved: મોકલ્યા (159), મોકલ્યું (19), ક્લેશ (2) and other genuine ક્લ/conjunct
  words untouched.
- Total verses unchanged (34891); 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace keeps source provenance.
- Regression 165/165 (2 decoder-faithfulness cases õ/f + lexical positives +
  in-situ + idempotence + prefix/suffix boundary negatives + preservation words).
  Build test_verse_keys.py + anomaly scan unchanged. Pass 13-21 retained.

## Carried forward (unchanged)
Pass 20 Numbers 28:12-13 quantities remain review-only. Review queue (Hebrews
11:23 ડયાં, Rev 1:9, જોનારો, ત્યાંને, પટી, અપ્યાં, ખંચાવું, પરાકાષ્ટા) on hold.
Global-U / સાંપ- held. વિષ્ટા preserved. Native-reader/publisher proofread and
written publisher permission remain the gates before shipping.
