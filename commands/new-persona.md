---
description: "Build a new voice (primary or secondary) for a pack via the persona-builder"
---

Create a new voice using the adversarial, evidence-bound process. Spawn the **persona-builder** agent.

1. **Decide the type:** PRIMARY (reproduce the target's idiolect — the pack's own voice) or SECONDARY (strip
   idiolect, keep transferable craft — a borrowed-craft author). This inverts one rule; get it right first.
2. **Corpus → clean.** Point `skills/writer-style/tools/profile_corpus.py` at the cleaned corpus (`--paths name=dir` or
   `--corpus <root> --authors <name>`, with `--include` to filter on-register files; guest-reposts are skipped
   automatically). It emits `skills/writer-style/profiles/<pack>/evidence/<name>.profile.json` + `card_suggestions`.
3. **Mine → synthesize → judge.** Follow `skills/writer-style/authoring-personas.md` → `skills/writer-style/method/*`: parallel
   lens-miners (evidence-bound), synthesize a draft, then adversarial judges (secondary: cutter vs advocate;
   primary: fidelity hawk + generate-and-blind-compare).
4. **Author the data layer:** the persona `.md` (secondary: lead with a one-line lane scope header), the
   `.card.yaml` (only writer-actionable dials, from `card_suggestions` + judgment), and the exemplar bank
   (primary: ~7 slots from real passages; secondary: ~3 neutral-voice move-demos). Flag corpus thinness in `notes`.
5. **Wire it in:** update `PACK.md`, `ROUTING.md`, and the lane table in `SKILL.md`; then validate the router
   (`/validate-router`-style: route ~14 real topics, patch breakages).

Output the new files + the router-validation result.
