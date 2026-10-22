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

---

## Fixes: EXTRA-core o-matra (રહ્યો), anusvara+u order (મોકલ્યું)

**EXTRA conjunct core + o/au matra (રહ્યે → રહ્યો).** Cores like Ì=હ્ય have a
TABLE key of the 2-char form 'Ìt'=હ્ય. When the core takes an o-matra
('hÌkku' = ર હ્ય ો), the greedy table match grabbed 'Ìt'=હ્ય and stranded the
'u'(ે), giving રહ્યે. Fix: for each EXTRA core, pre-decode 'core+kku'/'core+kki'
to '<unicode> + ો/ૌ' before table decode (narrowly — only the o/au case, so
short-i handling like રાત્રિ is untouched).

**Anusvara + u order (મોકલ્યંુ → મોકલ્યું).** A 'ં' immediately followed by a
below vowel sign (ુ/ૂ) is mis-ordered; swap to put the vowel first:
'ં'+(ુ/ૂ) -> (ુ/ૂ)+'ં'. 53 occurrences corrected; 0 remain.

Note: વષર્/માગેર્ (→ વર્ષ/માર્ગે) and મં (→ મેં) were already fixed by the
earlier reph-on-half-form and lexical-pronoun changes; counts are now વર્ષ 655,
માર્ગે 256, રહ્યો 645, મોકલ્યું 19, and 0 of each wrong form.
Regression suite 37/37.

---

## Fix: જ્ઞ/ત્ર/ક્ષ-family conjunct cores losing their aa (આજ્ઞઓ → આજ્ઞાઓ)

Conjunct cores whose ONLY table key is the 2-char 'core'+'t' form — ¿=જ્ઞ,
º=ત્ર, û=ક્ષ, ²=સ્ર, Ì=હ્ય, Ò=ન્ન, ¥=ત્ત — absorb the aa into the glyph ('t').
So 'core kk' = conjunct + a real aa, but the generic k-collapse ate the second
k and dropped the aa:  yk¿kk 'આજ્ઞા' decoded as આજ્ઞ. Fix: for each such core,
'core'+'kk' -> <conjunct Unicode> + 'ા' (built automatically from the table).
Impact: આજ્ઞઓ 249 -> 1, આજ્ઞા 1 -> 872. Regression 52/52.

## Fix: 3 stranded-lone-matra source defects (verified in context)

The source occasionally emits a lone matra as its own space-delimited token.
A lone pre-base short-i 'િ' joins the FOLLOWING word (build step). Three
specific verses were confirmed against raw bytes + context and corrected via
scripts/lexical_fixes.py PHRASE_FIXES:
  - Matthew 5:19: 'જે કોઈે આજ્ઞાઓનું' -> 'જે કોઈ આજ્ઞાઓનું' (stray ે dropped)
  - Kirtansagar #102: 'વચાળે િ નજનું' -> 'વચાળે નિજનું'
  - Kirtansagar #103: 'જ્યાં િ છનવાયે' -> 'જ્યાં નિજ છવાયે'

After these, the anomaly scan reports 0 real-bug occurrences (only the
whitelisted word-final virama = correct Sanskrit, and Daniel 5 '=' = intentional).

---

## Fix: જો ligature (જોઈ/જોયો) — from Kirtansagar audit Pass-1

'ò'(0xf2) is the જ ligature base: alone it renders જા, but 'òu'+letter is the
જો ligature. The decoder was giving જે (ò=જા + ે collapsing). Verified every
'òuE'/'òuÞ'/'òuô'/'òuW' token corpus-wide (~2,600, 35 forms) is a જો verb form,
never genuine જે; bare 'òu' word-final stays જે (બીજે, કરજે). Fix in convert():
'òu[EÞ]'->જો+…, 'òuô'->જોઉં, 'òuW'->જોઉ. Bible જોઈ-prefix 0->1262.
Plus source-defect lexical fixes: સજ્ર્યો->સર્જ્યો, અપ્ર્યો->અર્પ્યો,
મબલક->મબલખ, અજેડ->અજોડ, ૫ણ->પણ. See reports/AUDIT_PASS1_RESOLUTION.md.

---

## Fix: 'Š' reph+short-i glyph (મૂર્તિ/કીર્તિ family) — Pass-2 audit

