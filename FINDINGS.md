# Gurjarvani APK extraction — findings

Source: `in.maxwellchristian.gurjarvani_1.0.3.xapk` (ApkPure), base APK
`in.maxwellchristian.gurjarvani.apk`. Package `in.maxwellchristian.gurjarvani`
("Gurjarvani"), version 1.0.3.

## ⚠️ Licensing
Extraction is technically trivial, but the Bible translation + songbooks are
almost certainly copyrighted. Reuse in another app requires **written permission
from the rights holder (publisher/diocese/Bible society)** — the app bundling it
does NOT make it public domain. User has stated they are pursuing publisher
permission. Do not distribute without it.

## Content inventory (all plain HTML, NOT encrypted)
Layout: `assets/<collection>/<book>/<chapter>.html`; verses marked with
`<a name="vN">N</a>` anchors inside a `<gujFont>` block.

- `assets/0/` — **Old Testament, 46 books** (Catholic canon incl. deuterocanon), 1068 chapter files
- `assets/1/` — **New Testament, 27 books**, 264 chapter files
- `assets/kirtansagar/` — 1049 hymns (Kirtan Sagar songbook)
- `assets/holi_gito/` — 38 songs
- `assets/natal_garba/` — 12 Christmas garba songs
- `assets/sc_2018*.html` — ~13 files, likely liturgical calendar (TBD)
- Total: 2444 HTML files.

## Encoding: legacy font "Gopika Two"
Text is NOT Unicode. It is bytes for the **Gopika Two** font
(`GopikaTWO_N.TTF` / `_B.TTF`; songbooks also use `SudhirTwo.TTF`), declared via
`customFontsAndStyles.css` (`<gujFont>` -> font-family GopikaTwo). ASCII-overlay
font: the TTF cmap maps Latin codepoints to glyphs whose NAMES are still Latin
(`A`,`k`,`space`), so the font gives NO machine-readable Unicode identity —
mapping must come from a known Gopika/Shree-Lipi table + verification.

- ~152 distinct byte values in the corpus; ~120 carry Gujarati glyphs.
- Bytes are **latin-1** (read files as latin-1, not utf-8).

### Confirmed mappings (from Genesis 1:1 ground truth)
Genesis 1:1 legacy `«kht¼{kt Eïhu ykfkþ yLku Ãk]Úðe MkßÞkO`
= Unicode `આરંભમાં ઈશ્વરે આકાશ અને પૃથ્વી સર્જ્યાં`.

| byte | hex | Unicode | char |
|------|-----|---------|------|
| k | 6b | U+0ABE | ા (aa-matra) — most frequent glyph |
| y | 79 | U+0A85/86 | અ/આ base vowel |
| L | 4c | U+0AA8 | ન |
| u | 75 | U+0AC7 | ે (e-matra) |
| f | 66 | U+0A95 | ક |
| þ | fe | U+0AB6 | શ |
| E | 45 | U+0A88 | ઈ |
| Ã | c3 | U+0AAA | પ (2nd most frequent) |
| ] | 5d | U+0AC3 | ૃ (ru-matra) |
| M | 4d | U+0AB8 | સ |

### Reordering / conjuncts (confirmed to exist, rules TBD)
- Pre-base short-i matra reorder expected (standard for legacy Gujarati fonts).
- Half-forms + virama (U+0ACD) conjuncts: word `MkßÞkO` -> `સર્જ્યાં` shows
  multi-byte half-form clusters (`ß` de/`Þ` df region) and a trailing `O` (4f)
  that maps to anusvara `ં` belonging earlier in logical order.

## Status: CONVERTER BUILT + JSON GENERATED
Converter: `scripts/gopika_decode.py` (table from RahulThakor/GujaratiFontConverter
myExpr.js, inverted) + `scripts/html_extract.py` (gujFont-scoped verse split).
Pipeline: UTF-8 decode -> collapse kk runs -> Arpita unswap -> short-i/reph
reorder -> table decode -> drop spurious aa-before-matra -> half-form fix.

