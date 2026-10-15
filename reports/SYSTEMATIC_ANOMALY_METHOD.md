# Systematic way to find conversion bugs (instead of random spot-checks)

Random reading finds bugs one at a time. The systematic method: **invalid
Gujarati has structural signatures.** A well-formed Gujarati syllable obeys
rules; any sequence that violates them is almost certainly a conversion bug.
`scripts/30_anomaly_scan.py` scans the whole converted corpus for these and
reports each class with a count + example tokens, so you fix the CLASS, not the
word.

## The invalid-sequence checks (what to look for)

| Check | Why it's invalid | Example bug found |
|-------|------------------|-------------------|
| two different matras in a row | one vowel sign per consonant | છેૃ -> છે |
| same matra repeated | font artifact | ખેેેડ -> ખેડ |
| virama + matra | virama precedes a consonant, not a vowel | (half-form leftovers) |
| duplicate virama ્્ | impossible | ક્્યાં -> ક્યાં |
| anusvara/candrabindu BEFORE a vowel sign | wrong canonical order | તંે -> તેં ; મોકલ્યંુ -> મોકલ્યું |
| matra after anusvara/visarga | nothing attaches after them | ખંેચી -> ખેંચી |
| independent vowel + matra | independent vowels take no matra | એા -> એ ; કોઈે |
| word-final virama | usually a dropped half-form... | ...BUT many are REAL (અર્થાત્, દંડવત્) — verify, don't blind-fix |
| orphan leading matra (space + mark) | a word split by a stray source space | હુ ં -> હું ; પ ોતાનાં -> પોતાનાં |
| reph ર્ at word end / before a matra | reph must sit on a consonant | કીતિર્ -> કીર્તિ |
| double anusvara | impossible | ક્યાંં -> ક્યાં |
| non-Gujarati char in Gujarati text | leftover Latin / markup | (Daniel 5 '=' is intentional) |

## How it drove this round's fixes

Running the scan surfaced, ranked by frequency, several classes NOT found by eye:
`matra after anusvara` (13), `double anusvara` (18), `reph at end` (2),
repeated/split matras. Fixes added to the converter:
- generalized anusvara-order (ં + any vowel sign -> vowel + ં)
- collapse duplicate anusvara and repeated vowel signs
- drop a 2nd matra / a matra after an independent vowel
- reph-at-end -> move onto the preceding consonant
- rejoin orphan combining marks split by a stray source space (build step)

Result: every invalid class went to 0 or near-0 (1–3 rare edges); the only large
remaining count is **word-final virama = 185, which is CORRECT** (Sanskrit
loanwords). Regression suite expanded to 50/50.

## Workflow to keep using

1. `python scripts/30_anomaly_scan.py`  — see all invalid classes + examples.
2. For a flagged class, trace a few examples to raw bytes with
   `scripts/26_check_issues.py` / `27_check_issues2.py` style scripts.
3. Decide: converter rule (structural) vs lexical/source defect.
4. Fix, add a regression case, re-run the scan until the class is 0.
5. Treat any NON-zero class as either a real bug or a KNOWN-GOOD exception you
   explicitly whitelist (like word-final virama).
