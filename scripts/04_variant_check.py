# -*- coding: utf-8 -*-
"""
Decide which GopikaTwo variant Gurjarvani uses (Arpita vs Bhashabharti).

The upstream table (Bhashabharti) has:  aa-matra ા = 't'(0x74),  anusvara ં = 'k'(0x6b)
The Arpita swap (k<->t, plus Œ<->Ë<->‚) flips aa/anusvara byte assignment.

Our Genesis 1:1 ground truth:
  legacy «kht¼{kt  =  આરંભમાં
  -> 'k'(6b) sits where aa-matra ા OR anusvara ં goes.
Decompose: આ ર ં ભ મ ા ં
           yt h  k ¼ {  t k   (if Arpita: aa=k? anusvara=t?)
We test both hypotheses against the aligned string and report which fits.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

legacy = '«kht¼{kt'          # first word, Genesis 1:1
unicode_word = 'આરંભમાં'      # ground truth

print("legacy word :", legacy, '=>', ' '.join(f'{ord(c):02x}' for c in legacy))
print("unicode word:", unicode_word, '=>', ' '.join(f'U+{ord(c):04X} {c}' for c in unicode_word))
print()
# Unicode decomposition of આરંભમાં:
#  આ(0A86) ર(0AB0) ં(0A82) ભ(0AAD) મ(0AAE) ા(0ABE) ં(0A82)
# legacy bytes: « k h t ¼ { k t   -> ab 6b 68 74 bc 7b 6b 74
# Map by position (legacy is visual order; here they happen to align L->R):
pairs = [
    ('«=ab', 'પ્ર?? NO - this is આ start?'),
]
print("Byte-by-byte alignment attempt (legacy visual order):")
lb = list(legacy)
print("  «(ab) k(6b) h(68) t(74) ¼(bc) {(7b) k(6b) t(74)")
print("  Expected Unicode cluster: આ ર ં ભ મ ા ં")
print()
print("Upstream base table says: ા(aa)=t(74), ં(anusvara)=k(6b), આ=yt, ર=h(68), ભ=¼(bc), મ={(7b)")
print("So WITHOUT Arpita swap: k=anusvara(ં), t=aa-matra(ા)")
print("Our word ...{kt ends: મ(7b) k(6b) t(74) = મ + k + t")
print("  If k=ં and t=ા  -> મં ... but ground truth ends મ ા ં  = મ+ા+ં")
print("  So trailing should be મ ા(t) ં(k)  => bytes { t k, but corpus has { k t")
print()
print(">>> Corpus has {(મ) k t ; ground truth મ ા ં needs મ + aa + anusvara.")
print(">>> Therefore k=aa-matra(ા), t=anusvara(ં): THIS IS THE ARPITA VARIANT (k<->t swapped).")
