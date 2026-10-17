# -*- coding: utf-8 -*-
"""
Shared HTML -> (verse_label, raw_gopika_text) extraction for Gurjarvani assets.

Design principle: be CONSERVATIVE. Never run broad regexes that could eat real
Gujarati content. We only:
  * UTF-8 decode (recovers true Gopika latin-1 chars).
  * Scope to <gujFont> blocks (that is where the Gujarati lives; keeps English
    titles / CSS href / file paths out without guessing).
  * Decode HTML entities.
  * Split verses on <a ... name="vN" ...>N</a> anchors (id may precede name).

Any residual markup leak is left intact and reported, rather than risk
corrupting scripture with aggressive stripping.
"""
import re
import html as _html

TAG = re.compile(r'<[^>]+>')
# anchor: match the <a ...> ... </a> where attributes contain name="vN"
ANCHOR = re.compile(r'<a\b[^>]*\bname="v(\d+)"[^>]*>\s*\d+\s*</a>', re.I)
GUJFONT = re.compile(r'<gujFont>(.*?)</gujFont>', re.S | re.I)

# Specific, anchored markup-leak patterns to cut (cannot match Gujarati text).
# 1. a broken/leaked anchor remnant: id="vN"> or name="vN"> possibly preceded
#    by a stray quote/digit (seen at a few verse boundaries).
LEAK_ANCHOR = re.compile(r'\d*"?\s*(?:id|name)="v\d+"\s*>\s*\d*', re.I)
# 2. an English chapter-title comment + any following CSS/href/file markup that
#    leaked inside a gujFont block (e.g. Ecclesiastes 11:9). Cut from the English
#    title onward — real Gujarati verses never contain an ASCII book title.
LEAK_TAIL = re.compile(r'[A-Za-z][A-Za-z ]{2,}-\s*Chapter.*$', re.S)
LEAK_HREF = re.compile(r'href="[^"]*".*$', re.S | re.I)
LEAK_FILE = re.compile(r'file:///\S*', re.I)


def _clean(fragment):
    # A leading stray 'v' (0x76) right after a verse anchor is a known source
    # typo ('...>40</a>v<gopika>'). Strip a single leading 'v' before the tag
    # strip, while still in raw-gopika form. Anchored + specific -> safe.
    fragment = re.sub(r'^\s*v(?=[A-Za-z -ɏ])', '', fragment)
    # cut anchored markup leaks BEFORE tag-strip (they live in/near attributes)
    fragment = LEAK_ANCHOR.sub('', fragment)
    fragment = LEAK_TAIL.sub('', fragment)
    fragment = LEAK_HREF.sub('', fragment)
    fragment = LEAK_FILE.sub('', fragment)
    t = TAG.sub('', fragment)
    t = _html.unescape(t)
    t = t.replace('\\', ' ')          # stray backslashes from markup
    t = re.sub(r'[ \t\r\n]+', ' ', t).strip()
    # a single stray ASCII letter immediately before Gujarati at the very start
    # is an anchor-remnant typo in the source (e.g. '...>40</a>v' -> leading 'v').
    t = re.sub(r'^[A-Za-z](?=[઀-૿])', '', t)
    return t


def extract_verses(raw_bytes):
    """raw_bytes: file bytes. Returns list of (label, gopika_text)."""
    raw = raw_bytes.decode('utf-8', 'replace')
    m = re.search(r'<body[^>]*>(.*)</body>', raw, re.S | re.I)
    body = m.group(1) if m else raw

    # Scope to gujFont blocks when present (keeps English/CSS out safely).
    guj_blocks = GUJFONT.findall(body)
    scope = '\n'.join(guj_blocks) if guj_blocks else body

    anchors = list(ANCHOR.finditer(scope))
    out = []
    if not anchors:
        txt = _clean(scope)
        if txt:
            out.append(('(whole)', txt))
        return out
    for i, a in enumerate(anchors):
        vnum = a.group(1)
        start = a.end()
        end = anchors[i + 1].start() if i + 1 < len(anchors) else len(scope)
        txt = _clean(scope[start:end])
        if txt:
            out.append((f"v{vnum}", txt))
    return _split_inline_verse_numbers(out)


