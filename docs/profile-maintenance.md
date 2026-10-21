# Profile maintenance

This repository is Christopher Woodyard's GitHub profile. The README is the entrance to the laboratory, not the laboratory notebook: within ten seconds a visitor should know who Christopher is, what he builds, and what they can try right now, and within a minute they should be holding something to explore.

## Structure

| Layer | File | Job |
| --- | --- | --- |
| Front door | `README.md` | Entrance banner, a short introduction, six doors, six rooms of exhibits, how the work connects, the evidence, the atlas, the art, and an invitation |
| Atlas data | `docs/atlas.json` | Every public repository plus public sites of private projects: theme, one-sentence description, what a visitor can do, maturity, links. Source of truth for the atlas |
| Atlas page | `docs/atlas.md` | Generated from `atlas.json` by `tools/build_atlas.py`, together with the README's atlas block |
| Research map | `docs/project-map.md` | The five research questions, the wider catalog by question, and what didn't survive contact |
| Ledger | `experiments/README.md`, `experiments/ledger.json` | Scoped evidence states and source records; the JSON is the source of truth |
| Build history | `experiments/unreasonably-fast.md` | Git-dated timelines and what AI did or did not shorten |
| Feasibility | `experiments/impossible-six-months-ago.md` | What recently became attemptable and what it still cannot tell us |
| Archive | `experiments/archive.md` | Earlier repositories read as strata, including the ones no longer public |
| Reviews | `docs/portfolio-review.md` | The dated 13 October editorial review, kept as written |
| Checks | `tools/check_profile.py`, `.github/workflows/check.yml` | Run on every push: ledger, states on every page, links and anchors, pinned media, figures, private-repository links, atlas sync, image weight |
| Coverage | `.github/workflows/atlas.yml` | Weekly: compares the atlas with the owner's public repositories (`tools/build_atlas.py --discover`) |
| Illustrations | `tools/draw_assets.py`, `tools/svgkit.py`, `tools/glyphs.json` | Draw every SVG in `assets/`, light and dark, from one layout. `tools/extract_glyphs.py` refreshes the glyph cache; see `tools/FONTS.md` |
| Captures | `assets/captures/*.webp` | Genuine screenshots of live public sites, taken when a project's repository has no capture of its own |

`docs/superpowers/` is a superseded June 2026 plan kept as a record; nothing in it describes the current profile.

## The front page

1. **Entrance.** `assets/hero-*.svg`: the name, *I make strange things and test whether they work*, the Adinkra symbol *Nea Onnim No Sua A, Ohu*, and a cabinet of fifteen project drawers with one left open. Then two sentences of introduction, the statement *AI is getting better at answering questions. We're working on making it better at knowing which answers deserve to be trusted.*, and four links a visitor can try immediately.
2. **Six doors.** `assets/door-*.svg`, each linking to its room's heading: Play a world · Challenge an intelligent system · Hear the invisible · Explore a research lab · Use something practical · Discover the unusual. A plain-text row repeats them for phones and screen readers.
3. **Six rooms.** Each room has one to three full exhibits, sometimes a two-column pair of smaller ones, and an *Also in this room* list. Rooms are separated by `assets/rule-*.svg`.
4. **How the inventions connect.** `assets/chain-*.svg` and the table under it: Observation → Interpretation → Decision → Action → Measurement → Verification, with representative projects, the branch where uncertainty should stop action, and the loop back. The projects are separate systems; never present them as one architecture.
5. **What the evidence says**, **Every public project** (generated), **One practice, many forms**, **Join in**, **How I work** (its anchor is linked from `experiments/unreasonably-fast.md`), and the closing invitation.

### An exhibit

```text
### Name
**A plain-language question the project actually asks**
[real capture or labelled illustration, linked to the live experience]
Two or three sentences: what a visitor experiences and what the system does.
<sub>Caption: what the image shows, when it was captured, and its scope.</sub>
`MATURITY LABEL` · [**Primary action →**](live) · [Source](repo)
<details> Under the hood: what's distinctive · what was recorded · what failed · what isn't claimed
<!-- ledger:ID -->
Evidence ladder: `STATES` (scope).
</details>
```

Start with what is fascinating, then what the system does, then links to the method and evidence. Long methodology belongs in the project's own repository.

### Choosing what to feature

The exhibition is curated; the atlas is complete. A new public repository goes into `docs/atlas.json` first. Feature it only if it gives a visitor a distinct, honest way into the practice, has something real to show, and has been read closely enough to describe its boundaries. Prefer projects a visitor can try without installing anything.

## Editorial rules