`Š`(0x160) = reph ર્ + short-i િ pre-base unit riding the next consonant:
`Š`+C(+k) -> ર્+C+િ. Was misplaced (મૂત્રિ). Now મૂર્તિ, કીર્તિ, સમર્પિત,
પાર્થિવ, અહર્નિશ, મૂર્તિમંત. Plus Pass-2 lexical: સરજ-→સર્જ- (prefix, guarded),
ઉતાર્યું, નિર્મ્યો, અર્પિત, ૫ાપનો→પાપનો, 'પુત્ર વિના'. See AUDIT_PASS2_RESOLUTION.md.

---

## Fix: short-i before C+્ર (ખ્રિસ્ત) — Pass-3 audit

Pre-base short-i was landing before the ્ર conjunct (ખિ્રસ્ત). The cluster a
pre-base matra hops now includes an optional INH/AA sentinel + post-base ra
(ú/Ù), so C+્ર is hopped as one unit: ખ્રિસ્ત, પ્રિય, ગાબ્રિયેલ, અગ્રિપ્પા.
Corpus િ્ર 678→0; ખ્રિસ્ત 602. Plus lexical: અરપ→અર્પ prefix + 12 source typos.
See AUDIT_PASS3_RESOLUTION.md.

---

## Fix: expanded જો ligature (Bible Pass-1)

Enumerated every raw 'òu'+X; mapped 'òu' + JO-triggering glyphs (E Þ ô W z í h f
þ ¾ ø M x Ï ç ¤ ÷ R ý Ä) -> જો, while keeping 'òu' + <end>/L/ð/y/{/Ú/punct as
genuine જે (જેવું/જેમ/બીજે preserved). Bible: જેતાં/જેકે/જેડ/જેખમ/જેશે -> 0;
જોકે 123, જોખમ 50, જોડ 147, જોર 114. Lexical: વહંચ->વહેંચ (155), વિચાયું->
વિચાર્યું (40), + તેજોમય/જોરકડી/જોડિયો stragglers. See BIBLE_AUDIT_PASS1_RESOLUTION.md.

---

## Fix: verse-boundary recovery + Pass-2 defects (Bible)

html_extract.py now (a) recovers verses whose source anchor was missing by
splitting on an inline next-sequential verse number (+6 verses; 1 Chr 27:4/24),
and (b) strips a verse's own leaked leading numeral (James 3:8, Luke 1:13, 1 Cor
10:18). Lexical: ક્હ્યું->કહ્યું, તેમણ->તેમણે, જઈશ્વરનું->ઈશ્વરનું, ંબધા->બધા,
૫ારેવાનાં->પારેવાનાં, ઇસા્રયલ->ઇસ્રાયલ, stray-ચ (ચઅને/ચતેણે/…). See
BIBLE_AUDIT_PASS2_RESOLUTION.md.

---

## Fix: reph on half-form conjunct (વર્ત્યો) — Bible Pass-3

Reph 'o' on a HALF-form-led conjunct (ત્ય=íÞ) was riding the wrong consonant
(વત્ર્યો). Single-alternation reph regex now targets the first consonant of a
half-form conjunct, else a lone consonant, applied once (no double-apply; વર્ષ
preserved). Fixed: વર્ત્યો/મર્ત્ય/અર્પ્યા/સમર્પ્યો/નિર્મ્યા. Lexical: વર્તું,
માયે, તેણે, તેમને, કરીને, હું, એવું, સાંપ્યું, નિયમો, અન્નબલિ. Orphan '!ં'->'!'.
See BIBLE_AUDIT_PASS3_RESOLUTION.md.

---

## Fix: verse-boundary integrity (Bible Pass-4)

ANCHOR regex now tolerates whitespace around '=' (recovers Deut 7:14). Keyed
verse-recovery for 3 confirmed leaked-inline-own-number cases (Isaiah 27:2 drop
dup, Ezekiel 31:5 drop v4-spill, 1 Sam 29:2 recover v3) — NOT a general rule
(cross-refs/numbers/Esther-5 guardrail). Numbers 31:33-45 left as source grouping
(empty anchors, not lost text). Lexical: મર્યું/નર્યું/થયું, માણસો;પલિસ્તીઓએ.
Verses 34889->34891. See BIBLE_AUDIT_PASS4_RESOLUTION.md.

---

## Fix: 2-char conjunct-core short-i + reph over ૃ (Bible Pass-6)

