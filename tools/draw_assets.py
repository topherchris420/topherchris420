#!/usr/bin/env python3
"""Draw the profile's illustrations into assets/, in light and dark variants.

    python3 tools/draw_assets.py

Writes the entrance banner (hero), the six door cards, the chain diagram that
connects the projects, and the section rule. Every drawing comes from one
layout per asset, so the light and dark twins cannot drift. Text is drawn from
tools/glyphs.json; pictograms are plain vector paths. Standard library only.

Edit the content tables below (CABINET, DOORS, CHAIN), keep the README's alt
text in agreement, then run this script and `python3 tools/check_profile.py`.
"""

from __future__ import annotations

import math
from pathlib import Path

from svgkit import PALETTES, Canvas, num

OUT = Path(__file__).resolve().parent.parent / "assets"

# --- Pictograms ---------------------------------------------------------------
# Each is drawn in a 48 x 48 box centred on 0,0 with a 1.8 unit stroke.


def _helix() -> str:
    turns, amp, top, bottom = 1.5, 9.5, -19.0, 19.0
    height = bottom - top

    def x_at(y: float, sign: float) -> float:
        return sign * amp * math.sin(2 * math.pi * turns * (y - top) / height)

    def strand(sign: float) -> str:
        pts = [f"{num(x_at(top + i * 0.5, sign))} {num(top + i * 0.5)}" for i in range(int(height / 0.5) + 1)]
        return '<path d="M' + " L".join(pts) + '"/>'

    rungs = []
    for k in range(9):
        y = top + (k + 0.5) * height / 9
        x = x_at(y, 1)
        if abs(x) > 3.5:
            rungs.append(f'<path d="M{num(-x)} {num(y)} H{num(x)}" stroke-opacity="0.4" stroke-width="1.4"/>')
    return strand(1) + strand(-1) + "".join(rungs)


def _nautilus() -> str:
    a, b, end = 2.0, 0.17, 4.2 * math.pi

    def raw(t: float) -> tuple[float, float]:
        r = a * math.exp(b * t)
        return r * math.cos(t), -r * math.sin(t)

    samples = [raw(i / 300 * end) for i in range(301)]
    ox = -(min(x for x, _ in samples) + max(x for x, _ in samples)) / 2
    oy = -(min(y for _, y in samples) + max(y for _, y in samples)) / 2

    def point(t: float) -> tuple[float, float]:
        x, y = raw(t)
        return x + ox, y + oy

    spiral = '<path d="M' + " L".join(f"{num(x + ox)} {num(y + oy)}" for x, y in samples) + '"/>'
    septa = []
    for k in range(1, 12):
        t = end - k * 0.62
        if t < 2 * math.pi + 0.6:
            break
        (x2, y2), (x1, y1) = point(t), point(t - 2 * math.pi)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        cx, cy = mx + (y2 - y1) * 0.18, my - (x2 - x1) * 0.18
        septa.append(f'<path d="M{num(x1)} {num(y1)} Q{num(cx)} {num(cy)} {num(x2)} {num(y2)}" stroke-opacity="0.5" stroke-width="1.3"/>')
    return spiral + "".join(septa)