- Lead with something a visitor can experience. Connect the software, research, music and art through the actual work, and let the projects be the protagonists.
- Describe capabilities from current public source files and live sites. Distinguish an implementation, a prompt's intention, a roadmap, and a measured outcome. Never upgrade a claim to make a sentence work.
- Name the scope of every result: synthetic, simulated, scripted, live-model, public-data, or physical. Keep each project's own boundaries in its copy:
  - Pine Gap and Lop Nur Twin are public-source reconstructions and fictional games, not operational information; keep weapons-related game content and Blacksite imagery out of the profile.
  - GHOSTWHEEL is simulation only; no real vehicle can be connected, and no vulnerability in any real vehicle is claimed.
  - Luca is for devices and networks the user owns or may assess; a match is evidence to investigate, not proof of compromise. Credit Kaspersky's TinyCheck as its base.
  - Project Ascent is not an appraisal or financial advice; its 9.98% median error applies only to the DC single-family and rowhouse configuration it validated.
  - CIRCLE is not cleared for fabrication or human connection. Sentinel and DNA Music Molecules measure nothing about the body.
  - Nocturne controls no lights; DC figures are model estimates.
  - Quantum Noise Profiler's hardware warning accuracy is not established.
  - TRIAD's selective-risk metric is established prior art; its blind comparators were written by an AI agent of the same model family. The NIST submission implies no endorsement.
- Credit other people's work. `james_library`'s Rust runtime descends from ZeroClaw; Luca derives from TinyCheck; Anna is built on the Anna's Archive codebase; forks name their upstream in the atlas.
- **Private source, public site.** When a repository is private but its site is public (DNA Music Molecules, Waveform), link the site, label it *source not public*, and never link the repository. Such a project gets no new ledger state: `EXECUTABLE` means someone else can run it from a repository. Repositories that become private go into `no_longer_public` in `docs/atlas.json`; the check then fails on any link to them.
- Link text names the project, not the host. Some Vercel hostnames are historical and do not describe the project.
- Do not link a live site that promotes material the profile should not (Anna's live index includes a shadow-library directory) or that shows an outdated build. Link the repository instead.
- Use the evidence ladder in `experiments/README.md`. Same-seed reruns and same-author repetitions are not `REPRODUCED`; a project's local *supported* or *passed* verdict on a simulation is not `SUPPORTED`. A pre-registered test against external or physical evidence that the claim survives is `SUPPORTED`, at the scope of that test.
- Keep failures visible with their sources, even when later work addresses them. Never remove an earlier failed run to improve the story. Add new ones to the research map's *What didn't survive contact* and choose a few for the front page.
- Take timelines from Git history. Do not invent performance, clinical, safety, novelty, affiliation, or institutional claims.
- Keep contact information to the publicly listed collaboration address. Preserve the artist's voice and the closing quotation.
- No statistics cards, skill bars, badge walls, or decorative animation. Native headings and links must carry the whole page without images.

## Images

**Real captures only.** Use a project's own committed screenshots or recordings, pinned to a 40-digit commit, or a capture of its live public site taken for this profile and stored in `assets/captures/` as WebP (≤ 400 KB; the check enforces it). Each caption says what the image shows and its scope; captures of live sites carry their date. Never use design mockups, generated "screenshots", AI-generated people, or third-party photographs of real sites. Credit basemap imagery (Mannahatta's Esri/Maxar basemap).

The current captures were taken on 21 October 2026 with headless Chromium at 1440 px and resized to 1200 px:

| File | Source | Shows |
| --- | --- | --- |
| `ghostwheel-refusal.webp` | ghostwheel-one.vercel.app | A replayed command refused after a short drive |
| `mannahatta-storm.webp` | phaseroot.vercel.app | The illustrative example after a sealed 50 mm storm |
| `dna-music-instrument.webp` | arpa-h.vercel.app | The instrument's opening screen |
| `drr-live-lab.webp` | dynamic-resonance-rooting.vercel.app | A planted edge recovered in the live lab |
| `sentinel-studio.webp` | hello-goodbye-iota.vercel.app | Sentinel's opening screen |
| `luca-synthetic-demo.webp` | luca-rho-five.vercel.app | The synthetic sample report |
| `project-33-page.webp` | topherchris420.github.io/33 | The project page |
| `waveform-workstation.webp` | waveform-teleportation.vercel.app | The workstation's opening screen |
| `nocturne-restoration-brief.webp` | `examples/restoration/report.html` at `90a98878`, opened offline | Its report on an invented district |
| `qnp-evidence-explorer.webp` | `docs/assets/evidence-explorer.png` at `192a8a03`, cropped | The ibm_fez pilot in the offline explorer |

