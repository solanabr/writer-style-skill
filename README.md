![Writer Style Skill — generate human text with writer authenticity, quirks and thought patterns](assets/banner.png)

# Writer-Style

A Claude Code skill for writing **original** educational and long-form technical content in a **specific author's
voice** — without sounding like generic AI, and without getting the facts wrong.

It ships with the **`kaue` pack** (Kaue / Superteam Brazil, tuned for Solana/Web3 education) as the default,
but the engine is voice-agnostic: a *pack* supplies the voices, and you can build new ones.

## The idea

Two layers, plus a correctness guarantee:

1. **A primary voice** — the target author's own (Kaue), **always on**. Its idiolect is **reproduced** (the
   quirks are what make it sound like them).
2. **Secondary voices** — transferable *craft* borrowed from five master writers, with their surface idiolect
   **stripped**. One leads, chosen by the piece's **job**; you apply the craft *in Kaue's voice*, never as
   impersonation.

| Lane | Voice | Leads |
|---|---|---|
| structure & evidence | **helius** | practical how-to / integration / the real artifact |
| derivation, sustained | **vitalik** | deep tech / protocol internals / mechanism design |
| framing & scope | **balaji** | broad, interconnected theses |
| engagement & stamina | **hayes** | macro / markets / geopolitics / tokenomics |
| compression & collapse | **hotz** | demystification ("X is just Y", honestly) |

3. **Facts first, voice last.** Because voice prompting degrades factual accuracy, technical content is
   **established and verified in neutral prose first**, then restyled into the voice — which may never alter a
   number, code line, or API. A fact-preservation diff enforces it.

And a **naturalness floor** runs on every piece: write unevenly, a human seam in every passage — because even,
uniformly-polished prose is the #1 tell that a machine wrote it.

## The voices, same fact

One frozen fact, *Proof of History is a hash chain that acts as a clock: it settles the order of events without
messaging, and does **not** do consensus or judge validity*, rendered through each lens below. The facts stay
fixed; only the craft changes. Every passage clears `validate_voice.py` against its register's card (zero hard
tells, zero em-dashes, varied cadence). Click any voice to expand.

<details>
<summary><b>kaue</b> &nbsp;·&nbsp; <i>primary voice: felt, uneven, a human seam</i></summary>

The hardest thing for a thousand computers to agree on isn't who did what. It's *when*. Normally they'd message each other back and forth just to settle the order of events, and that chatter is most of what makes a chain slow.

Proof of History skips the argument. One node runs a long chain of hashes, each step feeding the next, and the sequence itself becomes a clock anyone can read. You don't trust a timestamp, you re-run the math and check that this came before that.

It doesn't pick winners or decide what's valid; that's a separate job. It just settles order, cheaply, before consensus starts. Take that fight off the table and the speed kind of explains itself.

</details>

<details>
<summary><b>helius</b> &nbsp;·&nbsp; <i>structure & evidence: show the artifact, quantify, name the boundary</i></summary>

Proof of History is a single append-only sequence of SHA-256 hashes. Take the previous output, hash it again, and again, each result is proof the one before it existed. Count the iterations between two hashes and you've measured elapsed time, because there's no way to produce them out of order.

The leader stamps each new transaction into this sequence as it arrives, so every transaction inherits a verifiable position in time with zero coordination messages between nodes. Generating the chain is strictly serial; verifying it is not, a validator splits the checks across cores and confirms the whole record fast.

One boundary worth stating plainly: PoH orders events and proves duration. It does not decide validity or finality. Tower BFT handles consensus on top of the clock it provides.

</details>

<details>
<summary><b>vitalik</b> &nbsp;·&nbsp; <i>first-principles derivation: rule out the naive fixes, price the cost</i></summary>

Start with the constraint. A distributed system has no shared clock, so the instant you want to agree on the order of events, the naive options are both bad: trust each machine's wall clock, which drifts and forces you to trust the machine, or exchange messages to agree a timestamp per event, which costs a network round-trip every time and buckles under load.

The reframe is to stop treating time as something you *read* and start treating it as something you *prove*. Build a computation where each step strictly depends on the one before, a hash chain nobody can fast-forward, and producing N steps is itself evidence that a knowable amount of work, and therefore time, has passed. Order becomes a byproduct of the computation rather than a thing you negotiate.

