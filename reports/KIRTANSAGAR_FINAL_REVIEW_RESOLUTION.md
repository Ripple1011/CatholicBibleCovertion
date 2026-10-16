# Kirtansagar — Final Review Resolution (remaining queue, Passes 1-3)

Every remaining-review item was traced to raw Gopika bytes and resolved per the
handoff's native readings. All applied as phrase/whole-word lexical corrections
in `scripts/lexical_fixes.py` (no converter change was needed — these are source
defects, not conversion bugs).

## Section A/D — resolved
| item | song | current -> fixed | raw | kind |
|------|------|------------------|-----|------|
| સંથે -> કંઠે | 507 | 'પૃથ્વીને સંથે' -> 'કંઠે' | MkUÚku | source consonant typo |
| મહાત -> માત | 236 | 'થાયે નહીં મહાત' -> 'માત' | {nkík | source (whole-word; સુમહાતમ્ in Song 75 is a real word, untouched) |
| આર્જતના -> અરજ તણા | 518 | 'અમ આર્જતના સુણનારા' | yksoíkLkk | phrase |
| મિરિયમ -> મરિયમ | 367 | Mary; book standard મરિયમ | r{rhÞ{ | editorial consistency |
| તાજપ -> તાજગી | 90 | 'અંગઅંગમાં તાજગી' | íkksÃk | source |
| ચકરઈ -> ચકરાઈ | 511 | 'આભા ચકરાઈ રહી' | [fhE | source (missing ા) |
| મશાંતિ -> ને શાંતિ | 239 | 'મહિમા ! ને શાંતિ' | {þktrík | phrase (liturgical) |

## Section B/C — જેજે / જેજન (the ò=જો ligature, resolved per context)
- Song 2: `જેજે કરશે` -> `જે જે કરશે` (two words) — phrase fix, runs first.
- Songs 11/208/231/334: `જેજે` -> `જોજે` ('look/see') — whole-word.
- Song 71: `જેજન` -> `જોજન` ('yojan', distance) — whole-word.
Raw: òusu/òuòu/òusLk (ò ligature + જ). Handled as lexical (context-dependent,
so NOT a blanket converter rule).

## Section E — Stations-of-the-Cross ordinals (Songs 283/284)
Source rendered digits as consonants with stray spaces (ર=૨, પ=૫, ૧ર=૧૨) before
the ordinal suffix. Normalized the 14 'N<space>suffix સ્થાન' headings to
૧લું/૨જું/૩જું/૪થું/૫મું/૬ઠ્ઠું/૭મું…/૧૪મું સ્થાન. Scoped to the 'સ્થાન'
heading context so standalone ર/પ/જું/મું elsewhere are untouched.

## Section F — kept as-is (per handoff)
નવ, માર્તિન, પરથમ, પુત્તર, નાહીં, ર્હે/ર્હેજે, પહાંચ/પ્હાંચ, કરજા — archaic/
poetic/devotional; not auto-corrected.

## Verification
- All target forms present; suspect forms zero (મશાંતિ/સંથે/ચકરઈ/આર્જતના/જેજન/
  તાજપ/'ર જું'/'૧ર મું' = 0). Remaining 'મહાત' ×1 is સુમહાતમ્ (Song 75, correct).
- Song 2 reads 'જે જે' (not double-processed to જો જો).
- Ordinals 283/284: all 14 normalized.
- Regression 67/67; anomaly scan unchanged (0 real-bug classes).

Kirtansagar is ready for a final native-reader spot-check. Recommend the Bible
audit next (the Pass-1/2/3 converter bugs — જો ligature, Š reph, ખ્રિસ્ત short-i
— all affected the Bible too).
