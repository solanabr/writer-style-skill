# The Router — david pack

> **One secondary: `helius`, scoped.** Primary is always on. `helius` is the single licensed guest, and it is
> licensed for its **evidence layer only** — never its structure. Every piece routes to
> `david.md` + `david.card.yaml` + `themes.md` + ~4 exemplars, plus `helius` when the piece is technical.
> The routing decisions are **which register mode**, **which exemplars**, and **whether helius is on**.

## 1. The roster: why `helius`, why scoped, and why nothing else

The pack's live use is **online course material for Solana**. That is code-bearing technical teaching, and
the david corpus contains **0 fenced code blocks and 0 inline code spans in ~3.7k words** — the code register
is entirely unevidenced here. Something has to carry it, and inventing a code voice out of a corpus that has
none would be fabrication. `helius` is the correct donor: its own lane header calls it *"the safe universal
guest"*, its craft is *"make the system navigable and every claim checkable"*, and it is the engine's
designated lead for practical Solana how-to and integration writing.

**What helius supplies (licensed):** the real struct or number on the page walked field by field · units on
every quantity · terms glossed inline at first use · claims traceable to something checkable · the technical
accuracy layer for anything Solana-specific.

**What helius must NOT supply (banned, measured):** its **structural** layer — numbered step lists, scannable
step scaffolds, bulleted procedures. This is not a taste call. In the 70/30 validation run, importing
helius's numbered-list structure cost **4.2 Flesch-Kincaid grades** (9.1 → 4.9) and 5 words of median
sentence length (17w → 12w); converting the same content to David's prose enumeration recovered it to FK 7.0
at 18w median with no other change. **David enumerates in prose** — *"First, archiving everything that I
already addressed…"* (exemplar 02) — and the corpus has no numbered procedure anywhere. Lists are the single
measured way this blend goes wrong. Keep them rare and short; prefer `First, … Then, … After that, …` chained
additively across full sentences.

**Weight.** Roughly **85 primary / 15 helius by volume** — helius is a layer, not a backbone. If a draft
reads navigable but flat, helius is over-weighted; the tell is short declarative steps and a missing run-on.

**Why no other secondary.** The two other obvious lanes contradict the voice rather than dosing it wrong. A
derivation backbone raises altitude, but David establishes authority by *downgrading* his credentials and
sourcing confident claims to a book or a personal trial. A framing/analogy backbone imports analogy as a
reasoning mode — measured at **0.0/1k** here, with the ban extending to figurative verbs. Adding either is a
contradiction, not a blend. Cap stands at **primary + helius = 2 layers**.

**Standing caveat.** The primary is 3.9k words deep with a fragile seam class, and a guest layer smooths
prose by definition. Helius earns its place because it covers a register the corpus genuinely lacks; it does
not get to touch registers the corpus already has. When a piece is *not* technical — a PM artifact, a
retrospective, a motivational course opener — **run primary-only** and say so in the manifest.

## 2. The decision procedure (end to end)

1. **Always-on:** the David primary. It carries the whole piece — tone, register, seams, closer.
2. **Decide whether `helius` is on.** On when the piece is technical: Solana mechanics, code, an API or
   struct, an integration step, anything the reader will run. Off for PM artifacts, retrospectives,
   motivation and course openers. When on, it contributes the evidence layer **only** (§1) — and if you
   catch yourself reaching for a numbered list, that is helius leaking past its licence.
3. **Pick the register mode** (§3).
4. **Pick the container contract** from `formats/` if the piece targets one. Container is orthogonal to
   register: it constrains the vessel, not the voice. **Note the corpus limit** — the only container with
   real evidence behind it is the 800–2,500-word Medium post. `course-lesson` is the pack's main working
   container and is an **extrapolation**; say so in the manifest.
5. **For anything technical, run facts-first.** Pass A grounds the Solana facts against the `solana-dev` /
   `context7` / Helius MCPs and freezes them; Pass B restyles the frozen facts. Voice never re-derives a
   number, an address, a struct field or a code line. This is `rules/facts-first.md` and it outranks
   everything below it.
