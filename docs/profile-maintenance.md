# Profile maintenance

This repository is Christopher Woodyard's GitHub profile. The README is the front door: someone should be able to understand the practice, choose something to try, and find the record behind it in about a minute.

## Structure

| Layer | File | Job |
| --- | --- | --- |
| Front door | `README.md` | Person, practice, playable lead project, three further entry points, recorded findings, invitation |
| Project map | `docs/project-map.md` | Five questions, the wider project catalog, discarded approaches |
| Ledger | `experiments/README.md`, `experiments/ledger.json` | Scoped experiment states and source records; JSON is the source of truth |
| Build history | `experiments/unreasonably-fast.md` | Git-dated timelines and what AI did or did not shorten |
| Feasibility | `experiments/impossible-six-months-ago.md` | What recently became attemptable and what it still cannot tell us |
| Archive | `experiments/archive.md` | Earlier repositories and their recorded connections |

The front page is curated. Add a project there when it gives a visitor a distinct, useful way into the practice. Put the wider catalog in the project map under the question it serves. A new repository does not automatically need a new front-page entry.

## Editorial rules

- Lead with the person and something a visitor can experience. Connect the software, research, music, and art through the actual work.
- Give each featured project a concrete description and an obvious first action. Lead with Pine Gap's playable experience and actual gameplay capture. Name setup requirements when they affect that action: Pine Gap's free agent is scripted; R.A.I.N.'s offline demo uses scripted dialogue; live models need configuration.
- Keep measured findings and gameplay media tied to reviewed commit permalinks. Project homepages and setup links follow the current default branch. A permalink identifies a stored artifact; it establishes the executed revision only if the run itself records that revision.
- Describe capabilities from current public source files. Distinguish an implementation, a prompt's intention, and a measured outcome.
- Use the evidence ladder in `experiments/README.md` for profile states. Always name synthetic, simulated, software, live-agent, or physical scope.
- Keep a project's own experiment verdict separate from the profile ladder. A local `PASSED` or `SUPPORTED` result applies to its registered criteria; it does not establish external or physical validation.
- Same-seed reruns by the same project do not establish independent replication under the profile's `REPRODUCED` definition.
- Keep failures visible with their sources, even when later work addresses them. Never remove an earlier failed run to improve the story.
- Take timelines from Git history. A first upload records when work entered Git; it may omit earlier work.
- Do not invent performance, clinical, safety, novelty, or institutional claims.
- Link to public projects. Keep contact information to the publicly listed collaboration address.
- Preserve the artist's voice, the invitation to contribute, and the distinction between Christopher's portfolio and the lab.
- No statistics cards, skill bars, animated widgets, or decorative badges. Native headings and links must carry the complete page without images.
- Keep the front page readable on a phone. Use vertically stacked project sections; wide comparisons belong in the evidence documents.

The September 2026 refreshes supersede `docs/superpowers/`, which remains a historical planning record. Sponsorship configuration belongs in `.github/FUNDING.yml`.

## Visual assets

SVGs are self-contained: native text and vector paths, no scripts, remote fonts, embedded images, or animation. Light and dark variants use a `<picture>` element with a light fallback. Everything they communicate must also exist as ordinary text.

- `nea-onnim-*.svg` — the profile banner. Preserve the drawing and the name of the Adinkra symbol *Nea Onnim No Sua A, Ohu*, an Akan symbol of knowledge and lifelong learning. Its geometry is mirror-symmetric on a 13 × 13 grid of 12 px cells. Keep the traditional form without distortion or decoration.
- `constellations-*.svg` — the September 27 project map, now in `docs/project-map.md`. The caption names the snapshot date and additions absent from the illustration. Rings indicate shared typed judgment; the dashed connection indicates IONS-X reuse in CIRCLE.
- `latency-*.svg` — the September 27 timeline snapshot, displayed in `experiments/unreasonably-fast.md`. Keep its date and scope explicit; update both variants and the source ledger together for a new snapshot.

The Pine Gap image in `README.md` is the project's actual `docs/media/screens/driving.jpg` capture, referenced at a reviewed commit. It shows the coffee mission and Indigo People on the radio. Keep it static, linked to the playable world, with descriptive alt text and a visible caption. The screenshot is about 94 KB; do not replace it with an autoplay GIF or a generated depiction of gameplay.

| Role | Light | Dark |
| --- | --- | --- |
| Background | `#F4F7F4` | `#091A1D` |
| Rule | `#CDDCDA` | `#234044` |
| Ink | `#12383C` | `#E8F2ED` |
| Muted | `#476B6E` | `#ADC7C3` |
| Accent | `#0B5D63` | `#8BD5CC` |
| Warm | `#A0522D` | `#E8A87C` |
| Grid | `#E3ECE9` | `#10292C` |

## Updating evidence

1. Update the relevant `ledger.json` entry with a source and `last_reviewed` date. The top-level review date is the latest partial review; it does not imply every project was rechecked.
2. Mirror changed states in `experiments/README.md`. Update front-page findings only when their exact source supports the change.
3. Keep recorded timelines intact unless Git history justifies a correction. Leave unreconstructed histories labelled.
4. Add newly discarded approaches to the project map and choose a few useful findings for the front page.

## Before publishing

1. Check changed public repository and evidence links against their destinations. Pin quoted findings and media to reviewed revisions; use default-branch links for current setup and source navigation. Most projects use `main`; `research` uses `master`.
2. Render the README in light and dark modes at desktop and phone widths. Check layout, heading order, readable links, and missing images.
3. Validate SVG XML and accessible title/description text.
4. Parse `experiments/ledger.json` and compare the displayed states with it.
5. Check relative file links and heading anchors across the documentation.
6. Run `git diff --check` and review the complete diff.
