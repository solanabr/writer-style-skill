#!/usr/bin/env python3
"""
style_lexicons.py — shared tokenizers + marker lexicons for the writer-style tools.

This is the deterministic, no-network, no-model substrate that profile_corpus.py
(the builder) and validate_voice.py (the validator) both import. It holds:

  - regex tokenizers (WORD_RE, SENT_RE) and the ~150 English FUNCTION_WORDS used
    for lexical-density,
  - small, transparent lexicons for the GENERATION-ACTIONABLE signals the style
    cards expose (hedges/boosters, discourse connectives, definition/analogy/
    example markers, AI-tell words),
  - a cheap syllable counter for a Flesch-Kincaid grade estimate.

Design note: the cosine-similarity "StyleScorer" that used to live in
style_score.py was intentionally DROPPED. Stylometric distance manufactures false
confidence (it scores function-word/punctuation vectors that a writer cannot act
on, against a small/polluted reference). Repetition `audit` + the AI-tell lint +
a human blind read replace it. What survives here is only what the builder needs
to DERIVE a card and the validator needs to CHECK output.
"""
from __future__ import annotations
import re

# ── tokenizers ───────────────────────────────────────────────────────────────
WORD_RE = re.compile(r"[A-Za-z']+")
SENT_RE = re.compile(r"[.!?]+")

# ~150 common English function words — used only to compute lexical DENSITY
# (content-word ratio). They are never surfaced to the writer as a target.
FUNCTION_WORDS = set((
    "a about above after again against all am an and any are aren't as at be because been "
    "before being below between both but by can't cannot could couldn't did didn't do does "
    "doesn't doing don't down during each few for from further had hadn't has hasn't have "
    "haven't having he he'd he'll he's her here here's hers herself him himself his how how's "
    "i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my "
    "myself no nor not of off on once only or other ought our ours ourselves out over own same "
    "shan't she she'd she'll she's should shouldn't so some such than that that's the their "
    "theirs them themselves then there there's these they they'd they'll they're they've this "
    "those through to too under until up very was wasn't we we'd we'll we're we've were weren't "
    "what what's when when's where where's which while who who's whom why why's with won't would "
    "wouldn't you you'd you'll you're you've your yours yourself yourselves"
).split())

# ── stance: hedges vs boosters (epistemic markers a writer can dial) ──────────
HEDGES = [
    "maybe", "perhaps", "might", "may", "could", "roughly", "probably", "possibly",
    "i think", "i guess", "sort of", "kind of", "somewhat", "fairly", "seems",
    "seemingly", "apparently", "arguably", "more or less", "in a sense", "at least for me",
    "honestly", "to some extent", "tends to", "generally", "usually", "i suspect",
]
BOOSTERS = [
    "clearly", "obviously", "definitely", "certainly", "undoubtedly", "of course",
    "without a doubt", "absolutely", "in fact", "the fact is", "always", "never",
    "must", "the truth is", "no question", "plainly", "simply put", "make no mistake",
]

# ── discourse connectives by relation (favor/avoid + argument structure) ──────
CAUSAL = ["because", "so ", "therefore", "thus", "hence", "as a result", "which means", "that's why"]
CONTRASTIVE = ["but ", "however", "yet ", "though", "although", "whereas", "on the other hand",
               "on the flip side", "even so", "still,"]
ADDITIVE = ["and ", "also", "moreover", "furthermore", "additionally", "plus ", "in addition",
            "what's more", "besides"]

# ── teaching-craft markers (educational / long-form technical levers) ─────────
DEFINITION_MARKERS = [" is a ", " is an ", " are a ", " refers to ", " means ", " defined as ",
                      "in other words", " is the ", " is when ", "that is,", "i.e."]
ANALOGY_MARKERS = ["like a ", "like the ", "as if", "imagine ", "think of it as", "think of ",
                   "is basically", "is essentially", "akin to", "picture ", "it's like"]
EXAMPLE_MARKERS = ["for example", "for instance", "e.g.", "say you", "suppose ", "consider ",
                   "let's say", "take the case", "concretely"]

