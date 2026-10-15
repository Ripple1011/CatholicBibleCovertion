# Resolution of Kirtansagar Spelling Audit — Pass 1

Each Pass-1 finding was traced through the raw Gopika bytes (per the guide) and
classified as converter-bug (structural fix) or source-defect (lexical fix).

## Converter bugs (fixed structurally in gopika_decode.py)

### જોવું verb family — the big one (~2,600 words corpus-wide)
`ò`(0xf2) is the જ ligature base that renders as જા alone, but **`òu` before a
following letter is the જો ligature**. Verified: EVERY `òuE`/`òuÞ`/`òuô`/`òuW`
token in the whole corpus (35 distinct forms, ~2,600 occurrences) is a જો form
(જોઈ, જોઈએ, જોઈને, જોયો, જોયું, જોયા, જોઉં, જોયેલા, compounds like
જાણીજોઈને …) — never a genuine જે. Bare `òu` at a word end stays જે correctly
(બીજે, કરજે, વંશજે). Fix: `òu[EÞ]`→જો+…, `òuô`→જોઉં, `òuW`→જોઉ.
Result: Bible જોઈ-prefix 0→1262, જેઈ(bad) →0; songbook જેઈ/જેયો/જેયું/જેયા →0.

## Source defects (fixed via lexical_fixes.py, whole-word, verified)

| fix | raw | ×  | note |
|-----|-----|----|------|
| સજ્ર્યો → સર્જ્યો | MkßÞkuo | 2 | reph absent in source (as સજ્યાં) |
| અપ્ર્યો → અર્પ્યો | yÃÞkuo | 1 | reph misplaced in source |
| મબલક → મબલખ | {çk÷f | 4 | source literally has ક; standard is ખ |
| અજેડ → અજોડ | yòuz | 1 | òu+z ligature; rare single word |
| ૫ણ → પણ | digit ૫ for પ | 1 | digit-for-consonant source typo |

## Left as-is (per maintainer decision — native-reader pass)

- **નવ (×63)**: the source genuinely writes નવ; used poetically for the negative
  ન. નવ is also a valid word (new/nine). Not a conversion error — leave to a
  native editor; do not auto-change.
- **જેજે (×~13), જેજન (×2)**: same ò ligature root (òusu=જોજે, òuòu, òusLk) but
  context-dependent (જોજે vs જે જે vs …). Needs per-occurrence human judgment.
- **તાજપ (×1)**: source matches output; intended word unclear. Review.
- The audit's "Checked and NOT flagged" list (તવ, કેરા, મારગ, સુણી, માંહે …) is
  correct — archaic/poetic/dialectal, not errors.

## Verification
- Regression suite: 52/52 (includes a new જોઈ/જોયો case).
- Anomaly scan unchanged (0 real-bug classes).
- All JSON regenerated.
