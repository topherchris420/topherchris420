# Profile maintenance

This repository is Christopher Woodyard's GitHub profile. The README is the front door: someone should be able to understand the practice, choose something to try, and find the record behind it in about a minute.

## Structure

| Layer | File | Job |
| --- | --- | --- |
| Front door | `README.md` | Person, philosophy, five entry points spanning research, governed agents, signals, worlds, and authorship; recorded findings and invitation |
| Project map | `docs/project-map.md` | Five questions, the wider project catalog, discarded approaches |
| Ledger | `experiments/README.md`, `experiments/ledger.json` | Scoped experiment states and source records; JSON is the source of truth |
| Build history | `experiments/unreasonably-fast.md` | Git-dated timelines and what AI did or did not shorten |
| Feasibility | `experiments/impossible-six-months-ago.md` | What recently became attemptable and what it still cannot tell us |
| Archive | `experiments/archive.md` | Earlier repositories and their recorded connections |
| Check | `tools/check_profile.py`, `.github/workflows/check.yml` | Compares every page with the ledger on each push: states, question labels, links, anchors, figures |

The front page is curated. Add a project there when it gives a visitor a distinct, useful way into the practice. Put the wider catalog in the project map under the question it serves. A new repository does not automatically need a new front-page entry.

## Editorial rules

- Lead with the person and something a visitor can experience. Connect the software, research, music, and art through the actual work.
- Give each featured project a concrete description and an obvious first action. Lead with the research philosophy and distinct ways in while keeping Pine Gap's playable experience and actual gameplay capture. The canonical R.A.I.N. Lab is `topherchris420/lop-nur-twin` (the previous `james_library` runtime was integrated on 6 October 2026). Keep links to `james_library` only as clearly marked historical evidence. Name setup requirements: Pine Gap's free agent is scripted; R.A.I.N.'s integrated offline meetings are scripted; the experimental autonomous researcher runs locally with a configured model.
- Keep measured findings and gameplay media tied to reviewed commit permalinks. Project homepages and setup links follow the current default branch. A permalink identifies a stored artifact; it establishes the executed revision only if the run itself records that revision.
- Describe capabilities from current public source files. Distinguish an implementation, a prompt's intention, and a measured outcome.
- Use the evidence ladder in `experiments/README.md` for profile states. Always name synthetic, simulated, software, live-agent, or physical scope.
- Give each featured project a ladder line and put `<!-- ledger:ID -->` on the line before it. The check compares the backticked states on that line with the entry in `ledger.json`, so a project without a ledger entry cannot be featured.
- Keep a project's own experiment verdict separate from the profile ladder. A local `PASSED` or `SUPPORTED` result applies to its registered criteria; it does not establish external or physical validation.
- Same-seed reruns by the same project do not establish independent replication under the profile's `REPRODUCED` definition.
- Keep failures visible with their sources, even when later work addresses them. Never remove an earlier failed run to improve the story.
- Take timelines from Git history. A first upload records when work entered Git; it may omit earlier work.
- Do not invent performance, clinical, safety, novelty, or institutional claims.
- Link to public projects. Keep contact information to the publicly listed collaboration address.
- Preserve the artist's voice, the invitation to contribute, and the distinction between Christopher's portfolio and the lab.
- No statistics cards, skill bars, animated widgets, or decorative badges. Native headings and links must carry the complete page without images.
- Keep the front page readable on a phone. Use vertically stacked project sections; wide comparisons belong in the evidence documents.

The September 2026 refreshes supersede `docs/superpowers/`, which remains a historical planning record with its own [note](superpowers/README.md). Sponsorship configuration belongs in `.github/FUNDING.yml`.

## Visual assets

SVGs are self-contained: native text and vector paths, no scripts, remote fonts, embedded images, or animation. Light and dark variants use a `<picture>` element with a light fallback. Everything they communicate must also exist as ordinary text.

- `nea-onnim-*.svg` — the profile banner. Preserve the drawing and the name of the Adinkra symbol *Nea Onnim No Sua A, Ohu*, an Akan symbol of knowledge and lifelong learning. Its geometry is mirror-symmetric on a 13 × 13 grid of 12 px cells. Keep the traditional form without distortion or decoration.
- `constellations-*.svg` — the September 27 project map, now in `docs/project-map.md`. The caption names the snapshot date and additions absent from the illustration. Rings indicate shared typed judgment; the dashed connection indicates IONS-X reuse in CIRCLE.
- `latency-*.svg` — the September 27 timeline snapshot, displayed in `experiments/unreasonably-fast.md`. Keep its date and scope explicit; update both variants and the source ledger together for a new snapshot.

