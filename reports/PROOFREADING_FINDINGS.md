# Proofreading Findings

> Template for the AI proofreading agent. Read `PROOFREADING_GUIDE.md` first.
> Fill in the tables below. Do NOT edit `output/*.json` or `scripts/*` — this
> findings file is the only deliverable; a human applies the fixes after review.
>
> For every suspect word: look it up in `reports/raw_trace.jsonl` and copy its
> `raw` / `hex`, then classify. The `raw`/`hex` is what lets a human verify your
> call, so always include it.

- **Agent / model:** <fill in>
- **Date:** <fill in>
- **Scope covered:** <e.g. bible.json OT Genesis–Deuteronomy, all songbooks, …>
- **Reference used (if any):** <e.g. Bible Society of India Gujarati; none>
- **How words were selected:** <e.g. top 5000 by frequency in raw_trace.jsonl; full read of N chapters; anomaly-scan output>

---

## Summary

| class | count | notes |
|-------|-------|-------|
| converter-bug  |   |  |
| source-defect  |   |  |
| review         |   |  |

---

## 1. converter-bug
Raw bytes clearly encode a DIFFERENT (correct) word → fix belongs in
`scripts/gopika_decode.py` (structural). Sort by frequency (impact) descending.

| word | raw | hex | expected | confidence | refs | note |
|------|-----|-----|----------|------------|------|------|
|  |  |  |  |  |  |  |

---

## 2. source-defect
Raw bytes already encode exactly the (wrong) output → the original app has the
typo. Candidate for a whole-word/phrase entry in `scripts/lexical_fixes.py`.

| word | raw | hex | expected | confidence | refs | note |
|------|-----|-----|----------|------------|------|------|
|  |  |  |  |  |  |  |

---

## 3. review (uncertain — do NOT change)
Looks off but you are not sure, or it may be a valid variant / translation
wording. Leave for a native reader.

| word | raw | context | why flagged | confidence |
|------|-----|---------|-------------|------------|
|  |  |  |  |  |

---

## 4. Not errors (verified good, noted to avoid re-flagging)
Optional: anything you checked and confirmed CORRECT that might look wrong at a
glance (e.g. Sanskrit virama-finals, valid rare spellings).

| word | why it is correct |
|------|-------------------|
|  |  |

---

## Open questions for the maintainer
<Anything you couldn't resolve, patterns you suspect but couldn't confirm,
books/sections not yet covered, etc.>