# ── AI tells: a TIERED, gated cliché system ───────────────────────────────────
# The key insight: a FLAT ban over-suppresses legitimate technical prose (in our
# own corpus, "ecosystem" appears in 200 files, "significant" in 221). So we gate.
#   Tier 1 — always flag: unambiguous LLM tells with no honest technical use; each
#            maps to a plain-word swap in REPLACEMENTS (surfaced inline).
#   Tier 2 — cluster-gated: flag only when ≥3 DISTINCT tier-2 words share a
#            paragraph (a MIX of buzzwords is the tell; one or two alone is usually fine).
#   Tier 3 — density-gated: high-frequency words that ARE legitimate in technical
#            writing (robust, scalable, ecosystem…); flag only when many distinct
#            ones pile up across the piece (i.e. buzzword soup, not honest use).
AI_TELL_WORDS = [  # Tier 1 — always flag (high precision: words with almost no honest technical use)
    "delve", "intricate", "tapestry", "multifaceted", "underscores", "underscore",
    "utilize", "boasts", "nestled", "vibrant", "thriving", "bustling", "meticulous",
    "pivotal", "beacon", "holistic", "synergy", "interplay", "symphony", "commence",
    "ascertain", "endeavor", "garner", "bolster", "showcase", "embark", "watershed", "testament",
    "a testament to", "deep dive", "thought leader", "best practices", "it's important to note",
    "in today's fast-paced world", "navigating the", "in the ever-evolving", "unlock the power",
    "game-changing", "at its core", "when it comes to", "the world of",
    "the future looks bright", "only time will tell", "due to the fact that", "in order to",
]
AI_TELL_TIER2 = [  # cluster-gated (≥3 distinct in one paragraph)
    "harness", "navigate", "foster", "fostering", "elevate", "unleash", "streamline", "empower",
    "facilitate", "underpin", "nuanced", "crucial", "myriad", "plethora", "encompass",
    "transformative", "cornerstone", "paramount", "poised", "burgeoning", "nascent", "overarching",
    "revolutionize", "catalyze", "cultivate", "reimagine", "actionable", "impactful", "cutting-edge",
]
AI_TELL_TIER3 = [  # density-gated; legit in technical prose — flag only when many pile up
    "significant", "innovative", "effective", "dynamic", "scalable", "compelling", "unprecedented",
    "exceptional", "remarkable", "sophisticated", "instrumental", "world-class", "state-of-the-art",
    "robust", "comprehensive", "seamless", "ecosystem", "throughput", "modular", "performant",
    # demoted from Tier-1: these have honest crypto/tech uses (leveraged trading, a new paradigm,
    # the realm of MEV) — a single use is fine; only a pile-up is the tell.
    "leverage", "paradigm", "realm",
]
# plain-word swaps surfaced inline when a Tier-1 tell fires (actionable, not just a flag)
REPLACEMENTS = {
    "delve": "dig into", "leverage": "use", "utilize": "use", "commence": "start",
    "ascertain": "find out", "endeavor": "try", "garner": "gather", "navigate": "handle",
    "harness": "use", "streamline": "simplify", "facilitate": "help", "deep dive": "close look",
    "multifaceted": "many-sided", "paradigm": "model", "in order to": "to", "showcase": "show",
    "due to the fact that": "because", "embark": "start", "bolster": "shore up",
    "underscore": "stress", "nestled": "set", "boasts": "has", "robust": "solid",
    "comprehensive": "complete", "myriad": "many", "plethora": "plenty",
}
# crypto/web3 boilerplate phrases (cluster-gated like Tier 2)
CRYPTO_CLICHES = [
    "the integration of", "the intersection of", "community-driven", "long-term sustainability",
    "decentralized compute", "tokenized incentive structures", "reward emissions", "emerging sector",
    "emerging space", "user engagement", "designed for long-term", "the power of blockchain",
]
# copula-avoidance: elaborate verbs where is/are/has would do (flag only as a CLUSTER)
COPULA_SUBSTITUTES = ["serves as", "stands as", "represents a", "represents the", "boasts",
                      "features", "marks a"]
# symbolic-gloss: telling-not-showing applied to mundane things (advisory — state the fact instead).
# NB: "represents the" is deliberately NOT here — it's plain English ("x represents the count of validators"),
# fired on 44 genuine corpus files, and already lives in COPULA_SUBSTITUTES (cluster-gated, far less noisy).
SYMBOLIC_GLOSS = ["symbolizes", "embodies", "speaks to the", "stands as a symbol", "is a metaphor for"]
# essay-bot connectives to avoid (favor the CONTRASTIVE/CAUSAL set instead)
AI_TELL_CONNECTIVES = ["moreover,", "furthermore,", "additionally,", "in conclusion,",
                       "first and foremost", "last but not least"]
