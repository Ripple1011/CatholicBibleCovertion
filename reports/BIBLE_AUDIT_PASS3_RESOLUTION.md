# Resolution of Bible Spelling Audit — Pass 3

## 🔴 Converter bug: reph on a half-form-led conjunct (વર્ત્યો family)

વત્ર્યો/મત્ર્ય/અપ્ર્યા/સમપ્ર્યો/નિમ્ર્યા — the reph 'o'(0x6f) marker, when the
cluster is a HALF-form + consonant conjunct (ત્ય = íÞ), was riding the WRONG
consonant (producing ત્ર્ય). Fixed the reph reorder to target the FIRST
consonant of a half-form-led conjunct, via a single alternation regex applied
once (conjunct case first, then the lone-consonant case) so it never double-
applies. A lone consonant like ષ in વર્ષ/વર્ષા is left correct.

Fixed corpus-wide: વર્ત્યો 16, મર્ત્ય 15, અર્પ્યા 3, સમર્પ્યો 1, નિર્મ્યા 1;
all wrong forms -> 0. Verified no regression (રાજકર્તા 107, વર્ષ 655 intact);
anomaly 'reph-not-on-consonant' stayed 0, 'word-final-virama' 185.

## Source defects (lexical, verified vs raw)
વતું->વર્તું (×2, source missing reph), માશે->માયે (Luke 1:14, source શ for ય),
તેણો->તેણે, તેમન->તેમને, કરીન->કરીને, હુ->હું, એવુ->એવું, સાંપ્યુ->સાંપ્યું
(missing final matra/anusvara). Damaged headings: નિયમા->નિયમો (×3; the valid
word નિયમાનુસાર is a substring and is untouched), અન્નબલિઆ->અન્નબલિ (stray આ).

## Structural cleanup
Orphan combining mark after punctuation/space -> dropped (Rev 14:8 '!ં' -> '!').
General rule in fix_unicode.

## Left as REVIEW (per audit)
અપ્યાં (Exodus 40:29 — may be archaic/poetic for આપ્યાં). Footnote digits
(આદમે૧, નૂહ૧...) — a separate footnote/formatting audit, not spelling.

## Verification
- Regression 80/80; anomaly scan clean (reph-not-on-cons 0, orphan-matra 0).
- Total verses 34889 (unchanged). Kirtansagar unchanged (ખ્રિસ્ત 42, મૂર્તિ 20).
