"""Small helpers for drawing the profile's SVG assets. Standard library only.

Text is drawn as outlines from tools/glyphs.json (see tools/extract_glyphs.py),
so every visitor sees the same letterforms whatever fonts their system has.
Each glyph is defined once per file and placed with <use>, which keeps the
files small. Everything an image says must also appear in its <desc> and in
the README's alt text.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

GLYPHS = Path(__file__).resolve().parent / "glyphs.json"

# The Vers3Dynamics palette. Accent is the deep spectral teal #0B5D63.
PALETTES = {
    "light": dict(bg="#F4F7F4", panel="#FBFCFA", rule="#CDDCDA", ink="#12383C", muted="#476B6E",
                  accent="#0B5D63", warm="#A0522D", grid="#E3ECE9", soft="#E6EFEC"),
    "dark": dict(bg="#091A1D", panel="#0D2226", rule="#234044", ink="#E8F2ED", muted="#ADC7C3",
                 accent="#8BD5CC", warm="#E8A87C", grid="#10292C", soft="#12302F"),
}

SHORT = {"display": "d", "display-regular": "r", "display-italic": "i", "mono": "m",
         "mono-medium": "n", "sans": "s", "sans-medium": "t"}

# Where to look when a style lacks a character (Fraunces has no arrows or sharps).
FALLBACK = {
    "display": ("sans", "mono"), "display-regular": ("sans", "mono"), "display-italic": ("sans", "mono"),
    "sans": ("mono",), "sans-medium": ("mono-medium", "mono"), "mono": (), "mono-medium": ("mono",),
}

_FONTS: dict | None = None


def fonts() -> dict:
    global _FONTS
    if _FONTS is None:
        _FONTS = json.loads(GLYPHS.read_text(encoding="utf-8"))["fonts"]
    return _FONTS


def num(value: float) -> str:
    """Compact number formatting for SVG attributes."""
    text = f"{value:.3f}".rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


class Canvas:
    """Collects SVG elements and the glyph definitions they use."""

    def __init__(self, width: int, height: int, title: str, desc: str):
        self.width, self.height = width, height
        self.title, self.desc = title, desc
        self.body: list[str] = []
        self.used: dict[str, str] = {}

    def add(self, element: str) -> None:
        self.body.append(element)

    # -- text ---------------------------------------------------------------

    def _resolve(self, style: str, char: str) -> str:
        for candidate in (style, *FALLBACK.get(style, ())):
            if char in fonts()[candidate]["glyphs"]:
                return candidate
        return style

    def _runs(self, text: str, style: str) -> list[tuple[str, str]]:
        """Split text into runs that share a font, falling back for missing glyphs."""
        runs: list[tuple[str, str]] = []
        for char in text:
            resolved = self._resolve(style, char)
            if runs and runs[-1][0] == resolved:
                runs[-1] = (resolved, runs[-1][1] + char)
            else:
                runs.append((resolved, char))
        return runs

    def _run_width(self, run: str, style: str, size: float, tracking: float) -> float:
        font = fonts()[style]
        units = 0.0
        for i, char in enumerate(run):
            units += (font["glyphs"].get(char) or font["glyphs"][" "])["w"]
            if i + 1 < len(run):
                units += font["kern"].get(char + run[i + 1], 0)
        return units * size / font["upm"] + tracking * len(run)

    def measure(self, text: str, style: str, size: float, tracking: float = 0) -> float:
        width = sum(self._run_width(run, s, size, tracking) for s, run in self._runs(text, style))
        return width - tracking if text else 0.0

    def text(self, text: str, x: float, y: float, style: str, size: float, fill: str,
             tracking: float = 0, anchor: str = "start", opacity: float | None = None) -> float:
        """Draw `text` with its baseline at y. Returns the drawn width."""
        width = self.measure(text, style, size, tracking)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        extra = f' opacity="{num(opacity)}"' if opacity is not None else ""
        cursor = x
        for run_style, run in self._runs(text, style):
            font = fonts()[run_style]
            scale = size / font["upm"]
            track_units = tracking / scale
            pen = 0.0
            uses = []
            for i, char in enumerate(run):
                glyph = font["glyphs"].get(char) or font["glyphs"][" "]
                gid = f"{SHORT[run_style]}{ord(char):x}"
                if glyph["d"]:
                    self.used.setdefault(gid, glyph["d"])
                    uses.append(f'<use href="#{gid}" x="{num(pen)}"/>')
                pen += glyph["w"] + track_units
                if i + 1 < len(run):
                    pen += font["kern"].get(char + run[i + 1], 0)
            if uses:
                self.add(f'<g transform="translate({num(cursor)} {num(y)}) scale({num(scale)})" fill="{fill}"{extra}>{"".join(uses)}</g>')
            cursor += self._run_width(run, run_style, size, tracking)
        return width

    def wrap(self, text: str, style: str, size: float, max_width: float, tracking: float = 0) -> list[str]:
        words, lines, line = text.split(), [], ""
        for word in words:
            trial = f"{line} {word}".strip()
            if line and self.measure(trial, style, size, tracking) > max_width:
                lines.append(line)
                line = word
            else:
                line = trial
        if line:
            lines.append(line)
        return lines

    # -- output -------------------------------------------------------------

    def svg(self, background: str | None = None, radius: int = 14, border: str | None = None) -> str:
        defs = "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in self.used.items())
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" fill="none" role="img" aria-labelledby="title description">',
            f'<title id="title">{escape(self.title)}</title>',
            f'<desc id="description">{escape(self.desc)}</desc>',
            f"<defs>{defs}</defs>",
        ]
        if background:
            out.append(f'<rect width="{self.width}" height="{self.height}" rx="{radius}" fill="{background}"/>')
        if border:
            out.append(f'<rect x="0.5" y="0.5" width="{self.width - 1}" height="{self.height - 1}" '
                       f'rx="{radius - 0.5}" stroke="{border}"/>')
        out.extend(self.body)
        out.append("</svg>\n")
        return "\n".join(out)
