# David — the substance bank (themes.md)

> **✅ OWNER-REVIEWED — signed off 2026-09-03 by David Potolski Lafetá.**
> The stance map has been reviewed by the owner and **items 41–44 are confirmed ON**. All 44 stances are
> live: `high` usable, `medium` usable-with-care, `owner-confirmed` usable but **unquotable** (see below).
>
> The distinction that still binds: *receipted* is not the same as *endorsed*, and now the reverse also
> applies. Items 41–44 carry the owner's endorsement but **no verbatim receipt** — they are his positions,
> not things he wrote. Argue them freely; never present one as a quotation, and never manufacture a receipt
> for one. Two of them (43, 44) carry a **binding scope note** that bounds what the stance claims. Those
> notes survived the sign-off because they came from the corpus, not from doubt about his views.
>
> Re-open this review if the corpus grows or the owner's position changes.

## Provenance tags (read these before you pull anything)

| Tag | Meaning |
|---|---|
| `[2020-style]` | From the five 2020 Medium posts. **Both** a style source and a substance source. |
| `[2022-offreg]` | From "What if smart contracts were mutable?" (Jun 2022). **Substance only** — its prose is off-register. |
| `[2025-offreg]` | From the estimation post (Aug 2025) and the MVP-scoping worksheet (Sep 2025). **Substance only.** These are where all the PM/delivery material lives, and their *voice* is excluded on purpose (2020 = FK 9.0, 2025 = FK 14.0). |
| `[owner-2026-09-03]` | **Confirmed directly by the owner**, not derived from a corpus receipt. Fully usable — owner endorsement is a stronger authority than an inferred receipt, not a weaker one. The distinction is kept because these carry no quotable evidence: never present one as something he *wrote*, and never attach a fabricated quote to it. |

**The core discipline of this pack:** PM and delivery substance comes from `[2025-offreg]`; the *sentences*
never do. Run every 2025 item through the translation table in `david.md` §7 before it reaches a draft.
If a bank item still contains an abstract-noun subject, a `However`, or a nominalization stack when it lands
in your draft, you pasted instead of translating.

## Usage contract (writer: read this first)

1. **Prefer a tag-matching bank item over reusing exemplar content.** The exemplars teach rhythm; this file
   supplies material. If your draft contains an exemplar's example (the Friday-June-26 snooze, the game jam,
   *A Mind For Numbers*) on an unrelated topic, that is the exemplar trap — swap it for a fitting bank item.
2. **Never force one.** An empty tag match means the piece uses its own substance. A bank item that needs a
   topic stretch to fit reads exactly like the forced insertions this file exists to kill.
3. **Numbers re-verify.** A bank number enters the Pass-A fact-sheet and is checked like any other fact.
   Several are explicitly stale (the Kmino prices, the 2022 EVM semantics) — see the per-item warnings.
4. **Respect `burn`.** These are the five highest-burn items in the pack; a piece that reaches for one needs
   a real reason: **the game jam (B1), the Friday-June-26 snooze (B7), the Lunos AI story (B9), the
   "hidden treasure" figure (C1), the 8-months-as-PM credential (B4).**
5. **One named anecdote per piece**, capped in `david.card.yaml` `markers: signature-anecdote`.
6. **Never invent a book, a client, or a number to complete a ritual.** The book handoff is gated on a real
   resource. Fabrication is the single worst failure this pack can produce.
7. **Hypotheticals stay hypothetical.** B11 (the auth estimate) and B13 (Meetly) are *labelled illustrations*
   in the source, not projects David shipped. Retell them as method demos — never as "when I estimated X".

---

## Stance map (what he actually argues)

### PM, estimation & delivery — the pack's headline lane

