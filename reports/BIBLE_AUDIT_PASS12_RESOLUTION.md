# Resolution of Bible Spelling Audit — Pass 12

## Family A — raw U glyph carries e-matra + anusvara, not just anusvara (FIXED, bounded)

This pass **corrects a long-standing documented assumption.** The decoder's
`EXTRA` table mapped raw `U`(0x55) to a bare anusvara `ં`. The Pass-12 audit
inspected the original font `source_assets/assets/GopikaTWO_N.TTF` and proved,
by glyph-outline comparison, that `U` has TWO contours:

- the FIRST contour is byte-for-byte identical to the entire `u`(e-matra ે)
  glyph — all 20 points and their on/off-curve flags;
- the SECOND contour is the nasal dot.

Independently reproduced in this repo's font: U contours = 2, u contours = 1,
first-contour identical = True, 20 points, contour
SHA-256 = `8563066f2fb962f13985e9259c58bfe5961c8eaee9497bf702ce231075201e3e`
(matches the handoff). So raw `U` = `ે` + `ં` = the raw pair `ut`. The legacy
`U->ં` mapping silently dropped the e-matra, producing valid-looking nasalized
forms that malformed-Unicode checks could not catch (e.g. ખેંચીને -> ખંચીને).

### Fix (bounded raw-stream expansion)
At the start of `convert()`, before any normalization/classification:

    s = re.sub(r'(?<=¾)U|(?<=V)U', 'ut', s)

We anchor on the STEM CONSONANT — raw `¾`(ખ) or `V`(ફ) immediately before U —
so every inflection of the two demonstrated stems is covered uniformly (plain
ચ/ક followers AND the ચ્ય/ક્ય conjuncts: ¾Uå->ખેંચ્ય-, VUõ->ફેંક્ય-).

### Why bounded, not global
A global `U->ut` was measured over the whole corpus and would rewrite **381
distinct forms**, including **60+ explicitly-frozen `પહાંચ-` words** (->પહોંચ-)
and the `સાંપ-` (aa+U) family (->સોંપ-). Those are held outside this release per
the standing do-not-change list. The bounded anchor is provably safe:
`પહાંચ-` is raw `h+U` (`ÃknkU[..`), which contains neither `¾U` nor `VU`;
`સાંપ-` is raw `MkkU..`; the nasal-only raw-`t` word `ખંચાવું` (`¾t[kðwt`, no U)
is untouched. All three verified unchanged (counts identical old/new: પહાંચ 719,
સાંપ 552, પહોંચ 9, સોંપ 10 — the latter two are genuine pre-existing source
forms, NOT introduced by this fix).

## Scope decision (maintainer-approved)
The handoff's literal candidate anchored on the follower (`U(?=\[)|U(?=f)`),
covering only plain ચ/ક. Two editorial choices were escalated and approved:
1. **Anchor on the stem consonant** (¾U/VU) so conjunct inflections
   (ખેંચ્યું/ફેંક્યો) are fixed consistently with ખેંચીને — otherwise the same
   two stems would be half-corrected.
2. **Include two further ફે- words** the ¾U/VU anchor reaches:
   `ફેંસલો`/`ફેંસલાની` (faisla, raw `VUMk..`) and `ફેંટો`/`ફેંટા` (raw `VUx..`).
   The SAME glyph evidence proves their U carries the e-matra, so ફંસલો/ફંટો
   were mis-decoded; these are genuine source-faithful restorations.

## Measured impact (full rebuild delta, not just the trace)
Compared the complete pre-Pass-12 build vs the rebuilt output, verse-by-verse.

**Bible: 189 verse values changed; 36 distinct word forms; 196 occurrences.**
Character-level audit: EVERY change is exactly an `ં` -> `ેં` e-matra insertion
(old form had anusvara-only, new form has e-matra+anusvara at the same position).
Zero non-conforming changes. Verse keys unchanged; 34891 verses; 236 placeholders.

Distinct forms (occurrences): ફેંકી×68, ખેંચી×53, ફેંસલો×18, ફેંકાઈ×7, ફેંટા×4,
ખેંચાઈ×4, ફેંકે×3, ફેંક્યો×3, ફેંકવામાં×3, ખેંચીને×2, ફેંટો×2, ખેંચતો×2, ખેંચે×2,
ખેંચેલા×2, ખેંચતા×2, and 21 further single-occurrence inflections (ફેંકવી,
ફેંકીને, ફેંકવા, ફેંકતો, ફેંક્યું, ફેંકતાં, ફેંકવાનાં, ચક્રફેંકની, ફેંકાય, ફેંકો,
ફેંકનાર, ફેંસલાની, ખેંચનાર, ખેંચાવું, ફેંકાવી, ખેંચ્યું, ખેંચ્યો, ખેંચતાં,
ખેંચાય, ખેંચ્યા, ખેંચતાણ).

The handoff's "minimum verified set" was 9 occurrences in 8 verses; the real
bounded impact is larger (as the handoff anticipated — "nine is the verified
minimum, not the full count"). Every changed form was enumerated with raw
evidence and confirmed to be an e-matra restoration.

**Songbooks** (shared converter — checked, not assumed): kirtansagar 15,
holi_gito 1, natal_garba 0 word changes, ALL pure `ં->ેં`, keys unchanged.

## Negative tests (must NOT change) — all verified
- Nasal-only raw-t `ખંચાવું` (`¾t[kðwt`, no U) -> stays ખંચાવું. (A separate
  raw-U variant `¾U[kðwt` correctly becomes ખેંચાવું; different source bytes.)
- Frozen `પહાંચ-` family (raw h+U): 719 occurrences unchanged.
- aa+U `સાંપ-` family: 552 occurrences unchanged (held for a future pass).
- Standalone pronoun lexical fixes {U->મેં, íkU->તેં: still work; now documented
  as decoder-level ેં words kept in the lexical layer only because the decoder
  fix is bounded.

## Documentation corrected (as the handoff required)
- gopika_decode.py header: the "U = anusvara only" note replaced with the
  two-contour (ે+ં) explanation.
- lexical_fixes.py pronoun note: updated to record that U genuinely carries the
  e-matra and these pronouns should migrate to the decoder if a global U mapping
  is ever approved.

## Verification summary
- Regression 119/119 (added 5 ખેંચ/ફેંક positives, 4 conjunct inflections,
  raw-t negative, aa+U control, frozen-પહાંચ control).
- Font contour proof reproduced (SHA-256 matches).
- Full rebuild delta: 189 Bible verses, all ં->ેં; songbooks all ં->ેં.
- Anomaly scan unchanged; 34891 verses; 236 placeholders; 46+27 canon.
- પહાંચ-/સાંપ- frozen families untouched; raw-t ખંચાવું untouched.

## Held outside this release (documented, not applied)
- GLOBAL U->ut (381 forms) — crosses frozen boundaries; needs explicit
  maintainer authorization to revise પહાંચ-/સાંપ-.
- aa+U family `સાંપ- -> સોંપ-` (same root cause) — held pending that decision.
- Review-only carried forward: Rev 1:9 સિંન્નધ્યમાં, જેનારો, ત્યાંને, પટી,
  અપ્યાં, and nasal-only `ખંચાવું` editorial question.

Native-reader/publisher proofread and written publisher permission remain the
gates before shipping.
