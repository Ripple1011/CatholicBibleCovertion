# Resolution of Bible Spelling Audit — Pass 9

## Family A — reph cannot cross an already-reordered ordinary short-i (FIXED)

The agent's diagnosis was exact and NOT a recurrence of the Pass-8 Š bug (no Š
in these tokens). The ordinary short-i 'r' is reordered to AFTER its consonant,
but the reph-'o' matra run (`[ktuwqe]]\x1d\x1e`) did not include ordinary 'r'.
So the reph could not cross the relocated short-i: ધાર્મિક -> ધામિર્ક,
સમર્પિત -> સમપિર્ત (reph stranded on the following consonant).

Fix: add 'r' to the reph matra run (the agent's exact one-line candidate). No
change to the Š handlers, consonant selection, or single-pass reph application.

## Trace-wide impact check (as required)
Ran the OLD vs NEW decoder over EVERY raw token in the whole corpus (Bible +
all songbooks). The delta is EXACTLY 2 records, both Bible, both expected:
- `ધામિર્ક -> ધાર્મિક`  (2 Chronicles 19:11, OT/14/19/11)
- `સમપિર્ત -> સમર્પિત`  (Deuteronomy 13:18, OT/5/13/18)
No other word changed anywhere; no name, no songbook, no side effect.

## Controls verified preserved
Valid િર્ words untouched: નિર્દોષ, જ્યોતિર્મય, કિર્યથ-યારીમ, તિર્સા. All prior
fixes intact (Š full+half, સાન્નિધ્ય, દુર્વૃત્તિ, યજ્ઞો, વર્ત્યો, ખ્રિસ્ત).
Deut 14:2 સમર્પિત (already correct) unchanged. જેનારો still review-only.

## Verification
- Regression 98/98 (added 2 fixtures + 3 control fixtures).
- Trace-wide decoder delta = exactly the 2 expected Bible words.
- Anomaly scan unchanged; verses 34891; 236 placeholders unchanged.
- Songbooks unchanged (ખ્રિસ્ત 42, no ધાર્મિક introduced).
- All Pass 8 names (ઈર્મિયા/પોર્કિયુસ) retained; no name change this pass.

## Note
Nine passes; this one a single narrow ordering gap (2 occurrences, 1 rule tweak).
Returns are deeply diminishing. Family B (જોનારો) and a native-reader/publisher
proofread remain the open items; the converter is not declared globally complete.