# ASCII or Gujarati digits that may appear INLINE as a verse marker inside a
# verse body when the source omitted the <a name> anchor (e.g. 1 Chr 27:4,24).
_DIG = '0-9૦-૯'
_ASCII2GUJ = {ord(c): d for c, d in zip('0123456789', '૦૧૨૩૪૫૬૭૮૯')}


def _to_int(numstr):
    try:
        return int(numstr.translate({ord('૦'): '0', ord('૧'): '1', ord('૨'): '2',
                                     ord('૩'): '3', ord('૪'): '4', ord('૫'): '5',
                                     ord('૬'): '6', ord('૭'): '7', ord('૮'): '8',
                                     ord('૯'): '9'}))
    except ValueError:
        return None


def _split_inline_verse_numbers(verses):
    """Recover verses whose anchor was missing in the source: if a verse body
    contains an inline numeral equal to the NEXT sequential verse number,
    immediately followed by a Gujarati letter, split it into a new verse. Only
    splits on the exact next-expected number to stay safe (never touches a
    numeral that is real data like '24 હજાર')."""
    out = []
    i = 0
    while i < len(verses):
        label, text = verses[i]
        cur = _to_int(label[1:]) if label.startswith('v') else None
        # the next anchored verse number (to know where to stop looking)
        nxt_anchor = None
        if i + 1 < len(verses) and verses[i + 1][0].startswith('v'):
            nxt_anchor = _to_int(verses[i + 1][0][1:])
        if cur is not None:
            expect = cur + 1
            # look for inline 'expect' (ascii or gujarati) + Gujarati letter, but
            # only split while the inline number stays below the next anchor.
            parts = [(label, text)]
            while expect != nxt_anchor:
                g = ''.join('૦૧૨૩૪૫૬૭૮૯'[int(d)] for d in str(expect))
                # The text here is still RAW GOPIKA (latin-range glyph bytes), so
                # the inline number is followed by a Gopika consonant byte, not a
                # Gujarati letter. Require: the numeral is preceded by space/punct,
                # and immediately followed by a NON-space, NON-digit glyph (the
                # start of the next verse's first word). Only the exact next
                # expected number is matched, so real numerals like '24 હજાર'
                # (followed by a space) never match.
                pat = re.compile(r'(?:^|(?<=[\s.,;:?!”’]))(' + re.escape(g) + r'|'
                                 + re.escape(str(expect)) + r')(?=[^\s0-9૦-૯])')
                lastlabel, lasttext = parts[-1]
                m = pat.search(lasttext)
                if not m:
                    break
                head = lasttext[:m.start()].strip()
                tail = lasttext[m.end():].strip()
                parts[-1] = (lastlabel, head)
                parts.append((f"v{expect}", tail))
                expect += 1
            out.extend(p for p in parts if p[1])
        else:
            out.append((label, text))
        i += 1
    # Strip a verse's OWN numeral leaked at the very start of its text
    # (e.g. James 3:8 body 'v8' text begins '8પણ...'). Only strip if the leading
    # number equals the verse key.
    cleaned = []
    for label, text in out:
        key = _to_int(label[1:]) if label.startswith('v') else None
        if key is not None:
            g = ''.join('૦૧૨૩૪૫૬૭૮૯'[int(d)] for d in str(key))
            # strip the verse's own number leaked at the start, whether it is
            # directly glued to the next word ('8પણ') or followed by a space
            # ('13 પણ', a doubled anchor+inline number). Not followed by another
            # digit, so multi-digit data numbers aren't clipped.
            text = re.sub(r'^\s*(?:' + re.escape(g) + r'|' + re.escape(str(key))
                          + r')\s*(?=[^\s0-9૦-૯])', '', text).strip()
        cleaned.append((label, text))
    return cleaned
