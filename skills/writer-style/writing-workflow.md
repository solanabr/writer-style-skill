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
2. **Marker gate check**: read the card's `markers:` block; decide per marker whether THIS brief earns it
   (identity/community markers need their `gate` keywords genuinely in the fact-sheet). Write the **marker
   budget ledger** before drafting — live markers with budgets, gated-off ones at `—` with their `fallback`.
3. **Route** the dominant *job* → pick the backbone secondary (+ ≤1 guest on a different lane). See
   `profiles/kaue/ROUTING.md`.
4. **Exemplars**: load ~4 from `exemplars/kaue/`: **always the `seam`**, plus `opener` + `close` + 1 body
   slot by job; plus the routed secondary's move-demos. Exemplars are **rhythm donors, never content
   donors** — their examples/analogies don't transfer to new topics; substance comes from the bank.
5. **Substance bank**: scan `profiles/kaue/themes.md` for items whose tags match the brief; shortlist ≤3
   into the fact-sheet (verify their numbers like any fact). Prefer a fitting bank item over exemplar
   content; never force one; respect `burn: high`.

Then **restyle the frozen fact-sheet into the voice.** The instruction to hold in mind:

> **Rephrase around the facts; never change them.** Every number, code line, and named API in the fact-sheet
> is frozen. You are choosing words, rhythm, hooks, seams, and structure, not re-deriving the content.

Apply the **naturalness floor** (`rules/naturalness.md`): write unevenly, enthusiasm at the edges, a human
seam in every passage, the body calm and a little loose. This is where the voice lives, and where a naive
"write it all in one pass" would let persona drift corrupt the numbers. It can't here, because the numbers are
already fixed.

## Course mode (when a curriculum exists)

A course lesson is not a standalone post. The brief carries a `context:` block — series, position N of M,
previous/next lesson titles, what's already covered. It changes three things: **closers** (point to the
actual next lesson or plain-close; sequel-teasers and "want me to cover X next?" are FORBIDDEN — the
next part is already scheduled), **openers** (continuation opens — "last lesson we X" — are available
mid-course; credential-disclaimer opens stop making sense once the teacher's authority is established),
and **substance** (a bank anecdote burned by lesson 2 is unavailable to lesson 7 — the batch ledger
tracks spends). For a batch/course, a **coordinator pass** deals each piece its mood, opener family,
closer family (or none), and marker spends BEFORE writers start — parallel writers can't see each other,
and uncoordinated rotation reproduces the stamp one token over (measured: 'cya' 4/8 in Round 1).

## Pass B.75 — Fresh-eyes revision (a different reader, bounded edits)

The writer re-reading its own minutes-old draft fills gaps from memory and feels every ending as earned —
self-review is anchored. A **separate reviser** with a deliberately clean context (the draft + the loaded
exemplars + LESSONS.md only — no brief, no fact-sheet, no ledger) reads as the blind reader and makes
**≤5 bounded edits**: cut stacked closing gestures to one, fix the stiffest sentence, merge bullet-rhythm
paragraphs, kill a compliance-tell. Never touch numbers, commands, code, or claims. Re-run `diff` after —
the fact gate still stands. Editing beats regenerating: keep 90%, fix 10%; a re-roll re-runs the whole
fact-risk surface and may lose what worked.

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

## Long-form mode (≥1,200 words)

Repetition compounds with length — a cap that "feels fine" per section stamps the piece by section six.
Two mechanics keep a long piece honest:

**1. Per-piece caps do NOT scale with length.** A 3,000-word piece still gets ONE identity beat (stakes or
close, gate permitting), ONE civilizational analogy (on the hardest concept), ONE anaphora burst, ONE
sign-off. Only per-word budgets (`per_words:` markers like triads or false-antithesis) scale. This is the
anti-compounding rule: if caps scaled, long-form would be maximally idiosyncratic exactly where restraint
matters most.

**2. The marker ledger.** Draft section-by-section; after each section, update the ledger and re-read the
previous section's final paragraph before starting the next (the mechanical defense against seam/opener
repeats that one-shot generation can't give). The ledger ships with the deliverable:

```
Ledger — 2,400w, 6 sections. Gates: identity=PASS (brief is adoption economics)
S1 open:   opener=pain-felt-number · seam=confession   · markers: —
S2:        shape=flat-mechanics    · seam=real-number  · markers: —            [plain]
S3:        shape=warm-reasoning    · seam=tool-credit  · markers: coined-handle 1/1
S4:        shape=flat              · seam=real-number  · markers: —            [plain]
S5 stakes: shape=zoom-out          · seam=named-credit · markers: identity 1/1, analogy 1/1
S6 close:  vision→encouragement→door · sign-off 1/1    · markers: —
```

Distribution rules across the piece: no marker lexeme twice within any ~800-word window; no seam type
twice within 3 consecutive sections; each section's opener type differs from the previous two; the
plainness quota (≥1 in 3 sections marker-free) and the enthusiasm topology (edges hot, middle ~60% ≤1
spike) from `rules/naturalness.md`.

## Pass C — Lint (catch styling damage)

Run the checks (`tools/validate_voice.py`, or the **voice-validator** agent):
- **`diff`**: fact-preservation: every number/identifier in the fact-sheet must survive into the styled
  output unchanged. A mutated `0.002 SOL`, a renamed `transfer_checked`, a changed `1232` → **hard fail**,
  rewrite that sentence.
- **`tells`**: AI-tell lint: banned words, "not X, it's Y" overuse, em-dash overuse, **uniform cadence**
  (sentence-length stdev below the floor, the top human-vs-AI signal).
- **`density`** (with `--facts <fact-sheet>`): marker budgets + context gates. An identity marker firing
  with no gate keyword in the fact-sheet = **hard fail** (the forced-insertion case); a doubled sign-off =
  **hard fail**; over-budget tics, clustering, and section spread are advisories the human gate weighs.
- **`audit`**: `--file <doc>` for one long piece (section-to-section opener variety, intra-doc n-gram
  overlap, duplicate paragraph openers); `--lessons <dir>` for a multi-lesson batch (catches "every lesson
  sounds the same").

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
