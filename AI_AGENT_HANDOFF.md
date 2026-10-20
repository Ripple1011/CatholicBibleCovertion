# AI Agent Handoff — Gujarati Catholic Bible Spelling Audit (take-over context)

You are taking over a long-running, multi-pass **spelling/conversion audit** of a
Catholic Gujarati Bible + 3 songbooks. A previous agent ran several audit passes;
a human maintainer (with a code-execution assistant) resolved each pass. Your job
is to **produce the next audit pass** (Bible Pass 5), in the same style and with
the same discipline as prior passes.

Read this entire file first. It gives you the full project, the method, what is
already fixed, the guardrails, and exactly what to produce.

---

## 1. What the project is

- Source: an Android app ("Gurjarvani", `in.maxwellchristian.gurjarvani`) whose
  Gujarati text is stored in a **legacy ASCII-overlay font ("Gopika Two", Arpita
  variant)** — NOT Unicode. Each Latin byte draws a Gujarati glyph.
- The maintainer reverse-engineered a **converter** that turns that legacy text
  into proper **Unicode Gujarati JSON** (book → chapter → verse).
- Repo (private): `https://github.com/Ripple1011/CatholicBibleCovertion`
- LICENSING: the translation + songbooks are copyrighted. This is a private
  digitization pending publisher permission. Do not redistribute.

## 2. Current state (as of this handoff)

- **Bible**: `output/bible.json` — shape `{testament: {book_id: {name, chapters:
  {chap: {verse: text}}}}}`. OT 46 books / NT 27 books. **34,891 verses.**
- **Songbooks**: `output/kirtansagar.json`, `holi_gito.json`, `natal_garba.json`
  — shape `{id: {text}}`.
- Regression suite: **80/80 passing**.
- Structural anomaly scan: **clean** (only known-good residue — see Section 6).
- Audit progress so far:
  - Kirtansagar: Pass 1, 2, 3, + final review queue — DONE.
  - Bible: Pass 1, 2, 3, 4 — DONE. **You produce Bible Pass 5.**

## 3. The files you have (from the repo; no APK needed)

| File | What it is |
|------|------------|
| `output/bible.json` | the Bible to audit |
| `output/kirtansagar.json` etc. | songbooks |
| `output/book_names.json` | book-id → English name index |
| `reports/raw_trace.jsonl` | CRUCIAL: 51,882 distinct words, each with its RAW Gopika bytes/hex + refs + frequency. Lets you classify converter-bug vs source-defect WITHOUT the APK. One JSON object per line: `{"u":<unicode word>, "raw":<gopika>, "hex":..., "unswap":..., "n":<freq>, "refs":[...]}` |
| `reports/CONVERTER_FIX_EXPLANATION.md` | every converter fix made so far |
| `reports/BIBLE_AUDIT_PASS[1-4]_RESOLUTION.md` | what each Bible pass fixed |
| `reports/AUDIT_PASS[1-3]_RESOLUTION.md`, `KIRTANSAGAR_FINAL_REVIEW_RESOLUTION.md` | songbook resolutions |
| `PROOFREADING_GUIDE.md` | the full method (read it) |
| `scripts/gopika_decode.py`, `lexical_fixes.py`, `html_extract.py`, `20_build_json.py` | the converter + build (the maintainer runs these, not you) |

## 4. The method (how to do an audit pass)

The point: find **invalid Gujarati that is still VALID-LOOKING** — structural
scanners miss it, only a reader catches it. Your value is linguistic judgment.

1. Scan `output/bible.json` verse text (skip the English `name` fields).
   Prioritize: high-frequency words; correct-vs-suspicious coexistence (a word
   appears both right and wrong in the corpus); known Gopika-sensitive
   conjuncts/ligatures; reph (ર્) families; verse-boundary sanity.
2. For EVERY suspect word, look it up in `reports/raw_trace.jsonl` and copy its
   `raw`/`hex`. This is mandatory — it lets the maintainer verify your call.
3. Classify each finding:
   - **converter-bug**: raw bytes clearly encode a DIFFERENT (correct) word.
   - **source-defect**: raw bytes already encode the wrong output (the app data
     itself is wrong).
   - **review**: unsure / may be valid archaic/poetic → do NOT change.
4. Group findings into FAMILIES (one root cause), not isolated words. Give counts
   and 2-3 example refs per family.
5. Output a handoff doc (see Section 7). DO NOT edit JSON yourself.

## 5. What is already fixed — DO NOT re-report these

Converter bugs already fixed (all structural, corpus-wide):
- **જો ligature**: `òu`+many consonants → જો (જોઈ, જોયો, જોતાં, જોકે, જોડ, જોર,
  જોખમ, જોગવાઈ, જોશે, કમજોર, સંજોગોમાં, તેજોમય…). `òu`+end/ન/વ/અ/મ/થ stays genuine
  જે (જે, બીજે, વંશજે, જેવું, જેમ, જેવા). ~3,400 words.
- **Š reph glyph** (reph + short-i): મૂર્તિ, કીર્તિ, સમર્પિત, પાર્થિવ, અહર્નિશ.
- **ખ્રિસ્ત short-i** (`િ` before `્ર`): ખ્રિસ્ત (Christ), પ્રિય, ગાબ્રિયેલ,
  અગ્રિપ્પા — short-i now hops C+્ર clusters.
