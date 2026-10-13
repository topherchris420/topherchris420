# The ledger

Where each Vers3Dynamics experiment stands, what moved it there, and what would move it further.

The profile [README](../README.md) is the map. This folder is the record behind it:

| File | What it holds |
| --- | --- |
| [`ledger.json`](ledger.json) | Machine-readable state, timeline, and sources for each experiment. The source of truth for everything below. |
| [`unreasonably-fast.md`](unreasonably-fast.md) | How long each step took, from Git history, and what AI did and did not shorten. |
| [`impossible-six-months-ago.md`](impossible-six-months-ago.md) | Capabilities that recently became attemptable for one person, and what each still cannot tell us. |
| [`archive.md`](archive.md) | The archived repositories, read as strata. |
| [`tools/check_profile.py`](../tools/check_profile.py) | The check that runs on every push: this file against the table below, the front page's ladder lines, the project map, every internal link, and every figure. |

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

**Current R.A.I.N. Lab:** [Lop Nur Twin](https://github.com/topherchris420/lop-nur-twin). The R.A.I.N. row below is intentionally linked to `james_library` because this ledger records historical experiments performed before the [October 6 runtime migration](https://github.com/topherchris420/lop-nur-twin/blob/main/docs/RAIN_MIGRATION.md). It does not identify the current development repository or certify the newer autonomous researcher.

Initial snapshot: 27 September 2026. A partial review on 30 September refreshed R.A.I.N. and Pine Gap's recorded outcomes and rechecked the DRR, CIRCLE, Lop Nur, Mannahatta, and Vanta descriptions. A review on 4 October added HumanTouch from its public source files and put this table under the automated check. A review on 12 October added James and TRIAD. The 13 October portfolio review added Quantum Noise Profiler and refreshed the current R.A.I.N., Mannahatta, James, and Pine Gap records. The historical R.A.I.N. row remains separate from the integrated lab's simulator observations. See each entry's `last_reviewed` in `ledger.json`; other entries retain their earlier review dates.

| Experiment | Question | State | What would move it |
| --- | --- | --- | --- |
| [R.A.I.N. historical tests](https://github.com/topherchris420/james_library) | confidence | `EXECUTABLE` · `OBSERVED` (seeded citation checks and simulated controls; same-seed reruns) | measured accuracy of real models behind the decision gate |
| [Pordenone](https://github.com/topherchris420/resonate-ai-mesh) | confidence | `EXECUTABLE` (telemetry simulated) | a recorded session on live inputs |
| [James](https://github.com/topherchris420/james) | confidence | `EXECUTABLE` (desktop preview; real-model Linux-container workflows and platform CI) | real-device acceptance scenarios and end-user release gates |
| [Anna](https://github.com/topherchris420/anna) | confidence | `EXECUTABLE` | a retrieval evaluation on a stated corpus |
| [Embedded AI Validation](https://github.com/topherchris420/embedded-ai-validation-platform) | confidence | `EXECUTABLE` (simulated targets) | a run on a physical board, with measured power |
| [Dynamic Resonance Rooting](https://github.com/topherchris420/dynamic-resonance-rooting) | signals | `OBSERVED` (synthetic) · `NOT SUPPORTED` (preregistered external test) | an external comparison that holds its false-alarm tolerance |
| [CIRCLE](https://github.com/topherchris420/circle) | signals | `OBSERVED` (simulated twin) · hardware `BUILDING` | review gates closed, a fabricated board, a bench measurement |
| [IONS-X](https://github.com/topherchris420/ions-x-deep-emergence-lab) | signals | `OBSERVED` (synthetic field) | the paired-control design applied to recorded data |
| [Pine Gap](https://github.com/topherchris420/satellite-vision-scape) | worlds | `EXECUTABLE` · `OBSERVED` (live Jev case studies and paired scripted episodes) | repeated live-model runs against scripted baselines, with a success rate |
| [Lop Nur Twin / current R.A.I.N. Lab](https://github.com/topherchris420/lop-nur-twin) | worlds | `EXECUTABLE` · `OBSERVED` (scripted and live-model-designed simulator experiments; no physical validation) | a new frozen numerical investigation meeting its analytic guards; repeated model-designed studies against baselines |
| [Mannahatta](https://github.com/topherchris420/cognisync-terrain-weaver) | worlds | `EXECUTABLE` · `OBSERVED` (model/public-data comparisons) · `NOT SUPPORTED` (holdout flood-report test) | a repaired model beating low elevation on a new frozen holdout |
| [Orpheus](https://github.com/topherchris420/orpheus-resonance-protocol) | worlds | `EXECUTABLE` (interface prototype) | — |
| [TRIAD](https://github.com/topherchris420/triad) | measurement | `EXECUTABLE` · `OBSERVED` (simulated sensor; frozen models on public datasets) · `NOT SUPPORTED` (pre-registered test against blind comparators) | a repaired rule set that wins a new frozen test its authors have not seen, judged by an unrelated team |
| [Quantum Noise Profiler](https://github.com/topherchris420/quantum-noise-profiler) | measurement | `EXECUTABLE` · `OBSERVED` (preregistered simulations; no quantum-hardware results) | independent replication and separately scoped, authorized hardware validation |
| [Dynamic Location Theory](https://github.com/topherchris420/research) | measurement | `CONCEIVED` (predictions untested) · `EXECUTABLE` (simulation prototype; not evidence) | an interferometry measurement that could reject it |
| [Woodyard model workstation](https://github.com/topherchris420/waveform-shift-quantum) | measurement | `EXECUTABLE` (simulation) | its stated falsification bound applied to published measurements |
| [hello_os](https://github.com/topherchris420/ideas) | measurement | `EXECUTABLE` (toy model) | — |
| [Project 33](https://github.com/topherchris420/33) | measurement | `BUILDING` (bench prototype; no flight claimed) | the first physical evidence artifact |
| [HumanTouch](https://huggingface.co/spaces/ciaochris/HumanTouch) | sound | `EXECUTABLE` · `OBSERVED` (offline calibration of its measurement instruments on synthetic fixtures; no model) | a live ablation published with its model, date, and per-case results |
| [Vers3Dynamics Studio](https://github.com/topherchris420/quantum-spin-sound) | sound | `EXECUTABLE` (live-coding instrument) | — |
| [Vanta](https://github.com/topherchris420/vanta) | sound | `EXECUTABLE` (portfolio and research atlas) | — |

No entry currently meets this profile's independent `REPRODUCED` or external/physical `SUPPORTED` definition. R.A.I.N. records same-seed reruns as “reproduced,” and Pine Gap's scripted experiment reports predictions as “SUPPORTED” under its own criteria. TRIAD describes Milestone 7 as replicating Milestone 6, and Milestone 8 as replicating Milestone 7's advantage over standard checks; those are same-author repetitions on new datasets. Those are scoped project verdicts; the profile ladder keeps independent replication and external evidence distinct.

## Recent recorded outcomes

- **TRIAD, Milestone 8.** A pre-registered test of whether TRIAD's claim-relative evidence rules beat reviewers written without seeing them, on 5,078 reliability claims from five public UCI datasets new to TRIAD, with truth computed from held-out outcomes. The protocol, case generator and both comparators were committed before any case existed. TRIAD's decision cost was 0.159; a blind statistical reviewer's was 0.121 (Δ +0.038, 95% interval +0.008 to +0.070), a blind REFORMS-style checklist's 0.160, and never endorsing any claim 0.125. Verdict: **not established**. The comparators were written by an AI agent of the same model family from a brief alone, and nothing has been adjudicated by a person. [Results](https://github.com/topherchris420/triad/blob/7be64c8c93f2ef3238ac18b386aa5bb81c214bbb/docs/metrology/milestone8-results.md) · [score](https://github.com/topherchris420/triad/blob/7be64c8c93f2ef3238ac18b386aa5bb81c214bbb/results/evidence-outcomes-v8/score/report.md).
- **TRIAD, real data.** On UCI Bike Sharing with frozen models, TRIAD's evidence-qualified day decisions cost slightly more than standard monitoring at a matched budget: +0.0049 per hour for ridge and +0.0062 for gradient boosting. That repeats the negative direction of Milestone 6 on OpenML Electricity. [Milestone 7 results](https://github.com/topherchris420/triad/blob/7be64c8c93f2ef3238ac18b386aa5bb81c214bbb/docs/metrology/milestone7-results.md).
- **James, first real-model session.** A llama.cpp-based server on the same machine served Qwen2.5 models to the desktop app under a virtual display. The 3B model's unedited replies became the README screenshot. In the same session a 0.5B model answered "Yes" when asked whether a simulator finding is real-world evidence, and a 1.5B model once claimed that *it* retains authority over its actions; a 90-second read timeout also cut off a slow reply. One observed session, not a benchmark. [Validation record](https://github.com/topherchris420/james/blob/31cdff1822b2026a916cb582d7be97afc7037d2f/docs/VALIDATION.md#readme-screenshot-session-2026-10-11).
- **R.A.I.N. (historical `james_library` source).** Exact-span citation checking passed its seeded corpus checks; typography normalization failed. A separate CIRCLE control experiment passed on simulated data. Original runs, same-seed reruns, measurements, criteria, and limits are in [RESULTS.md](https://github.com/topherchris420/james_library/blob/9c8811e343d21b8c143055f9cf549abdefa862f1/RESULTS.md).
- **Pine Gap, live Jev.** One [recorded session](https://github.com/topherchris420/satellite-vision-scape/blob/bff1f8095739d925a9e0bc13e3a6566cf2363d04/docs/traces/jev-after-hours-live-2026-09-27.json) completed After Hours in 457.82 seconds (7m 38s rounded), with zero human interventions. This is one completed run, not a repeated-run success rate or a human comparison. The pinned commit preserves the stored trace; it does not identify the executed code, whose build field is `development`.
- **Pine Gap, scripted controls.** Ten paired runs per scripted control-size condition: graded turns and taps locked all four terminals in every run; long holds locked none. [Report and raw traces](https://github.com/topherchris420/satellite-vision-scape/blob/bff1f8095739d925a9e0bc13e3a6566cf2363d04/experiments/results/tuning-control-magnitude/report.md). This tests a control-size effect; repeated live Jev performance remains open.
- **HumanTouch, instruments.** The offline evaluation runs 13 synthetic fixtures through the measurement code with no model. In the stored results file, timestamped 3 October 2026, hand-written faithful revisions score an unnecessary-change rate of 0.000 and over-edited ones 0.668, with the other metrics separating the same way; the Space's README quotes an earlier run. This calibrates the instruments. It says nothing about what a live model does. [Results file](https://huggingface.co/spaces/ciaochris/HumanTouch/blob/main/evals/results/offline.md) · [method](https://huggingface.co/spaces/ciaochris/HumanTouch/blob/main/README.md#evaluation).

## Updating

1. Change `ledger.json` first, with the source that justifies the new state.
2. Mirror the change in the table above and, if the experiment appears there, in the profile README.
3. Run `python3 ../tools/check_profile.py` from this folder, or `python3 tools/check_profile.py` from the repository root. It fails when this table, the front page, or the project map disagrees with `ledger.json`.
4. Never promote a state because of a deployment, a demo, or a passing build. Demote freely.
5. When a claim fails, add it to [“What didn’t survive contact”](../docs/project-map.md#what-didnt-survive-contact). Do not delete the entry when the work moves on.