PICTOGRAMS = {
    # R.A.I.N. Lab: a flask, the lab inside the world
    "flask": (
        '<path d="M-5 -19 V-7 L-15 14 Q-16.5 18 -12 18 H12 Q16.5 18 15 14 L5 -7 V-19"/>'
        '<path d="M-8.5 -19 H8.5"/>'
        '<path d="M-11.2 7 q3.7 -3 7.47 0 t7.47 0 t7.47 0"/>'
        '<circle cx="-3" cy="12.5" r="1.6"/><circle cx="4" cy="10.8" r="1.1"/>'
    ),
    # Pine Gap: a radome on its pedestal
    "radome": (
        '<circle cx="0" cy="-5" r="13"/>'
        '<ellipse cx="0" cy="-5" rx="5.5" ry="13" stroke-opacity="0.6"/>'
        '<path d="M-13 -5 Q0 0 13 -5" stroke-opacity="0.6"/>'
        '<path d="M-10.5 -12.5 Q0 -9 10.5 -12.5" stroke-opacity="0.6"/>'
        '<path d="M-6 8 L-8.5 16.5 H8.5 L6 8"/><path d="M-21 16.5 H21"/>'
    ),
    # Mannahatta: the same storm over a changed ground
    "storm": (
        '<path d="M-13 0 A5 5 0 0 1 -9.5 -9.2 A8 8 0 0 1 5.2 -10.6 A7 7 0 0 1 13 0 Z"/>'
        '<path d="M-7 4.5 l-2 6 M0 4.5 l-2 6 M7 4.5 l-2 6"/>'
        '<path d="M-19 16 q6 -3.2 12 0 t12 0 t12 0"/>'
    ),
    # GHOSTWHEEL: a steering wheel
    "wheel": (
        '<circle cx="0" cy="0" r="17" stroke-width="2.4"/><circle cx="0" cy="0" r="4.6"/>'
        '<path d="M-4.6 1 L-16.4 3.6 M4.6 1 L16.4 3.6 M0 4.6 V16.8"/>'
    ),
    # James: a pointer that waits for approval
    "cursor": (
        '<path d="M-13 -15 L-13 9 L-7.2 3.6 L-3.4 12.4 L0.4 10.8 L-3.3 2.2 L4.4 2.2 Z"/>'
        '<rect x="2" y="-19" width="14" height="14" rx="3"/>'
        '<path d="M5.4 -12.2 L8 -9.4 L12.8 -15"/>'
    ),
    # DNA Music Molecules: a double helix
    "helix": _helix(),
    # Project Ascent: a house and its price history
    "house": (
        '<path d="M-16.5 1.5 L0 -14 L16.5 1.5"/><path d="M-12 -2.6 V17 H12 V-2.6"/>'
        '<path d="M-7 12.5 L-2.4 7 L1.6 9.4 L7 3.2"/><path d="M3.4 3 H7.2 V6.8"/>'
    ),
    # Nocturne: a moon above a darkened horizon
    "moon": (
        '<path d="M3 -18 A13 13 0 1 0 16 2 A10 10 0 0 1 3 -18 Z"/>'
        '<path d="M-14 -13 v5 M-16.5 -10.5 h5 M15 -15 v3.6 M13.2 -13.2 h3.6 M-17 5 v3.4 M-18.7 6.7 h3.4" stroke-width="1.4"/>'
        '<path d="M-21 17 H21"/>'
    ),
    # Luca: a lens over a small network
    "lens": (
        '<circle cx="-3" cy="-3" r="12"/><path d="M5.6 5.6 L15.5 15.5" stroke-width="3"/>'
        '<path d="M-9 0 L-2 -9 L3 1 Z" stroke-opacity="0.6"/>'
        '<circle cx="-9" cy="0" r="2" fill="currentColor"/><circle cx="-2" cy="-9" r="2" fill="currentColor"/>'
        '<circle cx="3" cy="1" r="2" fill="currentColor"/>'
    ),
    # Jasmine: five petals, five steps of a workflow
    "flower": "".join(
        f'<circle cx="{num(12 * math.cos(math.radians(a)))}" cy="{num(12 * math.sin(math.radians(a)))}" r="3.6"/>'
        f'<path d="M{num(3.4 * math.cos(math.radians(a)))} {num(3.4 * math.sin(math.radians(a)))} '
        f'L{num(8.4 * math.cos(math.radians(a)))} {num(8.4 * math.sin(math.radians(a)))}"/>'
        for a in (-90, -18, 54, 126, 198)
    ) + '<circle cx="0" cy="0" r="2.6" fill="currentColor"/>',
    # TRIAD: three electrodes and an uncertain estimate
    "triad": (
        '<path d="M0 -15 L-14.5 11 H14.5 Z" stroke-opacity="0.45" stroke-dasharray="2.4 2.6"/>'
        '<circle cx="0" cy="-15" r="3" fill="currentColor"/><circle cx="-14.5" cy="11" r="3" fill="currentColor"/>'
        '<circle cx="14.5" cy="11" r="3" fill="currentColor"/>'
        '<ellipse cx="1.5" cy="1" rx="6.5" ry="4.6" stroke-dasharray="2 2"/><circle cx="1.5" cy="1" r="1.4" fill="currentColor"/>'
    ),
    # Quantum Noise Profiler: noise crossing a threshold
    "noise": (
        '<path d="M-20 -6 H20" stroke-dasharray="2.6 2.4" stroke-opacity="0.6"/>'
        '<path d="M-20 9 L-16.5 5 L-13 10.5 L-9.5 4 L-6 9.5 L-2.5 3 L1 7.5 L4.5 1 L8 5 L11 -2 L14 2.5 L16.5 -10 L20 -4"/>'
        '<circle cx="16.5" cy="-10" r="2.6"/>'
    ),
    # IONS-X: agents and the associations they share
    "swarm": (
        '<circle cx="0" cy="0" r="18.5" stroke-dasharray="2.4 2.8" stroke-opacity="0.5"/>'
        '<path d="M-9 -7 L2 -11 L10 -3 L6 8 L-4 3 Z M-4 3 L-10 10" stroke-opacity="0.55"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="currentColor"/>'
                  for x, y in ((-9, -7), (2, -11), (10, -3), (-4, 3), (6, 8), (-10, 10)))
    ),
    # CIRCLE: a pulse inside a circle
    "pulse": (
        '<circle cx="0" cy="0" r="17"/>'
        '<path d="M-17 2 H-9 L-6 -7.5 L-2 11 L2 -5 L4.6 2 H17"/>'
    ),
    # Project 33: a folding-fin rocket
    "rocket": (
        '<path d="M0 -21 C4.6 -15.5 6 -8 6 3 V10 H-6 V3 C-6 -8 -4.6 -15.5 0 -21 Z"/>'
        '<circle cx="0" cy="-7" r="2.6"/>'
        '<path d="M-6 2.5 L-12.5 13 V16.5 L-6 10.5 M6 2.5 L12.5 13 V16.5 L6 10.5"/>'
        '<path d="M-2 13.5 V19.5 M2 13.5 V19.5" stroke-dasharray="1.6 1.8"/>'
    ),
    # Doors
    "globe": (
        '<circle cx="0" cy="0" r="19"/><ellipse cx="0" cy="0" rx="8" ry="19"/>'
        '<path d="M-19 0 H19 M-16.4 -9.5 Q0 -6 16.4 -9.5 M-16.4 9.5 Q0 6 16.4 9.5" stroke-opacity="0.7"/>'
    ),
    "decision": (
        '<path d="M0 -18 L18 0 L0 18 L-18 0 Z"/>'
        '<path d="M-4.2 -4.4 Q-4.2 -9 0 -9 Q4.4 -9 4.4 -5 Q4.4 -2 0.6 -0.4 V2.6"/>'
        '<circle cx="0.6" cy="7" r="1.5" fill="currentColor"/>'
    ),
    "sound": (
        '<circle cx="-12" cy="0" r="2.8" fill="currentColor"/>'
        + "".join(
            f'<path d="M{num(-12 + r * math.cos(math.radians(-50)))} {num(r * math.sin(math.radians(-50)))} '
            f'A{r} {r} 0 0 1 {num(-12 + r * math.cos(math.radians(50)))} {num(r * math.sin(math.radians(50)))}" '
            f'stroke-opacity="{o}"/>'
            for r, o in ((8, 1), (15, 0.75), (22, 0.5), (29, 0.28))
        )
    ),
    "plot": (
        '<path d="M-19 -19 V17 H19"/>'
        '<path d="M-13 9 L17 -13" stroke-dasharray="2.4 2.6" stroke-opacity="0.5"/>'
        + "".join(
            f'<path d="M{x} {y - e} V{y + e} M{x - 2.2} {y - e} H{x + 2.2} M{x - 2.2} {y + e} H{x + 2.2}" stroke-opacity="0.65" stroke-width="1.4"/>'
            f'<circle cx="{x}" cy="{y}" r="2.4" fill="currentColor"/>'
            for x, y, e in ((-9, 8, 5), (2, -1, 6), (12, -9, 4))
        )
    ),
    "wrench": (
        '<path d="M-15.5 15.5 L3 -3" stroke-width="4.6" stroke-linecap="round"/>'
        '<path d="M2.4 -10.6 A9 9 0 0 1 13.6 -14.6 L8.2 -9.2 L9.4 -4.4 L14.2 -3.2 L19.6 -8.6 '
        'A9 9 0 0 1 8.2 2.6 Z"/>'
    ),
    "nautilus": _nautilus(),
}