The cost is real and worth pricing. The sequence must be produced serially, by one leader at a time, so you've converted a coordination problem into a liveness assumption. What you buy for it is ordering without messaging, and verification that parallelizes even though generation cannot.

</details>

<details>
<summary><b>balaji</b> &nbsp;·&nbsp; <i>framing & scope: extend one analogy, bound the pillar, place the lineage</i></summary>

Picture a thousand clerks in one hall, each with their own wristwatch, trying to file events in order. Before anything gets recorded they have to reconcile whose watch is right, and that reconciliation, not the filing, is the real work.

Proof of History is the time zone of a blockchain: one agreed clock everyone reads from, so no clerk negotiates a timestamp again. Push the analogy one step and it pays off. Just as a shared time zone lets distant offices schedule without a phone call, a shared hash-clock lets distant nodes agree on order without a round of messages.

It's one pillar, and worth bounding honestly: it orders events, it does not judge them or choose who writes the next page. On a longer arc it's the next move in a lineage that runs from Lamport clocks through verifiable delay functions, the same old problem, finally made cheap.

</details>

<details>
<summary><b>hayes</b> &nbsp;·&nbsp; <i>engagement & stamina: a metaphor spine, the stake, a round-number walk</i></summary>

Think of a notary sitting beside a printing press, stamping a number on every sheet the instant it comes off, where each stamp is mathematically welded to the one before it. That notary is Proof of History, and the stake for you is direct: it's why your transaction lands in a blink instead of waiting for the network to take a vote on what time it is.

Here's the route. The leader runs a hash, then hashes that result, then again, forever, say it's on hash one million when your transaction shows up. It stamps your transaction at one million and rolls on. Anyone, later, can recompute from nine hundred thousand up to one million and confirm: yes, this happened here, in this order, and real time passed to get there.

The press keeps printing whether or not the room agrees on anything else, and that's the whole point. Ordering stops being a meeting. It becomes a stamp you can check, and the network keeps pace.

</details>

<details>
<summary><b>hotz</b> &nbsp;·&nbsp; <i>compression & collapse: unhedged reframe, a visible therefore-chain, stop</i></summary>

The best way to think about Proof of History is a clock you can't fake.

Here's the chain. Each hash takes the previous hash as input, so you can't compute step one million without computing the 999,999 before it. No shortcuts. No parallel speedrun. Producing the sequence costs real, sequential time, so the sequence is a proof that time passed, and a transaction's position in it is a proof of when. How would you forge an earlier slot? You'd need a hash preimage. You can't.

So order isn't something the nodes vote on. It's settled by the math before voting starts. Consensus still picks the canonical fork (PoH was never doing that), but it never argues about time. Build the clock once, everything downstream gets cheaper.

</details>

### …and how they actually ship: primary + secondary

The pure lenses above are illustrative. In real use **kaue's voice is always on** and a secondary rides *on top*
of it: his seams kept, the secondary's idiolect stripped. That inversion, reproduce the primary's voice and
borrow only the secondary's craft, is the whole skill.

<details>
<summary><b>kaue + helius</b> &nbsp;·&nbsp; <i>his voice, helius's show-the-artifact craft</i></summary>

The first time someone showed me Proof of History I wanted the actual thing, not the metaphor. So here it is: it's a loop. Take a hash, feed it back in, hash it again, SHA-256, over and over, and the count of how many times you've done that becomes your clock. You can't fake the count, because you can't run the loop out of order.

The leader stamps each transaction into that running sequence as it arrives, so every transaction gets a verifiable spot in time and nobody had to send a message to agree on it. Producing the chain is strictly one-at-a-time. Checking it isn't, since a validator splits the work across cores and verifies the whole record fast. That asymmetry is the trick: slow to build, cheap to trust.

One thing it doesn't do, and I'd rather you hear it from me: it doesn't decide what's valid or which fork wins. That's consensus, a separate machine sitting on top. PoH just hands everyone an honest clock. Build on that and a lot of the usual coordination cost quietly disappears.

</details>

<details>
<summary><b>kaue + vitalik</b> &nbsp;·&nbsp; <i>his voice, vitalik's rule-out-the-naive-fixes derivation</i></summary>

