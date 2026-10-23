# Resolution of Bible Spelling Audit — Pass 23

## Family A — duplicated reph marker in a future-tense verb (FIXED, lexical)

One bounded **source-defect** correction: `સમર્પીર્શ` → `સમર્પીશ` at **Micah 4:13**
(OT/38/chapters/4/13; index name "Micha").

### Raw-byte proof
    deficient  Mk{Ãkeooþ  (hex 4d 6b 7b c3 6b 65 6f 6f fe) -> સમર્પીર્શ
                                             ^^^^^ oo = two reph markers (6f 6f)
    control    yÃkeoþ     (hex 79 c3 6b 65 6f fe)          -> અર્પીશ  (single o)
    diagnostic Mk{Ãkeoþ   (one o removed)                  -> સમર્પીશ  (the expected form)

The decoder is FAITHFUL to the source: both `o`s are present and `reorder_gopika`
correctly makes two rephs. The first `o` forms the VALID ર્પ cluster; the second
adds an unwanted ર્ before final શ. So this is a LEXICAL correction removing only
the second ર્ — NOT a global oo->o rewrite or a reph-algorithm change:

    current:  સ મ ર ્ પ ી ર ્ શ
    expected: સ મ ર ્ પ ી     શ   (delete ર U+0AB0 + ્ U+0ACD before શ)

### Controls
Ezekiel 36:26 (OT/31/36/26) has the related single-reph future form અર્પીશ (raw
yÃkeoþ) — kept unchanged. The expected સમર્પીશ was otherwise absent from the Bible
(so it is a genuine correction, not already attested). Valid ર્પ words preserved:
સમર્પિત (64), સમર્પણ (24), plus the Pass-21/earlier સમર્પિત fixes.

## Implementation
One WORD_FIXES entry in scripts/lexical_fixes.py with the existing Gujarati
boundary guard:

    'સમર્પીર્શ': 'સમર્પીશ',  # Micah 4:13

No decoder/table/source/trace change; no oo->o remap; no prefix/phrase entry; no
direct JSON patch.

## Verification (full rebuild)
- Complete Bible vs post-Pass-22 baseline: **exactly 1 verse value changed**
  (OT/38/4/13), length 217 -> 215 (two code points ર+્ removed at offset 212, as
  the handoff predicted). No other value/key/metadata change.
- Deficient સમર્પીર્શ removed corpus-wide (1 -> 0); સમર્પીશ 0 -> 1. Ezekiel 36:26
  control unchanged; valid ર્પ words (સમર્પિત/સમર્પણ) untouched.
- Total verses unchanged (34891); 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace keeps source provenance.
- Regression 175/175 (2 decoder-faithfulness cases oo/single-o + lexical
  positives/in-situ/idempotence/prefix-suffix negatives/preservation). Build
  test_verse_keys.py + anomaly scan unchanged. Pass 13-22 retained.

## Carried forward (unchanged)
Pass 20 Numbers 28:12-13 quantities review-only. Review queue (Hebrews 11:23
ડયાં, Rev 1:9, જોનારો, ત્યાંને, પટી, અપ્યાં, ખંચાવું, પરાકાષ્ટા) on hold.
Global-U / સાંપ- held. વિષ્ટા preserved. Native-reader/publisher proofread and
written publisher permission remain the gates before shipping.