(A) Conjunct cores ¿/²/Ò (table key 'core'+'t', e.g. Òt=ન્ન) now hop as ONE
atomic cluster for pre-base short-i, via an explicit 'core t' cluster
alternative (not a greedy t?). Fixes સિન્નધ્ય -> સાન્નિધ્ય (29). (B) reph matra
set now includes ']'(ૃ): ð]o -> ર્વૃ (દુર્વૃત્તિ). સાંનિધ્યમાં sibling preserved.
See BIBLE_AUDIT_PASS6_RESOLUTION.md.

---

## Fix: conjunct-core o-matra (યજ્ઞો/ઉન્નો) — Bible Pass-7

The _CONJ_CORE_T cores ¿/²/Ò lost their o-matra: core+kku fell through to the
generic shortening (-> core+ku -> જ્ઞ+ે). Extended the _CONJ_CORE_T loop to emit
core+kku -> <uni>+ો and core+kki -> <uni>+ૌ, while preserving core+ku (ે) and
core+kk (ા). Fixes યજ્ઞો/યજ્ઞોની/તત્ત્વજ્ઞો/ઉન્નો (14 locations); e/aa contrasts
and આજ્ઞા preserved. Family B (જેનારો) left review-only. See
BIBLE_AUDIT_PASS7_RESOLUTION.md.

---

## Fix: Š reph before a FULL consonant (ધાર્મિક) — Bible Pass-8

The Š (reph+short-i) handler only covered half-forms; before a FULL consonant
({=મ, ð=વ) it used the broken fallback -> મરિ instead of ર્મિ. Added a
full-consonant Š branch (new _FULL2UNI map) emitting ר्+C+િ without consuming the
consonant's inherent k. Fixes ધાર્મિક/ધર્મિષ્ઠ/ગર્વિષ્ઠ/નિર્વિવાદ (55) + names
ઈર્મિયા(Jeremiah)/પોર્કિયુસ (maintainer-approved, source-faithful) + songbook
ઊર્મિ. Half-form Š path preserved. See BIBLE_AUDIT_PASS8_RESOLUTION.md.

---

## Fix: reph over a reordered ordinary short-i (ધાર્મિક) — Bible Pass-9

Ordinary short-i 'r', after being reordered past its consonant, blocked the
reph-'o' rule (which lacked 'r' in its matra run). Added 'r' to that run.
Trace-wide delta = exactly 2 Bible words: ધામિર્ક->ધાર્મિક (2Chr 19:11),
સમપિર્ત->સમર્પિત (Deut 13:18). Valid િર્ words (નિર્દોષ/જ્યોતિર્મય/તિર્સા)
preserved. See BIBLE_AUDIT_PASS9_RESOLUTION.md.

---

## Fix: full-consonant Š reph over an Arpita-swapped carrier (સાર્દિસ) — Bible Pass-10

The full-consonant Š callback (_repl_reph_i_full) ran on the raw stream but
indexed the base-font table _FULL2UNI; for the swapped carrier raw Ë (=દ in this
Arpita source, but =સ in the base table) it emitted ר્સિ instead of ר્દિ, so
Sardis decoded as સાર્સિસ. Fix: normalize the single matched carrier via
unswap_arpita() before lookup. No-op for non-swapped carriers. Trace-wide delta =
exactly 4 raw records (3 Sardis verses Rev 1:11/3:1/3:4 + 1 Mark-preface
નિર્દિષ્ટ); live Bible diff = exactly 3 verses. See BIBLE_AUDIT_PASS10_RESOLUTION.md.

---

## Fix: half-form + candra-o (kkì) — Bible Pass-11

After a half-form consonant, the generic HALF+kk->aa branch consumed the first
two k's of kkì and stranded ì as a bare candra-e, so સૉને decoded as સાૅને (two
dependent vowels ા+ૅ). Added a HALF+kkì branch before the generic kk: first k ->
INH completion, remaining kì unswaps to tì (longest table key) -> candra-o ૉ.
Trace-wide delta = exactly 1 record (સાૅને->સૉને, 2 Kings 17:4). Anomaly
"two-matras-in-a-row" 1->0 corroborates. See BIBLE_AUDIT_PASS11_RESOLUTION.md.

---

## Fix: raw U glyph = e-matra + anusvara (ખેંચ-/ફેંક-) — Bible Pass-12

