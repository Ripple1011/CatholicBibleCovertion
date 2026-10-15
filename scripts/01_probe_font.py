"""
Diagnostic: inspect the Gopika Two font cmap and glyph names.

Legacy Gujarati fonts like Gopika Two are ASCII/Latin-1 "glyph substitution"
fonts: a Latin codepoint (e.g. 'E', 'k', '«') is mapped to a Gujarati glyph.
The glyph NAMES in the TTF often reveal the intended Unicode character, which
lets us build a byte -> Unicode mapping instead of guessing visually.

This script just prints the mapping so we can build the real converter.
"""
import sys
from fontTools.ttLib import TTFont

FONT = r"D:\My_Projects\ChurchConnect\BhajanSangrah\Docs\Gurjarvani_Data\source_assets\assets\GopikaTWO_N.TTF"


def main(path):
    font = TTFont(path)
    print("== Font tables ==", font.keys())
    cmap = font.getBestCmap()
    print(f"cmap entries: {len(cmap)}")
    # Map codepoint -> glyph name
    rows = []
    for cp, gname in sorted(cmap.items()):
        ch = chr(cp)
        printable = ch if ch.isprintable() and cp >= 0x20 else f"\\x{cp:02x}"
        rows.append((cp, printable, gname))
    for cp, printable, gname in rows:
        print(f"U+{cp:04X}  {printable!r:8}  glyph={gname}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else FONT)