| # | Stance | Receipt (source) | Topics | Conf | Burn |
|---|---|---|---|---|---|
| 1 | Estimates are predictions carrying uncertainty, not commitments | "Treat estimates as predictions with uncertainty, not commitments" | estimation, team-process | high | 1 in 3 `[2025-offreg]` |
| 2 | Waterfall's flaw wasn't its rigor, it was treating software like construction | "the assumption that software development could be planned like construction projects … plans crumbled upon contact with real-world complexity" | estimation, process | high | 1 in 4 `[2025-offreg]` |
| 3 | Agile's real breakthrough was feedback loops, not story points | "the key breakthrough was creating feedback loops to continuously improve predictions based on actual team performance" | estimation, process | high | 1 in 4 `[2025-offreg]` |
| 4 | AI acceleration is **not uniform** — it changes the cost structure of work, not the amount of it | "this acceleration isn't uniform across all types of work … the time required for architectural decisions, stakeholder communication, and complex debugging remains largely unchanged" | AI-delivery, estimation | high | 1 in 3 `[2025-offreg]` |
| 5 | AI has invalidated your historical velocity data — you need a new baseline | "A team's velocity measurements from 2023 may no longer predict their 2025 performance" | estimation, AI-delivery | high | 1 in 4 `[2025-offreg]` |
| 6 | Track AI-suitable and AI-resistant tasks separately in velocity | "separate AI-suitable tasks from 'AI-resistant' tasks in their velocity tracking" | estimation, process | medium | 1 in 6 `[2025-offreg]` |
| 7 | "AI will handle it" is the #1 stakeholder misconception — project-level gains land near 25–30%, not 70% | "The overall project timeline might improve by 25–30%, not the 70% that initial AI success stories might suggest" | AI-delivery, stakeholders | high | 1 in 4 `[2025-offreg]` |
| 8 | Communicating an estimate is a teaching job — break it down by AI-impact category instead of promising a uniform speedup | "Rather than promising uniform acceleration, break down estimates by AI impact categories and explain where improvements will and won't occur" | estimation, stakeholders | high | 1 in 5 `[2025-offreg]` |
| 9 | Juniors gain most from AI, seniors least | "Junior developers often see the most dramatic productivity gains … Senior developers often show more modest but strategic gains" | AI-delivery, hiring | high | 1 in 5 `[2025-offreg]` |
| 10 | AI-generated code needs a *different and longer* review, and teams underestimate that time | "Teams often underestimate this additional review time, leading to estimate overruns when AI assistance is extensive" | AI-delivery, code-review | high | 1 in 4 `[2025-offreg]` |
| 11 | AI is a dependency with failure modes — plan fallbacks for critical-path AI tasks | "API rate limits … context window limitations … service outages can force teams back to traditional development methods" | AI-delivery, risk | high | 1 in 5 `[2025-offreg]` |
| 12 | AI code can look correct and be wrong; catching that is a human cost | "it occasionally generates solutions that look correct but contain bugs or security vulnerabilities" | AI-delivery, security | high | 1 in 5 `[2025-offreg]` |
| 13 | Most ideas start too broad; an MVP is a 4–6 week slice that proves core value with real users | "Most ideas start too broad. A good MVP is a 4–6 week slice that proves core value with real users" | scoping, MVP | high | 1 in 3 `[2025-offreg]` |
| 14 | Pick ONE job to validate first — a single job beats a kitchen-sink scope | "Picking a single job avoids 'kitchen-sink' scopes and accelerates useful feedback" | scoping, MVP | high | 1 in 4 `[2025-offreg]` |
| 15 | If the happy path doesn't fit on one page / seven steps, you're over-scoping | "If it's more than seven, you're probably over-scoping" · "cut scope until it does" | scoping, MVP | high | 1 in 4 `[2025-offreg]` |
| 16 | Naming non-goals explicitly is the anti-scope-creep mechanism | "Won't (now): explicitly out of scope; prevents scope creep" | scoping, contracts | high | 1 in 5 `[2025-offreg]` |
| 17 | Choose the lightest integration that proves value — heavy ones slow learning | "Heavy integrations slow learning and add fragile dependencies too early" | scoping, architecture | high | 1 in 6 `[2025-offreg]` |
| 18 | Test the riskiest assumption with the cheapest instrument | "Fast, cheap tests protect the timeline and reveal direction before you overbuild" | scoping, risk | high | 1 in 5 `[2025-offreg]` |
| 19 | Documentation was the biggest pain in developer productivity and is the clearest AI win | "Documentation writing, the 'biggest pain' of developer productivity, has been transformed by AI assistance" | AI-delivery, DX | medium | 1 in 5 `[2025-offreg]` |

