---
id: nl-01-ecosystem-issue
title: "Newsletter: this week — Anchor 1.0, fee hygiene, course open"
container: newsletter
words_target: 600
audience: subscribers — devs + crypto-curious who opted into a personal dev newsletter
dominant_job: announcement
route_expected: any
context: standalone (issue of a recurring personal newsletter; the sender is a person, not a brand)
expect:
  latam-framing: 0
  sign-off_max: 1
  game-changer_max: 1
  hard_fails: 0
---

## Brief

One issue (~600 words) of a personal dev newsletter carrying three items: (1) Anchor 1.0 shipped
— what it means, should you move; (2) a short "stop overpaying priority fees" nudge that teaches
ONE thing and links out to the full guide (`[LINK-FEES]`, verbatim); (3) course enrollment open
(`[LINK-COURSE]`, verbatim). One voice throughout — an email from a person, not a links digest;
items connected where honest, not force-threaded. Subject line included. Load
`formats/newsletter.md`.

## Fact-sheet (FROZEN — imported subsets of testbed/briefs/06 + 01 + 03; do not re-derive)

Anchor 1.0:
- Targets Solana 3.x / Agave, bundles its own toolchain; TS package renamed `@coral-xyz/anchor` →
  `@anchor-lang/core`; `CpiContext` now takes the program `Pubkey`, touching every CPI call site;
  SPL transfers use `transfer_checked`.
- Verdict space: new projects start on 1.0; production programs migrate behind a branch.

Priority fees (the one thing to teach):
- The fee is charged on the REQUESTED CU limit, not actual usage — simulate first, read
  `unitsConsumed`, set the limit to that +10–20%, then price from recent fee data.

Course:
- "Solana Development Fundamentals": free, 6 modules over 8 weeks, any-language prerequisite,
  outcome = a program on devnet + a frontend (portfolio piece). Weeks 2–3 (Rust) are the hardest
  stretch.
