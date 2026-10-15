# Converter fix — how the raw Arpita `k` marker is now parsed

## The root cause (confirmed against raw bytes)

In the Gopika Two "Arpita" stream, byte **`0x6b` (`k`)** is NOT a literal
Unicode `ા`. It is the font's **inherent-vowel / consonant-completion marker**.
Its meaning depends on the glyph it follows:

| Raw context | Meaning | Unicode |
|-------------|---------|---------|
| **HALF-form** glyph (e.g. `L`=ન્) + `k` | complete the half-form to a bare consonant carrying the inherent *a* | consonant, **no matra** (e.g. `sLk` → જન) |
| HALF-form + `kk` | consonant + genuine long-ā | consonant + `ા` (e.g. `økkZ` → ગાઢ) |
| HALF-form + `k` + vowel byte (`u e w q ] i`) | consonant + that vowel sign (the `k` is the completion) | e.g. `yLku` → અને |
| HALF-form + `kku` / `kki` | consonant + `ો` / `ૌ` | |
| **FULL** consonant glyph (e.g. `h`=ર, `{`=મ) + `k` | genuine ā-matra | consonant + `ા` (e.g. `{khk` → મારા) |

The discriminator is **half-form vs full-consonant glyph**, which the font
encodes distinctly (half-forms map to `C + virama`; full consonants map to a
single consonant). This is why `વચન` (`ð[Lk`, ends in half-na) must drop its
final `ા` while `મારા` (`{khk`, ends in full-ra) must keep it — a distinction
that is impossible to make by position or k-count alone, but trivial by glyph
class.

## What changed in `gopika_decode.py`

The previous code did a blind `re.sub(r'k{2,}', 'k', s)` and only special-cased
a couple of patterns. It has been replaced by explicit raw-stream parsing that
tags each half-form decision with a sentinel, resolved after table decode:

```
INH = '\x1d'   # half-form completed to bare consonant (inherent a) -> drop virama, no matra
AA  = '\x1e'   # half-form + genuine long-aa -> drop virama, add ા
```

Order (longest first), applied on the raw gopika BEFORE unswap/reorder:

1. `HALF + kku` / `HALF + kki`  → `HALF INH ku` / `HALF INH ki`  (o/au matra kept)
2. `HALF + kk`                  → `HALF AA`                      (genuine ā)
3. `HALF + k + <vowel byte>`    → `HALF INH <vowel>`             (e.g. ને)
4. `HALF + k`                   → `HALF INH`                     (inherent a → bare consonant)
5. FULL-consonant `kku`/`kki`   protected, then a residual `k{2,}` collapse for
   stray doubled markers after full consonants. A single `k` after a full
   consonant is left to decode as `ા` (so મારા/રાજા are preserved).

`fix_unicode()` then resolves the sentinels structurally:

```python
u = re.sub(r'([ક-હ])્' + INH, r'\1', u)   # C ્ INH  -> C   (drop virama, inherent a)
u = re.sub(r'([ક-હ])્' + AA,  r'\1ા', u)  # C ્ AA   -> C ા
u = re.sub(r'્્+', '્', u)                 # collapse duplicate virama (ક્્ય -> ક્ય)
```

An NFC-style duplicate-virama collapse fixes the `ક્્યાં → ક્યાં` family
(caused by a half-form `õ`=ક્ already carrying a virama, then `â`=`્ય` adding
another).

## Measured impact (before → after)

From `reports/*_before_after.md` (full tables there):

| pattern | bible | kirtansagar |
|---------|-------|-------------|
| `ક્્યાં` (dup virama) | 438 → 0 | 88 → 0 |
| `ક્્યારે` | 78 → 0 | 28 → 0 |
| `પાંથ` | 66 → 0 | 68 → 0 |
| `નાભમંડળ` | 12 → 0 | 8 → 0 |
| `દુર્જના` | 68 → 0 | 5 → 0 |
| duplicate virama `્્` (total) | 1137 → 0 | 162 → 0 |
| leftover Latin | 0 → 0 | 0 → 0 |

Top word corrections (bible): `પાણ→પણ` ×6804, `ઉપાર→ઉપર` ×4703,
`પાછી→પછી` ×3176, `તામે→તમે` ×2813, `નાહિ→નહિ` ×1716, `બાધા→બધા` ×1647.

`અને` remains correct; `અનો` count rose 19→45 but those are the proper noun
**અનોશ** (Enosh), i.e. correct. Genesis 1:1 and all 28 regression cases pass.

## Regression tests

`scripts/test_gopika_regressions.py` — 28 cases, **28/28 pass**: the spurious-ā
family (જન/વચન/જીવન/મન/પંથ/અડગ), the keep-ā words (મારા/તારા/રાજા/પિતા/માતા/હતા),
અને/તે/તો, Genesis 1:1 words, conjunct/short-i/reph cases, and the
no-duplicate-virama case (મૂક્યાં).

## Remaining residual (documented, not auto-fixed)

A small tail of double-matra sequences (`ેે`, `ૃિ`, `ેિ` — low hundreds total
across 11 MB) from rare cluster edges, and the Daniel 5:25-28 `=` ("means",
intentional source formatting). These are for a native-reader pass; they are no
longer the dominant systematic error.