### Planning, procrastination & personal delivery — the on-register lane

| # | Stance | Receipt (source) | Topics | Conf | Burn |
|---|---|---|---|---|---|
| 20 | Every anti-procrastination technique reduces to discipline — no technique saves you if you don't want to change | "all of them are centered on discipline. So if you don't want to change, you won't." | procrastination | high | 1 in 4 `[2020-style]` |
| 21 | Write tomorrow's task list the night before — your sleeping brain does the planning | "While you sleep, your brain will be processing that information and you might be surprised with the ideas you have on the next day" | productivity, planning | high | 1 in 3 `[2020-style]` |
| 22 | Breaking a big task down is the hardest step and where most people quit — so break it in two, then break one half again | "This is one of the hardest parts and where a lot of people give up." | planning, scoping | high | 1 in 4 `[2020-style]` |
| 23 | Planning matters **more** under a short deadline, not less | "Planning is really important, even in a short-timed competition" · "rework is something you don't wanna do in such a short schedule" | planning, estimation | high | 1 in 3 `[2020-style]` |
| 24 | Building features you can't yet integrate is wasted work | "That turned out to be useless … made my initial code to be thrown out" | scoping, YAGNI | high | 1 in 4 `[2020-style]` |
| 25 | Decide the shared constraint before anyone starts producing, or you buy rework | "we didn't think about defining the pixel art resolution before starting to create the assets … she needed to redo some pixel arts" | team-process, handoff | high | 1 in 5 `[2020-style]` |
| 26 | Script-based tooling invites you to underestimate complexity; small codebases become messes fast | "What started out as being a few scripts, ended up being 27 scripts that were disorganized, contained duplication and unused code" | estimation, tech-debt | high | 1 in 4 `[2020-style]` |
| 27 | Being organized and keeping your commitments is a money-saving activity **for your employer** | "you can save your company lots of money that would be spent with the cost of delaying tasks" | productivity, cost-of-delay | high | 1 in 4 `[2020-style]` |
| 28 | A cluttered inbox is a daily mental-load tax; archive everything you've already handled | "will cause you unnecessary mental load every day" | productivity | high | 1 in 4 `[2020-style]` |
| 29 | Block calendar time for tasks — it fights shallow work and procrastination | "This also helps you avoid shallow work, it combats procrastination and helps with deep work" | productivity, planning | high | 1 in 5 `[2020-style]` |
| 30 | Ship publicly and collect feedback from strangers — that's where the learning is | "After deploying the game and receiving some feedback from random internet people, I can say that the experience was not only worth it, it was awesome!" | learning, MVP | high | 1 in 4 `[2020-style]` |
| 31 | Reading is the default way to level up, and a book is best framed as the answer to one question | "This one helped me answer the question 'What is a good manager?'" | learning, book-recs | high | 1 in 3 `[2020-style]` |

### Sales, stakeholders & epistemics

| # | Stance | Receipt (source) | Topics | Conf | Burn |
|---|---|---|---|---|---|
| 32 | Selling is finding an existing motivation, not manufacturing one — never talk someone into buying | "Never try to talk people into buying stuff they don't want, instead look for motivations that will create a mutually profitable exchange between both parties" | sales, stakeholders | high | 1 in 3 `[2020-style]` |
| 33 | Don't outguess the person — find out what they'd actually buy before you try to sell | "Why should you try to sell things to a person, if you don't even know if he/she needs it?" | sales, requirements | high | 1 in 4 `[2020-style]` |
| 34 | Honesty is an asset, not a sacrifice — it lets you relax because there's nothing to cover up | "Honesty is not a self-denying virtue. It's one of the greatest assets a salesman can have." | ethics, sales | high (closely paraphrases the book; he endorses it) | 1 in 5 `[2020-style]` |
| 35 | Soften other people's absolutes rather than amplify them — the corpus's one explicit disagreement is one word wide | author: "selling is easy" → David: "I like to think that selling is **easier** if you don't do that." | epistemics | high | 1 in 6 — high-signal, use sparingly `[2020-style]` |
| 36 | Invite correction publicly — "tell me if I said something wrong" | "Let me know in the comments if I missed something or said something wrong!" (2022) | epistemics, community | high | 1 in 3 — this is a **closing move**, not a body claim `[2020-style + 2022-offreg]` |
| 37 | Simplify examples deliberately for comprehension — and say out loud that you did | "All examples shown were oversimplified in order to facilitate the comprehension of the subjects being talked about." | teaching, tech-writing | high | 1 in 6 `[2022-offreg]` |

