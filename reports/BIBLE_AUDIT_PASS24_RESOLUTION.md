# Resolution of Bible Spelling Audit — Pass 24 (REVIEW-ONLY, no change)

## Disposition: zero Bible changes. One new review item + one preserved form.

Pass 24 was a review-only handoff. No WORD_FIXES / PHRASE_FIXES / decoder / build
change was made. Output, converter, scripts, and raw trace are unchanged. I
verified both findings against raw bytes and (for Family A) closed the APK source
gap the agent flagged.

## Family A — ચેરનાર (Job 42:3) — HELD for review (new item #10)

| Field | Value |
|---|---|
| Current | `ચેરનાર` |
| Candidate | Unresolved — NO replacement approved |
| Reference | Job 42:3 (OT/22/chapters/42/3) |
| Class | review (LOW confidence any specific fix is justified) |

Verse: "...મારી ધારણાને વિવેક વગર ચેરનાર એવો તું કોણ?..."

### Independently verified (source gap closed)
- Decoder is FAITHFUL: `[uhLkkh` -> `ચેરનાર`, no dropped reph/matra. A converter
  defect is RULED OUT.
- APK source inspected (`assets/0/22/42.html`,
  sha256 7014cca21aab12aa8b9cd787fc220675772b4ed7cfb047fa154d8b84a00d0d79): the
  raw clause genuinely contains `[uhLkkh`. So the source really has this word.
- Context control: the parallel challenge at Job 38:2 uses the clear verb
  પડકારનાર (raw `ÃkzfkhLkkh`). So ચેરનાર is either an obscure/edition-specific
  verb or a source wording error.

### Why held
No dictionary entry reliably settles whether ચેરનાર is valid, and "not found" is
not proof of invalidity. This is a native-reader / publisher lexical judgement,
not an automated fix. Do NOT copy પડકારનાર from Job 38:2 or guess a replacement.
Added as item #10 in reports/REVIEW_QUEUE.md with the full evidence.

## Family B — સુઝાડતો (Galatians 5:8) — CHECKED and PRESERVED

Raw `MkwÍkzíkku` -> `સુઝાડતો` (decoder faithful). GujaratiLexicon has the headword
સુઝાડવું, the causative of સૂઝવું, with a short initial u. So the short-u is
ATTESTED — this is NOT an error. Keep it; no સુઝ->સૂઝ remap. Recorded in the
review queue's "checked and preserved" note.

## Verification
- No output change: bible.json and all songbooks unchanged from post-Pass-23.
- Decoder/lexical/scripts/trace unchanged; regression still 175/175.
- All prior corrections (Pass 13–23) retained; held decisions intact.

## Carried forward (unchanged)
All review-queue items (now 10) and held global-U / aa+U / Numbers 28:12-13
decisions on hold. Native-reader/publisher proofread and written publisher
permission remain the gates before shipping.