6. **Load ~4 exemplars**: always `04-seam-failure-report.md`, plus one opener, the close, and one body slot
   by job (`exemplars/david/index.yaml` has the map).
7. **Scan `themes.md`** for fitting substance, respecting `burn:` rates and the DO-NOT-USE flags. One named
   anecdote per piece.
8. **Write the marker ledger first**, then draft. Check the card's gates against the **fact-sheet**, not the
   draft.
9. **Protect the naturalness floor above everything** — the seams, the tail-loaded heat, the booster warmth,
   the plainness quota, and §5.6's rule against a clean arc.

## 3. Register modes (the actual routing table)

Route on the piece's **job**, as usual. The output is a register mode plus a helius on/off call.

| The piece's dominant job | Mode | FK band | Body exemplar | Notes |
|---|---|---|---|---|
| **Teach a Solana concept or mechanism in a course lesson** | **course-lesson** | 8–9.5 | `02-derivation-plain-mechanics` + `04` | **helius ON** (evidence layer only). The pack's main working mode and an **extrapolated container** — no course content in the corpus. Facts-first is mandatory. Prose enumeration, not step lists. Code blocks are helius's register entirely; keep David's prose *around* them, never inside them. |
| **Open or close a course / motivate** | **course-opener** | 7.5–9 | `01-opener-qualification` + `06-close-book-handoff` | **helius OFF** — nothing technical to evidence. Heat is tail-loaded by default; if a brief asks for a warm opener, that is off-corpus and belongs in the manifest. |
| Teach a repeatable procedure the reader can run tonight (how-to, workflow, tooling) | **how-to** | 7.5–9 | `02-derivation-plain-mechanics` | The question hinge is native here. Announce the count, then name the units. The corpus's strongest, best-evidenced mode. |
| Show a concrete instance so the method lands (a walkthrough, a worked case) | **worked-example** | 8–9 | `03-worked-example-dated` | The date, tool and outcome must come from the fact-sheet — `fabricated-instance-guard` is a **hard** gate. |
| Extract lessons from something that went wrong (retrospective, post-mortem, "lessons learned") | **retrospective** | 9–10.5 | `04-seam-failure-report` | The one mode licensed to use full-imperative-sentence headings with no terminal period. Failure reported flat and agentless; the value lands after. Question hinge may be **absent entirely** (the real retrospective post has zero). |
| Recommend resources (book list, tool roundup, reading path) | **roundup** | up to 10.5 | `06-close-book-handoff` | The only mode where `helped-answer-question` is licensed, once. Drift the FK up with **named-thing nouns**, never with `-tion` abstractions. |
| PM / delivery artifact (estimation write-up, scoping doc, team-process note) | **pm-artifact** | 9–10 | `02-derivation-plain-mechanics` | **Substance from `themes.md` `[2025-offreg]`, style from 2020 only.** Run every item through the `david.md` §7 translation table. See PACK.md's register-tension note. |
| Reassure a reader who is about to bounce (onboarding, "will this break my X?") | **reassurance** | 7.5–9 | `05-question-hinge` | The reader's worried question as a heading, answered in one word. |
| Anything ≥1,200 words | any of the above + | — | add `07-restraint-plain-body` | Long-form needs a proven flat stretch. The corpus has **no piece over ~950 words** — flag the extrapolation in the tone manifest. |

**Tie-breaks.** A piece that both teaches a procedure *and* narrates how it was learned → **how-to** with the
narration as seams, not **retrospective** (the corpus does this: the procrastination post is a how-to
carrying an app-building story). A PM artifact that is mostly a list of resources → **roundup**, and skip the
translation table. When two modes tie, prefer the one whose body exemplar you have *not* used most recently
in the batch.

**how-to vs pm-artifact** — the tie the pack's own scope creates, so decide it by the reader's next action.
If the reader is meant to *run* the thing (a scoping worksheet, a checklist, an estimation template walked
through step by step) → **how-to**, with the PM substance still translated through §7. `pm-artifact` is for
pieces that *report or justify* a delivery decision — an estimate and its assumptions, a scope negotiation, a
process change. "Define your MVP scope: a practical worksheet" is a **how-to** by this test, despite being PM
material end to end.