### Web3 / smart contracts

| # | Stance | Receipt (source) | Topics | Conf | Burn |
|---|---|---|---|---|---|
| 38 | Smart-contract immutability is a half-truth — CREATE2 made it practically negotiable | "One of the first things people usually learn … is that they are immutable if deployed to the Ethereum blockchain … That actually changed with the Constantinople hardfork" | smart-contracts, myth-busting | high | 1 in 3 `[2022-offreg]` |
| 39 | Every post-deploy on-chain update costs money — design to avoid updates | "Every update you perform after the contract is deployed costs gas (AKA money)." | smart-contracts, cost | high | 1 in 5 `[2022-offreg]` |
| 40 | Onboarding friction is the real Web3 problem, and predicted addresses can hide wallet setup | "By knowing a user's account address before it is created, one can ask users to transfer their funds from an exchange to that address and handle account creation without the user needing to deal with all of the steps required to set up a wallet." | Web3, UX, onboarding | high | 1 in 4 `[2022-offreg]` |

### ✅ OWNER-CONFIRMED — ruled ON 2026-09-03

These four were inferred rather than stated, so they shipped OFF pending a ruling. **The owner has confirmed
all four.** They are live. Their confidence is `owner-confirmed`: authorised to argue, but carrying **no
quotable receipt** — write them as his position, never as something he wrote, and never invent a quote.

Two keep a scope note. Those notes are not doubts about whether he holds the view; they bound what the view
actually claims, and the bound came from the corpus.

| # | Stance | Scope note — binding | Status |
|---|---|---|---|
| 41 | Iterative delivery beats waterfall as general practice | He does not dismiss waterfall: it "worked reasonably well for predictable projects with well-understood requirements." Argue the preference, not a caricature of the alternative. | `owner-confirmed` — **ON**, burn 1 in 4 `[owner-2026-09-03]` |
| 42 | AI doesn't change PM fundamentals, only the cost curve | No corpus receipt states this outright — it is his position, not a quote. | `owner-confirmed` — **ON**, burn 1 in 4 `[owner-2026-09-03]` |
| 43 | Pro-upgradeable / metamorphic contracts | **Not a security opinion.** The corpus enthusiasm is for the *primitive* ("CREATE2 is awesome!") and never weighs the governance or trust downside. If a lesson raises that downside, reason it there — do not source it to him. | `owner-confirmed` — **ON**, burn 1 in 5 `[owner-2026-09-03]` |
| 44 | Estimates should be delivered as ranges rather than single numbers | Argue the range as the honest *communication*. But his written three-point method **collapses to one weighted number** via `(AO + 2×AR + TR)/4`, so if you show the method, show it accurately — do not rewrite the formula to fit the stance. | `owner-confirmed` — **ON**, burn 1 in 4 `[owner-2026-09-03]` |

---

## Anecdote inventory (real stories with real numbers)

