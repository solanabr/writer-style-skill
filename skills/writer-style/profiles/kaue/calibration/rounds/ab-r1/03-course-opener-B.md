# Welcome to Solana Development Fundamentals

You've probably done this before. You find a promising course, the first lesson lands, and then somewhere around week two you hit a wall nobody warned you about, some concept the instructor breezed past because it was obvious to them, and you quietly close the tab telling yourself you'll come back later. You don't come back. I've done it more times than I'd like to admit, and the courses weren't even bad. They just never told me where the hard part was.

So let's run this one differently. This is **Solana Development Fundamentals**: free, online, self-paced, with weekly checkpoints. I'm going to spend this opening lesson being straight with you about what's inside, what it asks of you each week, and exactly where it gets hard. Most courses hide their wall. Ours is on the map from day one.

## What the eight weeks look like

6 modules over 8 weeks:

1. **Solana core concepts.** Accounts, transactions, programs. The mental model everything else hangs on.
2. **Rust for Solana.** Only the Rust you need. Not the whole language, not a systems-programming degree; the working subset that Solana programs actually use.
3. **Anchor framework.** Program development, which is where you start writing code that runs on-chain.
4. **Client development.** TypeScript and the wallet adapter, so actual humans can use the thing you built.
5. **Testing and security.** LiteSVM and the common vulnerability classes. In most software a bug becomes a ticket; on-chain it can become somebody's missing money, so security gets a full module here.
6. **Capstone.** Ship a full dApp, program plus frontend, to devnet. Modules 1 through 5 exist to make this one possible.

What do you need walking in? Comfort in ANY programming language. That's the whole list: no Rust, no blockchain background required. I came to this from Python and TypeScript myself, for what it's worth, so the "any language" bar is not marketing. And if you've never touched crypto at all: honestly, fine. Fewer habits to unlearn.

## The honest part

Plan on 5–7 hours a week. Some weeks will take less. Weeks 2–3 will not be those weeks: the Rust stretch is the hardest part of this course, and it's where most dropouts happen. I'd rather tell you that in lesson one than have you discover it mid-slump and conclude you're not cut out for this. You are, that stretch is just steep for everyone.

My own first contact with Rust went badly, for the record. I fought one borrow-checker error for an entire evening, decided the language hated me personally, and didn't touch the project for a week; when I finally came back, the fix took ten minutes. What flipped it for me was realizing the compiler isn't hazing you, it's catching, at compile time, the exact class of bug that drains real accounts in production. Once that clicked, the fights got shorter. Yours will too.

The weekly checkpoints exist for exactly this stretch. Self-paced doesn't mean alone: when week 2 starts chewing on you, bring the ugly error message and we'll get you through it together. Anchor sits right on the other side, and Anchor is where this stops feeling like homework and starts feeling like building.

## What you walk away with

By week 8, you'll have deployed a working program to devnet and built a frontend that talks to it. A live thing with an address, something you can put in front of anyone. That's the outcome this course is built around: a portfolio piece, not a certificate. Nobody can argue with software that runs; it either does the thing or it doesn't, and yours will.

Oh, and money, since this industry has a reputation there: you don't need any. The course is free, the tooling is free, and the devnet SOL you'll deploy with comes out of faucets. No money needed, start to finish. For learning, faucets are a godsend. You get to break things and redeploy until it works, and the mistakes cost nothing.

## See you in module 1

This welcome ran a little long, so let me land it. Eight weeks from now there can be a program you wrote running on devnet, with a frontend in front of it that you built end to end. The path between here and there is laid out, and the steep part has a checkpoint sitting right next to it. Guard your 5–7 hours. When the Rust weeks bite (they will), come ask instead of closing the tab; that one habit separates the people who finish from the people who almost did. You've got this. Happy building! 🚀
