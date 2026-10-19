# Resolution of Bible Spelling Audit — Pass 4 (verse-boundary integrity)

## Phase A — extraction integrity (structural)

### Deuteronomy 7:14 — malformed anchor (fixed structurally)
Source anchor was `<a name ="v14" ...>` with a SPACE before '=', so the ANCHOR
regex missed it and v14 fused into v13. Made the regex tolerate whitespace
around '='. v14 now recovered cleanly (only 1 such anchor corpus-wide).

### Isaiah 27:2, Ezekiel 31:5, 1 Samuel 29:2 — leaked inline own-number marker
Source places the anchor early, then the verse body contains a leaked inline
marker equal to its OWN number (`૨તે`, `૫એને`, `૨પલિસ્તી`) with the real verse
after it. Confirmed each against source HTML; a GENERAL rule is unsafe (would
break cross-refs '17:16-27', numbers '41,500', and the deuterocanonical
Esther-5 embedded numbering). So recovery is keyed to the 3 exact locations:
- Isaiah 27:2: text before '૨' duplicated v1 -> dropped; real v2 kept.
- Ezekiel 31:5: text before '૫' was v4 spillover -> dropped; real v5 kept.
- 1 Samuel 29:2: text after '૨' recovered as the missing verse 3.
Plus the source malformed join માણસાપલિસ્તીઓએ -> માણસો; પલિસ્તીઓએ (lexical).

### Numbers 31:33-45 — NOT a bug (source grouping)
Source has empty self-closing anchors `<a name="v33" />` with no text; the
summary genuinely lives in v46. Per the audit's own section 9 (236 legitimate
'-' placeholders), these are the app's grouping convention, NOT lost text. Left
as-is; no verses fabricated. (The '6,75,000' etc. in v46 are real quantities,
not lost verse markers.)

### Esther 5:2 — guardrail respected
The embedded (૧૫)/૨/૩/૪/૫ deuterocanonical numbering is intentional; the recovery
logic explicitly excludes it. Verified unchanged.

## Phase B — lexical source defects
મયું->મર્યું (×5, missing reph), નયું->નર્યું, ઠયું->થયું (source ઠ for થ).

## Verification
- Total verses 34889 -> **34891** (+Deut 7:14, +1 Sam 29:3). No other verse
  counts changed; 236 '-' placeholders unchanged.
- Regression 80/80; anomaly scan clean; no digit-leading verses.
- Esther 5:2 embedded numbering preserved; Numbers 31 not fabricated.
- Kirtansagar/songbooks unchanged.
