# Resolution of Bible Spelling Audit — Pass 2

## 1. Verse-boundary / extraction defects (build-logic fix, NOT lexical)

The source HTML omits some verse anchors, so a verse's text was fused into the
previous verse (e.g. 1 Chr 27:4 & 24 missing). Added two careful steps to
`html_extract.py`:
- **Recover missing verses**: if a verse body contains an inline numeral equal
  to the NEXT sequential verse number, immediately followed by a (non-space,
  non-digit) glyph, split it into a new verse. Only the exact next-expected
  number matches, so real data numerals ('24 હજાર', space after) are never
  touched. Recovered **6 verses** (34883 -> 34889), incl. 1 Chr 27:4/24.
- **Strip a verse's own leaked numeral** at the start of its text (James 3:8
  '8પણ'; Luke 1:13 doubled anchor '13 13 પણ'; 1 Cor 10:18 '18જન્મજાત').
Result: verses starting with a digit 5+ -> 0. Isaiah 27 keys complete; Ezekiel
31:5 fusion fixed.

## 2. Leading stray 'ચ' ('[' byte) — Sirach cluster
Raw '['(0x5b) normally maps to ચ (7,864 genuine ચ-words: ચાલ્યો, ચરણ, ચપળ…), so
it must NOT be remapped globally. The audit's cases are a stray leading '[' before
a COMPLETE word. The only STRUCTURALLY-unambiguous ones are '[' + an independent
-vowel word (ચ before a vowel is impossible): ચઅને->અને, ચઅભિમાની->અભિમાની. The
rest (ચતેણે/ચપ્રભુ/ચપણ/ચમારા/ચજ્યારે/ચપહેલા) are added as explicit whole-word
lexical fixes (confirmed, bounded).

## 3. Converter-ish matra-before-્ર (aa variant)
ઇસા્રયલીઓનાં (×1): a genuine aa-matra before ્ર. Rare single case; fixed as a
whole-word lexical entry (ઇસ્રાયલીઓનાં). [The pre-base short-i variant ખ્રિસ્ત
was already fixed structurally in Pass-3.]

## 4. High-confidence source defects (lexical)
ક્હ્યું->કહ્યું (×2), તેમણ->તેમણે (×1), જઈશ્વરનું->ઈશ્વરનું (×1, stray જ),
ંબધા->બધા (×1, stray anusvara), ૫ારેવાનાં->પારેવાનાં (digit-for-consonant).

## 5. Left as REVIEW (per audit)
માશે (Luke 1:14), પટી (Exodus 25/37 — likely valid noun). Native/source review.

## Verification
- Regression 76/76; anomaly scan unchanged (orphan-matra 1->0); leftover Latin 0.
- Total verses 34889 (+6 recovered). Verses starting with a digit: 0.
- Kirtansagar unchanged.
