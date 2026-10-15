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
# EXTRA (defined below) also holds single-byte glyphs that decode to consonant
# clusters (º=ત્ર્, û=ક્ષ્, ¥=ત્ત્, Ì=હ્ય, Ù=્ર, †=સ્ત્ર). These are cluster
# cores too and must be hoppable by a pre-base matra (fixes રાત્રિ). We add them
# to the base set after EXTRA is defined (see _finalize_cluster below).
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
    # reph 'o' after cons(+matras) -> before. The consonant may be a half-form
    # (e.g. 'í'=ત્) and the matra run may include the INH/AA half-form sentinels
    # (\x1d/\x1e) — include both so reph on a half-form still reorders
    # (ðíkuo = વ ત્ INH ે reph -> વર્તે, not વતેર્).
    s = re.sub(r'([' + CONS_CLASS + _HALF + r'])([ktuwqe\x1d\x1e]*)o', r'o\1\2', s)
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

# EXTRA glyphs that are consonant-cluster CORES (their Unicode contains a
# consonant) must be hoppable by a pre-base matra. Add them to the cluster
# character classes and rebuild CLUSTER / CONS_CLASS. (Pure matra/anusvara
# EXTRA entries like r,o,O,U,®,Š,Â are NOT cores.)
_NOT_CORES = set('roŠ®ÂOU')  # pure matra / reph / short-i markers, never cluster cores
_EXTRA_CORES = ''.join(
    g for g, u in EXTRA.items()
    if g not in _NOT_CORES and any('ક' <= ch <= 'હ' for ch in u)
)  # -> g(ખ્ત), â(્ય), û(ક્ષ્), ¥(ત્ત્), º(ત્ર્), Ì(હ્ય), Ù(્ર), †(સ્ત્ર), &(શ્)
_BASE = _BASE + ''.join(re.escape(c) for c in _EXTRA_CORES)
CONS_CLASS = CONS_CLASS + ''.join(re.escape(c) for c in _EXTRA_CORES)
CLUSTER = r'(?:[' + _HALF + r']+[' + _BASE + r']?|[' + _BASE + r'])'


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


# Sentinels used by convert() to carry raw-stream decisions through the decode:
INH = '\x1d'   # inherent-vowel completion of a half-form (-> bare consonant, no matra)
AA = '\x1e'    # genuine aa-matra that a half-form explicitly took (-> ા)
CONS_RANGE = r'ક-હ'


def fix_unicode(u):
    # 1) Resolve the inherent-completion sentinel INH that follows a decoded
    #    half-form (consonant + virama). 'C ્ INH' means the half-form was
    #    completed to a FULL consonant carrying the inherent 'a' (implicit in
    #    Unicode): drop the virama, emit no matra.
    u = re.sub(r'([' + CONS_RANGE + r'])' + VIRAMA + INH, r'\1', u)
    # 2) Resolve the explicit aa sentinel AA the same way but WITH an aa-matra:
    #    'C ્ AA' (half-form + genuine aa) -> C + ા.
    u = re.sub(r'([' + CONS_RANGE + r'])' + VIRAMA + AA, r'\1ા', u)
    # any stray sentinels (defensive): INH -> nothing, AA -> aa
    u = u.replace(INH, '').replace(AA, 'ા')

    # existing cleanups
    u = re.sub(VIRAMA + r'([' + MATRAS + r'])', r'\1', u)
    # spurious aa before another vowel sign: ાX -> X  (X = non-aa matra)
    u = re.sub(r'ા([' + OTHER_MATRAS + r'])', r'\1', u)
    u = re.sub(r'([' + OTHER_MATRAS + r'])ા', r'\1', u)
    # collapse an impossible duplicate virama (e.g. ક્્ય -> ક્ય); never touch a
    # single valid virama.
    u = re.sub(VIRAMA + VIRAMA + r'+', VIRAMA, u)

    # Visarga vs punctuation colon. The table maps ':' <-> ઃ, so every ASCII
    # colon became ઃ. A GENUINE visarga attaches to a letter on both sides
    # (દુઃખ). A PUNCTUATION colon has a space before/after or a digit neighbour
    # (list intros 'કરી : અનાજ', references '1:12'): restore those to ':'.
    VIS = 'ઃ'
    u = re.sub(r'(?<=\s)' + VIS, ':', u)          # space before  ->  :
    u = re.sub(VIS + r'(?=\s)', ':', u)           # space after   ->  :
    u = re.sub(VIS + r'(?=$)', ':', u)            # end of string ->  :
    u = re.sub(r'(?<=\d)' + VIS, ':', u)          # digit before  ->  :
    u = re.sub(VIS + r'(?=\d)', ':', u)           # digit after   ->  :
    return u