**Unmapped jobs — the honest fallback.** Three jobs have **no mode**, because the 2020 corpus contains no
instance of them. Do not invent a band for them; route as below and declare it.

| Job with no corpus instance | Route it as | Declare |
|---|---|---|
| Argue a thesis / opinion piece | **how-to**, if it can be honestly reframed as "here is how to think about X, in order". If it can't, hold the how-to FK band anyway. The only argumentative post in the wider corpus is off-register (*"What if smart contracts were mutable?"*, 2022) — mine it for substance, never for prose. | `· extrapolated: thesis-register` |
| Announce something | the `formats/community-announcement` container, body at the **reassurance** band (closest attested warmth). | `· extrapolated: announcement` |
| Anything code-bearing | the fitting mode above; the corpus has **0 fenced blocks and 0 inline code spans**, so the code register is entirely unevidenced. | `· extrapolated: code` |

## 4. Failure modes (ranked by damage)

1. **Fabrication to complete a ritual.** An invented book title for the handoff, or an invented dated
   anecdote ("last week we decided on a call…"). This is not a style error; it is a false statement in the
   author's name, and it is easy and invisible. Both are `enforce: hard` gates. *The blind-compare pass
   produced exactly this failure, which is why the guard exists.*
2. **Importing the 2025 consultant register into a PM piece** because the substance came from there. The
   symptom is an abstract-noun subject or a `However`; the fix is `david.md` §7.
3. **Helius structure leaking past its licence** — the measured failure of this blend. Numbered step lists,
   scannable procedures, short declarative instruction sentences. It reads clean and it is wrong: it cost
   **4.2 FK grades and 5 words of median sentence length** in the validation run. Symptom: a run of one-line
   steps and no run-on anywhere on the page. Fix: prose enumeration (§1). Helius may put a *number with a
   unit* in a sentence; it may not put the sentence in a list.
4. **Sanded-off seams.** A piece with zero non-native seams reads smoothed, not authored. It is the single
   biggest fidelity loss available and it happens by default.
5. **Caricatured seams** — the opposite failure, and the more embarrassing one: seams at 2–3× rate, one per
   paragraph metronomically, or (worst) invented misspellings. Reproduce the grammar, never the spelling.
   Note that **closing lines are not the problem** — the corpus puts a seam in 5/5 closers, so a clean
   sign-off is the smoothing tell, not the caricature tell (`david.md` §5.2 rule 1). Caricature is about
   *rate and comprehensibility*: if a reader re-reads a sentence and still can't recover the meaning, cut it.
6. **A cold body.** Tail-loaded heat is right; a body with zero boosters is colder than any real post.
7. **The stamped closer.** "Let me know … in the comments!!" on every piece in a batch. The real recipe holds
   in only 3/5, and only 2/5 posts end on an exclamation mark at all. Vary everything after "Let me know".
8. **Generalizing a single-post tic** — `lots of`, `This one helped me answer the question`, the bare
   `1 Item.` list, gerund+colon headings, `Disclaimer:`, `:)`. Each is capped at 1 per piece and gated by
   format; each was loud in exactly one of the five posts.
9. **A clean arc.** Every section advancing the argument, each device firing once in order. No real post
   looks like that.

**Meta-failure:** any of the above producing a body that is *uniformly polished and evenly paced*. With no
secondary layer to blame, the primary owns this outright.

## 5. Tone manifest (always)

Every delivery ends with ONE metadata line in the chat/report — **never inside the piece itself**:

`tone[david 85 · helius 15] · mode: course-lesson · markers: closing-ask 1, game-jam 1 · route: auto · extrapolated: course-lesson, code`

Primary-only pieces report `tone[david primary-only]` and drop the weight pair. Report helius's weight
whenever it is on, so an over-weighted guest is visible in the log rather than only in the prose.

If the container or the length went beyond the corpus, **add `· extrapolated: <what>`** so the requester
knows which part of the output the corpus does not actually support. For this pack that is the common case,
not the exception: `course-lesson` (no course content in the corpus), `code` (0 fenced blocks, 0 inline
spans), anything over ~950 words, threads, and scripts.
