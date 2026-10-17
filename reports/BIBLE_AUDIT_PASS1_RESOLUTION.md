# Resolution of Bible Spelling Audit — Pass 1

## 🔴 The big one: expanded 'òu' → જો ligature (742+ Bible occurrences)

Pass-1 (Kirtansagar) only handled `òu`+E/Þ/ô/W. The Bible revealed `òu` before
MANY more consonants is also જો. I enumerated EVERY `òu`+X across the corpus
(scripts/46_ou_enumerate.py) and classified by the following glyph:

- **JO-triggering next glyph** (word is clearly જો): E Þ ô W z í h f þ ¾ ø M x Ï
  ç ¤ ÷ R ý Ä  → structural map `òu[those]` → જો.
  Fixes: જોતાં, જોતો, જોકે, જોડ/જોડી, જોર/જોરથી, જોખમ, જોગવાઈ, જોશે/જોશો,
  કમજોર, સંજોગોમાં, …
- **JE-keeping next glyph** (genuine જે): <end>, L ð y { Ú + punctuation.
  PRESERVED: જે, બીજે, વંશજે, વંશજેને, **જેવું, જેવા, જેમ** (the critical
  guardrail — these must not become જો).

Result (Bible): જેતાં/જેકે/જેડ/જેખમ/જેશે families → 0; જોકે 123, જોખમ 50,
જોડ 147, જોતાં 87, જોર 114. જેમ(1202)/જેવા(600)/જેવું(207)/બીજે(337) intact.

Context-dependent `su`-ligature + `òu{`(મ) + `òur`(short-i) stragglers handled
as lexical: તેજોમય, જોરકડી/જોરોજ, જોડિયો/જોડિયાં, ઝંઝોડી.

## Source defects (lexical)
- **વહંચ- → વહેંચ-** (×155): source byte U(0x55)=anusvara in most words
  (નોંધ/પહોંચ), but the 'distribute' root needs ેં. Prefix-normalized (guarded).
- **વિચાયું → વિચાર્યું** (×40): source missing the reph ર (like સજ્યાં).

## Kept as-is (per audit — edition/house style)
કયું (×1183; edition-wide), પહાંચ-, Sanskritic/older forms (શાન્ત). Not modernized.

## Verification
- Regression: 76/76 (added જો-family + the જેવું/જેમ/જેવા guardrail cases).
- Anomaly scan unchanged (0 real-bug classes); leftover Latin 0.
- Kirtansagar unchanged (ખ્રિસ્ત 42, મૂર્તિ 20, જોજે 12 preserved — no regression).
- Audit example verses verified (Gen 18:2 જોતાં, Gen 20:12 જોકે, Gen 32:8
  વિચાર્યું/વહેંચી, Deut 5:25 જોખમ, Matt 17:5 તેજોમય).
