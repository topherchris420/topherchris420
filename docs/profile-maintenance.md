# Profile maintenance

This repository is the GitHub profile for Christopher Woodyard. The README is
the product: keep it useful in raw Markdown, on a narrow screen, and without
loading external images.

## Structure

The profile uses progressive disclosure. A visitor should understand the lab in
about a minute from the README; anyone curious can keep descending.

| Layer | File | Job |
| --- | --- | --- |
| Map | `README.md` | Who, the rule, five questions, where each experiment stands, what failed, the strata |
| Ledger | `experiments/README.md`, `experiments/ledger.json` | State of every experiment, with sources; `ledger.json` is the source of truth |
| Latency | `experiments/unreasonably-fast.md` | Git-dated timelines: what AI compressed and what it did not |
| Feasibility | `experiments/impossible-six-months-ago.md` | What recently became attemptable, and what it still cannot tell us |
| Strata | `experiments/archive.md` | The archived repositories, read in order |

The README is organized by question, not by repository. Add a new project under
the question it serves. If it serves none of the five, that is worth noticing
before adding a sixth.

## Editorial rules

- Lead with the person, the lab, and the questions. Let projects be the evidence.
- Use the evidence ladder in `experiments/README.md` for every state. Name the
  scope (synthetic, simulated, physical). Never promote a state because of a
  deployment, a demo, or a passing build.
- Keep failures on the page. A `NOT SUPPORTED` result or an unresolved claim is
  part of the record; do not remove it when the work moves on.
- Take timelines only from Git history on the default branch. If no interval
  can be read honestly, write *timeline not reconstructed yet*.
- Describe an archived repository from its own README. Give a reason for
  archiving only if the repository records one. Call a connection to later work
  a lineage only when it is explicit (same name, same stated idea, reused code);
  otherwise call it an echo, or say nothing.
- Link only to public repositories. Private repositories return 404 to visitors.
- Do not introduce unverified performance, safety, clinical, novelty, or
  institutional claims. Avoid "pioneering", "first", "revolutionary", and their
  relatives unless the exact claim is sourced.
- No badges, statistics cards, skill bars, or animated widgets. GitHub already
  shows the contribution graph beneath the README.
- Preserve the artist's voice and the invitation to contribute.

The September 2026 refreshes supersede the earlier layout proposal in
`docs/superpowers/`; those files remain historical planning records. The
contribution-snake workflow was removed in the second refresh; it can be
restored from Git history if wanted.

## Visual assets

All SVGs in `assets/` are self-contained: native text and vector paths, no
scripts, remote fonts, embedded images, or animation. Each has a light and a
dark variant, selected by a `<picture>` element, with the light image as the
fallback. Everything a figure says also appears as ordinary Markdown.

- `nea-onnim-*.svg` — the banner. Its figure is a drawing of the Adinkra symbol
  *Nea Onnim No Sua A, Ohu* ("one who does not know can know from learning"),
  an Akan symbol of knowledge and life-long learning. It is drawn on a 13 × 13
  grid of 12 px cells, mirror-symmetric on both axes, and redrawn for this
  profile rather than copied from another artwork. Keep it faithful to the
  traditional form: no distortion, recolouring beyond the palette, or
  decoration, and keep its name beneath it. It replaced an earlier
  interlaced-curve figure that read too much like another company's logo.
- `constellations-*.svg` — projects grouped around the five questions. Rings mark
  projects that share the typed-judgment layer (Jev); the dashed arc marks the
  IONS-X engine reused in CIRCLE. Update it when a project is added or moves.
- `latency-*.svg` — days from first commit to runnable, and to the first
  controlled or external test, per project. Its numbers must match
  `experiments/ledger.json`. The "still open" date in its legend is the date of
  the last review.

The dark variants of `constellations` and `latency` are pure colour
substitutions of the light files, so geometry changes need to be made in both.

| Role | Light | Dark |
| --- | --- | --- |
| Background | `#F4F7F4` | `#091A1D` |
| Rule | `#CDDCDA` | `#234044` |
| Ink | `#12383C` | `#E8F2ED` |
| Muted | `#476B6E` | `#ADC7C3` |
| Accent (built) | `#0B5D63` | `#8BD5CC` |
| Warm (tested, open, shared) | `#A0522D` | `#E8A87C` |
| Grid | `#E3ECE9` | `#10292C` |

## Before publishing an edit

1. Open every changed project, commit, or evidence link and check its
   destination. Repository files are on `main` except `research`, which uses
   `master`.
2. Preview the README in light and dark mode at desktop and phone widths.
   Verify that figures scale, text wraps, and tables do not clip.
3. Check the SVG files for valid XML and useful title and description text.
4. Validate `experiments/ledger.json` (it must parse) and confirm that states in
   the README match it.
5. Run `git diff --check` and review the complete diff.

Sponsorship configuration belongs in `.github/FUNDING.yml`.
