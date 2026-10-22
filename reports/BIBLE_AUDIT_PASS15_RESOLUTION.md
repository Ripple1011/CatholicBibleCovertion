# Resolution of Bible Spelling Audit — Pass 15

## Family A — person/place transposition in 2 Timothy 4:20 (FIXED, phrase-level)

One bounded **source-defect** correction — the first in this project that
restores MEANING rather than orthography. Both names are valid Gujarati and
decode correctly; the source sentence put them in the wrong grammatical slots.

    OLD (NT/16/4/20): ...અને મિલેતસને હું ત્રોફિમસમાં માંદો મૂકી આવ્યો હતો.
    NEW (NT/16/4/20): ...અને ત્રોફિમસને હું મિલેતસમાં માંદો મૂકી આવ્યો હતો.

Trophimus is the sick person left behind; Miletus is the place. The source
wrongly attached the object marker ને to Miletus and the locative માં to
Trophimus.

### Why this is a source defect, not a converter bug
The decoder is FAITHFUL to the source: r{÷uíkMkLku -> મિલેતસને and
ºkkurV{Mk{kt -> ત્રોફિમસમાં both decode exactly as the source bytes dictate.
Both names decode correctly everywhere else in the edition. The fault is the
source WORDING (which name is in which slot), so the fix is a full-verse
PHRASE_FIXES overlay — not a font remap, suffix rule, or name replacement.

### Same-edition controls (identities established from WITHIN this translation)
- Acts 20:4  — Trophimus listed among travelling companions (a person).
- Acts 21:29 — already uses the object form ત્રોફિમસને.
- Acts 20:15 — મિલેતસ as a destination.
- Acts 20:17 — મિલેતસથી ("from Miletus"), a place.
Independently corroborated by USCCB 2 Timothy 4:20 (roles only, not phrasing).

## Implementation
One exact full-verse entry added to PHRASE_FIXES in scripts/lexical_fixes.py.
Full verse so it cannot half-apply and no name/suffix is replaced globally. No
decoder/table/source change; no new WORD_FIXES; no raw/trace edit; no direct
JSON patch.

## Verification (full rebuild)
- Complete Bible vs post-Pass-14 baseline: **exactly 1 verse value changed**
  (NT/16/4/20), the full proposed verse; all other text/keys/metadata identical.
- Acts 20:4 / 20:15 / 20:17 / 21:29 controls unchanged.
- Regression **143/143** (positive full-verse + idempotence + NEGATIVE controls:
  the two names appearing separately, and the Acts control phrases, are NOT
  swapped — only the exact verse matches).
- Anomaly scan unchanged; 34891 verses; 236 placeholders; 46+27 canon.
- All three songbooks byte-identical; raw trace keeps source provenance.
- Pass 13 (આજ્ઞાઓ) and Pass 14 (કૃતઘ્ન-) corrections retained.

## NOT changed this pass (explicitly)
- **B — review-only:** Wisdom 14:27 પરાકાષ્ટા (candidate પરાકાષ્ઠા). Left
  unchanged; same-edition evidence is mixed (both spellings attested). Needs a
  native-reader/publisher decision. No entry added.
- **C — checked and preserved:** વિષ્ટા / વિષ્ટાની (4 occurrences). The spelling
  is an attested Gujarati dictionary headword (excrement/dung) matching the verse
  contexts; NOT an error. No ષ્ટ->ષ્ઠ rule; other ષ્ટ words (દુષ્ટ, ભ્રષ્ટાચાર,
  અનિષ્ટ...) likewise untouched.

## Carried forward (unchanged)
Global U mapping and પહાંચ-/સાંપ- decisions remain held. Review-only: Rev 1:9
સિંન્નધ્યમાં, જોનારો/જેનારો, ત્યાંને, પટી, અપ્યાં, nasal-t ખંચાવું, and now
Wisdom 14:27 પરાકાષ્ટા. Native-reader/publisher proofread and written publisher
permission remain the gates before shipping.
