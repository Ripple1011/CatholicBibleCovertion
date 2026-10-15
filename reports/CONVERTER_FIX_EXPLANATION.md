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

---

## Follow-up fix: conjunct-core pre-base short-i (રાત્રિ)

The pre-base short-i (`r`) and reph reorder rules hop exactly one orthographic
*cluster*. The `CLUSTER` regex originally recognized only table consonants and
half-forms, but NOT the single-byte EXTRA conjunct cores (`º`=ત્ર, `û`=ક્ષ,
`¥`=ત્ત, `Ì`=હ્ય, `Ù`=્ર, `†`=સ્ત્ર). So in `hkrºk` (રાત્રિ) the short-i could
not hop `º`(ત્ર) and landed wrong → `રિત્ર`.

Fix: add the EXTRA consonant-cluster cores to the cluster character class
(excluding the pure matra/reph markers r,o,Š,®,Â,O,U). Result: `hkrºk` → રાત્રિ.
Regression suite now 30/30 (added રાત્રિ and સર્જનહાર). Whole-Bible scan shows
**0** `matra+short-i` sequences and **0** duplicate-virama.

## Note: સર્જ્યાં (Genesis 1:1) — source defect, not a converter bug

Genesis 1:1's last word decodes to **સજ્યાં**, not સર્જ્યાં. The raw bytes are
`MkßÞkO` = સ + (inherent) + જ્ય + ાં — there is **no reph glyph** in the source.
The `ßÞ`=જ્ય pattern occurs 539× and is correct elsewhere (જ્યોતિ, રાજ્યમાં,
જ્યારે); reph, when present, is the `o` marker (e.g. `MksoLk`=સર્જન). So the
missing reph on this one word is a **source-data defect in the app**, which the
app itself would render as સજ્યાં. It is a candidate for an output-level
lexical correction, not a decoder rule (the decoder must not invent bytes).

---

## Fix: punctuation colon vs visarga (ઃ)

The mapping table pairs `:` <-> ઃ, so EVERY ascii colon was becoming visarga ઃ
(e.g. a list intro "કરી : અનાજ" or a reference "1:12" rendered "ઃ"). But ઃ is a
real character in Gujarati (દુઃખ). Classified the raw corpus:
- 590 colons have a SPACE before, 104 have a DIGIT neighbour  -> PUNCTUATION
- 66 are letter-attached both sides (દુઃખ etc.)               -> GENUINE visarga

`fix_unicode()` now restores ઃ -> ':' only when space- or digit-adjacent (or at
end of string); letter-attached visarga is kept. Result: 419 genuine visarga
retained, 2410 punctuation colons restored; Gen 1:12 reads "...કરી : અનાજ...".

## Fix: output-level lexical corrections (scripts/lexical_fixes.py)

A SEPARATE, auditable module applies whole-word corrections for CONFIRMED
source-data defects, after the structural decode. Currently:
  સજ્યાં -> સર્જ્યાં,  સજ્યું -> સર્જ્યું   (missing-reph source typo; see the
  સર્જ્યાં note above — the reph is absent from the source bytes). Occurrences:
  6 + 2. Word-boundary guarded (does not fire inside larger tokens).
Wired into 20_build_json.py: convert() = apply_lexical_fixes(decode()).
Gen 1:1 now reads "...આકાશ અને પૃથ્વી સર્જ્યાં."

---

## Fixes: reph-on-half-form, repeated matras, pronouns, હવા

**Reph on a half-form consonant (વતેર્ → વર્તે).** The reph `o` reorder rule
required a consonant immediately before the matra run, but after the half-form
`k`-marker fix a half-form carries an INH sentinel (`í`=ત્ + \x1d + ે). The rule
now (a) accepts a half-form as the consonant and (b) includes the INH/AA
sentinels in the matra run, so `ðíkuo` → વર્તે (was વતેર્). Fixed પ્રવર્તે too.

**Repeated dependent-vowel matras (ખેેેડ → ખેડ, ભેેટો → ભેટો).** The font
sometimes emits a matra byte 2–3× in a row (`¾uuuz`). A run of the same matra
byte `[uewqi]+` is collapsed to one. 0 repeat-matra sequences remain corpus-wide.

**Sentinel byte collision.** The FULL-consonant o/au temp used `\x1e`, which
equals the AA sentinel — changed the temp to `\x1f` to remove any overlap.

**Lexical layer additions (scripts/lexical_fixes.py).** Byte `U`(0x55) is
anusvara ં in most words (નોંધ, પહોંચી, સોંપી), but the 1st/2nd-person pronouns
need ેં; and હવા is a full-consonant spurious-ā case (not rule-separable from
મારા). All whole-word, boundary-guarded:
  તં→તેં (×305), મં→મેં (×291), હાવા→હવા (+ હવાને/હવામાં).

Gen 4:10 now "...કહ્યું, "તેં આ શું કયું?..."; Gen 4:14 "...ખેડખેતરમાંથી ...
ભેટો થશે...". Regression suite 30/30; 0 repeat-matra, 0 duplicate-virama,
0 leftover Latin across all JSON.
