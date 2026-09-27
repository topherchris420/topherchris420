# Unreasonably Fast

A public record of idea-to-reality latency: how long each step took, what AI shortened, and what it did not.

**How the dates were established.** Every date below is a Git author date on the repository's default branch, and every interval is counted from that repository's first commit. Git records when work was committed, not when it was imagined, so these are not "idea to executable" times. Where a repository opens with an upload, earlier work happened off the record and the entry says so. Where no honest interval can be read from the history, the entry says *timeline not reconstructed* instead of guessing. The same data is in [`ledger.json`](ledger.json).

**How to read an entry.** *Compressed* lists work that AI tools made fast here; AI coding agents appear as commit authors in most of these repositories. *Not compressed* lists what no tool made faster. The second list is the one that decides what a project may claim.

---

## CIRCLE

**Question.** Can a closed-loop biosignal instrument be designed so that every claim it makes — measured, inferred, or acted on — is reviewable before anyone is connected to it?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2026-08-14 | [Safety basis](https://github.com/topherchris420/circle/commit/5fb038724297f33b4ef5c863e0e377e7667b56f3), reproducible schematic execution, machine-checkable interlocks |
| 3 | 2026-08-17 | [Rev B electronics engineering package](https://github.com/topherchris420/circle/commit/611723ddd09ed76b1ba9976cebc45c03e334bfce) |
| 42 | 2026-09-25 | [Physiology twin, signal pipeline, auditable closed loop](https://github.com/topherchris420/circle/commit/74fa8e5af08211d751d5ce43d3151ca5ce2b9319) |
| — | open | Fabrication; human connection |

**Compressed.** Schematics as code, safety contracts as tests, KiCad in CI, a seeded physiological twin with held-out scoring.
**Not compressed.** Fabrication. Electrical-safety and EMC review. Any measurement on a person.
**Evidence.** [Review gates](https://github.com/topherchris420/circle/blob/main/docs/review-gates.md) · [physiology pipeline](https://github.com/topherchris420/circle/blob/main/docs/physiology-pipeline.md)

The first three days fit the [72-hour question](../README.md#unreasonably-fast-deliberately-bounded). The answer the package gave was the useful kind: *not cleared for fabrication or human connection*.

## Pine Gap: After Hours

**Question.** Can an AI agent act inside a real-time 3D world through the same controls as a person, with every choice on the record — and what does one run actually prove?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2026-07-15 | 3D site viewer from an app-builder template |
| 72 | 2026-09-25 | [Playable third-person open world](https://github.com/topherchris420/satellite-vision-scape/commit/3863c121a8281309fc8927a9f0cca2712130fcf8) |
| 73 | 2026-09-26 | [After Hours mission and agent runtime](https://github.com/topherchris420/satellite-vision-scape/commit/f6d4a60237bdec8558b2b0a10f44c9c48348e074) |
| 74 | 2026-09-27 | [Agent runtime test suites](https://github.com/topherchris420/satellite-vision-scape/commit/3e7b4f06d31bb684411b3346dd314ca40e497fab) |
| — | open | A success rate |

**Compressed.** The world, the physics, the agent runtime, the trace format, the tests.
**Not compressed.** Knowing whether the agent is good at the task. The README says it directly: *one run is an existence proof, not a success rate.*
**Evidence.** [Agent runtime, contracts and limits](https://github.com/topherchris420/satellite-vision-scape/blob/main/docs/AGENT_RUNTIME.md)

## Dynamic Resonance Rooting

**Question.** Can rhythm, lag, and structural change in multivariate signals be detected with operators whose false-alarm rate is known?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2025-06-14 | [447-line framework module](https://github.com/topherchris420/dynamic-resonance-rooting/commit/1dafd59a953df139faaf79948a2123fef3e6a2c7) and tutorial notebook |
| 465 | 2026-09-22 | [Claim boundaries and the preregistered QBO comparison](https://github.com/topherchris420/dynamic-resonance-rooting/commit/bebd3512cadd0780d23b465cc1122d1fcf20be5c): **not supported** |
| 468 | 2026-09-25 | Surrogate calibration; depth made unit- and grid-invariant |

**Compressed.** The operators, a browser port checked for parity with the Python package to 1e-9, benchmark and reproduction scripts.
**Not compressed.** Choosing a fair external test, fixing it in advance, and accepting the answer.
**Evidence.** [External evidence](https://github.com/topherchris420/dynamic-resonance-rooting/blob/main/docs/external-evidence.md) · [validation report](https://github.com/topherchris420/dynamic-resonance-rooting/blob/main/DRR_VALIDATION_REPORT.md) · [benchmarks](https://github.com/topherchris420/dynamic-resonance-rooting/blob/main/DRR_BENCHMARKS.md)

The longest interval in this record, and the most informative. The framework went into Git on the first afternoon. A fair test took fifteen months.

## IONS-X

**Question.** Does a collective-sensing detector respond differently when the coupling it claims to find is absent?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2025-12-17 | [Simulation committed](https://github.com/topherchris420/ions-x-deep-emergence-lab/commit/90676553c1030e3d4307e8a4051d92892d81cf7a) |
| 281 | 2026-09-24 | [Paired coupled/uncoupled controls](https://github.com/topherchris420/ions-x-deep-emergence-lab/commit/9fddbba87100b41c9c4996cfe2fb96d1d05d0d85) |

**Compressed.** Simulation, rendering, packaging.
**Not compressed.** Deciding what the control should be. The engine existed for nine months before it could answer its own question.
**Evidence.** [Experiment design and limitations](https://github.com/topherchris420/ions-x-deep-emergence-lab/blob/main/docs/experiment-design.md)

## R.A.I.N. Lab

**Question.** Can a research assistant separate generation, evidence, judgment, and authorization, so that a model's confidence never becomes permission by itself?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2026-02-12 | Meeting launcher and agent SOUL files |
| 222 | 2026-09-22 | [Promotion gate: independent bounded evidence before a claim is promoted](https://github.com/topherchris420/james_library/commit/0c24982bf6b93443676a2f9864dee6a2b83c947d) |
| — | open | Real-model accuracy and speed behind the gate |

**Compressed.** Multi-agent orchestration, citation verification, replay tooling, documentation in six languages.
**Not compressed.** Measuring whether real models make good decisions.
**Evidence.** [Bounded decisions](https://github.com/topherchris420/james_library/blob/main/docs/bounded-decisions.md) · [typed judgment](https://github.com/topherchris420/james_library/blob/main/docs/typed-judgment.md)

The Rust runtime descends from ZeroClaw and carries its contributors' history; the dates here refer to the R.A.I.N. Lab research layer.

## Embedded AI Validation Platform

**Question.** Can the discipline of CI — baselines, regression gates, provenance — be applied to edge-AI firmware before it reaches a device?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2026-07-10 | Upload, then [v0.3.0](https://github.com/topherchris420/embedded-ai-validation-platform/commit/b45a541cd377d8e16b67adc430fb600100b59b1a) the same day: fusion filters, hardware-in-the-loop simulator, firmware for four boards, CI |
| — | open | Measured power on physical hardware |

**Compressed.** The plugin architecture, filters, fault injection, dashboard, tests.
**Not compressed.** Measurement on a physical board. The hardware power monitors are listed as planned.

## Project 33

**Question.** How much of a low-cost rocket testbed can be made reviewable before anything is built or flown?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2026-07-03 | Upload, then [raised into a verifiable engineering package](https://github.com/topherchris420/33/commit/22d7f4c4fbabf2ed53714644388f8636db9ab67b) with a deployed project page |
| — | open | The first physical evidence artifact |

**Compressed.** Firmware hardening, dashboard, evidence tooling, documentation.
**Not compressed.** Bench measurements, an assembled mechanism, any flight. The evidence catalog records zero physical artifacts.
**Evidence.** [Evidence Observatory](https://github.com/topherchris420/33/blob/main/docs/EVIDENCE_OBSERVATORY.md) · [paper alignment](https://github.com/topherchris420/33/blob/main/docs/PAPER_ALIGNMENT.md)

## Lop Nur Twin

**Question.** How far can public Earth-observation data be pushed into an explorable model while every building keeps its citation and confidence?

| Day | Date | Step |
| ---: | --- | --- |
| 0 | 2026-07-17 | [3D airfield twin](https://github.com/topherchris420/lop-nur-twin/commit/7cbff5a9adbe65d00286b40e52bea26904c18718) |
| 2 | 2026-07-19 | [Grounded in reproducible public evidence](https://github.com/topherchris420/lop-nur-twin/commit/4a90c4813826f4db35f1ff4fb969124765e51f67) |
| 19 | 2026-08-05 | [Evidence ledger, release manifest, accessible analysis view](https://github.com/topherchris420/lop-nur-twin/commit/c52bb8582e29c4c1abf80788cfa9ed7daf5c8ba9) |

**Compressed.** Geometry, rendering, the ledger, the comparison tooling.
**Not compressed.** Ground truth. A public-source reconstruction can record where every shape came from; it cannot confirm what is there.

## Location as resonance

**Question.** Can position be described as a property of a system's resonance rather than an external label — and what measurement would say no?

This line of work spans three repositories, so its intervals are counted in calendar dates rather than from one first commit.

| Date | Step |
| --- | --- |
| 2025-08-06 | [teleportation](https://github.com/topherchris420/teleportation) (archived): "vibrational variables as location" |
| 2026-01-16 | Preprint on Zenodo: [10.5281/zenodo.18263032](https://doi.org/10.5281/zenodo.18263032) |
| 2026-03-31 | [research](https://github.com/topherchris420/research): paper site and simulation prototype |
| 2026-08-10 | [Woodyard model workstation](https://github.com/topherchris420/waveform-shift-quantum) rebuilt as a falsification engine |
| open | An interferometry bound applied to the model |

**Compressed.** Simulation, visualization, typesetting, a workstation that compares the proposal with standard baselines.
**Not compressed.** Any measurement. The predictions concern atomic clocks and matter-wave interferometers; nothing on a laptop can settle them.

---

## Timeline not reconstructed yet

- **[Anna](https://github.com/topherchris420/anna)** — built on the Anna's Archive codebase, whose history starts in 2022.
- **[Mannahatta](https://github.com/topherchris420/cognisync-terrain-weaver)** — current history begins with an import of earlier work.
- **[Pordenone](https://github.com/topherchris420/resonate-ai-mesh)** — the repository began in 2025 as a different prototype and was rebuilt in September 2026; the ledger records both dates, but no single interval describes it.
- **[Orpheus](https://github.com/topherchris420/orpheus-resonance-protocol)**, **[hello_os](https://github.com/topherchris420/ideas)**, **[Vers3Dynamics Studio](https://github.com/topherchris420/quantum-spin-sound)**, **[Vanta](https://github.com/topherchris420/vanta)** — no milestone that marks a testable version.

## Adding an entry

Take dates from `git log` on the default branch, link the commit, and count days from the first commit. If the repository opens with an upload, say so. If no step marks a testable version, write *timeline not reconstructed yet*. Fill in *not compressed* before *compressed*.
