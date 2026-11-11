# Add another pair of eyes

This repository is the public entrance to Christopher Woodyard's Vers3Dynamics lab. Good contributions make a project easier to try, a claim easier to check, or an error easier to see.

For a scientific reproduction, use the relevant project's issue tracker. Include the source revision, environment, inputs or data provenance, command, expected result, actual result, and the original output files. A disagreement with a published result is useful evidence.

For this profile, report a broken link, an inaccessible interaction, an outdated description, or a claim whose scope is unclear. Name the page and point to the source that would correct it.

## Work locally

Use Python 3.11 or 3.12 and Node 24.15+. The Python generators use only the standard library. The Observatory itself needs only a browser; JSDOM is a development dependency for testing its interactions.

```sh
python3 tools/build_atlas.py
python3 tools/build_observatory.py
npm ci --ignore-scripts --no-audit --no-fund
npm test
python3 -m unittest discover -s tests -v
python3 tools/check_profile.py
python3 tools/build_observatory.py --check
node --check tools/observatory.js
git diff --check
```

Node is only needed for development checks. Open `docs/observatory.html` directly for an offline preview. The [research index](docs/research.md) is the readable Markdown edition. The DOM tests cover filtering, comparison, URL restoration, exports, printing and the no-JavaScript reading edition; they do not substitute for visual layout checks.

## Change the source of truth

| Change | Edit |
| --- | --- |
| Project description, theme, link or visibility | `docs/atlas.json` |
| Recorded evidence, scope, source or next experiment | `experiments/ledger.json`, then its manually curated ledger table and exhibition markers |
| Observatory layout and behavior | `tools/observatory.html`, `tools/observatory.css`, `tools/observatory.js` |
| Narrative, invitations or featured work | `README.md` and `docs/exhibition.md` |

Run the generators after edits. Commit their outputs together with the inputs. CI checks that the HTML, Markdown and SHA-256 manifest match exactly. The manifest identifies bytes; it does not establish scientific truth.

Review dates belong to the records actually inspected. A link correction or interface change does not refresh every experiment. Preserve failed results and name the exact conditions of every claim. Catalog maturity, successful execution, independent reproduction and external support are different things.

## Check the experience

Try light and dark modes at phone and desktop widths. Search for a project and for text inside a limitation. Filter `SUPPORTED` and `NOT SUPPORTED` separately; the same project may belong to both. Select three projects, change filters, reload the URL, export the results, and print the comparison. Follow an archived project's permalink. With JavaScript disabled, all records and source links should remain readable.

Network checks are explicit:

```sh
python3 tools/build_atlas.py --discover
python3 tools/check_profile.py --external
```

See [profile maintenance](docs/profile-maintenance.md) for image provenance, editorial boundaries and the evidence definitions.