def pictogram(name: str, cx: float, cy: float, scale: float, color: str, stroke: float = 1.8) -> str:
    return (f'<g transform="translate({num(cx)} {num(cy)}) scale({num(scale)})" stroke="{color}" color="{color}" '
            f'stroke-width="{num(stroke)}" stroke-linecap="round" stroke-linejoin="round">{PICTOGRAMS[name]}</g>')


# The Adinkra symbol Nea Onnim No Sua A, Ohu, on its 13 x 13 grid of 12-unit cells.
ADINKRA = (
    "M0 0h60v12h-60zM72 0h12v12h-12zM96 0h60v12h-60zM48 12h12v12h-12zM72 12h12v12h-12zM96 12h12v12h-12z"
    "M12 24h48v12h-48zM72 24h12v12h-12zM96 24h48v12h-48zM48 36h12v12h-12zM72 36h12v12h-12zM96 36h12v12h-12z"
    "M0 48h156v12h-156zM0 60h12v12h-12zM24 60h12v12h-12zM48 60h12v12h-12zM96 60h12v12h-12zM120 60h12v12h-12z"
    "M144 60h12v12h-12zM0 72h12v12h-12zM24 72h12v12h-12zM48 72h60v12h-60zM120 72h12v12h-12zM144 72h12v12h-12z"
    "M0 84h12v12h-12zM24 84h12v12h-12zM48 84h12v12h-12zM96 84h12v12h-12zM120 84h12v12h-12zM144 84h12v12h-12z"
    "M0 96h156v12h-156zM48 108h12v12h-12zM72 108h12v12h-12zM96 108h12v12h-12zM12 120h48v12h-48zM72 120h12v12h-12z"
    "M96 120h48v12h-48zM48 132h12v12h-12zM72 132h12v12h-12zM96 132h12v12h-12zM0 144h60v12h-60zM72 144h12v12h-12z"
    "M96 144h60v12h-60z"
)


