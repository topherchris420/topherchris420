# The ledger

Where each Vers3Dynamics experiment stands, what moved it there, and what would move it further.

The profile [README](../README.md) is the map. This folder is the record behind it:

| File | What it holds |
| --- | --- |
| [`ledger.json`](ledger.json) | Machine-readable state, timeline, and sources for each experiment. The source of truth for everything below. |
| [`unreasonably-fast.md`](unreasonably-fast.md) | How long each step took, from Git history, and what AI did and did not shorten. |
| [`impossible-six-months-ago.md`](impossible-six-months-ago.md) | Capabilities that recently became attemptable for one person, and what each still cannot tell us. |
| [`archive.md`](archive.md) | The archived repositories, read as strata. |

## The evidence ladder

| State | Means |
| --- | --- |
| `CONCEIVED` | Stated precisely, with at least one prediction or success condition. Not yet running. |
| `BUILDING` | Code or hardware design exists. Not yet runnable end to end by someone else. |
| `EXECUTABLE` | Someone else can run it from the repository. |
| `OBSERVED` | It produced a recorded result under stated conditions. The scope — synthetic, simulated, or physical — is always named. |
| `REPRODUCED` | The result was regenerated independently: another person, another dataset, or another instrument. |
| `SUPPORTED` | The claim survived a test stated in advance, against external or physical evidence. |
| `NOT SUPPORTED` | The claim failed a test stated in advance. It stays on the record. |

Three rules keep the ladder honest:

1. **Name the scope.** `OBSERVED` on a synthetic system and `OBSERVED` on a person are different results. The scope is part of the state.
2. **One experiment can hold two states.** A simulation can be `OBSERVED` while the hardware it models is still `BUILDING`.
3. **Nothing climbs by being deployed.** A live demo, a passing CI run, or a polished interface does not move an experiment up a rung.

## Where things stand

Initial snapshot: 27 September 2026. A partial review on 30 September refreshed R.A.I.N. and Pine Gap's recorded outcomes and rechecked the DRR, CIRCLE, Lop Nur, Mannahatta, and Vanta descriptions. See each entry's `last_reviewed` in `ledger.json`; remaining entries retain the initial snapshot.

| Experiment | Question | State | What would move it |
| --- | --- | --- | --- |
| [R.A.I.N. Lab](https://github.com/topherchris420/james_library) | confidence | `EXECUTABLE` · `OBSERVED` (seeded citation checks and simulated controls; same-seed reruns) | measured accuracy of real models behind the decision gate |
| [Pordenone](https://github.com/topherchris420/resonate-ai-mesh) | confidence | `EXECUTABLE` (telemetry simulated) | a recorded session on live inputs |
| [Anna](https://github.com/topherchris420/anna) | confidence | `EXECUTABLE` | a retrieval evaluation on a stated corpus |
| [Embedded AI Validation](https://github.com/topherchris420/embedded-ai-validation-platform) | confidence | `EXECUTABLE` (simulated targets) | a run on a physical board, with measured power |
| [Dynamic Resonance Rooting](https://github.com/topherchris420/dynamic-resonance-rooting) | signals | `OBSERVED` (synthetic) · `NOT SUPPORTED` (preregistered external test) | an external comparison that holds its false-alarm tolerance |
| [CIRCLE](https://github.com/topherchris420/circle) | signals | `OBSERVED` (simulated twin) · hardware `BUILDING` | review gates closed, a fabricated board, a bench measurement |
| [IONS-X](https://github.com/topherchris420/ions-x-deep-emergence-lab) | signals | `OBSERVED` (synthetic field) | the paired-control design applied to recorded data |
| [Pine Gap](https://github.com/topherchris420/satellite-vision-scape) | worlds | `EXECUTABLE` · `OBSERVED` (one complete live Jev run and paired scripted episodes) | repeated live-model runs against scripted baselines, with a success rate |
| [Lop Nur Twin](https://github.com/topherchris420/lop-nur-twin) | worlds | `EXECUTABLE` | — a public-source twin records sources; it cannot confirm a site |
| [Mannahatta](https://github.com/topherchris420/cognisync-terrain-weaver) | worlds | `EXECUTABLE` | routed storms compared against a recorded flood |
| [Orpheus](https://github.com/topherchris420/orpheus-resonance-protocol) | worlds | `EXECUTABLE` (interface prototype) | — |
| [Dynamic Location Theory](https://github.com/topherchris420/research) | measurement | `CONCEIVED` (predictions untested) | an interferometry measurement that could reject it |
| [Woodyard model workstation](https://github.com/topherchris420/waveform-shift-quantum) | measurement | `EXECUTABLE` (simulation) | its stated falsification bound applied to published measurements |
| [hello_os](https://github.com/topherchris420/ideas) | measurement | `EXECUTABLE` (toy model) | — |
| [Project 33](https://github.com/topherchris420/33) | measurement | `BUILDING` (bench prototype; no flight claimed) | the first physical evidence artifact |

No entry currently meets this profile's independent `REPRODUCED` or external/physical `SUPPORTED` definition. R.A.I.N. records same-seed reruns as “reproduced,” and Pine Gap's scripted experiment reports predictions as “SUPPORTED” under its own criteria. Those are scoped project verdicts; the profile ladder keeps independent replication and external evidence distinct.

## Recent recorded outcomes

- **R.A.I.N.** Exact-span citation checking passed its seeded corpus checks; typography normalization failed. A separate CIRCLE control experiment passed on simulated data. Original runs, same-seed reruns, measurements, criteria, and limits are in [RESULTS.md](https://github.com/topherchris420/james_library/blob/main/RESULTS.md).
- **Pine Gap.** Ten paired runs per scripted control-size condition: graded turns and taps locked all four terminals in every run; long holds locked none. [Report and raw traces](https://github.com/topherchris420/satellite-vision-scape/blob/main/experiments/results/tuning-control-magnitude/report.md). This tests a control-size effect; repeated live Jev performance remains open.

## Updating

1. Change `ledger.json` first, with the source that justifies the new state.
2. Mirror the change in the table above and, if the experiment appears there, in the profile README.
3. Never promote a state because of a deployment, a demo, or a passing build. Demote freely.
4. When a claim fails, add it to [“What didn’t survive contact”](../docs/project-map.md#what-didnt-survive-contact). Do not delete the entry when the work moves on.
