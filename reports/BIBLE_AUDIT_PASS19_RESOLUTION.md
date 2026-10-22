# Resolution of Bible Spelling Audit — Pass 19

## Family A — truncated oath in Genesis 14:22 (FIXED, phrase-level)

The agent flagged Genesis 14:22 ending in a bare `ક` (likely incomplete `કે`)
but could NOT retrieve the source evidence, so it held the finding as review-only.
This resolution CLOSED that evidence gap via direct APK source inspection and,
with maintainer approval, implemented the confirmed correction.

    Before (OT/1/14/22): ...પ્રભુ પરમેશ્વર આગળ સોગંદ લીધા છે ક
    After  (OT/1/14/22): ...પ્રભુ પરમેશ્વર આગળ સોગંદ લીધા છે કે

Verse 23 begins "મારે તારી કોઈપણ વસ્તુ ન લેવી..." — the oath is "I have sworn
THAT [I will take nothing]", so the connective કે is required.

### Source-byte proof (what the agent lacked)
Source asset `assets/0/1/14.html`
(sha256 8526a36e1f5c07eb897fae2962061bb97056448d2a3ff541090286cfcef971e5).
The raw v22/v23 boundary is:

    ...MkkuøktË ÷eÄk Au f\n<a id="v23" name="v23">23</a> {khu íkkhe f

The verse ends in a LONE raw byte `f` (=ક) with NO following matra byte. `fu`
would be needed for `કે` (f=ક, u=ે) and it is absent. So the decoder (f->ક) and
the extractor (verse boundary at the v23 anchor) are BOTH faithful — the SOURCE
word is truncated. The trace record confirms it:
`{"u":"ક","raw":"f","hex":"66","refs":["Genesis 14",...],"n":7}`.

### Why කే and why safe
- "છે કે" ("...is/has ... that ...") occurs 982× in this edition.
- Genesis 14:22 is the ONLY verse in the entire Bible ending in a bare ` ક`.
So the intended word is unambiguous and the correction is isolated.

## Implementation
One exact full-value entry in PHRASE_FIXES (scripts/lexical_fixes.py) adding the
missing ે matra. IMPORTANT pipeline detail: apply_lexical_fixes runs PHRASE_FIXES
BEFORE the મં->મેં WORD_FIX, so the phrase key uses the decode-stage form “મં
(not the final “મેં); the WORD_FIX then produces “મેં in the same call. (Verified
by the full rebuild diff — testing only against the stored JSON value, which
already has મેં, would have silently no-op'd.) No decoder/extractor/source/trace
change; verse keys v22 and v23 kept separate.

## Verification (full rebuild)
- Complete Bible vs post-Pass-18 baseline: **exactly 1 verse value changed**
  (OT/1/14/22), +1 char (ે matra), ending ...છે ક -> ...છે કે.
- v22 and v23 remain separate keys; v23 unchanged; verses NOT joined.
- No verse ends in a bare ` ક` anymore (was 1, now 0).
- Total verses unchanged (34891); 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace keeps source provenance.
- Regression 150/150 (phrase fix + bare-ક negatives); build test_verse_keys.py
  and anomaly scan unchanged. Pass 13-17 corrections retained.

## Carried forward (unchanged)
Hebrews 11:23 ડયાં remains review-only (Pass 18). Global-U / પહાંચ- / સાંપ-
decisions held. Other review-queue items unchanged. Native-reader/publisher
proofread and written publisher permission remain the gates before shipping.
