# Formats — container contracts

A **container** is the vessel a piece ships in (an X post, a course lesson, a video script). It is
orthogonal to the **job** (which routes the secondary voice) and to the **voice** (the pack). When
a piece targets a specific container, load exactly ONE file from here in Pass B alongside the pack
files. These specs are **voice-agnostic** — engine-level, like the rules; anything
author-specific stays in the pack.

| Container | File | Also covers |
|---|---|---|
| Single X/Twitter post | [x-post.md](x-post.md) | short takes for similar feeds |
| X thread | [x-thread.md](x-thread.md) | |
| LinkedIn post | [linkedin-post.md](linkedin-post.md) | |
| Blog post | [blog-post.md](blog-post.md) | standalone explainers, docs-adjacent guides |
| Course lesson | [course-lesson.md](course-lesson.md) | modules, serialized tutorials |
| Video script | [video-script.md](video-script.md) | shorts/reels AND long talking-head |
| Email newsletter | [newsletter.md](newsletter.md) | |
| Community announcement | [community-announcement.md](community-announcement.md) | Discord/Telegram posts |

No file for the container you're writing? The default long-form workflow
(`../writing-workflow.md`) is the fallback; consider whether the container deserves a spec.

## Rules that apply across ALL containers

1. **Facts stay frozen at every size.** Compression is scope-cutting, never rounding: a tweet
   carries fewer facts than a blog, but the facts it carries are verbatim-faithful. `0.000003 SOL`
   does not become "basically free" without the real number nearby.
2. **Markers scale DOWN faster than length.** The card's budgets are ceilings for FULL pieces; a
   short container has no room to prove the voice. A tweet with a catchphrase AND a sign-off is a
   costume. Under ~200 words, default to zero markers unless one lands perfectly.
3. **Seams shrink with the container.** At short scale a seam is a real number from your own use or a
   first-person cost ("cost me a weekend"), not a confession paragraph. At most one per short piece —
   and zero is also human (a tweet doesn't owe you a seam; a scheduled one reads inserted).
4. **The naturalness floor applies at container scale.** Burstiness inside a tweet is word-level
   (a two-word sentence against a long one); inside a script it's breath-level; the "write
   unevenly" law never turns off, it changes unit.
5. **Each container has its own AI tells.** The per-file "reads as AI here" lists are as binding
   as the global deslop rule — platform readers are primed on their own platform's slop.
6. **Placeholders survive verbatim.** `[LINK]`-style tokens from the brief are carried exactly;
   never invent a URL.
