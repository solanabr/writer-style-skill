---
description: "Draft or restyle a piece in a voice pack (facts-first, voice-last)"
---

Write the requested content in the target author's voice using the **writer-style** skill. Default pack:
`kaue`. Spawn the **voice-writer** agent (or run the procedure yourself).

1. **Confirm the brief**: topic, length, audience, target container (load `formats/<container>.md` if one
   applies), which pack/author (default Kaue), and any **explicit tone override** (`tone: hayes`,
   `helius 0.7 / hotz 0.3`, `primary-only`). If the dominant *job* is unclear, infer it from the brief
   (how-to → helius, derive-why → vitalik, broad thesis → balaji, economics/macro → hayes, demystify → hotz,
   motivation → primary only). An explicit tone request outranks the router (cap still applies; a crossed
   guardrail gets noted in the manifest, not silently re-routed).
2. **Pass A — Facts (voice OFF).** Draft outline + every claim/number/code/API in neutral prose, grounded
   against `solana-dev` / `context7` / Helius MCPs (not memory). Emit a fact-sheet.
3. **Gate — Verify** the fact-sheet; freeze the facts.
4. **Pass B — Voice.** Load `skills/writer-style/profiles/kaue/kaue.md` + card + ~4 exemplars (always the seam) + the routed
   secondary. **Check the card's `markers:` gates first** (identity beats need their gate keywords in the
   fact-sheet — write the marker budget ledger) and scan `profiles/kaue/themes.md` for fitting substance
   (≤3 items, verified). Restyle the frozen facts; apply the naturalness floor (write unevenly, a human
   seam per passage, ≥1 in 3 sections marker-free). Long-form (≥1,200w): section-by-section with the
   ledger (see writing-workflow.md "Long-form mode").
5. **Pass C — Lint.** Run `skills/writer-style/tools/validate_voice.py diff` (facts preserved) + `tells` (no AI tells, varied
   cadence) + `density --facts <fact-sheet>` (marker budgets + context gates — a gate-missed identity
   beat or doubled sign-off is a hard fail) + `audit --file` for ≥1,200w. Fix flagged sentences.
   Optionally hand to the **voice-validator** agent.
6. **Deliver** the piece + the **tone manifest** (one line, in chat — never inside the piece):
   `tone[helius 0.8, hayes 0.2] · mood: <declared> · markers: <spends|none> · route: auto|requested`
   plus facts-preserved / tells-clean / markers-in-budget (+ the ledger for long-form). The manifest is
   what lets the requester iterate ("again, hayes 0.5").

Honor the scope: Kaue's register with AI tells engineered out and facts verified first — not a perfect clone.
