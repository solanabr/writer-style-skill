---
description: "Facts first, voice last — verify technical content BEFORE styling; voice never invents or alters a number, code line, or API. Always applies to technical pieces."
---

# Facts first, voice last

Persona/voice prompting improves style **but measurably degrades factual accuracy.** For technical Solana
content a wrong number or renamed instruction is the worst possible output. So:

> **Voice is the last transform over verified facts — never the medium in which facts are discovered.**

## The rule
1. **Establish facts with voice OFF.** Draft every claim, number, unit, address, CU/lamport figure, account
   size, version-sensitive API, and all code in **plain neutral prose** first.
2. **Ground against sources, not memory.** Use `solana-dev`, `context7`, and Helius MCPs; run
   `program_autofixer` on Rust program code. The ecosystem outruns any training cutoff.
3. **Verify, then freeze.** Fact-check the terse fact-sheet (cheap — facts aren't buried in prose). Nothing
   gets styled until the facts are solid.
4. **Restyle, don't re-derive.** When applying the voice, **rephrase around the frozen facts** — never change
   a number, code line, or named API. You're choosing words, rhythm, hooks, and structure, not re-computing.
5. **Diff after styling.** Run `validate_voice.py diff` — every number/identifier from the fact-sheet must
   survive unchanged. A mutated `0.002 SOL` or a renamed `transfer_checked` is a **hard fail**; rewrite that
   sentence.
6. **Admit uncertainty.** If a fact can't be verified, say so in the piece rather than smoothing over it. A
   confident wrong claim detonates "don't trust, verify."
7. **First-person incidents ARE facts.** A lived receipt (a dated memory, a named repo, "last year I…")
   under the author's byline is a factual claim about the author's life; inventing one is a fact violation,
   not a style choice — and it's the seductive one: evolution R1 measured blind judges preferring fabricated
   memoirs 6-0 over honest observation. An incident seam may only draw from the fact-sheet's attested-
   receipts annex (themes.md — see the workflow's substance-bank step), the sheet itself, or the piece's own
   practice (something the piece actually walks through). **When no receipt fits, the degrade ladder** (owner
   ruling, R1): on teaching/motivation pieces where the receipt is load-bearing, leave a
   `[RECEIPT — confirm: <one-line claim>]` placeholder for the owner to fill or strike before publish; on
   everything else, degrade silently to a practice or stance seam — a cooler true piece beats a warmer fake
   one. Never fabricate the middle ground.

## Why it works
Voice can't corrupt a fact it never touched. The fact-check is cheap because the statements are terse and
neutral. And the voice is *freer* in Pass B precisely because it operates on locked content. The trade is
deliberate: restyle-over-verified beats voiced-from-scratch for anything where being wrong is worse than being
slightly less you.
