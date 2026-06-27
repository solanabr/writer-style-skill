# The writing workflow — facts first, voice last

The empirical reason this skill is structured the way it is: **persona/voice prompting improves alignment and
style but measurably degrades factual accuracy.** For brand copy that's harmless; for **technical Solana
content a wrong number or renamed instruction is the worst possible output.** So the rule is absolute:

> **Voice is the last transform over verified facts — never the medium in which facts are discovered.**

Write the facts in a neutral register, freeze and verify them, *then* restyle. Five steps.

---

## Pass A — Facts (voice OFF)

Produce the lesson's substance in **plain neutral prose**, no persona loaded:
- the outline / section order,
- every **claim, number, unit, address, CU/lamport figure, account size, version-sensitive API**,
- any **code** (commands, structs, instructions), exactly as it must appear.

**Ground against sources, not memory.** The Solana ecosystem moves faster than any training cutoff. Use the
doc MCPs:
- `solana-dev` (`Solana_Documentation_Search`, `get_documentation`, `Solana_Expert__Ask_For_Help`, and
  `program_autofixer` for any Rust program code),
- `context7` for library/SDK/API specifics (Anchor, web3.js/kit, SPL, etc.),
- Helius MCP for live chain reads when a current on-chain number is part of the claim.

**Output: a fact-sheet**, terse bullets/statements with the load-bearing numbers and code. This is the source
of truth Pass B may not contradict.

## Gate — Verify (before any styling)

Fact-check the fact-sheet. It's cheap precisely because the facts are terse and not buried in warm prose:
- numbers/units against the docs; code against `program_autofixer` / the SDK;
- flag anything unverifiable and either resolve it or cut it.
- **Scope the frozen fact-sheet to the claims THIS piece will actually assert.** Pass A gathers everything
  to verify it; before freezing, drop the facts the piece won't use (background SIMD numbers, source
  filenames, every instruction name). The Pass-C `diff` reports a sheet fact absent from the lesson — it
  only *hard*-fails a genuine **mutation** (a value changed), but a tightly-scoped sheet keeps that report
  signal, not noise.
- The human author is the final gate. **Nothing proceeds to voice until the facts are frozen.**

## Pass B — Voice (restyle, don't re-derive)

Now load the pack:
1. **Primary**: `profiles/kaue/kaue.md` + `kaue.card.yaml` (always).
2. **Route** the dominant *job* → pick the backbone secondary (+ ≤1 guest on a different lane). See
   `profiles/kaue/ROUTING.md`.
3. **Exemplars**: load ~4 from `exemplars/kaue/`: **always the `seam`**, plus `opener` + `close` + 1 body
   slot by job; plus the routed secondary's move-demos.

Then **restyle the frozen fact-sheet into the voice.** The instruction to hold in mind:

> **Rephrase around the facts; never change them.** Every number, code line, and named API in the fact-sheet
> is frozen. You are choosing words, rhythm, hooks, seams, and structure, not re-deriving the content.

Apply the **naturalness floor** (`rules/naturalness.md`): write unevenly, enthusiasm at the edges, a human
seam in every passage, the body calm and a little loose. This is where the voice lives, and where a naive
"write it all in one pass" would let persona drift corrupt the numbers. It can't here, because the numbers are
already fixed.

## Pass B.5 — Blind-compare (the anti-impostor check)

The most likely failure isn't wrong facts (Pass C catches those) or AI tells — it's prose that's competent,
even, on-register, and follows every rule, yet reads like *someone who studied Kaue's checklist*, not Kaue.
The persona-builder catches this with a generate-and-blind-compare pass; the writer needs the same forcing
function. Before linting, re-read the draft against the **loaded exemplars only** (the always-loaded seam +
the opener, **never the corpus**; at write-time the corpus is pure token-waste) and ask: *would a blind
reader say this is Kaue, or a rule-follower?* Rule-follower tells: a definition-led open instead of a felt
scenario, even cadence, the same seam every section, no loose run-on or hedge, enthusiasm spread evenly. If
it reads that way, regenerate toward a pain-first felt opener, uneven rhythm, a rotating seam per passage, a
loose body, and at most one civilizational analogy. Match the exemplars' *texture*, not their topic.

## Pass C — Lint (catch styling damage)

Run the checks (`tools/validate_voice.py`, or the **voice-validator** agent):
- **`diff`**: fact-preservation: every number/identifier in the fact-sheet must survive into the styled
  output unchanged. A mutated `0.002 SOL`, a renamed `transfer_checked`, a changed `1232` → **hard fail**,
  rewrite that sentence.
- **`tells`**: AI-tell lint: banned words, "not X, it's Y" overuse, em-dash overuse, **uniform cadence**
  (sentence-length stdev below the floor, the top human-vs-AI signal).
- **`audit`**: for a multi-lesson batch: opener-type diversity, duplicate openings, cross-lesson n-gram
  overlap (catches "every lesson sounds the same").

Then a **human read** for voice fidelity, the one thing no metric judges honestly (style-distance scorers
manufacture false confidence; we don't ship one).

---

## Why this ordering wins
- **Correctness is protected**: voice can't invent or alter a fact it never touched.
- **The fact-check is cheap**: terse neutral statements, not facts hidden in prose.
- **The voice is freer**: Pass B can be as warm and uneven as the author really is, because it's operating on
  locked content. The trade is deliberate: voiced-from-scratch would sound marginally more like the author and
  be more likely wrong; restyle-over-verified is the right call for technical teaching.

## Drafting from scratch vs editing
- **From scratch:** run A → Gate → B → C.
- **Editing/restyling existing copy:** treat the existing draft's verified facts as the fact-sheet (extract +
  verify them first), then B → C. Same guarantee: facts frozen, voice applied last.
