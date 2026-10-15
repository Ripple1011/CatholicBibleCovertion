# -*- coding: utf-8 -*-
"""
Gopika Two (Arpita variant) -> Unicode Gujarati decoder  [v3 - stable]

Source HTML is UTF-8; decoding it recovers the true Gopika latin-1 chars.

Proven rules (verified against this app's corpus):
  * Arpita variant: swap k<->t and the Œ/Ë/‚ cycle to reach the base table.
  * base short-i matra = 'r' (0x72), stored BEFORE its consonant -> move AFTER.
  * reph = 'o' (0x6f), trailing marker AFTER a consonant cluster -> leading ર્.
  * 'O' (0x4f), 'U' (0x55) = anusvara ં appearing after a matra / word-final.
  * half-form (C+virama) directly before a vowel matra -> drop the virama.

This reaches ~99.997% Latin-free. Remaining residue (~180 chars across the
whole corpus, plus some spurious aa-matra clusters) is reported by the
companion script 13_residue_report.py with full verse context for manual fix.
"""
import re
from gopika_table import load_pairs

PAIRS = load_pairs()
G2U = {}
for uni, gop in PAIRS:
    if gop not in G2U:
        G2U[gop] = uni
GOP_KEYS = sorted([k for k in G2U if k], key=len, reverse=True)

CONS_UNI = set(chr(c) for c in range(0x0A95, 0x0ABA))
GOP_CONS = set()
for uni, gop in PAIRS:
    if len(gop) == 1 and len(uni) == 1 and uni in CONS_UNI:
        GOP_CONS.add(gop)
GOP_CONS |= set('ÃLM™')
CONS_CLASS = ''.join(re.escape(c) for c in GOP_CONS)


def unswap_arpita(s):
    s = s.replace('k', '\x00').replace('t', 'k').replace('\x00', 't')
    s = s.replace('Œ', '\x01').replace('Ë', 'Œ').replace('\x01', '‚')
    return s


# Half-form gopika glyphs (their Unicode value ends in virama, i.e. C + ્).
HALF_CONS = set()
for uni, gop in PAIRS:
    if len(gop) == 1 and uni.endswith('્'):
        HALF_CONS.add(gop)

# Full-conjunct gopika glyphs: a single gopika char mapping to a multi-consonant
# cluster that does NOT end in a bare virama (e.g. 'Ø'=દ્ધ, 'ù'=શ્ચ). These are
# complete syllable cores and must count as one cluster for pre-base reordering.
CONJ_CONS = set()
_CONS_CHARS = set(chr(c) for c in range(0x0A95, 0x0ABA))
for uni, gop in PAIRS:
    if len(gop) == 1 and not uni.endswith('્') and any(ch in _CONS_CHARS for ch in uni) \
            and gop not in GOP_CONS and len(uni) > 1:
        CONJ_CONS.add(gop)
GOP_CONS |= CONJ_CONS  # treat full conjuncts as base-consonant-equivalent cores
CONS_CLASS = ''.join(re.escape(c) for c in GOP_CONS)  # rebuild to include conjuncts
# A consonant cluster in the gopika stream = zero or more half-forms followed by
# exactly ONE base consonant (e.g. 'õí' = ક્+ત). A pre-base matra belongs to the
# single orthographic syllable, so it must hop exactly one cluster — NOT a greedy
# run of separate full consonants (that bug turned દિવસ into દવસિ).
_HALF = ''.join(re.escape(c) for c in HALF_CONS)
_BASE = ''.join(re.escape(c) for c in GOP_CONS)
HALF_CONS_CLASS = _HALF  # for use in character classes elsewhere
# One orthographic cluster = either a conjunct (one or more half-forms, then an
# optional base consonant, e.g. 'õí'=ક્ત or 'õf'=ક્ક) OR a single base consonant.
# A pre-base matra hops exactly one such cluster — so a run of SEPARATE full
# consonants (દવસ) is three clusters and the matra stays on the first.
CLUSTER = r'(?:[' + _HALF + r']+[' + _BASE + r']?|[' + _BASE + r'])'


def reorder_gopika(s):
    # '®' = short-i + anusvara (િં) stored before consonant (JS: િં -> ®).
    s = re.sub(r'®(' + CLUSTER + r')', r'\1®', s)
    # 'Š' = reph + short-i ( ર્િ ) stored before consonant (JS: ર્િ -> Š).
    s = re.sub(r'Š(' + CLUSTER + r')', r'\1Š', s)
    # 'Â' (0xc2) = short-i િ in a CONJUNCT context, pre-base -> move past cluster.
    s = re.sub(r'Â(' + CLUSTER + r')', r'\1Â', s)
    # short-i 'r' before consonant cluster -> after
    s = re.sub(r'r(' + CLUSTER + r')', r'\1r', s)
    # reph 'o' after cons(+matras) -> before
    s = re.sub(r'([' + CONS_CLASS + r'])([ktuwqe]*)o', r'o\1\2', s)
    return s