Quality: ~80% of output chars are Gujarati (rest spaces/punct/digits); only
**8 stray Latin chars in the whole corpus** (all source-HTML defects, see
MANUAL_FIXES.md); double-matra artifacts cut from ~200k to ~3k.

Output JSON in `output/`:
  bible.json (11MB, OT 46 books/1068 ch + NT 27 books/260 ch),
  kirtansagar.json (524 songs), holi_gito.json (38), natal_garba.json (12),
  manifest.json, book_names.json.

### FINAL quality (after 2nd polish pass)
- Songbooks (574 songs): **0 strays**. Bible verse TEXT: only **3** entries with
  any latin/markup char — all Daniel 5:25-28, where `=` means "means"
  (મનો=ગણેલું etc.), the source's intentional formatting, NOT an error.
  (The English `name` fields are the book-name index, English by design.)
- Double-matras down to ~316 (from ~200,000 originally).
- Verified fluent: John 3:16, Psalm 23:1, Genesis 1.
- Converter fixes applied: I->ૌં, g->ખ્ત, â->્ય, ®->િં, Š->ર્િ, Â->િ(conjunct),
  û->ક્ષ્, ¥->ત્ત્, º->ત્ર્, Ì->હ્ય, Ù->્ર, †->સ્ત્ર, &->શ્ (પ્રશ્ન/અશ્લીલ) ;
  short-i(r)/reph(o) reorder with CORRECT single-cluster hop (conjunct-aware:
  half-forms + full-conjuncts Ø/ù counted) — fixed દિવસ/વૃદ્ધિ/નિશ્ચિત/શક્તિ;
  kk-collapse; spurious-aa-before-matra drop; half-form+matra virama drop.
- **અનો->અને fix (the word "and", ~25,300 occurrences)**: a single inherent
  'k' between a HALF-FORM consonant and a real matra is spurious and dropped
  (yLku = અ ન્ [k] ે -> અને). The o/au matras (íkku=તો, 'kku') are protected
  with a sentinel BEFORE the kk-collapse so તો vs તે stay distinct. Now
  અને=25297 vs અનો=19 in bible.json; verified તે/તો/પોતાનો/એકનો correct.
- html_extract trims anchored markup leaks (href/file/broken id="vN"/leading
  stray 'v') — cleaned Ecclesiastes 11:9, Maccabees/Psalms anchors, Matthew 22:40.

### Known residuals for manual/native-reader pass (MANUAL_FIXES.md)
- The trailing spurious `ા` (`માણસા`->માણસ, `વાતા`->વાત, `પાછી`->પછી). NOT
  auto-fixable: a word-final single raw `k`(0x6b) is genuine aa in `મારા`/`હતા`/
  `ગયા` (correct) but spurious in `માણસ`/`વાત`. Position cannot distinguish them
  — needs a dictionary or the consonant-marker model. Left intact to avoid
  corrupting the many correct -ા words. THIS is the main remaining quality item.
- `સાજ્યાં`->`સર્જ્યાં` (reph in સ-ર cluster). (અનો->અને now FIXED, see above.)
- rare ÌË (હૃદ) left as હ્ય.
- Daniel 5:25-28 `=` ("means") left as source formatting.
- book46 title in source = 'Genesis' but is Psalms (150 ch) - corrected in builder.

### Book canon = CATHOLIC (confirmed)
OT 46 incl. Tobit, Judith, 1&2 Maccabees, Wisdom, Ecclesiasticus/Sirach, Baruch.

## Environment notes
- Python 3.13 (miniconda at D:\AI_DATA\miniconda) has fonttools, bs4, lxml.
- Console is cp1252 — set `$env:PYTHONIOENCODING='utf-8'` or wrap stdout for
  Gujarati output.
