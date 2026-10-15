# Resolution of Kirtansagar Spelling Audit — Pass 2

## Converter bug (fixed structurally): the 'Š' reph+short-i glyph

`Š`(0x160) = reph ર્ + short-i િ as a PRE-BASE unit (JS table: ર્િ -> Š). It
rides ON the following consonant: `Š` + C(+inherent k) -> **ર્ + C + િ**. The
old handling misplaced it (મૂત્રિ instead of મૂર્તિ; the reph became a ત્ર
cluster). Fix: decode `Š`+half-form to `ર્` + the FULL consonant + `િ`, dropping
the half-form's inherent k.

Cleared whole families corpus-wide:
- મૂત્રિ -> મૂર્તિ (20) ; કીત્રિ -> કીર્તિ (4) ; સમપ્રિત -> સમર્પિત (2) ;
  પાથ્રિવ -> પાર્થિવ (2) ; અપ્રિત(stray via Š) -> અર્પિત ; અહન્રિશ -> અહર્નિશ ;
  મૂર્તિમંત, કીર્તિવંત, માત્રિન -> માર્તિન. All wrong forms now 0.

## Source defects / normalization (lexical_fixes.py)

| fix | kind | note |
|-----|------|------|
| સરજ- -> સર્જ- (prefix, ~28 inflections) | source orthography | book alternates સરજ-/સર્જ-; normalized to the standard form present in the same book. Guarded word-initial (વિસરજન untouched). |
| ઉતાયું -> ઉતાર્યું ; તાયું -> તાર્યું | source defect | reph genuinely absent in bytes |
| નિમ્ર્યો -> નિર્મ્યો | reph order (મ્ cluster) | ×2 |
| અપ્રિત -> અર્પિત | source/reph | ×1 |
| ૫ાપનો -> પાપનો | digit-for-consonant | ×1 (same class as ૫ણ) |
| 'પુત્ર વની મને' -> 'પુત્ર વિના મને' | phrase (Song 267) | દેવની elsewhere untouched |

## Left as REVIEW
- માત્રિન (Saint Martin): now decodes માર્તિન (closer; ત vs ટ is a source
  transliteration choice). Not forced to માર્ટિન.
- Ordinal artifacts (ર જું, ૪ થું, ૬ ઠું …): a separate number/ordinal
  formatting family; needs its own pass, not generic replacement.

## Verification
- Regression suite: 63/63 (added મૂર્તિ/કીર્તિ/સમર્પિત/પાર્થિવ/અહર્નિશ cases).
- Anomaly scan unchanged (0 real-bug classes); leftover Latin 0.
- All JSON regenerated.