EXTRA = {
    'r': 'િ', 'o': 'ર્', 'O': 'ં', 'U': 'ં',
    'I': 'ૌં',   # MkkIËÞo = સૌંદર્ય (au-matra + anusvara); verified 127x
    'g': 'ખ્ત',  # Ãkwg = પુખ્ત (adult); verified
    'â': '્ય',   # post-base ya: upstream rule [કછટઢફ]્ય -> $1â ; invert
    '®': 'િં',   # short-i + anusvara (JS: િં -> ®), reordered after consonant
    'Š': 'ર્િ',  # reph + short-i (JS: ર્િ -> Š), reordered after consonant
    'Â': 'િ',    # short-i in conjunct context (reordered after cluster)
    # standalone conjunct glyphs (appear when their trailing 't' = aa was absent):
    'û': 'ક્ષ્',  # લûમી = લક્ષ્મી  (ût=ક્ષ ; standalone before consonant = ક્ષ્)
    '¥': 'ત્ત્',  # મહ¥વ = મહત્ત્વ  (¥t=ત્ત)
    'º': 'ત્ર્',  # આમંºયા = આમંત્ર્યા  (ºt=ત્ર)
    'Ì': 'હ્ય',   # dominant: Ìk(5753x)=હ્ય ; rare ÌË=હૃ left as-is
    'Ù': '્ર',    # post-base ra in ટ્ર/ડ્ર split cases (હ્રાસ, ...)
    '†': 'સ્ત્ર',  # વસ્ત્ર, શાસ્ત્ર, સ્ત્રી — verified across all contexts
    '&': 'શ્',    # પ્રશ્ન, અશ્લીલ, આશ્લેષ, પુણ્યશ્લોક — verified across contexts
}


def decode_table(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        hit = None
        for k in GOP_KEYS:
            if s.startswith(k, i):
                hit = k
                break
        if hit:
            out.append(G2U[hit])
            i += len(hit)
        elif s[i] in EXTRA:
            out.append(EXTRA[s[i]])
            i += 1
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


VIRAMA = '્'
MATRAS = 'ાિીુૂૃૄેૈોૌંઁ'


OTHER_MATRAS = 'િીુૂૃૄેૈોૌ'  # vowel signs other than aa; two vowel signs on one
                              # consonant is invalid in Gujarati, so a 'ા' directly
                              # before another vowel sign is the spurious inherent
                              # marker and is dropped.


def fix_unicode(u):
    u = re.sub(VIRAMA + r'([' + MATRAS + r'])', r'\1', u)
    # spurious aa before another vowel sign: ાX -> X  (X = non-aa matra)
    u = re.sub(r'ા([' + OTHER_MATRAS + r'])', r'\1', u)
    # spurious aa after a vowel sign then another: Xા? handled above; also
    # drop a aa that precedes a short-i that got reordered: િ cases
    u = re.sub(r'([' + OTHER_MATRAS + r'])ા', r'\1', u)
    return u


# Raw gopika matra bytes (dependent vowel signs other than the inherent marker).
# Used to detect a spurious inherent 'k'(0x6b) sitting between a consonant and a
# real matra (e.g. 'yLku' = અ ન [k=spurious] ે -> અને, not અનો).
RAW_MATRA = re.escape('uewq]i')   # ે ી ુ ૂ ૃ ૈ ; escape so ']' is literal


def convert(gopika_text):
    s = gopika_text
    # 1) Protect the o/au matras BEFORE any 'k' collapsing. In this app a full
    #    consonant's o-matra is 'kku' (ત+ો = íkku) and au is 'kki'; the first k
    #    is the consonant's inherent slot, 'ku'/'ki' the matra. Replace with
    #    sentinels so the kk-collapse below doesn't destroy them.
    s = s.replace('kku', '\x1Eo').replace('kki', '\x1Ea')  # \x1E = kept consonant slot
    # 2) Collapse remaining runs of the inherent marker 'k': doubled 'kk' makes a
    #    spurious extra aa (પાાણી -> પાણી). Single k is genuine aa and untouched.
    s = re.sub(r'k{2,}', 'k', s)
    # 3) Drop the inherent 'k' between a HALF-FORM consonant and a real matra:
    #    fixes અનો->અને ('L'=ન્ half + k + u). Full consonants keep their 'ku'.
    s = re.sub(r'([' + HALF_CONS_CLASS + r'])k([' + RAW_MATRA + r'])', r'\1\2', s)
    # restore sentinels to the RAW o/au matra form 'ku'/'ki' (unswap turns the
    # k into base 't', yielding table 'tu'=ો / 'ti'=ૌ).
    s = s.replace('\x1Eo', 'ku').replace('\x1Ea', 'ki')
    base = unswap_arpita(s)
    base = reorder_gopika(base)
    u = decode_table(base)
    u = fix_unicode(u)
    return u


if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    v1 = '«kht¼{kt Eïhu ykfkþ yLku Ãk]Úðe MkßÞkO.'
    print("Genesis 1:1 ->", convert(v1))