The Pine Gap image in `README.md` is the project's actual `docs/media/screens/driving.jpg` capture, referenced at a reviewed commit. It shows the coffee mission and Indigo People on the radio. Keep it static, linked to the playable world, with descriptive alt text and a visible caption. The screenshot is about 94 KB; do not replace it with an autoplay GIF or a generated depiction of gameplay.

The R.A.I.N. and Bethesda screenshots are genuine project captures in [`lop-nur-twin`](https://github.com/topherchris420/lop-nur-twin), pinned to revision `f1dfe3f880c071f98836ab46edcce6f92641b613` so media changes cannot silently rewrite what was shown. The profile uses `docs/screenshots/rain-lab-meeting.png`, `docs/screenshots/rain-lab-record.png`, `docs/screenshots/bethesda-street.png`, and `docs/screenshot-lens.png`. Captions explicitly distinguish scripted meetings, simulation records, and reconstructed geography from live-model or real-world validation. These external media paths should be checked against their source repository whenever the capture is refreshed.

No GIFs were available among the R.A.I.N. repository's media at its original review. The wider profile now includes two existing animations, linked to their own repositories: Pine Gap's `docs/media/agent-drive.gif` is a replay of a recorded **scripted baseline**, not a live Jev run; CIRCLE's `diagrams/circle-3d-animation.gif` is an **intended hardware geometry visualization**, not footage of fabricated hardware. Do not confuse either with new scientific validation. Keep animations compact, link an MP4 alternative when possible, preserve captions describing provenance, and do not synthesize apparent recordings of events that did not happen.

| Role | Light | Dark |
| --- | --- | --- |
| Background | `#F4F7F4` | `#091A1D` |
| Rule | `#CDDCDA` | `#234044` |
| Ink | `#12383C` | `#E8F2ED` |
| Muted | `#476B6E` | `#ADC7C3` |
| Accent | `#0B5D63` | `#8BD5CC` |
| Warm | `#A0522D` | `#E8A87C` |
| Grid | `#E3ECE9` | `#10292C` |


The October 2026 multi-project media pass also pins the source revisions used for each visual; update the image link, evidence caption and (when needed) the ledger independently:

| Linked project | Illustrated artifact | Pinned revision |
| --- | --- | --- |
| Pordenone / Resonate AI Mesh | Research cockpit replay screenshot | `f90f0f732516` |
| Dynamic Resonance Rooting | Project research flier (not experimental proof) | `862c4f75e609` |
| CIRCLE | Simulated physiology plot and geometry-concept GIF | `774ddf8750db` |
| Pine Gap | Scripted-agent replay GIF and smaller MP4 alternative | `345760768049` |
| rain-pipeline | V3D-EXP-0003 figure (held-out, no improvement shown) | `d85ec37f80e7` |
| Vanta | Impasto portrait painting | `120c6c4d3635` |

Where a repository has no committed interface captures (for example HumanTouch on Hugging Face or the Studio UI at this review), prefer a direct link over a generic screenshot, mockup or unrelated image. The GitHub profile checker validates relative links and local vector assets but **does not verify that cross-repository images resolve**. Re-check pinned external media links when refreshing them.

## Updating evidence

1. Update the relevant `ledger.json` entry with a source and `last_reviewed` date. The top-level review date is the latest partial review; it does not imply every project was rechecked.
2. Mirror changed states in `experiments/README.md` and on the front page's ladder lines. Update front-page findings only when their exact source supports the change.
3. Run `python3 tools/check_profile.py`. It fails when any page disagrees with the ledger.
4. Keep recorded timelines intact unless Git history justifies a correction. Leave unreconstructed histories labelled. The check verifies that each milestone's day count matches its date.
5. Add newly discarded approaches to the project map and choose a few useful findings for the front page.

## Before publishing

1. Run `python3 tools/check_profile.py`. It parses the ledger, compares every displayed state with it, resolves relative links and heading anchors, and validates the SVG assets. Add `--external` to also confirm that outside links answer. The same check runs in GitHub Actions on every push.
2. Check changed public repository and evidence links against their destinations. Pin quoted findings and media to reviewed revisions; use default-branch links for current setup and source navigation. Most projects use `main`; `research` uses `master`; HumanTouch lives on Hugging Face Spaces.
3. Render the README in light and dark modes at desktop and phone widths. Check layout, heading order, readable links, and missing images.
4. Run `git diff --check` and review the complete diff.
