# Resolution of Bible Spelling Audit — Pass 21

## Family A — reversed short-u / long-u vowel lengths (FIXED, lexical)

One bounded **source-defect** correction: `ખાતમૂહુર્ત` → `ખાતમુહૂર્ત` at
**Job 38:7** (OT/22/chapters/38/7). The two u-vowel LENGTHS are reversed.

### Raw-byte proof
    deficient  ¾kík{qnwíko  (hex be 6b ed 6b 7b 71 6e 77 ed 6b 6f) -> ખાતમૂહુર્ત
                             ^^ {q = મ+ૂ(long)   nw = હ+ુ(short)
    corrected raw order ¾kík{wnqíko -> ખાતમુહૂર્ત  ({w = મ+ુ, nq = હ+ૂ)
    markers: w(77)=ુ short-u ; q(71)=ૂ long-u

The decoder is FAITHFUL to both markers (verified: w->ુ, q->ૂ). The source word
simply has the two vowel lengths in the wrong order. Remapping q/w in the
converter would corrupt every genuine u-vowel, so this is a LEXICAL whole-word
correction.

### Same-edition control
Ecclesiasticus (Ben Sirah) 14:12 (OT/26/14/12) already reads the correct root
મુહૂર્ત — raw `{wnqíko` (w=ુ then q=ૂ, the right order). It decodes correctly with
no entry and is left unchanged. GujaratiLexicon lists the compound ખાતમુહૂર્ત and
the root મુહૂર્ત, supporting the corrected spelling (not another translation).

## Implementation
One WORD_FIXES entry in scripts/lexical_fixes.py with the existing Gujarati
boundary guard:

    'ખાતમૂહુર્ત': 'ખાતમુહૂર્ત',  # Job 38:7

No decoder/table/source/trace change; no q/w remap; no prefix rule; no PHRASE
entry needed; no direct JSON patch.

## Verification (full rebuild)
- Complete Bible vs post-Pass-20 baseline: **exactly 1 verse value changed**
  (OT/22/38/7), exactly TWO code-point swaps at the two u-vowels
  (U+0AC2 ૂ <-> U+0AC1 ુ), ZERO length change. No other value/key/metadata change.
- Job 38:6 placeholder `-` kept; protected કયું at verse end preserved.
- Sirach 14:12 control મુહૂર્ત unchanged.
- Total verses unchanged (34891); 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace keeps source provenance.
- Regression 155/155 (positive + in-situ + idempotence + control મુહૂર્ત +
  bare reversed-root negative). Build test_verse_keys.py + anomaly scan unchanged.
- Pass 13-19 corrections retained; Pass 20 quantities remain review-only.

## Carried forward (unchanged)
Review queue (Hebrews 11:23 ડયાં, Numbers 28:12-13 quantities, Rev 1:9, જોનારો,
ત્યાંને, પટી, અપ્યાં, ખંચાવું, પરાકાષ્ટા) all on hold. Global-U / સાંપ- held.
વિષ્ટા preserved. Native-reader/publisher proofread and written publisher
permission remain the gates before shipping.
