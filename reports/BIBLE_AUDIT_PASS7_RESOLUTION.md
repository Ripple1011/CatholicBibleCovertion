# Resolution of Bible Spelling Audit — Pass 7

## Family A — completed conjunct cores lose their o-matra (converter bug, FIXED)

The agent's diagnosis was exact. The explicit `core+kku` -> o-matra handling
looped only over `_EXTRA_CORES`; cores `¿`(જ્ઞ) and `Ò`(ન્ન) live in
`_CONJ_CORE_T` only, so their `kku` fell through to the generic shortening,
leaving `¿t`+`u` -> જ્ઞ+ે. Result: યજ્ઞો -> યજ્ઞે, ઉન્નો -> ઉન્ને.

Fix: extend the `_CONJ_CORE_T` loop to handle the vowel contrasts explicitly,
in the right order:
- `core + kku` -> <uni> + ો   (NEW)
- `core + kki` -> <uni> + ૌ   (NEW, symmetry)
- `core + kk`  -> <uni> + ા   (existing aa case, preserved)
- `core + ku`  -> decodes to <uni> + ે  (PRESERVED — the critical distinction)

Result (all 6 forms, 14 Bible locations):
- યજ્ઞે 0 (was 7), યજ્ઞોની/થી/ત્સવ fixed, તત્ત્વજ્ઞે 0, ઉન્ને 0.
- યજ્ઞો now 12+ (incl. suffixes), તત્ત્વજ્ઞો 1, ઉન્નો 1.
- Controls verified preserved corpus-wide: આજ્ઞા 872 (aa case untouched),
  the e-matra `core+ku` forms unchanged, Pass-6 fixes intact.
- Proper-name safeguard (A6): ઉન્નો restores only the encoded vowel; consonants
  unchanged; not harmonized to another transliteration.

## Family B — જેનાર- / જોનાર- : REVIEW ONLY (NOT changed)

Genesis 37:19 જેનારો and 2 Macc 3:17 જેનારાને (raw òu+L). Context suggests the
'seeing' root (જોનારો), BUT `òu`+`L` is the intentionally PROTECTED જે decoding
(વંશજેને, પૂર્વજેના…). Per the handoff and maintainer instruction, these are left
UNCHANGED pending native-reader/publisher approval. `L` was NOT added to _JO_NEXT.
Verified: જેનારો still present (1), untouched.

## Verification
- Regression 89/89 (added 6 cases incl. e/aa contrast guards for જ્ઞ/ન્ન cores).
- Anomaly scan unchanged; verses 34891; 236 placeholders unchanged.
- Shared-converter: any songbook જ્ઞ-o-matra counterparts corrected the same way.
- All prior guardrails honored (સાંનિધ્ય, Isaiah 55:2 માણશો, ત્યાંને review,
  names, verse boundaries, English fields, canon).

## Note
Seven Bible passes have now each found progressively rarer, deeper edge cases.
This closes the completed-core o-matra path (sibling of Pass-6's short-i path).
Family B and a native-reader/publisher proofread remain the open items; do not
treat the converter as proven globally complete.
