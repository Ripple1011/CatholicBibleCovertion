# Resolution of Bible Spelling Audit — Pass 17

## Family A — erroneous digit in Ephraim's census figure (FIXED, lexical)

One bounded **source-defect** correction: `૪૫,૫૦૦` → `૪૦,૫૦૦` (Ephraim's count)
inside the grouped Numbers 2:24 value (OT/4/chapters/2/24; the figure is
conventionally Numbers 2:19).

### Raw-byte proof
The source token is ASCII `45,500` (hex `34 35 2c 35 30 30`); the font table
pairs `5`->૫ and `0`->૦, so the converter FAITHFULLY renders ૪૫,૫૦૦. The error is
the source digit, not the decoder. Remapping digits would be absurd, so this is a
full-value LEXICAL (PHRASE_FIXES) correction.

### The evidence is internally decisive (arithmetic)
The value's OWN stated western-camp subtotal is ૧,૦૮,૧૦૦ (108,100):

    current:  45,500 + 32,200 + 35,400 = 113,100   (off by 5,000)
    required: 108,100 - 32,200 - 35,400 = 40,500
    fixed:    40,500 + 32,200 + 35,400 = 108,100    ✓ reconciles

Same-edition control: Numbers 1:33 reads ૪૦,૫૦૦ for Ephraim. USCCB gives 40,500
at Numbers 2:19 and 108,100 at 2:24 (corroboration only; no wording imported).

## Implementation
One exact full-value entry added to PHRASE_FIXES in scripts/lexical_fixes.py
(the whole 417-char stored value as key, with only the one digit changed). No
WORD_FIXES bare-number entry; no decoder/table/extractor/builder/source/trace
change; no direct JSON patch; no change to number conversion.

## Verification (full rebuild)
- Complete Bible vs post-Pass-16 baseline: **exactly 1 verse value changed**
  (OT/4/2/24), a SINGLE code point at offset 158: ૫ (U+0AEB) -> ૦ (U+0AE6), same
  length. No other value/key/key-order/name/metadata change.
- Arithmetic now reconciles (40500+32200+35400 = 108100 = stated subtotal).
- Protected numbers untouched: Gad ૪૫,૬૫૦ (×2, Numbers 2 south camp), Gad ૪૦,૫૦૦
  at Numbers 26:18 (different census). Grouping intact: no new key 19, placeholder
  at 18 and absent keys 19-23 preserved.
- Total verses unchanged (34891); 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace keeps source provenance.
- Regression 146/146 (added full-value phrase fix + idempotence + protected-
  number negatives ૪૫,૫૦૦ bare / ૪૫,૬૫૦ / ૪૦,૫૦૦). Build test_verse_keys.py now
  also asserts the Numbers 2:24 reconciliation. Anomaly scan unchanged.
- Pass 13-16 corrections retained (આજ્ઞાઓ, કૃતઘ્ન-, person/place, Luke 6:36).

## Carried forward (unchanged)
Global-U / પહાંચ- / સાંપ- decisions held. Review-only: Rev 1:9 સિંન્નધ્યમાં,
જોનારો/જેનારો, ત્યાંને, પટી, અપ્યાં, nasal-t ખંચાવું, Wisdom 14:27 પરાકાષ્ટા.
વિષ્ટા preserved. Native-reader/publisher proofread and written publisher
permission remain the gates before shipping.
