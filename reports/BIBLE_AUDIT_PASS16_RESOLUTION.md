# Resolution of Bible Spelling Audit — Pass 16

## Family A — transposed digits in a source verse anchor (FIXED, build pipeline)

Luke 6:36's text was stored under key `63` (between 35 and 37); key `36` was
absent. This pass CLOSED the handoff's source-evidence gap by inspecting the
original APK HTML anchor directly.

### Source-anchor evidence (the smoking gun)
Source asset `assets/1/3/6.html` (NT=1 / Luke=book 3 / chapter 6),
sha256 `663fd364bbdad8d723aada345724a9e03b7aa65cadb0818c974892f7cb496f53`.
The anchor for this verse is:

    <a id="v36" name="v63">36</a>

TWO of three signals say 36 — the `id` attribute AND the visible numeral. Only
the `name` attribute has transposed digits (`v63`). `extract_verses` captures
from `name="vN"`, so it emitted the single wrong signal as the key. This is a
genuine SOURCE-ANCHOR DEFECT, and the correct number is confirmed from within
the same anchor (no external versification needed; USCCB/Vatican corroborate).

`assets/1/3/6.html` is the ONLY file in the entire corpus with the pattern
"v35 present, v36 absent, v37 present, v63 present" — confirming this is an
isolated defect, not a systemic parser issue.

### Fix — location-scoped relabel (not an unscoped v63->v36 rule)
Added a `relabel` mode to `_VERSE_RECOVERY` in scripts/20_build_json.py, keyed on
the exact tuple ('1', 3, 6, '63') (NT, Luke, chapter 6, label 63). It renames the
key to 36 IN PLACE, with an assertion that 36 does not already exist (never
overwrite/merge). No decoder/lexical/font change; no global key rule; the parser
ANCHOR regex is unchanged. Verse text is untouched; total count is unchanged
(relabel, not a verse recovery).

## Verification (full rebuild)
- Complete Bible vs post-Pass-15 baseline: key-set delta = EXACTLY one key
  removed ('NT/3/6/63') and one added ('NT/3/6/36'); ZERO verse-value changes
  among all common keys; the value under 36 is byte-identical to the old 63.
- Key 36 is in correct sequence (34,35,36,37,38), NOT appended at chapter end.
- Total verses unchanged (34891); 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace unchanged (word-level, not anchors).
- New build regression scripts/test_verse_keys.py (5 checks) passes; decoder/
  lexical regression 143/143 unchanged; anomaly scan unchanged.
- Prior passes retained (Pass 15 person/place, Pass 14 કૃતઘ્ન-, Pass 13 આજ્ઞાઓ).

## Not changed (explicitly)
- The attached heading "બીજાના કાજી થશો નહિ (માથ્થી ૭:૧-૫)" stays in verse 36's
  value (reattaching it to v37 would be a separate editorial change, out of scope).
- Review-only queue unchanged (Rev 1:9, જોનારો, ત્યાંને, પટી, અપ્યાં, Wisdom
  14:27 પરાકાષ્ટા). Global-U / પહાંચ- / સાંપ- decisions still held. વિષ્ટા preserved.

Native-reader/publisher proofread and written publisher permission remain the
gates before shipping.
