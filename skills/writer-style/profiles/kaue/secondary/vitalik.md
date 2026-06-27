# Writing Craft Profile — distilled from Vitalik Buterin

> **Lane — derivation, sustained.** *Reconstruct the path to the idea:* anchor the status-quo limit, rule
> out the naive fixes in tiers, define precisely, answer the sharp objections, and keep deriving the
> tradeoffs and failure modes — never stop at the one-liner. **Leads** deep-tech / protocol-internals /
> mechanism-design pieces. (Reframes and *keeps going*, the opposite of Hotz, who collapses and stops.)

*Captures the **transferable craft and intellectual quality** that make his explanations excellent —
how he thinks, teaches, reasons, and structures. It is **not** a voice impersonation: this profile is
applied in YOUR voice to produce ORIGINAL work. Surface idiolect (his punctuation habits, signature
phrases, openers, personas) is deliberately excluded. See the note at the end.*

**What to lift from him specifically:** he **reconstructs the path to an idea** instead of stating it, and
once he reframes a problem he *keeps deriving* its consequences rather than stopping at the one-liner. The engine:
anchor in the status quo and its concrete limit → surface the motivating question → rule out the naive
answers first → define precisely → answer the sharp objections → ground in numbers and structure-carrying
analogy → situate in the larger arc. Around it: steelmanning, "compared to what?", paired-cost tradeoffs,
calibrated confidence, and *building the vocabulary the reader needs to think with*. The craft below is a
menu; pull what serves the lesson.

---

## 1. The explanatory method — the question-ladder (core engine)
Make a hard idea understood by reconstructing the *path* to it, not just stating the conclusion:
1. **Anchor in the status quo and name its concrete limitation**: start from how things work now and
   the specific pain, ideally with a number ("Bitcoin ~3–7 tx/sec because every node processes every
   transaction"). The anchor exists to *expose the limit that provokes the question* (status quo →
   friction → question), not to build a teaching bridge to an analogue — that latter move is Helius's.
2. **Surface the motivating question** the reader would naturally ask, and pivot the whole piece on it
   ("if two transactions touch separate accounts, why should one wait for the other?").
3. **Rule out the naive solutions first, in tiers.** List the obvious "easy answers," give each its
   fatal flaw, *then* the real one. Showing why the obvious fails builds the *need* for the mechanism.