def adinkra(x: float, y: float, size: float, color: str) -> str:
    return f'<path transform="translate({num(x)} {num(y)}) scale({num(size / 156)})" fill="{color}" d="{ADINKRA}"/>'


def registration(x: float, y: float, color: str, size: float = 6) -> str:
    return f'<path d="M{num(x - size)} {num(y)} H{num(x + size)} M{num(x)} {num(y - size)} V{num(y + size)}" stroke="{color}"/>'


# --- The entrance banner ------------------------------------------------------

# Fifteen drawers, one per project the profile introduces, and one left open.
CABINET = [
    ("R.A.I.N. LAB", "flask"), ("PINE GAP", "radome"), ("MANNAHATTA", "storm"), ("GHOSTWHEEL", "wheel"),
    ("JAMES", "cursor"), ("DNA MUSIC", "helix"), ("ASCENT", "house"), ("NOCTURNE", "moon"),
    ("LUCA", "lens"), ("JASMINE", "flower"), ("TRIAD", "triad"), ("QUBIT NOISE", "noise"),
    ("IONS-X", "swarm"), ("CIRCLE", "pulse"), ("PROJECT 33", "rocket"), (None, None),
]

HERO_DESC = (
    "Christopher Woodyard. Vers3Dynamics, an independent open-source laboratory. "
    "I make strange things and test whether they work. "
    "Beside the name, a cabinet of sixteen specimen drawers, each labelled with a project and a small drawing: "
    + ", ".join(f"{name} ({pic})" for name, pic in CABINET if name)
    + ", and one empty drawer marked with a question mark for the next experiment. "
    "Below the name, the Adinkra symbol Nea Onnim No Sua A, Ohu: one who does not know can know from learning."
)


