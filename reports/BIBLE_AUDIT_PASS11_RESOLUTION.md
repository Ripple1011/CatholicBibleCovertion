# Resolution of Bible Spelling Audit — Pass 11

## Family A — half-form completion consumed the candra-o carrier (FIXED)

The agent's diagnosis was exact. After a half-form consonant, `convert()`
protects `kku`/`kki` (o/au) but then collapses any remaining `kk` to genuine aa.
There was no branch for `kkì`, so the generic `kk`→aa consumed the first two k's
and stranded `ì` as a bare candra-e:

    M k kì L k u   (raw)
    સ્ + [first k = half-form completion] + candra-o(kì) + ન્ + completion + e
    = સૉને
but the old path produced  સ્ + AA(ાૅ... split) = સાૅને  (two dependent vowels
ા + ૅ after સ, which is not a valid encoding of the intended candra-o ૉ).

Table proof (source_assets/myExpr.js): `ì`→ૅ (candra-e), longest key `tì`→ૉ
(candra-o), `t`→ા. Arpita unswap maps raw k→t, so the completing+carrier pair
`kkì` must stay together to form unswap `tì` = the ૉ table key.

### Fix (the agent's candidate, verified)
Insert ONE branch between the half-form `kki` branch and the generic `kk`:

    s = re.sub(r'(' + H + r')kkì', r'\1' + INH + 'kì', s)

The first k becomes INH (half-form completion, virama drops); the remaining
`kì` unswaps to `tì` and decodes via the existing longest-key lookup to ૉ. No
Unicode-stage substitution, no lexical entry, no change to o/au/aa logic or the
Š/reph rules. Single-k candra-e (`Mkì`→સૅ) is untouched because it has no leading
completing k.

## Trace-wide impact check (as required)
OLD vs NEW decoder over EVERY raw token in the whole corpus (Bible + all
songbooks). Delta = EXACTLY 1 record, Bible only:
- `સાૅને -> સૉને`   2 Kings 17:4  (OT/12/17/4)  raw `MkkìLku`

Live Bible diff = exactly one token in one verse value. Songbooks byte-identical.

## Independent corroboration
The anomaly scanner's "two matras in a row" count dropped 1 -> 0 with this fix:
that lone flag WAS this `ાૅ` double-dependent-vowel defect. The structural repair
is confirmed by an orthogonal check, not just the targeted fixture.

## Name is source-faithful
`ૉ` (candra-o) is the single sign the source table encodes (`tì`). The consonant
સ and suffix ને are unchanged; the verse meaning, punctuation, and trailing
heading are all unchanged. This chooses no new name and modernizes nothing. The
strings differ at code-point level under NFC/NFD/NFKC/NFKD, so a generic
normalization call would NOT have fixed it.

## Controls / preservation verified
- 11/11 handoff fixtures pass, incl. corpus controls `સ્ટૉઈક` (Acts 17:18) and
  `મૉર` (Job 15:33, Song 7:14) — full-consonant+kì, unchanged — and the candra
  contrasts સૅ/સો/સૌ/સા/સે/સ/ને/ટૉ.
- B1 (Rev 1:9 સિંન્નધ્યમાં) UNCHANGED, review-only. Valid સાંનિધ્યમાં preserved.
- All prior fixes and approved names preserved (…સાર્દિસ, ઈર્મિયા, પોર્કિયુસ…);
  જે/જો, _JO_NEXT, house/poetic forms untouched.

## Verification summary
- Regression 107/107 (added A1 + candra-e + 2 full-cons controls).
- Trace-wide decoder delta = exactly 1 raw record.
- Live Bible diff = exactly 1 token in 1 verse (OT/12/17/4).
- Anomaly scan: two-matras-in-a-row 1->0; all else unchanged.
- Verses 34891; 236 placeholders; 46+27 canon; songbooks unchanged.

## Carried forward
B1 (Rev 1:9), જેનારો, ત્યાંને, પટી, અપ્યાં remain review-only. Native-reader /
publisher proofread and written publisher permission remain the gates before
shipping.