# the false-antithesis parallelism tell: "not X, it's Y" / "not X, but Y". Catches the CONTRACTED form too
# (isn't/aren't/wasn't/weren't/ain't) — Kaue's real exemplar 01 is "This isn't regulation, it's a wall", which
# the old \bnot\b regex silently missed while still firing on the formal "is not X".
FALSE_ANTITHESIS_RE = re.compile(
    r"\b(?:not|(?:is|are|was|were|ai)n['’]?t)\s+[\w ,'’-]{1,40}?,\s+(it['’]?s|but|rather)\b", re.I)
# deterministic, voice-neutral machine-paste fingerprints (always flag — near-dispositive).
# These are real copy-paste artifacts, NOT style — so a hard fail is safe (no false positives on prose).
AI_FINGERPRINTS = [
    ("chatgpt-utm", re.compile(r"utm_source=(chatgpt|openai|copilot|claude|perplexity)", re.I)),
    ("citation-leak", re.compile(r"citeturn\d+\w*|oai_citation|contentReference\[oaicite", re.I)),
    ("placeholder-name", re.compile(r"\[your name\]|\[insert [^\]]+\]", re.I)),
    # NB: no bare \[date\] — it collided with Markdown ref-link labels ([date]: <> ...) in real corpora
    # (168 Vitalik blog files); the genuine "[insert date]" placeholder is caught by placeholder-name above.
    ("placeholder-date", re.compile(r"\b20\d{2}-XX-XX\b|\bYYYY-MM-DD\b", re.I)),
]
# stacked hedging — ADVISORY only (not a fingerprint): two hedge adverbs in a row, e.g. "potentially
# eventually". A plain modal + one adverb ("may eventually ship") is normal English and must NOT fire.
HEDGE_STACK_RE = re.compile(
    r"\b(potentially|possibly|likely|arguably|conceivably)\s+"
    r"(potentially|possibly|eventually|ultimately|arguably|conceivably)\b", re.I)

# Discourse-scaffolding tells of fluent BARE LLM output — the "essay frame" a model leaves even when it dodges
# the word-lists (smooth, well-structured, but un-deslopped). Each measured at ~0% on 793 human corpus docs AND
# the kaue canon, so they are clean signals of default-assistant prose. SUMMARY_CLOSER is matched against the
# last 1-2 sentences only (a closing restatement); the other two are rate-gated (a pile-up, not one use).
# NB: deliberately EXCLUDES "Overall"/"All in all" (real human sign-offs) and "keep in mind" (a real Kaue-ism).
SUMMARY_CLOSER_RE = re.compile(r"^\s*(in summary|in conclusion|to summarize|to sum up|to recap)\b", re.I)
META_HEDGE_RE = re.compile(
    r"it'?s worth noting|it is worth noting|worth noting that|it'?s important to note|it is important to note|"
    r"important to note|it'?s worth mentioning|it should be noted|it'?s worth pointing out", re.I)
AT_ITS_CORE_RE = re.compile(r"at its core|think of it as|in essence|in a nutshell", re.I)

_VOWEL_GROUP = re.compile(r"[aeiouy]+")


def syllables(word: str) -> int:
    """Cheap heuristic syllable count (good enough for an FK-grade estimate)."""
    w = word.lower().strip("'")
    if not w:
        return 0
    groups = _VOWEL_GROUP.findall(w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ie")) and n > 1:
        n -= 1  # silent terminal 'e'
    return max(1, n)


def flesch_kincaid_grade(words: list[str], n_sentences: int) -> float:
    """Flesch-Kincaid grade level from already-tokenized words + a sentence count."""
    nw = max(1, len(words))
    ns = max(1, n_sentences)
    syl = sum(syllables(w) for w in words)
    return round(0.39 * (nw / ns) + 11.8 * (syl / nw) - 15.59, 1)


def count_markers(text_lower: str, markers: list[str]) -> int:
    """Total occurrences of any phrase in `markers` within a lowercased text."""
    return sum(text_lower.count(m) for m in markers)
