# Container: course lesson

One lesson inside a series. The student chose to be here, has done (or skipped) the previous
lesson, and will decide during THIS lesson whether to do the next one. The long-form workflow
(`../writing-workflow.md`) governs the writing; this spec adds the serialized-context edges.

## Contract
- **Honor the series position** (the brief's `context:`): a continuation open is available when
  the previous lesson is assumed done ("last time you deployed X — now…"); never re-teach the
  previous lesson; never assume material from a FUTURE lesson.
- **The closer is a bridge to the ACTUAL next lesson**: name it, or describe what the student does
  there — phrased from the artifact they just built ("Next lesson `btc_rpc.py` grows eyes"). A
  content-teaser must be verified against the next lesson's brief: mis-aiming at a lesson two rungs
  away is a defect a named pointer can't have. Still banned: marketing energy ("You won't believe
  what's next!"), teasing content beyond the literal next lesson, comments-invites (a
  standalone-post move). The FINAL lesson inverts the pattern — say there is no next lesson and
  point outward. (Redrawn in evolution R2 against the owner-accepted corpus: the earlier absolute
  teaser ban over-generalized a standalone-post ruling; LESSONS #4's actual rule — point to the
  real next lesson or close plain — stands.)
- **One concept per lesson.** Adjacent concepts get named and deferred to their lesson, with the
  lesson named. Scope discipline is what makes a series feel designed.
- **"You" is the student in the room**, mid-course, terminal open. Address their current state
  (including frustration, in troubleshooting lessons) — not a generic reader.
- **Troubleshooting lessons: fix first, feelings once.** The reader arrives mid-failure, skimming
  for the fix. The first actionable step (symptom-match table or command) lands within the first
  ~150 words. ONE reassurance/empathy beat max before it — fold the war story into that beat or
  place it after the fix; a second consecutive empathy paragraph reads as padding or condescension.
- **Checkpoints are concrete**: "you should now see X" / a command whose output proves progress.
  A student who can't tell whether it worked churns.
- **Method claims are promises.** Any sentence about what the student will do or has done in THIS
  lesson ("you'll reproduce the failure yourself") must be cashed by an activity or checkpoint that
  literally is that thing; if the lesson explains rather than exercises, say what actually happens
  ("once you've seen why the simpler design fails"). Forward promises about later weeks are course
  copy, not method claims.
- **Code is first-class**: exact commands for the interesting steps, expected output where the
  student must recognize success or failure, terse prose for routine steps.
- **Warm register scales with student level** (beginners get warmth, never a shrug) — but
  teaching warmth is receipts and patience, not exclamation marks.

## Reads as AI here (instant fails)
- "In this lesson, you will learn…" objective-list openers (curriculum-doc voice).
- A recap section at the end of any lesson — the recap function lives in the NEXT lesson's opener
  and in checkpoints, never as a closing section. Series uniformity is measured at the SURFACE,
  not the beat: a stable beat-set across lessons is course design; verbatim headers, unrotated
  refrain wording, or a cloned seam skeleton across lessons is the series tell.
- Encouragement quotas: "Great job!" after every step. Praise the milestone that cost something.
- Teasing the next lesson with marketing energy ("You won't believe what's next!").

## Craft notes
- The best lessons acknowledge the student's actual failure modes at the moment they'd hit them
  ("if you're seeing X right now, that's the Y mismatch — fix it with Z, then come back").
- A lesson may run documentation-flat for long stretches; the instructor's presence lives at the
  decision points, not in every paragraph.
