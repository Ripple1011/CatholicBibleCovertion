# Resolution of Bible Spelling Audit — Pass 8

## Family A — Š reph+short-i before a FULL consonant (converter bug, FIXED)

The agent's diagnosis was exact. The `Š` handler (`_repl_reph_i`) only covered
HALF-form consonants (`HALF_CONS_CLASS`). `Š` before a FULL consonant ('{'=મ,
'ð'=વ) fell through to the old `reorder_gopika` fallback, which put the reph
AFTER the consonant; `fix_unicode` then dropped the virama -> valid-looking but
wrong order: `મ ર્ િ` -> `મરિ` instead of `ર્મિ`. Result: ધાર્મિક -> ધામરિક,
ધર્મિષ્ઠ -> ધમરિષ્ઠ, ગર્વિષ્ઠ -> ગવરિષ્ઠ, નિર્વિવાદ -> નિવરિવાદ.

Fix: added a full-consonant `Š` branch mirroring the half-form one, using a new
`_FULL2UNI` map (full gopika glyph -> its Unicode consonant). It emits
ר्(\x10) + <full consonant> + િ(\x11), WITHOUT consuming the consonant's inherent
'k' (full + k = genuine aa, unlike half-forms). The existing half-form path
(મૂર્તિ/કીર્તિ/સમર્પિત) is untouched.

Result: all 12 forms / 55 occurrences repaired; the correct forms now read
ધાર્મિક(19)/ધર્મિષ્ઠ(23)/ગર્વિષ્ઠ(9)/નિર્વિવાદ(1); old forms -> 0.

## Proper names — APPLIED (maintainer decision)

The same structural fix also corrected names the audit flagged review-only.
Maintainer approved applying them because these are the SOURCE's OWN encoded
reading (not a foreign-edition substitution) and are now fully consistent:
- Jeremiah: ઈમરિયા -> **ઈર્મિયા** (~185×, all inflections; old form 0; Jer 1:1
  reads "ઈર્મિયા, તને શું..."). The name was ALWAYS mis-decoded by this bug.
- Porcius: પોકરિયુસ -> **પોર્કિયુસ** (Acts 24:27).

This restores the source's encoding uniformly; it does NOT harmonize to another
Bible's transliteration (which remains prohibited).

## Shared-converter songbook effect (expected)
Kirtansagar counterpart corrected too: ઊમરિ -> **ઊર્મિ** (0 old). Structural, so
the same source pattern is fixed everywhere.

## Verification
- Regression 93/93 (added ધાર્મિક/ધર્મિષ્ઠ/ગર્વિષ્ઠ/નિર્વિવાદ cases).
- Anomaly scan unchanged; verses 34891; 236 placeholders unchanged.
- All old forms (12 words + 2 names) -> 0 corpus-wide.
- Half-form Š path, Pass 6/7 short-i/o-matra, ખ્રિસ્ત, સાન્નિધ્ય, દુર્વૃત્તિ all
  preserved. All other guardrails honored (જે/જો, edition forms, canon, verse
  boundaries, English name fields).

## Note
Eight passes have each found rarer, deeper edge cases. This closes the
full-consonant Š reph path (the last-known Š gap). Family B (જોનારો) and a
native-reader/publisher proofread remain open. Converter not declared globally
complete.