Font-outline evidence (GopikaTWO_N.TTF) proved raw U(0x55) has two contours: the
complete e-matra (u/ે) outline PLUS a nasal dot, so U = ે+ં = raw 'ut'. The
legacy EXTRA U->ં mapping dropped the vowel (ખેંચીને decoded as ખંચીને). Fix:
expand U->'ut' on the raw stream, BOUNDED to the demonstrated stem consonants
¾(ખ)/V(ફ): re.sub(r'(?<=¾)U|(?<=V)U','ut',s). A global U->ut (381 forms) would
rewrite 60+ frozen પહાંચ- and the સાંપ- family and is held out of release. Full
rebuild delta: 189 Bible verses, ALL ં->ેં e-matra restorations; songbooks 16
likewise; frozen પહાંચ-/સાંપ- and raw-t ખંચાવું untouched. Corrected the old
"U = anusvara only" docs. See BIBLE_AUDIT_PASS12_RESOLUTION.md.

---

## Fix: source-defect plural આજ્ઞઓ->આજ્ઞાઓ (Psalm 119:172) — Bible Pass-13 (lexical)

The raw token yk¿kyku omits the extra k that encodes the long-ā after જ્ઞ, so it
genuinely reads આજ્ઞઓ; the correctly-encoded yk¿kkyku already decodes to આજ્ઞાઓ.
The decoder is faithful to both and must not invent the missing byte, so this is
a WORD_FIXES lexical entry, not a converter change. Full rebuild delta = exactly
1 Bible verse (OT/46/119/172); songbooks byte-identical. Same-chapter 119:176 is
the internal control. See BIBLE_AUDIT_PASS13_RESOLUTION.md.

---

## Fix: source half-dha->half-gha કૃતધ્ન->કૃતઘ્ન — Bible Pass-14 (lexical)

Source wrote half-dha æ(e6, ધ્) where the ingratitude word family needs half-gha
Î(ce, ઘ્). Decoder is faithful to both glyphs, so remapping æ would corrupt real
ધ્ words -> lexical, not converter. Two WORD_FIXES entries: કૃતધ્નતા->કૃતઘ્નતા
(Wisdom 14:26), કૃતધ્ની->કૃતઘ્ની (2 Timothy 3:2). Same-edition control કૃતઘ્નીઓ
(Luke 6:35, source Î) decodes correctly, untouched. Full rebuild delta = exactly
2 Bible verses; songbooks byte-identical. See BIBLE_AUDIT_PASS14_RESOLUTION.md.

---

## Fix: person/place transposition 2 Timothy 4:20 — Bible Pass-15 (phrase)

Source put the two valid names in the wrong grammatical slots: object marker ને
on Miletus (a place), locative માં on Trophimus (a person). Decoder is faithful
to both; the fault is source wording, so a full-verse PHRASE_FIXES overlay swaps
them back (ત્રોફિમસને હું મિલેતસમાં). Same-edition controls: Acts 21:29 ત્રોફિમસને,
Acts 20:17 મિલેતસથી. Full rebuild delta = exactly 1 Bible verse (NT/16/4/20);
songbooks byte-identical. B (પરાકાષ્ટા) review-only; C (વિષ્ટા ×4) preserved as an
attested spelling. See BIBLE_AUDIT_PASS15_RESOLUTION.md.

---

## Fix: Luke 6:36 transposed source anchor (name="v63") — Bible Pass-16 (build)

The source anchor assets/1/3/6.html reads <a id="v36" name="v63">36</a>: the id
and visible numeral both say 36, only name has transposed digits. extract_verses
captures from name, so the verse landed under key 63. Fixed with a location-
scoped 'relabel' mode in 20_build_json.py _VERSE_RECOVERY keyed on ('1',3,6,'63')
-> 36, guarded against collision. One-key rename, zero text/count change. The
file is the only one in the corpus missing v36 while having v63. See
BIBLE_AUDIT_PASS16_RESOLUTION.md.

---

## Fix: Ephraim census ૪૫,૫૦૦->૪૦,૫૦૦ (Numbers 2:24) — Bible Pass-17 (lexical)

Source digit typo: raw '45,500' faithfully decodes to ૪૫,૫૦૦ but must be ૪૦,૫૦૦.
The value's own stated subtotal ૧,૦૮,૧૦૦ only reconciles with 40,500
(40500+32200+35400=108100; 45500 gives 113100); Numbers 1:33 also reads ૪૦,૫૦૦.
One full-value PHRASE_FIXES overlay; single code-point change (U+0AEB->U+0AE6).
Full rebuild delta = exactly 1 Bible verse (OT/4/2/24); protected ૪૫,૬૫૦ (Gad) and
26:18 ૪૦,૫૦૦ untouched; grouping intact; songbooks byte-identical. See
BIBLE_AUDIT_PASS17_RESOLUTION.md.
