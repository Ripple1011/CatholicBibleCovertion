# Resolution of Kirtansagar Spelling Audit — Pass 3

## 🔴 Major converter bug: short-i before C+્ર (ખ્રિસ્ત = "Christ")

Output had `ખિ્રસ્ત`, `પિ્રય` — the pre-base short-i `િ` was placed BEFORE the
`્ર` conjunct instead of after the full consonant cluster. Root cause: the
cluster the short-i hops did NOT include the post-base ra `ú`(0xfa)=્ર (nor the
INH half-form sentinel that sits before it). Fix: extend CLUSTER with an
optional `[INH/AA sentinel]?[post-base ra ú/Ù]?` tail, so a pre-base matra hops
C(+्र) as one unit.

Impact (Bible + songbooks): **િ્ર malformed clusters 678 → 0**; ખ્રિસ્ત now
602, પ્રિય 60. Also fixes biblical names: ગાબ્રિયેલ (Gabriel), અગ્રિપ્પા
(Agrippa), ખાબ્રિસ. This affected the Bible heavily (the name "Christ").

## Source defects / normalization (lexical_fixes.py, verified)

Prefix normalization (guarded word-initial):
- `અરપ- → અર્પ-` (offer root; book uses અર્પ- ×40+; same class as સરજ-)

Whole-word source defects:
- શ્રધ્ધા→શ્રદ્ધા, આતમા→આત્મા, તારૂં→તારું, મારૂં→મારું, કરૂણા→કરુણા (long ૂ→short ુ),
  હૈયુ→હૈયું, જયારે→જ્યારે, ત્યા→ત્યાં, પરણામ→પ્રણામ, મત્યુને→મૃત્યુને,
  ઠયાં→થયાં, યિજ્ઞક→યજ્ઞક.

## Left as REVIEW (per audit's own caution — need source/native reader)
- Ordinals in Songs 283/284 (`ર જું`, `પ મું`, `૧ર` …): a separate
  number/ordinal formatting family; not generic word replacement.
- મશાંતિ, સંથે, ચકરઈ, આર્જતના, મહાત, મિરિયમ(vs મરિયમ): wrong-confidence high but
  replacement-confidence low; need source/native confirmation.
- Pass-1 queue still open: જેજે, જેજન, તાજપ.
- Kept unchanged (poetic/archaic): નવ, નાહીં, પરથમ, પુત્તર, ર્હે*, કરજા, etc.

## Verification
- Regression: 67/67 (added ખ્રિસ્ત/પ્રિય/ગાબ્રિયેલ/અગ્રિપ્પા).
- Anomaly scan unchanged (0 real-bug classes); leftover Latin 0.
- All JSON regenerated; the ખ્રિસ્ત fix corrected the Bible too (602 occurrences).
