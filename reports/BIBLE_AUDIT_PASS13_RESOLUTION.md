# Resolution of Bible Spelling Audit — Pass 13

## Family A — missing long-ā in the plural of આજ્ઞા (FIXED, lexical)

One bounded **source-defect** correction: `આજ્ઞઓ` → `આજ્ઞાઓ` at **Psalm 119:172**
(`OT/46/chapters/119/172`). Classification confirmed against raw bytes:

    deficient source  yk¿kyku   = 79 6b bf 6b    79 6b 75  -> આજ્ઞઓ
    correct   source  yk¿kkyku  = 79 6b bf 6b 6b 79 6b 75  -> આજ્ઞાઓ
                                              ^^ the extra source k that
                                                 carries the genuine long-ā

The decoder is FAITHFUL to both: it correctly returns આજ્ઞઓ for the deficient
token and આજ્ઞાઓ for the correct one (verified). The source simply omits one `k`.
A decoder must not invent a byte that is not in the source — doing so would
violate the standing guardrail and risk the 249 correctly-encoded આજ્ઞાઓ forms.
So this is a LEXICAL whole-word correction, not a converter change.

### Internal control
Same chapter, Psalm 119:176, already reads the correct plural
("તારી આજ્ઞાઓ સદા હું તો રાખું યાદ") — direct same-edition corroboration, not a
substitution from another translation.

## Implementation
One entry added to `WORD_FIXES` in scripts/lexical_fixes.py:

    'આજ્ઞઓ': 'આજ્ઞાઓ',

using the module's existing Gujarati-block boundary guard
`(?<![઀-૿]) ... (?![઀-૿])`. No decoder change, no prefix rule, no `જ્ઞઓ`
broadening, no raw/trace edit, no direct JSON patch.

## Verification (full rebuild)
- Rebuilt via the normal pipeline; compared the complete Bible against the
  post-Pass-12 baseline: **exactly 1 verse value changed** — OT/46/119/172,
  only આજ્ઞઓ->આજ્ઞાઓ. Punctuation, wording, surrounding verses, headings all
  unchanged. Book name still "Psalms" (the trace's "Genesis 119" label was
  provenance only; no book/metadata/key change made).
- All three songbooks **byte-identical** to the post-Pass-12 baseline (the
  shared lexical entry matched only this one Bible word).
- Regression **127/127** (added a LEX_CASES section exercising
  apply_lexical_fixes: positive આજ્ઞઓ->આજ્ઞાઓ + in-situ verse context, and
  NEGATIVE boundary controls આજ્ઞાઓ/આજ્ઞાઓનું/આજ્ઞા/યજ્ઞો/જ્ઞાન unchanged,
  Gujarati-prefix કોઈઆજ્ઞઓ -> no whole-word match).
- Anomaly scan unchanged; 34891 verses; 236 placeholders; 46+27 canon.
- Raw trace still shows u="આજ્ઞઓ" (source provenance deliberately preserved;
  the overlay fixes published output, not historical source evidence).

## Carried forward (unchanged)
Global U mapping and `પહાંચ-`/`સાંપ-` decisions remain held. Review-only:
Rev 1:9 સિંન્નધ્યમાં, જોનારો/જેનારો, ત્યાંને, પટી, અપ્યાં, nasal-t ખંચાવું.
Native-reader/publisher proofread and written publisher permission remain the
gates before shipping.