Start where the problem actually starts: a bunch of computers with no shared clock, trying to agree on what happened first. The obvious fixes both fail. Trust each machine's wall clock and you've trusted the machine, and clocks drift anyway. Have them message each other to agree a timestamp, and you've bought a network round-trip for every single event, which falls apart the moment things get busy.

So you change the question. Stop asking the network to tell you the time and make time something you can prove. Run a hash chain where each step needs the one before it, and producing a million steps is itself evidence that real, sequential work happened. Order stops being a negotiation and becomes a side effect of the math. Keep going, because the interesting part is the bill: the chain has to be produced serially, by one leader at a time, so you've traded a coordination problem for a liveness assumption.

That's the honest shape of it. You don't get ordering for free, you move the cost somewhere you can live with, and you get something nice back, that anyone can verify the whole clock in parallel even though only one party could build it. Not a free lunch. A good trade.

</details>

## Installation

| Method | Command | Scope |
|---|---|---|
| **Plugin** *(recommended)* | `claude plugin marketplace add solanabr/writer-style-skill` → `claude plugin install writer-style-skill@stbr` | every project |
| **npm** | `npm add @stbr/writer-style-skill` | the current project |
| **Clone** | `git clone https://github.com/solanabr/writer-style-skill` | run from the repo |

**Claude Code plugin** — the zero-config path; the skill, agents, and commands load in every project:

```bash
claude plugin marketplace add solanabr/writer-style-skill
claude plugin install writer-style-skill@stbr
```

(or, inside Claude Code: `/plugin marketplace add solanabr/writer-style-skill`, then `/plugin install writer-style-skill@stbr`)

**npm** — vendors the self-contained skill into the current project's `.claude/` (skill + agents + commands):

```bash
npm add @stbr/writer-style-skill          # alias of: npm install @stbr/writer-style-skill
```

The `postinstall` does the copy. To install without adding a dependency, or after `npm install --ignore-scripts`:

```bash
npx @stbr/writer-style-skill
```

**Clone and use** — for development, or to build your own voice pack: work from the repo root; `$SKILL` resolves to `skills/writer-style/`, and every command and agent reads its data and tools from there.

**Requirements:** Python 3 (standard library only) for `skills/writer-style/tools/validate_voice.py`. No other runtime dependencies.

## How to use it

- **Write:** `/write-in-voice` (or the **voice-writer** agent) — runs the facts-first 3-pass workflow.
- **Build a voice:** `/new-persona` (the **persona-builder** agent) — the adversarial, evidence-bound process.
- **Validate:** `/validate-voice` (the **voice-validator** agent) — fact diff + AI-tell lint + repetition audit.

Start at [skills/writer-style/SKILL.md](skills/writer-style/SKILL.md).

## How it was built

Each voice is distilled from a real corpus through an adversarial, multi-pass process (parallel lens-miners →
opposed judges → for the primary, a generate-and-blind-compare pass), not a one-shot "describe the style." The
corpus is cleaned hard first (HTML artifacts, newsletter chrome, and guest-reposts by other authors removed).
The writer-facing **style-cards** carry only dials a writer can actually act on (sentence-length spread,
readability band, hedge/boost lean, example/code density, favor/avoid word lists) — the raw stylometry is
walled off in `evidence/` for the builder and validator. The strongest signal is the **exemplar bank**: real
on-register passages, one per rhetorical slot. See [skills/writer-style/authoring-personas.md](skills/writer-style/authoring-personas.md).

## Honest scope

This produces content **in Kaue's register, with AI tells engineered out and facts verified first** — *not* an
indistinguishable voice clone. The primary voice is calibrated from a small on-register sample (4 technical
posts); fidelity is corpus-bounded and improves as more of his on-register writing is added.

## Tools

`skills/writer-style/tools/` is pure-Python (stdlib only, no network): `profile_corpus.py` (cleans + profiles a
corpus → builder-internal evidence + card dials), `validate_voice.py` (the Pass-C gate: a fact-preservation diff
that hard-fails a mutated value, an AI-tell + tiered-deslop lint, a sentence-cadence floor, and a cross-lesson
repetition audit), `style_lexicons.py` (shared tokenizers + the gated cliché lexicons). Run `python3
skills/writer-style/tools/test_tools.py` to verify.

## License

MIT — © 2026 Superteam Brazil. See [LICENSE](LICENSE).
