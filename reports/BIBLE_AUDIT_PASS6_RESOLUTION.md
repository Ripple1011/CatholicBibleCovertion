# Resolution of Bible Spelling Audit — Pass 6

The Pass-6 agent correctly identified TWO residual structural converter bugs
(not source defects). Both are now fixed in `gopika_decode.py`; no lexical
entries were used. The agent's byte-level diagnosis was exact.

## Family A — short-i before the ન્ન conjunct core (converter bug)

`Ò`(ન्न) is a two-char conjunct core (table key `Òt`); it was NOT hoppable by a
pre-base short-i (it was absent from the cluster set, unlike û/¥/º/Ì). So `rÒt`
left the short-i on the wrong syllable: `MkkrÒkæÞ` -> સિન્નધ્ય (+ lost long-ā).

Fix: add the missing conjunct cores (¿,²,Ò) to the cluster set, and give the
cluster an explicit `conjunct-core + 't'` alternative so the 2-char table key
stays ATOMIC during short-i movement — NOT a bare `t?` that could over-reach a
normal consonant's aa (the agent's warning). Verified પિતા/દિવસ/ખ્રિસ્ત/etc.
unaffected.

Result: સિન્નધ્ય family 29 -> 0; સાન્નિધ્ય -> 29. The valid sibling variant
**સાંનિધ્યમાં (Exodus 28:30, ×14) PRESERVED**. Jonah 2:5 hyphen retained.

## Family B — reph after the vocalic-r matra ']'(ૃ) (converter bug)

The reph `o` reorder allowed `[ktuwqe\x1d\x1e]*` between a consonant and its
trailing reph, but NOT `]`(ૃ). So `ð]o` (વ ૃ reph) was not reordered:
`દુવૃર્ત્તિ` instead of `દુર્વૃત્તિ`. Fix: add `]` to the reph matra set.

Result: દુવૃર્ત્તિ 2 -> 0; દુર્વૃત્તિ -> 2 (Romans 6:12, Colossians 2:23).

## Shared-converter effect on songbooks (expected)
Both are structural, so they also corrected Kirtansagar counterparts
(દુર્વૃત્તિ, સાન્નિધ્ય now correct there too; bad forms 0). This is the right
behaviour, not an unexpected diff.

## Verification
- Regression 83/83 (added સાન્નિધ્ય/સાન્નિધ્યમાં/દુર્વૃત્તિઓને cases).
- Anomaly scan unchanged; verses 34891; 236 placeholders unchanged.
- Guardrails honored: સાંનિધ્યમાં preserved; no English-name edits; no
  verse-boundary changes; ત્યાંને still review; all prior protected forms intact.

## Note
The agent was right that "converter complete" (Pass-5 assessment) was too strong.
These two edge cases are now closed. Further systematic bugs are increasingly
unlikely but not impossible; a native-reader/publisher proofread remains the
recommended complement to continued automated passes.
