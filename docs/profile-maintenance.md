# Profile maintenance

This repository is the GitHub profile for Christopher Woodyard. The README is
the product: keep it useful in raw Markdown, on a narrow screen, and without
loading external images.

## Editorial choices

- Lead with the person, the lab, and the work visitors can inspect.
- R.A.I.N., DRR, and CIRCLE are entry points into research orchestration, signal
  analysis, and instrumentation. They are separate projects, not a claim of a
  fully integrated or validated platform.
- Check each project's current README and linked evidence before changing its
  description. A repository check, simulation result, and measured hardware
  result are different kinds of evidence.
- Keep experimental status beside the project it qualifies. Do not introduce
  unverified performance, safety, clinical, novelty, or institutional claims.
- Prefer durable repository links over changing star counts, test counts,
  activity statistics, or third-party badge services.
- Preserve the artist's voice and the invitation to contribute.

The September 2026 refresh supersedes the earlier profile layout proposal in
`docs/superpowers/`; those files remain historical planning records.

## Visual assets

`assets/resonance-light.svg` and `assets/resonance-dark.svg` are self-contained
SVGs. They use native text and vector paths, with no scripts, remote fonts,
embedded images, animation, or build step. Their curves are an abstract drawing
of coupled rhythms, not recorded biosignals or experimental results.

The light palette uses spectral teal `#0B5D63` on `#F4F7F4`; the dark palette
uses `#8BD5CC` on `#091A1D`. Keep the SVG view boxes, text, and geometry aligned
when editing either variant. The README's `<picture>` selects the theme, and
the light image is the fallback. Essential identity and project information
also appears as ordinary Markdown.

## Before publishing an edit

1. Open every changed project or evidence link and check its destination.
2. Preview the README in light and dark mode at desktop and phone widths.
   Verify that the banner scales, text wraps, and the table does not clip.
3. Check both SVG files for valid XML and useful title/description text.
4. Run `git diff --check` and review the complete diff.

The existing contribution animation is optional, behind a collapsed details
section. Its `output` branch and scheduled workflow are independent of the
profile content. Sponsorship configuration belongs in `.github/FUNDING.yml`.
