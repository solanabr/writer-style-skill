# Designing & validating the router

When the system has more than one craft persona, you need a router: given a piece of content, which
craft(s) to lean on (the spine is always the tone). Design it adversarially, then **validate it
empirically.** The live router this skill ships lives in `../profiles/kaue/ROUTING.md` — study it as the
worked example; this file is the *method* for (re)building one.

## Principles that make a router work

1. **Route on the DOMINANT JOB, not the surface topic.** "Tokenomics" isn't a route; "make value-flows
   legible to a cold audience" (Hayes) vs "derive why this emission curve is right" (Vitalik) are. Two
   pieces on the same topic can route differently by what they're *for*.

2. **Find the AXES.** Profile each craft and identify the *axis* it operates on (e.g. structure-&-evidence,
   derivation, compression/reframe, framing/scope, engagement/stamina). This is the key to safe stacking:
   crafts on **different axes** reinforce; two crafts on the **same axis** fight. Most "which persona?"
   confusion dissolves once you see they're on different axes and can co-exist (one backbone + one guest).

3. **Disambiguate "similar" personas by their underlying *operation*, not their surface domain.** Our
   sharpest example: two "technical genius" personas looked interchangeable, but one **builds an idea up**
   (first-principles derivation, for intricate/contested topics with no honest one-liner) and the other
   **collapses it down** ("X is just Y", for hyped/misframed things a clean reframe dissolves). Whenever
   two personas seem to compete, write the **one-question decision rule** that separates them (here: "does
   the reader need it built up or cut down?") plus a tie-break. Lumping similar personas is the costliest
   routing error.

4. **The spine carries some jobs alone.** Not every job wants a craft backbone. Pure motivation / "why
   this matters" / course-openers are best carried by the *spine* (its native hooks + values) with at most
   one light guest — never a heavy framing backbone (over-claim risk). Always check: is there a job here
   the spine should just own?

5. **Stack across axes, with a hard cap.** One craft owns the backbone (global structure); at most one
   guest contributes local moves on a *different* axis. **Cap = spine (free) + backbone + ≤1 guest = 2
   craft layers.** More than two and the spine's naturalness (the human seam, the uneven texture) gets
   crowded out — which is the fastest way to lose the voice. A wish for a third layer means *split the
   piece*.

6. **One craft is usually "hygiene" / a universal guest.** In our system Helius's concreteness (show the
   artifact, quantify, name the limit) is good on *every* piece regardless of backbone. Identify whether
   your system has such a baseline-craft and apply it everywhere.

## How to build it (the two agents, then you reconcile)
1. **Adversarial design** (`agent-prompts.md` E1): per-persona trigger/anti-trigger conditions, the
   disambiguation rule(s) for similar personas, stacking rules + cap, failure modes, a decision procedure.
   Critically evaluate any starting hunches — they're usually directionally right but too coarse.
2. **Empirical validation** (`agent-prompts.md` E2): route ~14 realistic, varied topics through the draft
   router; find the topics that mis-route, the boundary cases, the missing content types, and any place
   the SKILL.md procedure and the routing doc disagree. *This always finds real gaps* — for us it added
   content types the hunches missed (troubleshooting, security, motivational) and fixed a "novelty"
   heuristic that conflated novelty with the build-up/cut-down axis.
3. **Reconcile and patch.** Apply the validator's refinements; make SKILL.md and ROUTING.md *agree*
   (mismatches between them are a real failure mode — the validator should check this).

## What the router doc should contain (match `../profiles/kaue/ROUTING.md`)
- The axes list.
- Per-persona triggers & anti-triggers.
- The disambiguation rule(s) for similar personas (+ tie-break).
- Stacking rules, the safe pairs, and the cap (state what counts toward it; the spine is free).
- Failure modes, ranked by damage.
- A compact end-to-end decision procedure.

## Common router failure modes
- **Lumping two similar personas** (no disambiguation rule) → arbitrary, often-wrong picks.
- **Routing on topic, not job** → e.g., forcing the "explainer" persona onto a persuasive piece (a tidy
  teardown of an argument that was never made).
- **A heavy persona on the wrong scale** → the big-picture framer on a how-to becomes oracular bloat.
- **A persona's guardrail leaking** (e.g. a cynical edge on an optimistic voice) → tonal break.
- **Over-stacking** → crowds out the spine's seam.
- **SKILL.md ↔ routing doc disagreement** → the procedure read alone mis-routes.
- **Meta-failure:** any route that smooths the body into *uniformly polished, evenly enthusiastic* prose.
  The router's last guardrail is **dosage** — pull craft at the positions that need it; leave routine
  stretches plain.
