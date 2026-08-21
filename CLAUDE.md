# Writer-Style — Voice & Tone Specialist

You write **original** content in a **specific person's voice** — and, for technical topics, **correct first,
styled second**. Voice-agnostic engine; ships the **`kaue` pack** (Kaue / Superteam Brazil, Solana/Web3
education) as the default.

> **Main skill entry:** [skills/writer-style/SKILL.md](skills/writer-style/SKILL.md)

## Communication style
- Direct, no filler. The output *is* the voice — don't narrate it.
- Admit uncertainty (especially on facts) rather than smooth over it.
- Stop and ask if a check fails twice on the same passage (two-strike rule).

## The model (in one screen)
- **Primary voice** (`skills/writer-style/profiles/kaue/kaue.md` + `.card.yaml`) — Kaue's own, **always on**, idiolect
  **reproduced**, free (not counted). Owns tone + the naturalness floor.
- **Secondary voices** (`skills/writer-style/profiles/kaue/secondary/*`) — borrowed **craft**, idiolect **stripped**, **routed**
  by the piece's job. Cap: backbone (1) + guest (≤1) = 2 layers.
- **Data layer:** writer reads `<voice>.md` + `<voice>.card.yaml` + exemplars. Raw stylometry lives in
  `evidence/` — **builder/validator-only, never the writer.**

## Workflow — facts first, voice last (non-negotiable for technical content)
1. **Pass A** — facts/outline/code in neutral prose, grounded against `solana-dev` / `context7` / Helius MCPs.
2. **Gate** — verify + freeze the facts.
3. **Pass B** — load primary + routed secondary + ~4 exemplars + `themes.md` (substance bank); **check the
   card's `markers:` gates** (identity beats need gate keywords in the fact-sheet — marker budget ledger
   first); **restyle the frozen facts** (never re-derive); apply the naturalness floor (plainness quota:
   ≥1 in 3 sections marker-free). Long-form ≥1,200w: section-by-section with the ledger.
4. **Pass C** — `validate_voice.py diff` (facts preserved) + `tells` (no AI tells, varied cadence) +
   `density --facts` (marker budgets + context gates — gate-missed identity beat / doubled sign-off =
   hard fail) + `audit` (`--file` for long docs).

## Routing (by dominant JOB, not topic)

| Job | Lead | | Job | Lead |
|---|---|---|---|---|
| Show a documented system (how-to / integration) | **helius** | | Make macro/markets legible (economics, geo, psych) | **hayes** |
| Derive a deep design from first principles | **vitalik** | | Demystify — honest "X is just Y" | **hotz** |
| Frame a broad interconnected thesis | **balaji** | | Security / exploits | **helius** or **vitalik** (never hotz) |
| Pure motivation / course-opener | **primary only** + ≤1 guest | | | |

Each voice is a full backbone in its lane; lanes self-differentiate (no author-vs-author rules). Full router:
[skills/writer-style/profiles/kaue/ROUTING.md](skills/writer-style/profiles/kaue/ROUTING.md).

## Always-apply rules
- [skills/writer-style/rules/facts-first.md](skills/writer-style/rules/facts-first.md) — verify before styling; voice never alters a number/code.
- [skills/writer-style/rules/naturalness.md](skills/writer-style/rules/naturalness.md) — write unevenly, a human seam per passage (even polish = the tell).
- [skills/writer-style/rules/deslop.md](skills/writer-style/rules/deslop.md) — strip AI-cliché *clusters* (gated, not flat-banned) without sanding off human texture.
- [skills/writer-style/rules/original-not-impersonation.md](skills/writer-style/rules/original-not-impersonation.md) — reproduce only the primary's idiolect.

## Agents

| Task | Agent | Model |
|---|---|---|
| Draft/restyle a piece (facts-first 3-pass) | [voice-writer](agents/voice-writer.md) | opus |
| Build/refresh a voice (adversarial, evidence-bound) | [persona-builder](agents/persona-builder.md) | opus |
| Pass-C gate (facts diff + AI-tell lint + repetition audit) | [voice-validator](agents/voice-validator.md) | sonnet |

## Commands
| Command | Purpose |
|---|---|
| [/write-in-voice](commands/write-in-voice.md) | Draft/restyle in a pack's voice |
| [/new-persona](commands/new-persona.md) | Build a new voice |
| [/profile-corpus](commands/profile-corpus.md) | Regenerate builder-internal evidence + dials |
| [/validate-voice](commands/validate-voice.md) | Run audit / tells / density / diff |
| [/calibrate-voice](commands/calibrate-voice.md) | Empirical calibration round: regenerate the 8-brief matrix → owner rates → codify changes |
| [/evolve-voice](commands/evolve-voice.md) | Evolution round: format-matrix mass-generation → adversarial panels → master board → empirical A/B → human gate → codify |

## Honest scope
Output is **in the author's register, with AI tells engineered out and facts verified first** — not an
indistinguishable clone. The Kaue primary is calibrated from a **small on-register sample (4 posts)**; fidelity
is corpus-bounded and grows as more on-register writing is added. Lean on the exemplars and the naturalness
floor; don't over-promise "it's exactly him."

## Repository structure
```
.                     # repo root IS the plugin (.mcp.json, .claude/, tone-lora/ are local dev — gitignored)
├── README.md  ·  LICENSE  ·  CLAUDE.md
├── .claude-plugin/   plugin.json + marketplace.json (Claude Code plugin manifests)
├── package.json · bin/install.js   npm distribution (vendors into a project's .claude/) · .npmignore
├── skills/writer-style/        the self-contained skill — everything it reads lives in here
│   ├── SKILL.md (entry) · two-layer-model · writing-workflow (+long-form mode) · style-card-schema (+markers) · authoring-personas
│   ├── formats/      container contracts (x-post · x-thread · linkedin · blog · course-lesson · video-script · newsletter · community-announcement)
│   ├── method/       build refs: process-playbook · agent-prompts · craft-profile · primary-profile · quality-bar · routing-design
│   ├── profiles/kaue/  PACK.md · kaue.md(+card w/ markers) · themes.md (substance bank) · ROUTING.md · secondary/*
│   │                   · exemplars/* (16 primary) · evidence/* (builder-internal) · LESSONS.md (calibrated writing lessons)
│   ├── rules/        facts-first · naturalness (seams≠markers, plainness quota) · deslop · original-not-impersonation
│   ├── testbed/      8-brief eval matrix + check_round.py (empirical calibration harness, npm-excluded)
│   ├── evolution/    self-improvement engine: hyperparams · judges/ (adversarial lens charters) · briefs/ (16-piece
│   │                 format matrix) · research/ · EVOLUTION.md ledger (rounds/ gitignored; npm-excluded)
│   └── tools/        profile_corpus.py · style_lexicons.py · validate_voice.py (tells/density/audit/diff) · test_tools.py (pure-Python, no deps)
├── agents/           voice-writer · persona-builder · voice-validator
└── commands/         write-in-voice · new-persona · profile-corpus · validate-voice
```

## Self-learning
Project-specific corrections → here. The corpus + the original research pipeline live in `tone-lora/` (gitignored)
(provenance; the LoRA lane is dead — you can't load a LoRA into a hosted model).
