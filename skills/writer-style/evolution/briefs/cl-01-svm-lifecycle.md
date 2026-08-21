---
id: cl-01-svm-lifecycle
title: "Course lesson: where your transaction goes after send"
container: course-lesson
words_target: 1300
audience: course students who use Solana daily but never traced a tx below the RPC
dominant_job: derivation
route_expected: vitalik
context: course-mid (series "How Solana Actually Works", lesson 2 of 4; previous lesson: "Transaction anatomy" — assume it's done, a continuation open is available; next lesson: "Consensus and finality"; closer contract: point to the actual next lesson or plain-close — NO teasers/comments-invites)
expect:
  latam-framing: 0
  game-changer_max: 1
  civilizational-analogy_max: 1
  sign-off_max: 1
  hard_fails: 0
---

## Brief

A course lesson (~1,300 words): follow a transaction from `sendTransaction` through the leader's
pipeline — and derive WHY each stage exists (why no mempool, why blockhash expiry, why account
locks) rather than naming stages. This is the testbed deep-dive's scope cut to one lesson:
submission → scheduling → execution. Consensus/finality belongs to the NEXT lesson — do not
spend words there. Load `formats/course-lesson.md`.

## Fact-sheet (FROZEN — imported subset of testbed/briefs/05-deepdive-svm-lifecycle.md; do not
re-derive)

- Transaction anatomy: signatures + message (header, account keys, recent blockhash,
  instructions). Every account an instruction touches is declared up front, writable or
  read-only — this declaration is what makes parallel execution possible.
- The recent blockhash is a recent PoH hash acting as a timestamp; accepted while within the last
  150 blocks (`MAX_PROCESSING_AGE = 150`); roughly 60–120 seconds wall-clock. Durable nonces
  exist for offline/delayed signing.
- No public global mempool: the RPC node forwards directly to the current and next scheduled
  leaders (Gulf Stream); the leader schedule is known an epoch in advance.
- Leader pipeline (TPU): Fetch → SigVerify → Banking stage → PoH → broadcast.
- Banking stage: the scheduler assigns non-conflicting transactions to executor threads via
  account locks — writable = exclusive, read-only = shared. Disjoint transactions run in parallel
  (Sealevel); contention on one writable account serializes. This is why hot-account congestion
  is local, not global (local fee markets).
- Execution: programs are SBF bytecode metered in compute units; per-transaction ceiling 1.4M CU.
- Failure modes developers actually hit: blockhash expired before inclusion; fee too low for a
  contended writable account; lock contention serializing what they assumed was parallel.