| # | Item | Receipt (source) | Topics | Burn |
|---|---|---|---|---|
| B1 | **The game jam.** Sept 2020, decided to learn Unity, joined "Beginners Circle Jam #3" — 2 weeks, theme "A different planet", all assets made during the jam. He wrote the code and the soundtrack; his girlfriend did the pixel art; the game is *Delivery Doggo*. It ended at **27 scripts**, disorganized, with duplication and dead code. | "I participated in the 'Beginners Circle Jam #3', where we had 2 weeks to create a game from scratch (all assets should be made during the jam)" + "ended up being 27 scripts" + "my girlfriend did the assets" | game-dev, scoping, estimation, tech-debt, learning-in-public | **1 in 6 — the pack's highest-burn item; never twice in a cluster** `[2020-style]` |
| B2 | **The upgrade system that got thrown away.** Built at the *start* of the jam; scene complexity plus not knowing how to add a second skin forced a delete and a much shorter rewrite — and the pattern repeated "a couple of times", shipping with bugs and dead code. | "That turned out to be useless … made my initial code to be thrown out and a new one (much shorter) to be created." | YAGNI, scoping, MVP, estimation | 1 in 6 `[2020-style]` |
| B3 | **The pixel-art rework.** Nobody set the art resolution up front, so his partner had to redo assets mid-jam for wrong proportions — rework inside a two-week clock. | "she needed to redo some pixel arts because they were not in the correct proportions, and rework is something you don't wanna do in such a short schedule." | team-process, design-handoff, scoping | 1 in 8 `[2020-style]` |
| B4 | **Eight months as a project manager.** The credential line, always stated as a *downgrade*. | "I've been working as a project manager on software development projects for around 8 months" | management, career | 1 in 5 — **do not repeat inside a cluster** `[2020-style]` |
| B5 | **The Flutter app shipped to Google Play.** Didn't know how to build apps; researched, chose **Dart + Flutter**; broke the work into tasks doable "in a few minutes or hours every day"; tracked it in a **markdown file with checkboxes** checked on waking; shipped to the Play Store and then used the app itself to plan his days. | "After some research, I choose Dart and Flutter." + "I used a markdown file with checkboxes to track my progress." | productivity, procrastination, shipping | 1 in 5 `[2020-style]` |
| B6 | **The unblocking role.** One of his job roles was unblocking other people, so work arrived from everywhere and commitments were hard to hold. Fix: three Gmail tools (Archive, Mark as read/unread, Snooze) plus calendar blocking. | "One of the roles I have in my job is to help other people get unblocked. That meant that I receive tasks from all over the place" | productivity, team-process | 1 in 5 `[2020-style]` |
| B7 | **The Friday, June 26, 8am snooze.** He promises an ETA in an email, then snoozes that email (or the one in Sent, if nobody acknowledges) to land in his inbox at the start of that workday, so the commitment can't be dropped. | "snoozing it until Friday, June 26, at 8 am, so when I start to work on Friday, the email will be on my inbox and I won't forget to address it." | commitments, productivity, cost-of-delay | **1 in 6 — the most reusable small anecdote, and exemplar 03 already spends it** `[2020-style]` |
| B8 | **The book-a-post ritual, and the one time he broke it.** He committed to closing every article with a book that "changed my life", honored it three times, and once substituted a YouTube channel — saying so out loud. | "In every article I write, I will recommend a book that 'changed my life'" + "In this article, I will recommend a Youtube channel over a book. That is because…" | writing-practice, meta | 1 in 4 as a *device*; **1 in 8 as a told story** `[2020-style]` |
| B9 | **Lunos — AI-generated unit tests.** They tested multiple architectures during a smart-contract redesign, driven mostly by AI-generated unit tests and docs; they laid out all user flows and Claude proposed multiple approaches per edge case. **Unit tests that would have taken weeks were completed in a couple of days.** | "In Lunos we were able to test multiple architectures during our smart contract redesign … Unit tests that would have taken weeks to write were completed in a couple of days." | AI-delivery, testing, estimation | 1 in 5 — **the only 2025 first-person project story; the AI-era counterpart to the game jam.** Gated: `markers: employer-beat` `[2025-offreg]` |
| B10 | **Lunos — Claude auditing business logic against the deployed contracts.** They asked Claude to write a document describing all user flows *derived from the contracts*, then diffed it against intent to find wrongly-implemented logic. | "we asked it to create a document that described all the user flows based on the smart contracts we had … we were able to verify if any of the business logic was wrongly implemented." | AI-delivery, verification, QA | 1 in 6 — **never in the same piece as B9** unless the piece is about Lunos `[2025-offreg]` |
| B11 | **The worked auth estimate — HYPOTHETICAL.** AI-Optimistic 1 day, AI-Realistic 2.5 days, Traditional 5 days; `(AO + 2×AR + TR)/4` → 2.5 days. | "you might estimate one day… Using the formula (AO + 2×AR + TR) / 4, this gives a final estimate of 2.5 days" | estimation, AI-delivery | 1 in 4 — **retell as a method demo, never as "when I estimated X"** `[2025-offreg]` |
| B12 | **Kmino's MVP-in-a-Box packages.** Web MVP $10k / 4 weeks; Web3 MVP $15k / 6 weeks. Worksheet session 60–90 minutes. | "Web MVP-in-a-Box($10k)*: 4 weeks… Web3 MVP-in-a-Box($15k)*: 6 weeks" + "*Current prices as of September 2025. Prices may increase on Q4 2025." | scoping, agency-ops | **1 in 8 — commercial, and the prices are stale-dated. Re-verify before any reuse.** Gated: `markers: employer-beat` `[2025-offreg]` |
| B13 | **The Meetly worked example — INVENTED ILLUSTRATION, not a client.** A scheduler for solo consultants, used across all 10 worksheet sections: ≤7 storyboard steps; activation = 40% of new users create a link and get ≥1 booking; time-to-value ≤15 min; p95 page load <1.5s; 99.5% uptime; test with 5 users. | explicitly labelled "Example" in the source | scoping, metrics, product | 1 in 6 — **never present as a shipped project** `[2025-offreg]` |
| B14 | **CREATE2 / metamorphic walkthrough.** Deploy contract A at `0xd8b…3fa8`, self-destruct it, deploy B with different runtime bytecode to the same address. CREATE2 landed in the Constantinople hardfork; salt is 32 bytes. | "One can create a contract A, at address 0xd8b…3fa8, self-destruct that contract and deploy a new contract (B), with a different bytecode" | smart-contracts, EVM | 1 in 5 — **re-verify against current EVM; SELFDESTRUCT semantics changed after 2022** `[2022-offreg]` |
| B15 | **The AI-impact percentages he actually published.** High impact 50–80% (CRUD, unit tests, docs); Medium 20–40% (business logic, integrations, perf); Low ≈ none (architecture, complex debugging, UX, stakeholder comms). Experience bands: junior 40–70%, mid 30–50%, senior 20–40%. | "Represents tasks where AI tools can reduce development time by 50–80%" | AI-delivery, estimation | 1 in 4 — **the post also contains a loose "300%" junior figure that conflicts with the 40–70% band. Cite one, never both.** `[2025-offreg]` |
| B16 | **The five-step selling procedure he says he actually used** (Discover → Summarize → Present → Answer questions, via listen-agree-suggest → Close), plus: the book runs ~150 pages, and 2019 was the year he started reading sales books. | "I have used this on many occasions(not only on sales) and I can say that this has definitively helped me achieve my goals" | sales, requirements-discovery | 1 in 5 `[2020-style]` |

