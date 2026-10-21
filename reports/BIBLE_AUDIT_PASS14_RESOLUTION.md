# Resolution of Bible Spelling Audit — Pass 14

## Family A — source half-dha ધ્ where the word needs half-gha ઘ્ (FIXED, lexical)

Two bounded **source-defect** corrections in one word family (ingratitude):

| Reference | Path | Before | After |
|---|---|---|---|
| Wisdom 14:26 | OT/25/chapters/14/26 | કૃતધ્નતા | કૃતઘ્નતા |
| 2 Timothy 3:2 | NT/16/chapters/3/2 | કૃતધ્ની | કૃતઘ્ની |

### Raw-byte proof
The half-consonant glyphs differ by one source character:

    A1 Wisdom:   f]íkæLkíkk  = 66 5d ed 6b e6 4c 6b ed 6b 6b  -> કૃતધ્નતા
    A2 2 Tim:    f]íkæLke    = 66 5d ed 6b e6 4c 6b 65        -> કૃતધ્ની
    control:     f]íkÎLkeyku = 66 5d ed 6b ce 4c 6b 65 79 6b 75 -> કૃતઘ્નીઓ
                                      ^^ source æ(e6)=ધ્  vs  Î(ce)=ઘ્

The decoder is FAITHFUL to both glyphs (verified: æ->ધ્, Î->ઘ્). The source
simply wrote the wrong half-consonant. Remapping æ in the converter would corrupt
every genuine ધ્ word (મધ્ય, ધ્યાન, અધ્યક્ષ...), so this is a LEXICAL whole-word
correction — same discipline as Pass 13.

### Internal control
Same edition, Luke 6:35 (NT/3/6/35), already reads the correct કૃતઘ્નીઓ (source
Î). It decodes correctly with no entry and is left untouched — direct
same-edition corroboration, not a cross-translation import.

## Implementation
Two entries added to WORD_FIXES in scripts/lexical_fixes.py, using the module's
existing Gujarati-block boundary guard:

    'કૃતધ્નતા': 'કૃતઘ્નતા',  # Wisdom 14:26
    'કૃતધ્ની': 'કૃતઘ્ની',    # 2 Timothy 3:2

No decoder/table/source change; no prefix rule; no generic ધ્ન replacement; no
raw/trace edit; no direct JSON patch.

## Verification (full rebuild)
- Complete Bible compared vs the post-Pass-13 baseline: **exactly 2 verse values
  changed** (OT/25/14/26, NT/16/3/2), each a single ધ->ઘ substitution; all other
  text, keys, book names, and metadata identical.
- Luke 6:35 control unchanged; Pass-13 આજ્ઞાઓ correction retained.
- All three songbooks **byte-identical** to the post-Pass-13 baseline.
- Regression **137/137** (added positives + in-situ verse + idempotence controls
  કૃતઘ્નીઓ/કૃતઘ્નતા/કૃતઘ્ની + ધ-word negatives મધ્ય/ધ્યાન/અધ્યક્ષ + Gujarati-suffix
  boundary negative કૃતધ્નીઓ -> no match).
- Anomaly scan unchanged; 34891 verses; 236 placeholders; 46+27 canon.
- Raw trace keeps the uncorrected source readings (provenance preserved).

## Carried forward (unchanged)
Global U mapping and પહાંચ-/સાંપ- decisions remain held. Review-only: Rev 1:9
સિંન્નધ્યમાં, જોનારો/જેનારો, ત્યાંને, પટી, અપ્યાં, nasal-t ખંચાવું. Native-reader/
publisher proofread and written publisher permission remain the gates before
shipping.
