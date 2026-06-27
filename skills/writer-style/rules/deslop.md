---
description: "Deslop guardrails — remove AI-cliché tells without over-correcting or harming facts/voice. Applies after Pass B.5, before Pass C."
---

# Deslop — strip the AI tells, keep the human

After the blind-compare (Pass B.5), do a quick deslop pass. The principle, above everything:

> **Clusters, not isolated tells.** A single em-dash, one "however", one "robust" means nothing. Em-dashes
> *plus* rule-of-three *plus* a buzzword pile *plus* a "Conclusion" heading is a confession. Hunt the cluster.

The lint does the mechanical half. `validate_voice.py tells --card <voice>.card.yaml` reports Tier-1 clichés
(with plain-word swaps), gated Tier-2/Tier-3 buzzword clusters, crypto-boilerplate, copula clusters,
symbolic-gloss, machine-paste fingerprints, and Markdown hygiene. **Most are advisory; only the fingerprints
and the burstiness floor are hard fails.** Apply judgment: a flagged technical word in honest use (a `robust`
retry loop, right next to code) is fine — that's why Tier-3 is density-gated, not banned.

## Three quick tests the lint can't run
1. **Paragraph-reshuffle.** Could you swap two body paragraphs without breaking the piece? If yes, it's
   AI-structured. Each paragraph should *depend* on the last (a number it set up, a thread it continues),
   not sit as an interchangeable module. Add the real connective tissue.
2. **Treadmill / "what's actually new here?"** Every paragraph must add information, not restate the previous
   one in fresh words. "In other words," "Put simply," "Essentially," "At its core" usually mark 400 words of
   restatement around 100 words of content. Cut the restatement.
3. **Read it out loud.** Does any sentence sound like a press release, or like something no human would
   actually say? ("X stands as a testament to the enduring power of…") Cut it or say it plainly.

## Manufactured profundity — cut or ground it
The aphorism formula ("X is the language of trust," "the currency of attention," "X is not a tool but a
mirror") and the symbolic gloss ("the closed factory *represents* the decline of manufacturing") are
telling-not-showing. **State the concrete fact and let the reader draw the meaning** (facts-first): *"The
factory closed in 2009. Three hundred jobs."* The lint flags the gloss verbs; you supply the fact.

## Preserve these human signs — do NOT over-correct
Deslopping is subtractive, but over-editing pushes prose *back toward* the generic AI mean. Leave these alone:
- **Specific, unusual, hard-to-fabricate detail**: a real number from your own use, an exact name, a date.
  AI rounds specifics off; humans hoard them. Never sand these down chasing a cleaner sentence.
- **Mixed feelings / unresolved tension**: "worth it, but I'd be lying if I said the limit never bit me."
- **Sentence-length variety**: the burstiness is the point; don't smooth it into a uniform 15-25 words.
- **Genuine asides and self-corrections**: "(well, mine)", "I lied a little before", a mid-flow "this ran
  long". These read unmistakably human; they are the seam, not noise.

The goal isn't zero flags — it's prose that reads like a person who knows the material, with the machine tells
gone and the human texture intact.