4. **Introduce the mechanism with a precise definition** of the load-bearing idea, just-in-time.
5. **Anticipate the objections** a sharp reader would raise, and answer them in turn.
6. **Ground everything in concrete numbers and a structure-carrying analogy.**
7. **Situate the idea in its larger arc** (history, roadmap, where it's going).

*Design move (before writing):* draft the **literal ladder of questions** a learner climbs from naive to
subtle, where *each rung is the objection the previous answer provokes* — that ordered list can become
your section headers; the prose just answers them in turn.

*Reframe-then-keep-deriving (his edge over a pure compressor):* a sharp reframing ("a more useful way to
think about X is Y") is a *launch point*, not a destination. Once it lands, spend the new frame — derive
its consequences, failure modes, numbers. Never stop at the one-liner.

## 2. Teach difficulty in stages
- **Simplify first, then add back the complexity you hid, out loud.** Teach a deliberately partial
  version ("for simplicity, this design tracks data blobs only"), let it land, then say "now, in reality,
  here's what that left out" and resolve it.
- **Derive through one concrete worked instance before generalizing,** then extract the principle ("so
  what we just did is…"). Often follow with **"what can we learn from this more generally?"**, lift the
  transferable lessons, and *test them against several more cases* to show they hold.
- **Ladder intuition → toy numeric example → formal statement,** treating any formula as a *compression of
  something the reader already pictures* (derive "quadratic" from "your n'th vote costs $n" → triangle
  area → n², and tell the reader the intuitive version is the one to keep).
- **Recap after a hard stretch** with one plain-language restatement before the next layer; close with a
  bulleted summary that re-states each load-bearing claim.
- **Drop register deliberately when the math gets thick**: flag it ("this part is mathier; skip ahead if
  you like"), or hand over a frankly simplified picture to reset, then climb back. Mark such a picture *as*
  the simplification so it isn't mistaken for the mechanism.

## 3. Abstraction & analogy
- **Motivate before you define;** drop to the concrete the moment the abstraction gets thin, then climb back.
- **Use analogies that carry the actual *structure* of the idea** (the relationship, not the vibe) and
  **flag where the analogy breaks** so it's never mistaken for the mechanism ("a 1-of-N system can *feel*
  like 1-of-1 because you go through one actor — but if yours disappears you just switch to another").
- **Build a named taxonomy/vocabulary as the thinking tool, then reason *inside* it.** Coining the right
  categories *is* the explanation: lay out the spectrum (e.g. trust as 1-of-1 / N-of-N / N/2-of-N / 1-of-N
  / few-of-N / 0-of-N), then *place* every example in that frame. Define a category by its **extremes/edge
  cases** before the realistic middle; tabulate options when comparing.
- **Name the core tension and reason in resource terms.** Give the central tradeoff or trilemma a crisp
  name so the reader carries a durable handle; then fix a couple of variables (e.g. "c = resources per
  node, n = size of the ecosystem") and re-express every property and cost in them, turning vague "it
  scales" claims into checkable ones.

## 4. Reason with intellectual honesty
- **Calibrate confidence to evidence**: let firm and tentative claims coexist, each marked for how
  strongly it's held; when you hedge, still say which way you lean and why.
- **Flag a bold claim's strength before defending it,** then give the single strongest reason to take it
  seriously (and, where you can, an exact figure or worked case).
- **Steelman the opposing view, and grant its valid part by name *before* you refine it.** Quote or name
  the strongest critic, concede "these are real concerns; I've had them myself," *then* show what the
  picture misses. Treat even a position you reject as "coherent on its own terms."
- **Judge against the realistic alternative: "compared to what?"** Never evaluate in isolation; always
  anchor to the concrete baseline ("this is barely better than just spinning up that many separate
  chains"; "42,000 gas versus the 21,000 of a basic transaction").
- **Separate average-case from worst-case explicitly.** A mechanism that "works well in the average case
  but fails catastrophically in the worst case" is a *different* object from one that degrades gracefully —
  say which, and name the worst case concretely.
- **Build to conclusions through visible steps** rather than asserting them; show the reasoning that
  forces the result.
- **Earn authority from concrete specifics,** including your own changes of mind ("this *is* a shift from
  how I thought about it in 2021") and real artifacts you've touched.

## 5. Quantify honestly
- Express improvements as **ratios against a named baseline**, and state the **paired cost in the same
  breath** ("~100x more throughput, but the security threshold drops from 50% to ~30–40%").
- **Itemize a cost when it's the crux.** When a number is the whole argument, break it into its parts (the
  per-field byte budget; the gas line items that sum to the overhead) so the reader sees *where it comes
  from*, not just the total — then the comparison becomes self-evident.
- **Ranges for estimates, exact values for known constants**: don't fuzz a number you actually know,
  don't fake precision on one you don't; flag which is which.
- **Put the comparison in a table** when more than two options vary on more than one axis: one row per
  option (or property), with the tradeoff cell shown, not hidden.

## 6. Structure to fit the goal
- **Match the shape to the intent:** a cascade of the reader's escalating questions for an explainer;
  *problem → naive attempt → why it breaks → refined solution* for a design; *claim → strongest objection →
  resolution* for an argument; *several distinct paths converging on one destination* when you want to show
  a conclusion is robust to which assumption turns out true.
- **Manage the reader's mind:** state assumed knowledge up front; define terms just-in-time, not in a
  front-loaded glossary; put motivation ("why care") before mechanism; keep paragraphs short and one-idea.
- **End by dissolving the fuzziness, not just summarizing.** A strong close often hands the reader a
  *diagnostic question set*, "next time someone says X, ask them: do they mean A, B, or C?", converting
  the lesson into a tool they can re-use.

## The signature strengths (what this author does better than most)
- **First-principles derivation, sustained**: rebuilds an idea from the ground up so the reader owns
  *why*, and keeps deriving *after* the reframing instead of stopping at a slogan.
- **Question-driven momentum**: advances by voicing and answering the reader's next real objection, in order.
- **Frameworks you can think with**: leaves the reader a named vocabulary/taxonomy, not just a fact.
- **Rigorous fairness**: the most generous, accurate version of every position, opponents' included,
  with the valid part granted before the rebuttal.
- **Honest tradeoff reasoning**: no free lunches; every gain named with its cost, its uncertainty, and
  its worst case.

## Generation guidance (+ worked example, in neutral original voice)
**To apply this craft to a Solana lesson:** walk the §1 ladder: status quo + concrete limit → motivating
question → naive fixes ruled out in tiers → precise definition → structure-carrying analogy with its limit
flagged → the 2–3 real objections → paired-cost tradeoff. If you reframe, *keep going* and derive the
consequence; don't stop at the slogan. Write it in *your* voice — the craft is scaffolding, not wording.

**Worked micro-example — Sealevel: why pre-declaring accounts is necessary:**
> Most blockchains run transactions one after another, in a single line. It's easy to reason about, but it
> wastes the hardware: a modern processor has many cores, and a single-file queue uses exactly one. So the
> natural question is: if two transactions touch entirely separate accounts, why should one wait for the
> other at all?
>
> The naive answer, "just run everything at once", fails the instant two transactions touch the *same*
> account, where a hidden double-spend could slip through. The next-most-naive, "let the runtime notice
> the conflict mid-execution", fails too: by the time you discover the clash you've already paid for work
> you must now throw away. So the real question is narrower: how can the scheduler know, *before* running
> anything, which transactions are safe to run together?
>
> That narrowed question forces the design. To sort transactions into "can run in parallel" and "must be
> ordered" *before* executing, the scheduler needs each transaction's read/write set *before* executing —
> so Solana requires every transaction to declare, in advance, the accounts it will touch and whether each
> is read or write. With that list the runtime works like a database query planner: non-overlapping
> transactions run on separate cores, and ones that share a writable account get serialized.
>
> The payoff is real but not free. Throughput now scales with cores instead of being capped at one. But
> the developer must know the full account list ahead of time, which is awkward when one account's address
> depends on what you read from another, and over-declaring writes needlessly blocks other transactions
> from running beside yours. That single up-front-information requirement is the seed from which most of
> Solana's program-design constraints grow.

*(Craft used: status-quo + limitation → motivating question → naive fixes ruled out *in tiers* →
reframe-then-keep-deriving (the narrowed question forces the mechanism) → precise read/write-set definition
→ structure-carrying analogy (query planner) → paired-cost tradeoff → larger arc. No borrowed phrasings,
punctuation tics, or personas, the reasoning quality only, in a neutral voice you can make your own.)*

---
## What this profile deliberately EXCLUDES
The point is original writing, so the author's surface idiolect is **not** captured and should **not** be
reproduced: his connective/hedging tics ("kind of," "in expectation," "to be precise," "waaaay," trailing
"but we'll get to it :)"), the rhetorical-question header style and FAQ self-interview as a *verbal
signature*, ritual "Special thanks to … for feedback and review" openers, the em-dash-and-aside cadence,
and the recurring in-group examples and personas (Alice/Bob, the "I'm 12 years old" bit, Ethereum-specific
name-drops). Keep the derivation engine and the intellectual honesty; drop the fingerprints.