Pinned media from other repositories:

| Project | Artifact | Revision |
| --- | --- | --- |
| Pine Gap | `docs/media/agent-drive.gif`, the scripted baseline at 10× (not an AI model) | `3457607680492edf4e4c9117859429846695f10c` |
| R.A.I.N. Lab | `docs/screenshots/rain-lab-meeting.png`, `rain-lab-record.png` (scripted; no model ran) | `f1dfe3f880c071f98836ab46edcce6f92641b613` |
| James | `docs/assets/james-conversation.png`, a real session with Gemma 3 4B | `465f58dda921a7de0575b50348cbc5b5ae43122b` |
| TRIAD | `results/milestone7-plots/bike-sharing.png`, a negative result | `917fc17338dffdc13f924c498c64aab493ad211a` |
| Project Ascent | `evidence/ascent-studio-preview.png`, the fictional sample home | `698e8fe8a345bf9a5522a0d8031a230775c14182` |
| Jasmine | `docs/images/test-real-model.png`, a small local model answering from a PDF | `b66dcbdca5df8b61a1b04993910663ac24a92df3` |
| CIRCLE | `diagrams/circle-3d-animation.gif` (concept render) and `diagrams/physiology-polygraph.png` (simulated physiology) | `774ddf8750dbe03fd207403d1b4bc428816f3967` |
| Vanta | `public/work/impasto-head.webp`, Christopher's painting | `120c6c4d36356fc7a7b5ffa3fc8729d1ecc0b069` |

Preserve the Pine Gap and CIRCLE animations: the author asked for their restoration on 13 October 2026. Keep their captions: the Pine Gap GIF is the scripted baseline, and the CIRCLE GIF is a concept render whose labels are not claims. The checker verifies that external media are pinned to a commit; it does not fetch them, so re-check pinned URLs when refreshing a capture.

## Illustrations

All SVGs are self-contained: vector paths only, no scripts, remote resources, embedded raster images or animation. Text is drawn as outlines from `tools/glyphs.json` (Fraunces for display, JetBrains Mono for labels, Inter for body text, all under the SIL Open Font License), so every visitor sees the same letterforms. Light and dark variants are paired in a `<picture>` element with the light version as the fallback, and everything an image says also appears in its alt text or in the page.

Edit the content tables in `tools/draw_assets.py` (`CABINET`, `DOORS`, `CHAIN`), then run `python3 tools/draw_assets.py` and update the README's alt text to match. `constellations-*.svg` (the September 27 map in `docs/project-map.md`) and `latency-*.svg` (the September 27 timeline in `experiments/unreasonably-fast.md`) are dated snapshots drawn earlier; keep their dates in their captions.

| Role | Light | Dark |
| --- | --- | --- |
| Background | `#F4F7F4` | `#091A1D` |
| Panel | `#FBFCFA` | `#0D2226` |
| Rule | `#CDDCDA` | `#234044` |
| Ink | `#12383C` | `#E8F2ED` |
| Muted | `#476B6E` | `#ADC7C3` |
| Accent (deep spectral teal) | `#0B5D63` | `#8BD5CC` |
| Warm (a person decides) | `#A0522D` | `#E8A87C` |

## Adding a public repository

1. Read its README and source. Write one entry in `docs/atlas.json`: one sentence on what is implemented, a short *what you can do*, a maturity label from the atlas legend, and its live URL if one works.
2. Run `python3 tools/build_atlas.py`, then `python3 tools/check_profile.py`.
3. If it makes claims worth tracking, add a ledger entry, a row in `experiments/README.md`, and a line in `docs/project-map.md`.
4. Feature it on the front page only by editorial decision, and then also add it to `CABINET` or `DOORS` if it changes what those show.

## Updating evidence

1. Update the entry in `ledger.json` with the source that justifies the state and a `last_reviewed` date. The top-level `reviewed` date equals the latest `last_reviewed`.
2. Mirror changed states in `experiments/README.md` and on the front page's ladder lines. If an entry reaches or loses `SUPPORTED` or `REPRODUCED`, update the front page's **so far** lines; the check names any entry they leave out.
3. Never promote a state because of a deployment, a demo, or a passing build. Demote freely, and say why in the ledger.
4. Add newly discarded approaches to the research map.

## Before publishing

1. Run `python3 tools/check_profile.py`. Add `--external` to confirm that outside links answer; Bandcamp and Ko-fi refuse automated clients and are listed for a check by hand.
2. Render the README in light and dark modes at desktop and phone widths: check the door grid, the two-column pairs, every image, heading order and anchor links.
3. Run `git diff --check` and review the complete diff.
