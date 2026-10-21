#!/usr/bin/env python3
"""Extract the glyph outlines the profile's SVG assets are drawn with.

GitHub serves SVGs as images, so they cannot load web fonts and fall back to
whatever the visitor's system has. The assets in assets/ therefore draw their
text as vector outlines. This script copies the needed outlines, advance widths
and pair kerning from three open-licensed type families into tools/glyphs.json,
so that tools/draw_assets.py can stay standard-library only.

Run it only when a new character or style is needed:

    pip install fonttools brotli
    python3 tools/extract_glyphs.py \
        --font display=Fraunces-500.woff --font display-italic=Fraunces-400-italic.woff \
        --font mono=JetBrainsMono-Regular.ttf --font mono-medium=JetBrainsMono-Medium.ttf \
        --font sans=Inter-Regular.otf --font sans-medium=Inter-Medium.otf

Sources (all SIL Open Font License 1.1):
  Fraunces        © 2020 The Fraunces Project Authors (npm @fontsource/fraunces)
  JetBrains Mono  © 2020 The JetBrains Mono Project Authors
  Inter           © 2016 The Inter Project Authors
The outlines are used to draw text in the profile's illustrations; see
tools/FONTS.md for the license notice.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parent / "glyphs.json"
CHARSET = "".join(chr(c) for c in range(32, 127)) + "·—–→’‘“”♯é×°…↗←↓↑§¶"


class CompactPathPen(BasePen):
    """SVG path data in font units, y pointing down, integer coordinates."""

    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.parts: list[str] = []

    @staticmethod
    def _pt(p):
        return f"{round(p[0])} {round(-p[1])}"

    def _moveTo(self, p):
        self.parts.append("M" + self._pt(p))

    def _lineTo(self, p):
        self.parts.append("L" + self._pt(p))

    def _qCurveToOne(self, p1, p2):
        self.parts.append("Q" + self._pt(p1) + " " + self._pt(p2))

    def _curveToOne(self, p1, p2, p3):
        self.parts.append("C" + self._pt(p1) + " " + self._pt(p2) + " " + self._pt(p3))

    def _closePath(self):
        self.parts.append("Z")

    def data(self) -> str:
        return "".join(self.parts)


def pair_kerning(font: TTFont, names: dict[str, str]) -> dict[str, int]:
    """Horizontal pair adjustments from the GPOS 'kern' feature, limited to CHARSET."""
    if "GPOS" not in font:
        return {}
    gpos = font["GPOS"].table
    if not gpos.FeatureList:
        return {}
    by_glyph = {g: c for c, g in names.items()}
    lookups = set()
    for record in gpos.FeatureList.FeatureRecord:
        if record.FeatureTag == "kern":
            lookups.update(record.Feature.LookupListIndex)
    kern: dict[str, int] = {}

    def add(left, right, value):
        if value and left in by_glyph and right in by_glyph:
            key = by_glyph[left] + by_glyph[right]
            kern.setdefault(key, value)

    for index in sorted(lookups):
        lookup = gpos.LookupList.Lookup[index]
        for sub in lookup.SubTable:
            if lookup.LookupType == 9:
                sub = sub.ExtSubTable
            if getattr(sub, "LookupType", 2) != 2 and lookup.LookupType not in (2, 9):
                continue
            if not hasattr(sub, "Format"):
                continue
            coverage = sub.Coverage.glyphs
            if sub.Format == 1:
                for left, pairset in zip(coverage, sub.PairSet):
                    for rec in pairset.PairValueRecord:
                        value = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                        add(left, rec.SecondGlyph, value)
            elif sub.Format == 2:
                class1 = sub.ClassDef1.classDefs
                class2 = sub.ClassDef2.classDefs
                seconds: dict[int, list[str]] = {}
                for glyph in by_glyph:
                    seconds.setdefault(class2.get(glyph, 0), []).append(glyph)
                for left in coverage:
                    if left not in by_glyph:
                        continue
                    row = sub.Class1Record[class1.get(left, 0)]
                    for c2, rec in enumerate(row.Class2Record):
                        value = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                        if value:
                            for right in seconds.get(c2, []):
                                add(left, right, value)
    return kern


def extract(path: Path) -> dict:
    font = TTFont(path)
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]
    names = {c: cmap[ord(c)] for c in CHARSET if ord(c) in cmap}
    glyphs = {}
    for char, name in names.items():
        pen = CompactPathPen(glyphset)
        glyphset[name].draw(pen)
        glyphs[char] = {"w": hmtx[name][0], "d": pen.data()}
    os2 = font["OS/2"]
    return {
        "name": font["name"].getDebugName(4),
        "upm": font["head"].unitsPerEm,
        "ascent": font["hhea"].ascent,
        "descent": font["hhea"].descent,
        "capHeight": getattr(os2, "sCapHeight", 0),
        "xHeight": getattr(os2, "sxHeight", 0),
        "glyphs": glyphs,
        "kern": pair_kerning(font, names),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--font", action="append", required=True, metavar="STYLE=PATH")
    args = parser.parse_args()
    fonts = {}
    for item in args.font:
        style, _, path = item.partition("=")
        fonts[style] = extract(Path(path))
        print(f"{style}: {fonts[style]['name']}, {len(fonts[style]['glyphs'])} glyphs, {len(fonts[style]['kern'])} kerning pairs")
    OUT.write_text(json.dumps({"fonts": fonts}, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parent.parent)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
