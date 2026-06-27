---
description: "Draft or restyle a piece in a voice pack (facts-first, voice-last)"
---

Write the requested content in the target author's voice using the **writer-style** skill. Default pack:
`kaue`. Spawn the **voice-writer** agent (or run the procedure yourself).

1. **Confirm the brief**: topic, length, audience, and which pack/author (default Kaue). If the dominant *job*
   is unclear, infer it from the brief (how-to → helius, derive-why → vitalik, broad thesis → balaji,
   economics/macro → hayes, demystify → hotz, motivation → primary only).
2. **Pass A — Facts (voice OFF).** Draft outline + every claim/number/code/API in neutral prose, grounded
   against `solana-dev` / `context7` / Helius MCPs (not memory). Emit a fact-sheet.
3. **Gate — Verify** the fact-sheet; freeze the facts.
4. **Pass B — Voice.** Load `skills/writer-style/profiles/kaue/kaue.md` + card + ~4 exemplars (always the seam) + the routed
   secondary; restyle the frozen facts; apply the naturalness floor (write unevenly, a human seam per passage).
5. **Pass C — Lint.** Run `skills/writer-style/tools/validate_voice.py diff` (facts preserved) + `tells` (no AI tells, varied
   cadence). Fix flagged sentences. Optionally hand to the **voice-validator** agent.
6. **Deliver** the piece + a one-line note: route taken, facts-preserved, tells-clean.

Honor the scope: Kaue's register with AI tells engineered out and facts verified first — not a perfect clone.
