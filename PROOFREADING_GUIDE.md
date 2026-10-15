# Proofreading Guide (for an AI agent)

You are proofreading a **Catholic Gujarati Bible + 3 songbooks** that were
converted from a legacy font (Gopika Two) to Unicode Gujarati. The conversion is
already structurally clean; your job is the **linguistic / meaning layer**:
find words that are *valid-looking but wrong*, misspellings, and awkward
readings that automated structural scans cannot catch.

Read this whole file before you start. The #1 rule: **do not "fix" text you
don't understand — flag it.** Corrupting a correct word is worse than leaving a
wrong one.

## What you have in this repo

- `output/bible.json` — `{testament: {book_id: {name, chapters: {chap: {verse: text}}}}}`
- `output/kirtansagar.json`, `holi_gito.json`, `natal_garba.json` — `{id: {text}}`
- `output/book_names.json`, `output/manifest.json` — indexes
- `reports/raw_trace.jsonl` — **CRUCIAL**: one row per distinct converted word with
  its RAW source bytes. Use it to tell a conversion bug from real source text.
- `scripts/` — the converter (`gopika_decode.py`), table (`gopika_table.py`,
  `source_assets/myExpr.js`), anomaly scanner (`30_anomaly_scan.py`), tests.
- `reports/CONVERTER_FIX_EXPLANATION.md`, `SYSTEMATIC_ANOMALY_METHOD.md` — how
  conversion works and what's already fixed.

## The ONE question for every suspicious word

For any word you think is wrong, open `reports/raw_trace.jsonl`, find the row
whose `"u"` equals that word, and look at `"raw"` / `"hex"`:

1. **If the raw bytes clearly encode a DIFFERENT (correct) word** → it's a
   **CONVERTER BUG**. Report it with: the word, the raw/hex, the expected word,
   and 1-2 `refs`. These should be fixed in `gopika_decode.py` (structural), not
   by editing the JSON.
2. **If the raw bytes already encode exactly what the output shows** → it's a
   **SOURCE DEFECT** (the original app has the typo). Report it as a candidate
   for `scripts/lexical_fixes.py` (whole-word/phrase correction), WITH the
   correct word and your confidence.
3. **If you're not sure it's wrong** → flag as "REVIEW" with your reasoning. Do
   not change it.

This distinction is the whole game. A word like હાવા (should be હવા) and a word
like મારા (correct) can have byte-identical patterns; only the raw trace +
meaning together resolve it.

## How to proofread (recommended passes)

1. **High-frequency first.** `raw_trace.jsonl` is sorted by frequency. The top
   few thousand words cover most of the text. A wrong high-frequency word (like
   the earlier અનો→અને, 25k×) is worth far more than a rare one.
2. **Read in context.** Judge words inside their verse, not in isolation —
   Gujarati spelling/sandhi depends on context.
3. **Compare to a reference** if you can: a published Gujarati Catholic Bible
   (e.g. Bible Society of India Gujarati, or other Gujarati editions). Flag
   where this text diverges in a way that looks like an error (not just a
   translation-wording difference).
4. **Use the structural scanner as a pre-filter**, not the main tool:
   `python scripts/30_anomaly_scan.py` — it already reports near-zero; anything
   it flags is either a known-good exception (below) or a rare real defect.

## KNOWN-GOOD — do NOT flag these

- **Word-final virama ્** on Sanskrit loanwords: અર્થાત્, દંડવત્, શરણમ્,
  સ્વાગતમ્, સાક્ષાત્. These are CORRECT (~185 of them). Not bugs.
- **Daniel 5:25-28 '='**: મને=ગણેલું, તેકેલ=તોળેલું, પાસ્રિન=ભાગ — the '='
  means "means/interpreted-as" and is the source's intentional formatting.
- **English book `name` fields** in bible.json (Genesis, MATHEW, …): intentional
  index, English by design. Only the VERSE TEXT is Gujarati.
- **Deuterocanonical books** (Tobit, Judith, 1&2 Maccabees, Wisdom,
  Ecclesiasticus/Sirach, Baruch): correct — this is the Catholic canon.

## Already fixed (don't re-report)

See `reports/CONVERTER_FIX_EXPLANATION.md`. Includes: spurious-ા
(પાંથ→પંથ etc.), અનો→અને, દિવસ, reph (વર્તે/માર્ગે/સર્જન), રાત્રિ, રહ્યો,
મોકલ્યું, repeated matras (ખેડ/ભેટો), colon-vs-visarga, જ્ઞ/ત્ર conjuncts
(આજ્ઞાઓ), matra ordering (તેં/ખેંચી), double anusvara, and specific source
typos (સજ્યાં→સર્જ્યાં, હવા, મેં/તેં).

## How to REPORT findings

Produce a single file `reports/PROOFREADING_FINDINGS.md` (or JSON) with, per item:

| field | meaning |
|-------|---------|
| `word` | the suspect converted word |
| `raw` / `hex` | from raw_trace.jsonl (so it can be verified) |
| `expected` | the word you believe is correct |
| `class` | `converter-bug` \| `source-defect` \| `review` |
| `confidence` | high / medium / low |
| `refs` | 1-3 verse locations |
| `note` | why (one line) |

Group by `class`. Sort by frequency (impact) within each group. **Do NOT edit
`output/*.json` or `scripts/*` directly** — your deliverable is the findings
list; a human (or the converter author) applies fixes so each one is reviewed
and the structural fixes stay structural.

## Guardrails (critical)

- Never bulk-replace a word across the corpus without checking it isn't valid
  elsewhere (e.g. જન is both a wrong-conversion AND a real word "jan=people").
- A short token (તં, મં, ના) may be correct inside a larger word — only act on
  whole-word, boundary-checked matches.
- Gujarati has many valid spelling variants; divergence from your expectation is
  not automatically an error. When in doubt → `review`, low confidence.
- Honor the licensing note in FINDINGS.md: this content is copyrighted; do not
  redistribute outside this private workflow.