- **reph on half-form conjunct** (ત્ય): વર્ત્યો, મર્ત્ય, અર્પ્યા, સમર્પ્યો,
  નિર્મ્યા.
- **જ્ઞ/ત્ર conjunct aa**: આજ્ઞાઓ (was આજ્ઞ).
- **inherent-vowel 'k' / spurious ા**: પંથ, વચન, દિવસ, અને, તો/તે etc.
- **matra ordering**: તેં, ખેંચી, મોકલ્યું; repeated-matra ખેડ/ભેટો; double
  anusvara; colon-vs-visarga (ઃ vs :).
- **verse-boundary recovery**: Deut 7:14, Isaiah 27:2, Ezekiel 31:5, 1 Sam 29:3.

Source-defects already fixed (lexical): વહેંચ-, વિચાર્યું, મર્યું, નર્યું, થયું,
સર્જ-, અર્પ-, કહ્યું, તેમને, કરીને, હું, એવું, સાંપ્યું, નિયમો, મબલખ, પારેવાનાં,
ઈશ્વરનું, બધા, and more (full list in `scripts/lexical_fixes.py`).

## 6. KNOWN-GOOD — never flag these as errors

- **Word-final virama ્** on Sanskrit loanwords: અર્થાત્, દંડવત્, શરણમ્,
  સ્વાગતમ્, સાક્ષાત્ (~185). CORRECT.
- **`:`-as-meaning in Daniel 5:25-28** (મને=ગણેલું etc.) — source formatting.
- **236 literal `"-"` verse values** (Numbers 2/7, Ezra 2, Nehemiah 7, Psalms,
  Song of Songs…) — the app grouping/continuation convention, NOT lost text. Do
  NOT demand a verse for every missing key.
- **Numbers 31:33-45 missing keys** — empty source anchors by design; the summary
  is legitimately in v46. Not a bug.
- **Esther 5** embedded `(૧૫)/૨/૩/૪/૫` numbering — intentional deuterocanonical
  additional-material numbering. Do NOT treat as a verse-boundary bug.
- **Footnote digits glued to words** (આદમે૧, નૂહ૧, બાબિલ૧…) — footnote markers, a
  separate formatting concern, not spelling.
- **Edition/house style, do not modernize**: કયું (not કર્યું; ~1183×), પહાંચ-
  (not પહોંચ), નવ (poetic 'not'), નાહીં, પરથમ, પુત્તર, ર્હે/ર્હેજે, કરજા,
  archaic/folk/devotional forms, Sanskritic spellings (શાન્ત), proper-name
  transliteration variants (મરિયમ/મિરિયમ) unless clearly a single-song typo.
- English `name` fields in bible.json (Genesis, MATHEW…) — intentional index.
- Deuterocanonical books (Tobit, Judith, 1&2 Maccabees, Wisdom, Sirach, Baruch) —
  correct Catholic canon.

## 7. What to PRODUCE (your deliverable)

A single markdown handoff named `BIBLE_AUDIT_PASS5_HANDOFF.md`, matching the style
of prior passes. For each finding include:

| field | meaning |
|-------|---------|
| current | the suspect converted word/phrase |
| expected | the word you believe is correct |
| raw / hex | from `raw_trace.jsonl` (so the maintainer can verify) |
| count | occurrences |
| refs | 1-3 verse locations (book chap:verse) |
| class | converter-bug / source-defect / review |
| confidence | HIGH / MEDIUM / LOW |

Group by family. Lead with the highest-impact family. Add a "do not change"
section for anything you checked and confirmed CORRECT. End with a recommended
resolution order.

Critical rules:
- Do NOT edit `output/bible.json` or any script. Your output is the findings doc.
- Always include raw/hex from `raw_trace.jsonl` — a finding without it cannot be
  verified.
- Prefer families over isolated words.
- When unsure → class=review, confidence=LOW. For scripture, a false "fix" is
  worse than a missed one.
- Respect every item in Section 6.
- Note whether a family looks structural (same raw pattern → converter bug, high
  value) vs scattered (likely source typos → lexical).

## 8. Good places to look for Pass 5 (hints, not exhaustive)

- Remaining **reph (ર્) families** not yet covered (other half-form + consonant
  conjuncts; reph before specific clusters).
- **Proper names** (OT especially): kings, places, tribes — transliteration
  consistency (e.g. recurring name spelled two ways; -યલ vs -એલ endings).
- **Low-frequency vocabulary** where a correct high-frequency sibling exists
  (coexistence signal).
- Remaining **`ે` vs `ો` (o-matra)** confusions, or `ાૃ`/double-matra tails.
- Verse-tail sanity: text ending mid-word, stray single letters, leaked markup.

## 9. One-paragraph brief you can paste to start a fresh chat

"You are auditing a Catholic Gujarati Bible (`output/bible.json`) converted from a
legacy Gopika font to Unicode. Four Bible audit passes are done. Read
`AI_AGENT_HANDOFF.md`, `PROOFREADING_GUIDE.md`, and the
`reports/BIBLE_AUDIT_PASS*_RESOLUTION.md` files first. Then produce
`BIBLE_AUDIT_PASS5_HANDOFF.md`: find valid-looking spelling/conversion defects not
yet fixed, trace each to `reports/raw_trace.jsonl` (include raw/hex), classify
converter-bug vs source-defect vs review, group by family, and respect the
known-good / do-not-change list. Do not edit the JSON."
