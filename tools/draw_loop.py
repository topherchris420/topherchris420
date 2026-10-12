#!/usr/bin/env python3
"""Draw the profile's loop diagram: assets/loop-light.svg and assets/loop-dark.svg.

Both variants come from one layout, so the light and dark twins cannot drift.
Edit STAGES when a featured project changes where it does its main work, keep
the README's "On the loop" lines and the image's alt text in agreement, then
run `python3 tools/draw_loop.py` and `python3 tools/check_profile.py`.
Standard library only.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

PALETTES = {
    "light": dict(bg="#F4F7F4", rule="#CDDCDA", ink="#12383C", muted="#476B6E", accent="#0B5D63", warm="#A0522D", grid="#E3ECE9"),
    "dark": dict(bg="#091A1D", rule="#234044", ink="#E8F2ED", muted="#ADC7C3", accent="#8BD5CC", warm="#E8A87C", grid="#10292C"),
}

W, H = 960, 470
TOP, BOTTOM = 158, 342          # y of the two straight runs of the loop
XS = [170, 377, 583, 790]      # node positions along each run
R = (BOTTOM - TOP) / 2          # radius of the turning arcs
MID = (TOP + BOTTOM) / 2

# (stage, instruments) in loop order. Top run goes left to right; bottom run right to left.
STAGES = [
    ("observe", "CIRCLE · DRR"),
    ("propose", "R.A.I.N. Lab"),
    ("validate", "Pordenone"),
    ("authorize", "James · HumanTouch"),
    ("act", "James · Pine Gap"),
    ("measure", "TRIAD · rain-pipeline"),
    ("preserve", "R.A.I.N. Lab · Pordenone"),
    ("replay", "rain-pipeline · TRIAD"),
]

DESC = (
    "A loop of eight stages: observe, propose, validate, authorize, act, measure, preserve, replay, then back to observe. "
    "Each stage is labelled with the projects that do their main work there. "
    "Observe: CIRCLE and Dynamic Resonance Rooting. Propose: R.A.I.N. Lab. Validate: Pordenone. "
    "Authorize, the one stage highlighted in a warm colour as belonging to a person: James and HumanTouch. "
    "Act: James and Pine Gap. Measure: TRIAD and rain-pipeline. Preserve: R.A.I.N. Lab and Pordenone. "
    "Replay: rain-pipeline and TRIAD. "
    "Inside the loop: Intelligence may propose. Evidence must be checked. Authority stays with the human. "
    "Not every project implements every stage."
)

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def chevron(x, y, direction, color):
    s = 6
    if direction == "right":
        d = f"M{x - s / 2:g} {y - s:g} L{x + s / 2:g} {y:g} L{x - s / 2:g} {y + s:g}"
    elif direction == "left":
        d = f"M{x + s / 2:g} {y - s:g} L{x - s / 2:g} {y:g} L{x + s / 2:g} {y + s:g}"
    elif direction == "down":
        d = f"M{x - s:g} {y - s / 2:g} L{x:g} {y + s / 2:g} L{x + s:g} {y - s / 2:g}"
    else:
        d = f"M{x - s:g} {y + s / 2:g} L{x:g} {y - s / 2:g} L{x + s:g} {y + s / 2:g}"
    return f'    <path d="{d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def build(mode: str) -> str:
    p = PALETTES[mode]
    left, right = XS[0], XS[-1]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-labelledby="title description">',
        '  <title id="title">One loop, eight stages</title>',
        f'  <desc id="description">{DESC}</desc>',
        f'  <rect width="{W}" height="{H}" rx="12" fill="{p["bg"]}"/>',
        f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" stroke="{p["rule"]}"/>',
        f'  <g font-family="{FONT}">',
        f'    <text x="40" y="46" fill="{p["muted"]}" font-size="13" letter-spacing="2" font-weight="600">ONE LOOP · WHERE EACH INSTRUMENT DOES ITS MAIN WORK</text>',
        # the track
        f'    <path d="M{left} {TOP} H{right} A{R:g} {R:g} 0 0 1 {right} {BOTTOM} H{left} A{R:g} {R:g} 0 0 1 {left} {TOP} Z" stroke="{p["rule"]}" stroke-width="2"/>',
    ]
    # direction marks between nodes and on the turns
    for a, b in zip(XS, XS[1:]):
        out.append(chevron((a + b) / 2, TOP, "right", p["accent"]))
        out.append(chevron((a + b) / 2, BOTTOM, "left", p["accent"]))
    out.append(chevron(right + R, MID, "down", p["accent"]))
    out.append(chevron(left - R, MID, "up", p["accent"]))

    positions = [(x, TOP) for x in XS] + [(x, BOTTOM) for x in reversed(XS)]
    for (stage, who), (x, y) in zip(STAGES, positions):
        human = stage == "authorize"
        colour = p["warm"] if human else p["accent"]
        if human:
            out.append(f'    <circle cx="{x}" cy="{y}" r="15" stroke="{p["warm"]}" stroke-width="1.5"/>')
            out.append(f'    <circle cx="{x}" cy="{y}" r="7" fill="{p["warm"]}"/>')
        else:
            out.append(f'    <circle cx="{x}" cy="{y}" r="7" fill="{p["bg"]}" stroke="{p["accent"]}" stroke-width="2"/>')
        if y == TOP:
            stage_y, who_y = y - 30, y - 58
        else:
            stage_y, who_y = y + 44, y + 70
        out.append(f'    <text x="{x}" y="{stage_y}" fill="{colour}" font-size="20" font-weight="600" text-anchor="middle">{stage}</text>')
        out.append(f'    <text x="{x}" y="{who_y}" fill="{p["ink"]}" font-size="16" text-anchor="middle">{who}</text>')

    # the person's step, named inside the loop beside its node
    out.append(f'    <text x="{right}" y="{TOP + 38}" fill="{p["warm"]}" font-size="14" text-anchor="middle" letter-spacing="0.4">a person decides</text>')

    cx = (left + right) / 2
    out += [
        f'    <text x="{cx:g}" y="{MID - 20:g}" fill="{p["ink"]}" font-size="19" text-anchor="middle">Intelligence may propose.</text>',
        f'    <text x="{cx:g}" y="{MID + 8:g}" fill="{p["ink"]}" font-size="19" text-anchor="middle">Evidence must be checked.</text>',
        f'    <text x="{cx:g}" y="{MID + 36:g}" fill="{p["warm"]}" font-size="19" font-weight="600" text-anchor="middle">Authority stays with the human.</text>',
        f'    <text x="40" y="{H - 24}" fill="{p["muted"]}" font-size="13">Each name marks where a project does its main work. Not every project implements every stage.</text>',
        "  </g>",
        "</svg>",
        "",
    ]
    return "\n".join(out)


for mode in PALETTES:
    path = OUT / f"loop-{mode}.svg"
    path.write_text(build(mode), encoding="utf-8")
    print("wrote", path.relative_to(OUT.parent).as_posix())
