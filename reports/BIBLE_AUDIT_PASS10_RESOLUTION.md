# Resolution of Bible Spelling Audit — Pass 10

## Family A — full-consonant Š reph decoded with a base-font lookup (FIXED)

The agent's root-cause analysis was exact. The Pass-8 full-consonant `Š`
callback (`_repl_reph_i_full`) runs on the RAW Arpita stream but indexes
`_FULL2UNI`, which is built from the BASE Gopika table. For the two
Arpita-SWAPPED carriers the raw glyph points at the wrong base entry:

    raw Ë  : base-table says સ  — but in this Arpita source Ë encodes દ
    raw Œ  : base-table says દ  — but Arpita Œ encodes ત

So raw `ŠË` emitted `ר્સિ` (સ) instead of `ר્દિ` (દ): the city name Sardis
decoded as સાર્સિસ instead of સાર્દિસ. The carrier `Ë` was already replaced by
Unicode સ before the later whole-stream `unswap_arpita(s)` could recover દ.

### Fix (the agent's candidate, verified)
Normalize ONLY the single matched carrier through the existing
`unswap_arpita()` before the base-table lookup:

    def _repl_reph_i_full(m):
        return '\x10' + _FULL2UNI[unswap_arpita(m.group(1))] + '\x11'

This uses the established normalization as the source of truth rather than a
hard-coded Ë→દ exception. Non-swapped carriers are unchanged by unswap, so this
is a pure no-op for every previously-correct full-consonant Š word (ધાર્મિક,
ધર્મિષ્ઠ, ગર્વિષ્ઠ, નિર્વિવાદ all identical). The whole-stream `unswap_arpita(s)`
was NOT relocated; half-form/inherent-k/sentinel logic is untouched.

Guard verified: every carrier admitted by `_FULL_CONS_CLASS` normalizes to a
valid `_FULL2UNI` key (no KeyError possible).

## Trace-wide impact check (as required)
OLD vs NEW decoder over EVERY raw token in the whole corpus (Bible + all
songbooks). Delta = EXACTLY 4 records, all Bible/trace, none songbook:
- `સાર્સિસ -> સાર્દિસ`      Revelation 1:11  (NT/27/1/11)
- `સાર્સિસના -> સાર્દિસના`  Revelation 3:1   (NT/27/3/1)
- `સાર્સિસમાં -> સાર્દિસમાં` Revelation 3:4   (NT/27/3/4)
- `નિર્સિષ્ટ -> નિર્દિષ્ટ`   Mark preface (MARK 2_prelim) — trace-only

### Live Bible diff = EXACTLY 3 verses
A4 (`નિર્દિષ્ટ`) is a prefatory token, NOT in any verse value — confirmed absent
from bible.json before and after. So the verse-level change is the three Sardis
names only; the raw-trace change is four records. Both match the handoff.

## Name repair is source-faithful
The corrected દ is already encoded in the source bytes (raw `Ë`); this is a
decoder lookup fix, not a transliteration preference or a lexical overlay. The
vowel, reph, suffixes, and surrounding wording are all retained. Maintainer
accepts this source-backed name correction (same basis as Pass-8 ઈર્મિયા). It is
NOT extrapolated to any other name.

## Controls / preservation verified
- Isolated fragment contrasts all pass: ŠË→ר્દિ, ŠŒ→ר્તિ, Š‚→ר્તિ, Š{→ર્મિ,
  Šð→ר્વિ, Šf→ר્કિ (6/6).
- B1 (Revelation 1:9 સિંન્નધ્યમાં) left UNCHANGED — review-only; valid
  સાંનિધ્યમાં variant also preserved.
- જે/જો boundary, _JO_NEXT, Pass-7 review cases, Pass-9 reph regex all untouched.
- All resolved outputs preserved (ખ્રિસ્ત, સાન્નિધ્ય, દુર્વૃત્તિ, યજ્ઞો, વર્ત્યો,
  મૂર્તિ, કીર્તિ, ધાર્મિક, સમર્પિત, ...); names ઈર્મિયા/પોર્કિયુસ retained.

## Verification summary
- Regression 103/103 (added 4 Family-A fixtures + 1 raw/base contrast guard).
- Trace-wide decoder delta = exactly 4 raw records (3 verse + 1 preface).
- Live Bible diff = exactly 3 verses at the stated NT/27 paths.
- Anomaly scan unchanged; verses 34891; 236 placeholders; 46+27 canon.
- Songbooks unchanged (trace-wide delta showed 0 song changes).

## Carried forward
B1 (Rev 1:9 nasal placement) remains review-only — needs a source-font render or
native-reader/publisher decision. Prior open reviews (ત્યાંને, પટી, અપ્યાં,
જેનારો) unchanged. Native-reader/publisher proofread and written publisher
permission remain the gates before shipping.