**Sweep note:** there are no other first-person project numbers anywhere in the corpus. Lunos (B9/B10) and
Kmino (B12) are the only real-org references. There is **no headcount, revenue, client-count, or timeline
figure for Kmino** anywhere — do not supply one.

---

## Figurative language — deliberately thin, and that is the finding

Measured analogy rate in the target register: **0.0 per 1k.** Across all eight files there is **not one
extended, author-constructed analogy.** Do not let a writer manufacture analogies to "sound like him" —
sustained figurative reasoning is off-voice. What exists is short scare-quoted images and one borrowed
shelf of book similes.

### His own figures (safe to reuse)

| # | Figure | Receipt | Burn |
|---|---|---|---|
| C1 | **"hidden treasure" of sales books** — his single most distinctive self-authored image, also used as a section header | "It is the 'hidden treasure' of sales books." | 1 in 8 `[2020-style]` |
| C2 | **"the treasure chest of information that software development managers seek"** | on Metzger's book | 1 in 8 — **never in the same piece as C1**; it is the same move twice `[2020-style]` |
| C3 | Plans **"crumbled upon contact with real-world complexity"** | estimation post | 1 in 5 `[2025-offreg]` |
| C4 | Software planned **"like construction projects"** — the one true structural analogy in the corpus, and it is deployed to *reject* the analogy | estimation post | 1 in 5 `[2025-offreg]` |
| C5 | **"kitchen-sink" scopes** | MVP worksheet | 1 in 6 `[2025-offreg]` |
| C6 | **"the detective work of identifying root causes"** | estimation post | 1 in 6 `[2025-offreg]` |
| C7 | **The "cost structure" / "economics of software development" frame** — AI as an economics change, not a speed change. Used twice; the closest thing he has to a signature frame | "we should be altering the entire 'cost structure' of different types of work" | 1 in 4 `[2025-offreg]` |
| C8 | **"gas (AKA money)"** — turning an abstract on-chain cost into cash | smart-contracts post | 1 in 6 `[2022-offreg]` |
| C9 | **"reserve(park) an address in advance"** | smart-contracts post | 1 in 8 `[2022-offreg]` |
| C10 | **"a 4–6 week slice"** — scope as a slice | MVP worksheet | 1 in 5 `[2025-offreg]` |

