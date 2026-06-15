# Dynamic Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the GitHub profile README more dynamic, polished, and useful without adding new automation or dependencies.

**Architecture:** This is a README-only profile enhancement. The existing snake workflow remains unchanged, while the README gains clearer information architecture and dynamic image embeds. Design and plan artifacts live under `docs/superpowers/` for traceability.

**Tech Stack:** GitHub profile Markdown, shields.io badges, existing contribution snake workflow, GitHub README image embeds.

---

### Task 1: Replace The Profile README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the hard-to-read hero with a compact profile header**

Use this header:

```markdown
<div align="center">

# Christopher Woodyard

**Founder + CEO, Vers3Dynamics**

Researcher building adaptive systems for biosignal modeling, human-state inference, and closed-loop feedback.

`Washington, DC / Bethesda, MD` - `resonant intelligence` - `signal-first systems`

<a href="https://ko-fi.com/vers3dynamics"><img src="https://img.shields.io/badge/Ko--fi-Support%20the%20Lab-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-Fi" /></a>
<a href="https://github.com/topherchris420"><img src="https://img.shields.io/badge/GitHub-topherchris420-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>

</div>
```

- [ ] **Step 2: Add living focus and build sections**

Add sections named exactly:

```markdown
## Current Signal
## Featured Builds
## Stack
```

- [ ] **Step 3: Add dynamic GitHub sections**

Add sections named exactly:

```markdown
## GitHub Pulse
## Contribution Flow
```

Include the existing snake path:

```markdown
https://raw.githubusercontent.com/topherchris420/topherchris420/output/github-contribution-grid-snake.svg
```

- [ ] **Step 4: Add collaboration section**

Add a section named exactly:

```markdown
## Open Loops
```

Use it to describe collaboration interests and contact paths.

### Task 2: Verify README Shape

**Files:**
- Read: `README.md`
- Read: `.github/workflows/snake.yml`

- [ ] **Step 1: Confirm sections exist**

Run:

```powershell
rg -n "Current Signal|Featured Builds|GitHub Pulse|Contribution Flow|Open Loops" README.md
```

Expected: one match for each section.

- [ ] **Step 2: Confirm existing snake path is retained**

Run:

```powershell
rg -n "github-contribution-grid-snake.svg" README.md .github\workflows\snake.yml
```

Expected: README references the SVG and workflow outputs the same filename.

- [ ] **Step 3: Review git diff**

Run:

```powershell
git diff -- README.md docs/superpowers/specs/2026-06-15-dynamic-profile-readme-design.md docs/superpowers/plans/2026-06-15-dynamic-profile-readme.md
```

Expected: only intended README/profile planning changes.
