# Agent prompt packs

Copy-paste-able prompts for each agent role in the process. Fill the `{{slots}}`. Always give absolute
paths and tell agents to read the **real corpus/draft**, not your summary. Run independent agents in
parallel (one message, multiple calls); run judges after the draft exists.

Shared context to prepend to every miner/judge prompt:
> We're building a {{craft|spine}} voice persona for {{NAME}} to write original educational
> Solana/blockchain content. Corpus (read ALL relevant files): {{CORPUS_PATH}}. Use grep/bash for counts.
> Findings must be **evidence-bound**: tie every claim to a verbatim quote and/or a frequency count. No
> bare adjectives.

---

## A. CRAFT miners (run all 5 in parallel)
Each ends with: *"Capture only TRANSFERABLE craft applicable in anyone's voice. Do NOT capture surface
idiolect (punctuation tics, signature phrases, rituals, headers, personas, coined terms). Quotes are
evidence of a TECHNIQUE, never to be reproduced. Also FLAG anything that is idiolect so we exclude it, and
name this author's top 2–3 signature STRENGTHS. Return ranked dimensions: (a) name+technique, (b) why it
raises quality, (c) evidence quote(s)/count, (d) a 'how to apply generically' rule."*

1. **Learning-science / instructional design**: scaffolding, worked examples, difficulty staging,
   misconception handling, examples↔non-examples, how they make hard things clear.
2. **Rhetoric / argumentation**: how they reason, persuade, concede/rebut, calibrate confidence,
   establish authority, sequence an argument.
3. **Prose craft**: sentence/paragraph mechanics *as transferable moves* (topic-sentence habits,
   transitions, list-vs-prose decisions, emphasis). Flag the pure tics for exclusion.
4. **Technical communication**: handling of math/notation/code/diagrams, analogy taxonomy + when each
   breaks, quantification, defining terms, precision-vs-accessibility.
5. **Genre / document architecture**: how structure varies by content type; opening/closing logic;
   navigation; how a long piece is held together.

## B. SPINE miners (run all 4 in parallel) — note: we WANT the idiolect here
1. **Idiolect / stylometric**: surface fingerprints TO REPRODUCE: sentence rhythm, punctuation habits
   (count them, per-1k), signature words/phrases/openers/closers, formatting, emoji/slang tokens,
   capitalization, paragraph shape. Separate cross-register (core) from register-specific features.
2. **Cognitive / brain-patterns**: how they think and teach beneath the words: hook style, default
   structure, how they motivate/frame, analogy instinct, reasoning moves, recurring "thinking tics."
3. **Register & tonal range**: map each register (formal/casual/technical/personal); identify the
   through-line constant across ALL of them; recommend the target register + how to dial between them.
4. **Personality, affect & values**: enthusiasm, humor, warmth-behaviors, worldview/values that color
   the writing, relationship with the reader, cultural markers; and what would feel OFF-brand.
> Each spine miner adds: *"This is the user's own voice. Capture quirks; we WANT idiolect. Weight recent,
> on-target-register material; treat off-register/old material as range. Flag where their voice OVERLAPS
> any craft author (congruence we can lean on)."*

## C. CRAFT judges (run after the draft; reconcile their verdicts yourself)

**C1 — Ruthless minimalist editor (cutter):**
> Read {{DRAFT_PATH}}, a generative "write like {{NAME}}" craft skill an LLM loads to produce content.
> Find BLOAT and OVERKILL: (1) redundancies repeated across sections (propose merges); (2) marginal/
> low-fidelity items that add length without improving output; (3) rules that, followed literally, make
> output formulaic/over-engineered; (4) anything not load-bearing for generation. Output a prioritized
> CUT/MERGE list with a target % shorter. Don't cut the core method.

**C2 — Fidelity advocate (keeper):**
> Read {{DRAFT_PATH}} (+ the real corpus). Protect output quality: (A) MUST-KEEP core: items that, if
> removed, drag output toward generic; for each, one line on *how it concretely changes the output*.
> (B) Concede credibly: the 3–5 weakest items you'd cut. (C) GAPS: places too thin for faithful
> generation (a rule with no example; a high-frequency behavior under-weighted); propose concrete,
> load-bearing additions. Verify any frequency claims against the corpus.
- *Reconcile:* cut per C1, **and** add the gap-examples from C2. Net result: leaner **and** sharper.

## D. SPINE judges (run after the draft)

**D1 — Fidelity hawk:**
> Read {{DRAFT_PATH}} AND the real corpus. Adversarially stress-test fidelity: (A) MISSED/under-weighted
> authentic features (quote the corpus); (B) GENERIC/not-them lines to sharpen or cut; (C) OVER-FIT/
> caricature risks if rules are followed literally (recommend dosages/guards — watch for tics inflated by
> one corpus era/genre); (D) NATURALNESS: would a model following this read as a real person or
> assembled-from-rules?; (E) the single most important change. Be hard-nosed and evidence-bound.

**D2 — Generate-and-blind-compare (the decisive test):**
> STEP 1: Read ONLY {{DRAFT_PATH}} (not the corpus yet). Write a ~250–300 word sample on {{a topic NOT
> used as an example in the draft}}, in {{NAME}}'s voice, using only the spec. STEP 2: NOW read the real
> corpus and blind-diff your passage: where does it ring true vs false/generic/forced/too-tidy? Did you
> reproduce the UNEVEN texture (calm loose body + edge enthusiasm + a human seam) or distribute
> enthusiasm/polish evenly (the failure)? Which authentic trait did the spec fail to make you reproduce
> (a gap), which did you over-apply? STEP 3: blunt verdict (does the spec now produce authentically-them
> output?) + concrete spec fixes.
- *This catches what critique can't* (e.g., "calm" being read as "clean"). If it reads as a polite
  impostor, strengthen the naturalness floor and re-run.

## E. Router agents (only when multiple craft personas exist; see `routing.md`)

**E1 — Routing architect (adversarial, top-down):**
> Read all persona files. Design a router: given the content's DOMINANT JOB, which craft to lean on (the
> spine is always-on). For EACH persona define trigger + anti-trigger conditions. Give a crisp decision
> rule for any two "similar" personas (e.g. the two technical ones, when does a topic want one's craft
> vs the other's?). Adversarially evaluate the starting hunches. Define stacking rules (which crafts can
> combine — they should work different axes) + a cap. List the worst mis-routings. Output the decision
> procedure.

**E2 — Router validator (empirical):**
> Read the SKILL.md procedure + ROUTING.md + skim the personas. Invent ~14 realistic course topics
> across levels and types. Route each via the procedure; state the route (spine + backbone + guest +
> dosage) and JUDGE it. Hunt: mis-routes, hard boundary cases, over/under-stacking, content types the
> router doesn't handle, and SKILL↔ROUTING disagreements. Output the routing table, the breakages, and
> concrete router refinements. Be hard-nosed.

---

## Operating notes
- **You reconcile; the agents propose.** Read their outputs critically and decide what to apply.
- **Don't let a generator grade itself.** That's why D2 separates generation from the blind diff.
- **Parallelize** miners (and the two craft judges); the spine D1/D2 can also run in parallel.
- **Re-verify counts** any judge flags as inflated, against the corpus, before trusting them.