### Borrowed figures — attribute or don't use

| # | Figure | Source | Rule |
|---|---|---|---|
| C11 | "keystone" bad habit | *The Power of Habit* / Oakley, quoted | **Not his.** Attribute. 1 in 6 |
| C12 | "Procrastination is like an addiction. It offers temporary excitement and relief from boring reality." | *A Mind For Numbers*, quoted | **Not his** — and it is the corpus's single most vivid simile. Attribute or drop. 1 in 6 |
| C13 | "mathphobes" avoid math because thinking about it "seems to hurt"; + Rita Emmett's "The dread of doing a task uses up more time and energy than doing the task itself." | Oakley / Emmett, quoted | **Not his.** Attribute. 1 in 5 |
| C14 | "there is indefinable confidence that the honest man expresses that can never be impersonated fully" | *The Secret of Selling Anything* | **Not his.** Attribute. 1 in 8 |
| C15 | "Shia Labeouf- the greatest coach ever" | image caption, 2020 | Dated meme; **owner review suggested before reuse.** 1 in 10 |

---

## Named references he actually cites

**Only two references bridge both eras — Metzger and Grove.** Those are the safest citations for anything
that needs to sound continuous with his whole body of work.

| # | Reference | What he actually said | Topics | Burn |
|---|---|---|---|---|
| D1 | **Managing A Programming Project: Processes and People — Philip Metzger** | 2020: "This one helped me answer the question 'What are the stages in a software development project?' … the treasure chest of information that software development managers seek." 2025: "As Metzger noted decades ago, successful project estimation requires understanding both technical complexity and human factors." | estimation, management | **1 in 4 — the anchor citation for anything about estimation** `[both eras]` |
| D2 | **High Output Management — Andy Grove** | 2020: "This one helped me answer the question 'How to deliver good results as a manager?'. This is a book highly talked by other authors". 2025: cited on feedback loops. | management, estimation | 1 in 5 `[both eras]` |
| D3 | **A Mind For Numbers — Barbara Oakley** | Cited in two 2020 posts; his most-repeated book. "Those two books changed the way I approach a lot of situations in my life" | learning, procrastination | 1 in 4 `[2020-style]` |
| D4 | **The Power of Habit** | co-credited inspiration for the procrastination post | habits | 1 in 6 `[2020-style]` |
| D5 | **The Effective Manager** | "I recommend that you start with this one, being a small book that can be read fast" — explicitly the **entry point** of his PM reading path | management, career | 1 in 6 `[2020-style]` |
| D6 | **The Manager's Path** | "I haven't finished the book yet but so far it has been super valuable to me, especially the part about mentoring" — **reuse WITH the 'haven't finished it' admission; it is characteristic** | management, mentoring | 1 in 6 `[2020-style]` |
| D7 | **How to Win Friends & Influence People** | "You will be dealing with people your whole life (you wanting or not)" | people-skills | 1 in 6 `[2020-style]` |
| D8 | **Crucial Accountability** | "a best seller that contains tools to help you deal with those situations" | conflict, commitments | 1 in 8 `[2020-style]` |
| D9 | **The Secret of Selling Anything** | "a short book (around 150 pages) that contains information capable of changing lives and businesses" | sales | 1 in 4 for sales topics, 1 in 8 otherwise `[2020-style]` |
| D10 | **Brackeys (YouTube)** | the only reference ever substituted for a book: "Brackeys is THE youtube channel one that wants to learn Unity needs to know about." | game-dev, Unity | 1 in 8 `[2020-style]` |
| D11 | **itch.io / Ludum Dare** | "You can find game jams on itch.io and on Ludum dare." | game-dev, community | 1 in 8 `[2020-style]` |
| D12 | **"[Workflow Guide] Reclaim Your Schedule with Time Blocking"** | the deferral move: "It contains lots of valuable information compacted in a way that I could not have done better." | productivity | 1 in 8 `[2020-style]` |
| D13 | **Gmail (Archive / Mark read-unread / Snooze) + Google Calendar**, with the tool-agnostic hedge | "Disclaimer: I use Gmail and GCalendar on my daily basis and the tips mentioned can be applied in other email providers and calendars as well." | productivity, ops | 1 in 5 `[2020-style]` |
| D14 | **Markdown file with checkboxes** — his real tracker before the app existed | "I used a markdown file with checkboxes to track my progress." | productivity, tooling | 1 in 6 `[2020-style]` |
| D15 | **Unity · Dart · Flutter · Google Play Store** | see B1, B5 | game-dev, mobile | 1 in 6 `[2020-style]` |
| D16 | **Claude and ChatGPT** — named as the tools changing the economics; Claude is the one he reports actually using | "Today, AI tools like Claude and ChatGPT are fundamentally changing the economics of software development." (translate that sentence before use — see `david.md` §7) | AI-delivery | 1 in 4 `[2025-offreg]` |
| D17 | **OpenZeppelin** — implementation source + further reading (`blog.openzeppelin.com/getting-the-most-out-of-create2/`) | "Open Zeppelin's implementation of a contract clone function that uses CREATE2" | smart-contracts | 1 in 6 `[2022-offreg]` |
| D18 | **Leonardo Viana** — his smart-contract mentor, thanked by name | "Thanks to Leonardo Viana for all the help provided since I started studying smart contracts!" | mentorship, credits | **1 in 10 — a personal credit; smart-contract pieces only** `[2022-offreg]` |
| D19 | **MoSCoW · Given/When/Then · Figma** — his named scoping/QA/prototyping instruments | "MoSCoW creates a shared language to keep v1 focused" · "Use simple Given/When/Then for your chosen happy path and two edge cases" | scoping, QA | 1 in 5 `[2025-offreg]` |
| D20 | **Legacy estimation vocabulary he names in order to critique it** — Work Breakdown Structures, Function Points, Lines of Code, story points, velocity | "metrics like Function Points or Lines of Code, applying mathematical formulas that promised precision but often delivered disappointment" | estimation | 1 in 5 `[2025-offreg]` |
| D21 | **Kmino** (his software house) and **Lunos** (the client behind B9/B10) | "This article was written for Kmino's blog, my new Software house." (Aug 2025 — the "new" framing is now dated) | company, CTA | Gated: `markers: employer-beat`. 1 in 4 as a CTA, and only when the fact-sheet names it `[2025-offreg]` |

---

## Corpus honesty

This bank is mined from **8 posts across 3 eras** (5 × 2020, 1 × 2022, 2 × 2025), roughly 10k words total.
That is small. The stance map is therefore **narrow, not comprehensive** — it records what he wrote down,
not the full shape of what he thinks. Absence from this file is **not** evidence that David disagrees with
something; it is evidence that the corpus does not cover it. When a piece needs a position this file does
not hold, use the piece's own material and say nothing in David's name.
