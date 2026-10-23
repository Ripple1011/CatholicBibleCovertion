# Resolution of Bible Spelling Audit — Pass 20 (REVIEW-ONLY, no change)

## Disposition: source-evidence gap CLOSED; held as REVIEW by maintainer decision

The agent flagged a quantity inconsistency in the monthly grain-offering of
Numbers 28:12–13 (ram portion છ/6 and lamb portion ચાર/4, vs the expected 4/2),
but could not retrieve occurrence-level source evidence, so it held the family as
REVIEW and asked for inspection of `assets/0/4/28.html`.

This resolution CLOSED that source-evidence gap via direct APK inspection. The
finding is a **confirmed source-defect** (the printed edition is internally
inconsistent; the decoder is faithful). However, the maintainer **deliberately
kept it REVIEW and made NO output change**, because — unlike prior source-defect
fixes — the source text here is complete and well-formed, so correcting it would
override the printed Bible on the basis of cross-referencing. That is a
publisher / native-reader editorial decision, not an automated repair.

## Source evidence (what the agent lacked)
APK asset `assets/0/4/28.html`
(sha256 83a3a3d4e6fdc4aca2ee897576be43c43418b1647f283e97c04449732e44cc4f):

    28:12 ram clause raw:  ...{kuxk ½uxk ËeX íku÷u {kuÞu÷ku A þuh ÷kux   -> A  = છ  (6)
    28:13 lamb clause raw: ...LkkLkk ½uxk {kxu íku÷u {kuÞu÷ku [kh þuh ÷kux -> [kh = ચાર (4)
    control 28:20 ram:     ...{kuxk ½uxk ËeX ... [kh þuh ÷kux            -> [kh = ચાર (4)
    control 28:29 lamb:    ...LkkLkk ½uxk ËeX çkþuh ...                   -> çkþuh = બશેર (2)

Decoding confirmed: A->છ, [kh->ચાર, çkþuh->બશેર (matches the agent's trace record
for ચાર, raw `[kh`, hex 5b 6b 68). So the SOURCE itself carries the inconsistent
quantities; the decoder and extractor are faithful. Classification: **source-
defect (editorial), NOT a converter/extraction bug.**

## Why held rather than fixed
| Prior source-defect | Nature | Basis for auto-fix |
|---|---|---|
| Pass 17 census 45,500->40,500 | number wrong | the verse's OWN arithmetic (113100 != stated 108100) |
| Pass 19 oath ક->કે | mechanically incomplete word | lone raw byte, no matra |
| **Pass 20 Numbers 28:12–13** | **complete, well-formed text** | **only cross-reference disagreement — NOT self-evident** |

Correcting 28:12–13 would override what the printed edition states. The evidence
(3 same-chapter parallels 28:20–21/28:28–29 + USCCB 2/10 & 1/10 ephah) is strong,
but the call belongs to the publisher / a native reader. It may be a genuine
erratum in the printed edition worth reporting back to the publisher.

## Action taken
- NO change to output/bible.json, decoder, lexical layer, scripts, or trace.
- Recorded as item #9 in reports/REVIEW_QUEUE.md with full source evidence, the
  comparison table, and the exact minimal correction IF a reviewer approves it
  (28:12 ram છ શેર->ચાર શેર; 28:13 lamb ચાર શેર->બશેર; calf છ શેર untouched).

## Verification
- output/bible.json unchanged from post-Pass-19 (9fdd73e). Songbooks unchanged.
- All prior corrections (Pass 13–19) retained; regression still 150/150.

## Carried forward
Hebrews 11:23 ડયાં and all other review-queue items unchanged. Global-U / aa+U
held. Native-reader/publisher proofread and written publisher permission remain
the gates before shipping.
