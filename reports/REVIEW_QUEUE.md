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
| 9 | છ શેર / ચાર શેર | ram & lamb grain-offering quantities (see detail below) | Numbers 28:12–13 | `A` / `[kh` | SOURCE itself is internally inconsistent with 3 parallel passages + USCCB. Content/editorial call. Pass 20. |

## Detail for #9 — Numbers 28:12–13 grain-offering quantities (Pass 20)

**This is a CONTENT/quantity question, not spelling — needs a publisher/native
reader, and may be a genuine erratum in the printed edition worth reporting back
to the publisher.**

The monthly grain-offering portions in Numbers 28:12–13 disagree with the same
edition's three parallel passages and with USCCB:

| Animal | 28:12–13 (current) | 28:20–21 | 28:28–29 | USCCB (ephah) |
|---|---|---|---|---|
| calf/bull | છ (6) | છશેર (6) | છ શેર (6) | 3/10 |
| ram (large sheep) | **છ (6)** ← odd | ચાર (4) | ચાર (4) | 2/10 |
| lamb (small sheep) | **ચાર (4)** ← odd | બશેર (2) | બશેર (2) | 1/10 |

So in 28:12–13 both the ram and lamb portions are one step too high; the expected
descending 6/4/2 pattern is stated correctly three other times in the same chapter.

**Source-evidence (APK inspected, `assets/0/4/28.html`,
sha256 83a3a3d4e6fdc4aca2ee897576be43c43418b1647f283e97c04449732e44cc4f):**
- 28:12 ram clause raw: `...{kuxk ½uxk ËeX íku÷u {kuÞu÷ku A þuh ÷kux` → `A`=છ(6)
- 28:13 lamb clause raw: `...LkkLkk ½uxk {kxu íku÷u {kuÞu÷ku [kh þuh ÷kux` → `[kh`=ચાર(4)
- control 28:20 ram: `[kh`=ચાર(4); control 28:29 lamb: `çkþuh`=બશેર(2)

So the **decoder is FAITHFUL** — the printed source itself carries the inconsistent
quantities. This is NOT a converter/extraction bug; it is an editorial/translation
inconsistency in the source.

**Why held (not auto-fixed):** unlike the Pass-17 census (provably wrong by the
verse's own arithmetic) or the Pass-19 truncated oath (mechanically incomplete
word), this source text is COMPLETE and well-formed; it merely disagrees with
parallel passages. Correcting it would OVERRIDE what the printed Bible states,
based on cross-referencing — a decision for the publisher / a native reader.

**If a reviewer confirms the correction**, the minimal change is two verse-scoped
phrase overlays: 28:12 ram `છ શેર`→`ચાર શેર`; 28:13 lamb `ચાર શેર`→`બશેર`. Do NOT
touch the first calf `છ શેર` in 28:12, the animal counts in 28:11, the drink
offering in 28:14, or any parallel/control verse. Never globally replace છ/ચાર.

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
