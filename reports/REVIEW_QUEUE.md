# Review queue — items for a native-Gujarati reader / publisher

These are readings the automated audit passes deliberately did NOT change,
because resolving them needs human editorial / edition-specific judgement, not
more byte analysis. Each has been checked against raw source bytes: in every
case the decoder is FAITHFUL to the source, so any change would be a source /
editorial decision, not a converter fix. Do not auto-correct these.

For a native reader: for each item, decide whether the CURRENT reading is a
genuine edition/house/poetic spelling to keep, or a source defect to correct. If
a correction is confirmed, it should be applied as an exact verse-scoped lexical
/ phrase overlay (never a decoder remap, never a direct JSON edit), with a
rebuild showing exactly one affected verse.

| # | Current | Candidate / question | Reference | Raw | Why held |
|---|---|---|---|---|---|
| 1 | ડયાં | ડર્યાં? (omitted ર in past-tense "feared") | Hebrews 11:23 | `zÞkO` | No ર in source bytes; cf. protected કયું. Pass 18. |
| 2 | પરાકાષ્ટા | પરાકાષ્ઠા? (ષ્ટ vs ષ્ઠ) | Wisdom 14:27 | `Ãkhkfkük` | Both spellings attested in Gujarati; mixed same-edition use. Pass 15. |
| 3 | સિંન્નધ્યમાં | nasal/short-i ordering (cf. valid સાંનિધ્યમાં) | Revelation 1:9 | `MkkrtLLkæÞ{kt` | Extra nasal/order question; publisher intent unclear. Pass 10/12. |
| 4 | જોનારો / જેનારો | જે vs જો ligature ambiguity | (family) | — | ò+u ligature ambiguity; LOW confidence either way. Pass 7. |
| 5 | ત્યાંને | spacing/suffix question | (as recorded) | — | Carried review; unresolved. |
| 6 | પટી | spelling question | (as recorded) | — | Carried review; unresolved. |
| 7 | અપ્યાં | spelling question | (as recorded) | — | Carried review; unresolved. |
| 8 | ખંચાવું | nasal-only raw-t (NOT the Pass-12 ખેંચ- U family) | Sirach 7 / Isaiah 44 | `¾t[kðwt` | Raw has plain t, no U; no encoded e-matra to restore. Pass 12. |

## Separately: held pipeline DECISION (not a per-word review)

- **Global U mapping** and the **aa+U family (`સાંપ- -> સોંપ-`)**: the GopikaTWO_N
  glyph evidence (Pass 12) shows raw U = ે+ં everywhere, but a global expansion
  would also rewrite 60+ frozen `પહાંચ-` forms and the `સાંપ-` family. The impact
  is fully measured (381 forms). Held pending an explicit maintainer decision to
  revise those frozen boundaries. The bounded ખ+U/ફ+U (ખેંચ-/ફેંક-/ફેંસલ-/ફેંટ-)
  repair is already shipped.

## Checked and PRESERVED (do NOT "fix" — attested spellings)

- `વિષ્ટા` / `વિષ્ટાની` (×4): attested Gujarati dictionary headword
  (excrement/dung) matching the verse contexts. No ષ્ટ->ષ્ઠ rule. Pass 15.
- `કયું`, `પહાંચ-`, `નવ`, `નાહીં`, `પરથમ`, `પુત્તર`, `ર્હે/ર્હેજે`, `કરજા`,
  `શાન્ત`: protected edition/poetic forms.