def hero(mode: str) -> str:
    p = PALETTES[mode]
    W, H = 1200, 560
    c = Canvas(W, H, "Christopher Woodyard · Vers3Dynamics", HERO_DESC)
    for x, y in ((28, 28), (W - 28, 28), (28, H - 28), (W - 28, H - 28)):
        c.add(registration(x, y, p["rule"]))

    # The person and the promise
    c.text("VERS3DYNAMICS · OPEN-SOURCE LABORATORY", 66, 118, "mono-medium", 13, p["muted"], tracking=2.4)
    c.text("Christopher", 62, 214, "display", 80, p["ink"], tracking=-1.4)
    c.text("Woodyard", 62, 296, "display", 80, p["ink"], tracking=-1.4)
    c.text("I make strange things", 66, 360, "display-italic", 31, p["accent"])
    c.text("and test whether they work.", 66, 400, "display-italic", 31, p["accent"])
    c.add(f'<path d="M66 440 H548" stroke="{p["rule"]}"/>')
    c.add(adinkra(66, 462, 46, p["accent"]))
    c.text("NEA ONNIM NO SUA A, OHU", 128, 478, "mono", 11, p["muted"], tracking=1.9)
    c.text("One who does not know can know from learning.", 128, 501, "display-italic", 15.5, p["muted"])

    # The cabinet
    cols, rows, dw, dh, gap = 4, 4, 117, 95, 8
    x0, y0 = 640, 84
    cw, ch = cols * dw + (cols - 1) * gap, rows * dh + (rows - 1) * gap
    c.add(f'<rect x="{x0 - 14}" y="{y0 - 14}" width="{cw + 28}" height="{ch + 28}" rx="10" fill="{p["panel"]}" stroke="{p["rule"]}"/>')
    for i, (name, pic) in enumerate(CABINET):
        x = x0 + (i % cols) * (dw + gap)
        y = y0 + (i // cols) * (dh + gap)
        if name is None:
            c.add(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{dw - 1}" height="{dh - 1}" rx="6" stroke="{p["rule"]}" stroke-dasharray="3 3"/>')
            c.text("?", x + dw / 2, y + 52, "display-italic", 34, p["muted"], anchor="middle")
            c.text("NEXT", x + dw / 2, y + 80, "sans-medium", 11, p["muted"], tracking=1.6, anchor="middle")
            continue
        c.add(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{dw - 1}" height="{dh - 1}" rx="6" fill="{p["bg"]}" stroke="{p["rule"]}"/>')
        c.text(f"{i + 1:02d}", x + 10, y + 18, "mono", 10, p["muted"], tracking=0.6)
        c.add(pictogram(pic, x + dw / 2, y + 41, 0.82, p["accent"], stroke=2.0))
        c.text(name, x + dw / 2, y + 81, "sans-medium", 11, p["ink"], tracking=1.1, anchor="middle")
    c.text("FIFTEEN EXPERIMENTS · ONE DRAWER LEFT OPEN", x0 + cw / 2, y0 + ch + 44, "mono", 11, p["muted"], tracking=2.2, anchor="middle")
    return c.svg(background=p["bg"], border=p["rule"])


# --- The six doors -------------------------------------------------------------

# (anchor, title lines, invitation, pictogram, exhibits named on the card)
DOORS = [
    ("play-a-world", ["Play a world"], "Explore virtual cities, simulations and autonomous agents.", "globe",
     ["PINE GAP", "R.A.I.N. LAB", "MANNAHATTA"]),
    ("challenge-an-intelligent-system", ["Challenge an", "intelligent system"],
     "Investigate decisions, authorization, uncertainty and security.", "decision",
     ["GHOSTWHEEL", "JAMES", "PORDENONE"]),
    ("hear-the-invisible", ["Hear the invisible"],
     "Discover sound, molecular representations, frequency and resonance.", "sound",
     ["DNA MUSIC", "SENTINEL", "STUDIO"]),
    ("explore-a-research-lab", ["Explore a research lab"],
     "Inspect experiments, models, measurements and scientific results.", "plot",
     ["TRIAD", "QUBIT NOISE", "IONS-X"]),
    ("use-something-practical", ["Use something", "practical"],
     "Approachable software for homeowners, creators, device owners and researchers.", "wrench",
     ["ASCENT", "LUCA", "JASMINE", "NOCTURNE"]),
    ("discover-the-unusual", ["Discover the unusual"],
     "Experimental inventions that resist easy categorization.", "nautilus",
     ["CIRCLE", "PROJECT 33", "WAVEFORM"]),
]


def door(mode: str, index: int) -> str:
    p = PALETTES[mode]
    anchor, title, invitation, pic, exhibits = DOORS[index]
    W, H = 400, 280
    desc = (f"Door {index + 1}: {' '.join(title)}. {invitation} "
            f"Exhibits: {', '.join(e.title() for e in exhibits)}.")
    c = Canvas(W, H, " ".join(title), desc)
    c.add(f'<rect x="28" y="24" width="26" height="3" rx="1.5" fill="{p["accent"]}"/>')
    c.text(f"DOOR {index + 1:02d}", 28, 50, "mono-medium", 11.5, p["muted"], tracking=2.2)
    c.add(pictogram(pic, W - 52, 52, 1.05, p["accent"], stroke=1.9))
    # Titles sit on a shared baseline so the invitations line up across a row.
    y = 148 - 35 * (len(title) - 1)
    for line in title:
        c.text(line, 27, y, "display", 31, p["ink"], tracking=-0.4)
        y += 35
    y = 180
    for line in c.wrap(invitation, "sans", 15, W - 60):
        c.text(line, 28, y, "sans", 15, p["muted"])
        y += 21
    c.add(f'<path d="M28 {H - 50} H{W - 28}" stroke="{p["rule"]}"/>')
    label = " · ".join(exhibits)
    size = 11.5
    while c.measure(label, "mono", size, 1.0) > W - 92 and size > 8.5:
        size -= 0.25
    c.text(label, 28, H - 26, "mono", size, p["accent"], tracking=1.0)
    c.text("→", W - 28, H - 25, "mono-medium", 15, p["accent"], anchor="end")
    return c.svg(background=p["panel"], border=p["rule"], radius=12)


# --- How the inventions connect ---------------------------------------------------

# (stage, question, representative projects). Representative, not exhaustive:
# the projects are separate systems that ask the same questions.
CHAIN = [
    ("Observation", "What is actually there?", ["CIRCLE", "Luca", "Qubit Noise"]),
    ("Interpretation", "What might it mean?", ["DNA Music", "R.A.I.N. Lab", "DRR"]),
    ("Decision", "Is the evidence enough to act?", ["TRIAD", "James", "Pordenone"]),
    ("Action", "What does the system do?", ["Pine Gap", "GHOSTWHEEL", "Nocturne"]),
    ("Measurement", "What happened, and how sure are we?", ["Qubit Noise", "Ascent", "IONS-X"]),
    ("Verification", "Would it hold up again?", ["rain-pipeline", "Mannahatta", "Project 33"]),
]
ABSTAIN = ("Not enough evidence?", "Abstain, wait, or hand the decision to a person.",
           "TRIAD ABSTAINS · JAMES ASKS · GHOSTWHEEL REFUSES")
RETURN = "WHAT WAS LEARNED CHANGES WHAT WE LOOK FOR NEXT"

CHAIN_DESC = (
    "Six stages from left to right: "
    + "; ".join(f"{stage}, asking {question.lower().rstrip('?')}?, with {', '.join(names)}" for stage, question, names in CHAIN)
    + f". From Decision, a dashed branch leads down to a box: {ABSTAIN[0]} {ABSTAIN[1]} "
    "TRIAD abstains, James asks, GHOSTWHEEL refuses. "
    "A line returns from Verification to Observation: what was learned changes what we look for next. "
    "The projects are separate systems placed where they do their main work; they are not one integrated architecture."
)


def chain(mode: str) -> str:
    p = PALETTES[mode]
    W, H = 1200, 640
    c = Canvas(W, H, "How the inventions connect", CHAIN_DESC)
    c.text("HOW THE INVENTIONS CONNECT · ONE QUESTION, ASKED SIX WAYS", 60, 66, "mono-medium", 12.5, p["muted"], tracking=2.4)
    xs = [110 + i * 196 for i in range(6)]
    y = 160
    for a, b in zip(xs, xs[1:]):
        c.add(f'<path d="M{a + 14} {y} H{b - 14}" stroke="{p["rule"]}" stroke-width="1.6"/>')
        m = (a + b) / 2
        c.add(f'<path d="M{m - 3} {y - 5} L{m + 3} {y} L{m - 3} {y + 5}" stroke="{p["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (x, (stage, question, names)) in enumerate(zip(xs, CHAIN)):
        human = stage == "Decision"
        colour = p["warm"] if human else p["accent"]
        if human:
            c.add(f'<circle cx="{x}" cy="{y}" r="15" stroke="{colour}" stroke-width="1.5"/>')
        c.add(f'<circle cx="{x}" cy="{y}" r="8" fill="{p["bg"]}" stroke="{colour}" stroke-width="2.2"/>')
        c.text(f"{i + 1:02d}", x, y - 30, "mono", 11, p["muted"], tracking=1.2, anchor="middle")
        c.text(stage, x, y + 52, "display", 23, p["ink"], anchor="middle", tracking=-0.2)
        qy = y + 78
        for line in c.wrap(question, "sans", 14.5, 172):
            c.text(line, x, qy, "sans", 14.5, p["muted"], anchor="middle")
            qy += 20
        ny = y + 142
        for name in names:
            c.text(name.upper(), x, ny, "mono-medium", 11.5, colour, tracking=1.0, anchor="middle")
            ny += 21
    # The branch: when uncertainty should prevent action
    bx, top = xs[2], 400
    c.add(f'<path d="M{bx} {y + 214} V{top}" stroke="{p["warm"]}" stroke-width="1.6" stroke-dasharray="4 4"/>')
    c.add(f'<path d="M{bx - 5} {top - 7} L{bx} {top - 1} L{bx + 5} {top - 7}" stroke="{p["warm"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    bw, bh = 470, 104
    c.add(f'<rect x="{bx - bw / 2}" y="{top}" width="{bw}" height="{bh}" rx="10" fill="{p["panel"]}" stroke="{p["warm"]}" stroke-width="1.4"/>')
    c.text(ABSTAIN[0], bx, top + 34, "display-italic", 22, p["warm"], anchor="middle")
    c.text(ABSTAIN[1], bx, top + 60, "sans", 15, p["ink"], anchor="middle")
    c.text(ABSTAIN[2], bx, top + 86, "mono", 10.5, p["muted"], tracking=1.2, anchor="middle")
    # The return: verification feeds the next observation
    left, right, base = xs[0], xs[-1], 574
    c.add(f'<path d="M{right} {y + 214} V{base - 12} Q{right} {base} {right - 12} {base} H{left + 12} Q{left} {base} {left} {base - 12} V{y + 214}" '
          f'stroke="{p["rule"]}" stroke-width="1.6"/>')
    c.add(f'<path d="M{left - 5} {y + 222} L{left} {y + 215} L{left + 5} {y + 222}" stroke="{p["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    label_w = c.measure(RETURN, "mono", 11, 2.0) + 28
    c.add(f'<rect x="{(left + right) / 2 - label_w / 2}" y="{base - 10}" width="{label_w}" height="20" fill="{p["bg"]}"/>')
    c.text(RETURN, (left + right) / 2, base + 4, "mono", 11, p["muted"], tracking=2.0, anchor="middle")
    c.text("Each name marks where a project does its main work. They are separate systems, not one architecture.",
           60, H - 24, "sans", 13, p["muted"])
    return c.svg(background=p["bg"], border=p["rule"])


# --- The section rule ------------------------------------------------------------


def rule(mode: str) -> str:
    p = PALETTES[mode]
    W, H = 1200, 40
    c = Canvas(W, H, "Section rule", "A thin measuring rule with a short graduated scale at its centre, separating sections.")
    c.add(f'<path d="M0 20.5 H{W}" stroke="{p["rule"]}"/>')
    ticks = []
    for i in range(-10, 11):
        x = W / 2 + i * 7
        h = 9 if i % 5 == 0 else 4.5
        ticks.append(f"M{num(x)} {num(20.5 - h)} V20.5")
    c.add(f'<path d="{" ".join(ticks)}" stroke="{p["muted"]}" stroke-opacity="0.75"/>')
    c.add(f'<circle cx="{W / 2}" cy="20.5" r="3" fill="{p["accent"]}"/>')
    return c.svg()


def main() -> None:
    for mode in PALETTES:
        builds = [("hero", lambda m: hero(m)), ("rule", lambda m: rule(m)), ("chain", lambda m: chain(m))]
        builds += [(f"door-{d[0].split('-')[0]}", (lambda i: lambda m: door(m, i))(i)) for i, d in enumerate(DOORS)]
        for name, build in builds:
            path = OUT / f"{name}-{mode}.svg"
            path.write_text(build(mode), encoding="utf-8")
            print(f"wrote {path.relative_to(OUT.parent).as_posix()} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