# Raw gopika matra bytes (dependent vowel signs other than the inherent marker).
# Used to detect a spurious inherent 'k'(0x6b) sitting between a consonant and a
# real matra (e.g. 'yLku' = અ ન [k=spurious] ે -> અને, not અનો).
RAW_MATRA = re.escape('uewq]i')   # ે ી ુ ૂ ૃ ૈ ; escape so ']' is literal


def convert(gopika_text):
    """
    Raw-stream interpretation of the Arpita 'k'(0x6b) inherent-vowel marker.

    The 'k' byte is NOT a literal 'ા'. After a HALF-FORM glyph (e.g. 'L'=ન્):
        HALF + k        -> full consonant with inherent 'a'   (ન)       [INH]
        HALF + kk       -> full consonant + aa                (ના)      [AA]
        HALF + k + V    -> full consonant + that vowel matra  (ને)
        HALF + kku/kki  -> full consonant + ો / ૌ
    After a FULL consonant glyph the 'k' is a genuine aa-matra and is left to
    decode as 'ા' via the table (so મારા/રાજા are preserved).

    We tag the half-form decisions with sentinels INH / AA on the RAW stream so
    they survive unswap + reorder + table decode, then fix_unicode() resolves
    them structurally (drop the half-form virama; add 'ા' only for AA).
    """
    s = gopika_text
    H = '[' + HALF_CONS_CLASS + ']'

    # Order matters: longest 'k' runs / matra combos first.
    # HALF + kku / kki  -> half-form keeps virama, real o/au matra follows.
    #   (handled naturally: leave 'kku'/'kki' intact; the single leading k is the
    #    half-form's completion -> turn into INH so virama drops, then 'ku'/'ki'
    #    decodes to the o/au matra.)
    s = re.sub(r'(' + H + r')kku', r'\1' + INH + 'ku', s)
    s = re.sub(r'(' + H + r')kki', r'\1' + INH + 'ki', s)
    # HALF + kk -> genuine aa
    s = re.sub(r'(' + H + r')kk', r'\1' + AA, s)
    # HALF + k + (real matra byte) -> keep the matra, k is inherent completion
    s = re.sub(r'(' + H + r')k([' + RAW_MATRA + r'])', r'\1' + INH + r'\2', s)
    # HALF + k (nothing matra-ish after) -> inherent 'a' completion
    s = re.sub(r'(' + H + r')k', r'\1' + INH, s)

    # FULL-consonant o/au matras: protect 'kku'/'kki' from the collapse below.
    # Use \x1f temps (distinct from INH \x1d / AA \x1e to avoid any collision).
    s = s.replace('kku', '\x1fo').replace('kki', '\x1fa')
    # collapse any remaining spurious doubled inherent markers after full cons
    # (પાાણી -> પાણી). Single k after a full consonant stays = genuine aa.
    s = re.sub(r'k{2,}', 'k', s)
    s = s.replace('\x1fo', 'ku').replace('\x1fa', 'ki')

    # Collapse a run of the SAME repeated dependent-vowel matra byte, a font
    # artifact (ખેેેડ = ¾uuu -> ખેડ, ભેેટો = ¼uu -> ભેટો). Each vowel sign may
    # legitimately appear at most once per consonant.
    s = re.sub(r'([uewqi])\1+', r'\1', s)

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
