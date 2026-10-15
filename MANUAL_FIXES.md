# Manual fixes & known residues

Status after the converter (`scripts/gopika_decode.py` + `scripts/html_extract.py`):
conversion is ~99.999% clean. Below is everything that still needs a human eye.

## 1. Stray Latin characters — only 8 occurrences, in 4 verses

All are DEFECTS IN THE ORIGINAL APP HTML, not translation errors. Fix by
hand in the final JSON (or ignore — they are at verse boundaries, not in the
scripture text itself).

| Location | Stray | Cause | Fix |
|----------|-------|-------|-----|
| OT book20 (1 Maccabees) ch16 : v17 | `v` | source has broken anchor `7" id="v177">177` | delete the leaked `" ૈઙ્ઘ="v` debris at the start of the verse |
| OT book46 (Psalms) ch106 : v4 | `v` | broken anchor `" id="v4">4` | delete leaked `" ૈઙ્ઘ="v` debris at verse start |
| NT book1 (Matthew) ch22 : v40 | `v` | stray leading `v` byte in source | delete the leading `v` |
| OT book24 (Ecclesiastes) ch11 : v9 | `l p F l l` | English title + CSS href inside an HTML comment leaked into the gujFont block: `Ecclesiastes - Chapter 11--> ... href="...customFontsAndStyles.css"` | truncate the verse after the real text `...ઈશ્વર તાારો હિસાાબા માગાશે.` — everything after is garbage markup |

That's the entire manual Latin cleanup.

## 2. Known systematic artifact: spurious aa-matra (ા)  — READABILITY, not blocker

The byte 0x6b ('k' raw) is the consonant's inherent-vowel marker in this font.
The current converter keeps it as ા in some positions, producing an extra ા:
  * `પાછી` should be `પછી` (pachhi)
  * `તાો` should be `તો` (to)   — very common
  * `નાા` should be `નાા`→`ના`  etc.

The text is READABLE with these, but for publication accuracy they should be
removed. This is a single rule to perfect: "a consonant immediately followed by
the inherent-marker ા that is itself immediately followed by another matra or a
consonant = drop that ા." It needs native-reader spot-checking because a FEW ા
are genuine (e.g. `માં`, `આકાશ`). See FINDINGS.md "the k byte" for the proven
model (single marker = drop, doubled = real aa). This is the recommended next
refinement before shipping.

## 3. Rare unmapped conjunct glyph: `â`

Appears as e.g. `માંડâું` (should be `માંડ્યું`). `â` (0xE2) = the conjunct
`ડ્ય`/`ત્ય`-family post-base 'ya'. The upstream table comments this case
(`[કછટઢફ]્ય -> $1â`). Add a mapping `â -> ્ય` (virama+ya) and verify against a
few words. Low frequency; safe to batch-fix.

## 4. Verified glyph additions already applied
Already in `gopika_decode.py` EXTRA table (do not redo):
  * `I` (0x49) -> `ૌં`   (MkkIËÞo = સૌંદર્ય) — fixed 127 occurrences
  * `g` (0x67) -> `ખ્ત`  (Ãkwg = પુખ્ત)
  * `r` -> short-i reorder ; `o` -> reph reorder ; `O`,`U` -> anusvara

## Recommended finishing order
1. Perfect the spurious-ા rule (#2) with native-reader checks — biggest quality win.
2. Add `â -> ્ય` (#3).
3. Hand-fix the 4 verses in #1 in the final JSON.
4. Re-run `scripts/13_residue_report.py` and a fresh read-through of 2-3 chapters.
