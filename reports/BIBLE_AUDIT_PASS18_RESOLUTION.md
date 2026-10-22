# Resolution of Bible Spelling Audit — Pass 18 (REVIEW-ONLY, no change)

## Disposition: NO implementation change

Pass 18 was a review-only handoff. One source-spelling candidate was
investigated and **deliberately NOT approved for automatic correction**. No
WORD_FIXES / PHRASE_FIXES / decoder / build change was made. The output,
converter, scripts, and raw trace are unchanged this pass.

## Family A — possible omitted ર in `ડયાં` (Hebrews 11:23) — HELD for review

| Field | Value |
|---|---|
| Current | `ડયાં` |
| Candidate (NOT applied) | `ડર્યાં` |
| Reference | Hebrews 11:23 (NT/19/chapters/11/23) |
| Class | review (LOW confidence to authorize a change) |

Verse: "...રાજાની આજ્ઞાથી તેઓ **ડયાં** નહોતાં." (Moses' parents did not fear the
king's order.)

### Independently verified against raw bytes
Raw token `zÞkO` (hex `7a de 6b 4f`) decodes faithfully to `ડયાં`. It contains
NO ર marker — no reph `o`(6f), no `Š`(160), no ra `h`(68). So:
- This is NOT a converter dropping an encoded reph; the decoder is faithful.
- The candidate `ડર્યાં` would require INVENTING a ર that is not in the source
  bytes — which the standing guardrail forbids (same class as the protected
  કયું, which we do NOT normalize to કર્યું).

The meaning ("did not fear") is well supported (USCCB; the fear root appears
elsewhere in the edition, e.g. Genesis 18:15 ડરી, 20:8 ડરી). But meaning does not
settle this edition's ORTHOGRAPHY for this exact past-tense form. Absent a
publisher/native-reader ruling or a source-page comparison, a spelling change is
not authorized. **Left unchanged; added to the review queue (see REVIEW_QUEUE.md).**

## Verification
- No output change: bible.json and all songbooks unchanged from post-Pass-17.
- Prior corrections retained (Pass 13-17); review queue and held decisions intact.
