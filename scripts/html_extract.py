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
    return out
