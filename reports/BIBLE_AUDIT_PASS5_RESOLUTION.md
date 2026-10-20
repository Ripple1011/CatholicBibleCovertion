# Resolution of Bible Spelling Audit — Pass 5

## Assessment
The Pass-5 agent correctly found **no new corpus-wide converter bug** — the
systematic font families are exhausted. All accepted findings are scattered
SOURCE defects (raw bytes already encode the wrong form), resolved via scoped
lexical/phrase entries. Every finding was re-verified against raw bytes.

## Fixes applied (lexical / phrase)

Whole-word (each verified unique or safe):
| fix | raw | ref |
|-----|-----|-----|
| ચગુસ્સે -> ગુસ્સે | [økwMMku | Sirach 19:18 (stray leading ચ) |
| ચ"હું -> "હું | ["nwt | Sirach 19:21 |
| મંન -> મન | {tLk | Psalms 119:32 (extra anusvara) |
| થથરતો -> થરથરતો | ÚkÚkhíkku | 2 Macc 3:17 (dup syllable; correct form exists 4x) |
| અંતને -> અંતના | ytíkLku | Daniel 11:40 |
| માણસેને -> માણસોને | {kýMkukLku | 1 Chr 19:3 |
| કેવે -> કેવા | fuðu | 1 Cor 15:35 |

Phrase-scoped (whole-word would hit valid forms):
- Jeremiah 31:13: 'આનંદ માણશો.' -> 'આનંદ માણશે.' (3rd-person). **Isaiah 55:2
  'મોજ માણશો' (2nd-person) verified PRESERVED.**
- Sirach 19:5: stray standalone ચ between sentences -> removed ('લેવી. ચ જે' ->
  'લેવી. જે').

## Left as REVIEW (per agent)
ત્યાંને (1 Cor 16:6) — possibly older idiomatic 'ત્યાંને રસ્તે'; not normalized
without native/publisher confirmation.

## Confirmed CORRECT (agent's do-not-change list — honored)
તામારે(Tamar), પાશે, પાસો(lot/die), કારી, વાની(dish), આવ્યે/કર્યે/બોલ્યે/પડ્યે/
મળ્યે, પાની, ઝીવ(month Ziv), નિયમે, વર્ષાની, હાથા, લેહી, હાજી, વધેરે, વેડી, ચોડી,
ખેલી, પોલો, બેલે(Bel+e), કરા(hail), આજા, કાનો(deaf), માત્રા, ઉપરણા — all valid
in context; NOT changed.

## Verification
- Regression 80/80; anomaly scan unchanged; total verses 34891 (unchanged).
- Isaiah 55:2 માણશો preserved; ત્યાંને untouched; all bad forms -> 0.
- Kirtansagar/songbooks unchanged.

## Note on trajectory
Pass 5 found only scattered single-occurrence source typos — the converter is
now believed complete. Future passes will likely be low-yield (isolated typos +
review items). A native-reader/publisher proofread is the recommended next step
rather than more automated passes.
