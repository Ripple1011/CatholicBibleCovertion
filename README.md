# Catholic Gujarati Bible — Gopika (legacy font) → Unicode conversion

Tooling, mapping data, and converted output for turning the **Gurjarvani**
Android app's legacy-font Gujarati text (Catholic Bible + three songbooks) into
**Unicode Gujarati JSON**.

> ⚠️ **Licensing / copyright.** The Bible translation and songbooks are
> copyrighted. This repo is **private**; the content must not be redistributed
> without **written permission from the rights holder** (publisher / diocese /
> Bible society). See FINDINGS.md.

## What's here

| Path | What it is |
|------|------------|
| `scripts/gopika_decode.py` | **The converter.** Gopika Two (Arpita variant) → Unicode Gujarati. |
| `scripts/gopika_table.py` | Parses the glyph mapping table from `source_assets/myExpr.js`. |
| `scripts/html_extract.py` | Extracts verse text from the source HTML (UTF-8, gujFont-scoped). |
| `scripts/20_build_json.py` | Orchestrator: walks the APK, converts, writes JSON. |
| `scripts/test_gopika_regressions.py` | 28-case regression suite (raw→expected). |
| `scripts/23_before_after.py` | Old-vs-new diff / suspicious-pattern report generator. |
| `scripts/01..22_*.py` | Diagnostic / reverse-engineering scripts (not in output path). |
| `source_assets/myExpr.js` | Upstream Unicode↔Gopika table (credit: RahulThakor/GujaratiFontConverter). |
| `source_assets/assets/*.TTF` | GopikaTwo / SudhirTwo legacy fonts. |
| `output/bible.json` | OT 46 books / 1068 ch + NT 27 books / 260 ch, Unicode. |
| `output/kirtansagar.json`, `holi_gito.json`, `natal_garba.json` | Songbooks. |
| `output/manifest.json`, `book_names.json` | Counts + book-name index. |
| `reports/CONVERTER_FIX_EXPLANATION.md` | How the raw `k` marker is parsed (the big fix). |
| `reports/*_before_after.md` | Per-corpus before/after change tables. |
| `FINDINGS.md`, `MANUAL_FIXES.md`, `residue_report.txt` | Status + residuals. |

The 17 MB source HTML tree and the APK are not committed (reproducible, bulky).
`20_build_json.py` reads them from the APK zip — set the `APK` path at the top.

## Pipeline (summary)

1. Source: APK `in.maxwellchristian.gurjarvani v1.0.3`; HTML per chapter/song.
   No DOC/PDF, **no OCR**.
2. Read as UTF-8 → recovers Gopika Latin-1 glyph chars.
3. Isolate `<gujFont>` blocks; split verses on `<a name="vN">` anchors.
4. Font: Gopika Two **Arpita** variant (ASCII-overlay legacy font).
5. Mapping: `array_one` in myExpr.js, inverted for decode.
6. Arpita unswap (k↔t, Œ/Ë/‚), matra reorder (pre-base short-i, reph, ®/Š/Â),
   table decode, post-fix (sentinel resolution, virama, spurious-aa).
   **No Unicode normalization (NFC) is applied.**
7. JSON: json.dump(ensure_ascii=False, indent=1).

Run: `PYTHONIOENCODING=utf-8 python scripts/20_build_json.py`

## The core fix — raw `k` inherent-vowel marker

Byte 0x6b (`k`) is the font's inherent-vowel marker, NOT a literal `ા`. Meaning
depends on the preceding glyph class:

| Raw context | Unicode | Example |
|-------------|---------|---------|
| HALF-form glyph + `k` | bare consonant (inherent a, no matra) | `sLk` → જન |
| HALF-form + `kk` | consonant + `ા` | `økkZ` → ગાઢ |
| HALF-form + `k` + vowel byte | consonant + that vowel | `yLku` → અને |
| FULL consonant + `k` | genuine `ા` | `{khk` → મારા |

The half-form-vs-full-consonant distinction is the discriminator that makes
`વચન` drop its final `ા` while `મારા` keeps it. Implemented with raw-stream
sentinels (INH/AA) resolved after decode; duplicate virama `ક્્યાં → ક્યાં`
collapsed. Details: reports/CONVERTER_FIX_EXPLANATION.md.

Impact (bible): `પાણ→પણ` x6804, `ઉપાર→ઉપર` x4703, `પાછી→પછી` x3176,
`નાહિ→નહિ` x1716; `પાંથ` 66→0, `ક્્યાં` 438→0, duplicate-virama 1137→0,
leftover Latin 0. Regression suite 28/28 pass; Genesis 1:1 intact.

## Diagnosis reference

- Spurious `ા` → glyph-mapping/model (the `k` marker, now fixed structurally).
- `ક્્યાં` double virama → mapping overlap (`õ`=ક્ + `â`=`્ય`), collapsed.
- Missing reph / short-i edge cases → reorder logic (small tail remains).
- Legacy encoding itself → source reality, not a bug introduced here.
- No OCR anywhere; no Unicode normalization applied.

## Credits

Mapping table myExpr.js + GopikaTwo fonts: RahulThakor/GujaratiFontConverter
(GitHub). Reordering cross-checked vs Unicode 16 core spec Ch. 12 and Microsoft
OpenType Gujarati shaping docs. Runtime: Python stdlib only; fontTools only in
diagnostics.
