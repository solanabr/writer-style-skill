# Solana Development Fundamentals: Lesson 0

Some admin before anything else, since lesson 0 is the admin lesson: this course is free, it's fully online, and it's self-paced with weekly checkpoints. You move at your own speed, and once a week there's a scheduled moment where we look at where you are and unstick whatever needs unsticking. Budget 5–7 hours a week, for eight weeks. There's no code today; this lesson exists so you know exactly what you're signing up for, where it gets hard, and what's waiting at the end. I'll keep it short, the real work starts in module 1.

## The shape of it: 6 modules, 8 weeks

1. **Solana core concepts:** accounts, transactions, programs. The mental model everything else hangs off.
2. **Rust for Solana:** only the Rust you need. The working slice, not the whole language.
3. **Anchor framework:** program development proper. This is where it starts feeling like building.
4. **Client development:** TypeScript and the wallet adapter, so a person with a browser can actually touch what you wrote.
5. **Testing and security:** LiteSVM for tests, plus the common vulnerability classes and how to recognize them in your own code.
6. **Capstone:** ship a full dApp, program plus frontend, to devnet.

That last module is the point of the other five. By week 8 you'll have deployed a working program to devnet and built a frontend that talks to it, and that's a portfolio piece, not a certificate — a live thing a hiring manager or a hackathon judge can click on and poke at.

## What you need walking in

One prerequisite: comfort in any programming language. Python, JavaScript, Go, C#, whatever you currently write loops in. If functions and data structures are old friends, you qualify. No Rust required, no blockchain background either; module 1 assumes you've never touched a chain in your life.

Money isn't on the list either — no card on file at any step, nothing to stake, nothing to buy. The tooling is free end to end, and devnet SOL (the test-network currency you'll deploy with) comes out of faucets, so you can finish the entire course, capstone included, without spending anything.

And if your worry is the fuzzier kind, the "am I the type of person who does this" kind: I was set on becoming a musician. That was the plan, the whole plan, right up until 10th grade, when my programming teacher handed me an Arduino kit and I found out that little pieces of silica, copper and plastic fused with some programming spells could do the thing I'd been chasing through music. I still have the guitar, it mostly holds down a corner of the room these days — nobody arrives at this stuff on rails, me included.

## Weeks 2 and 3

I said I'd tell you where it gets hard, so here it is, up front: the Rust stretch, weeks 2 and 3, is the hardest part of this course, and it's where most dropouts happen. You should hear that in lesson 0, not discover it mid-slump.

What it actually feels like: week 1 goes fine, everything is new and slightly magic, and then somewhere in the second week the borrow checker starts rejecting code you are certain is correct, then rejecting your fix, then rejecting the fix for the fix, and around the third error on the same line you start to wonder whether you ever knew how to program at all. You did — that feeling is the wall, everyone who learns Rust hits it, and it passes, not through talent, mostly through volume: you write more Rust, and one week the errors start making sense before you've finished reading them.

Two concrete things for that stretch. First, module 2's subtitle is a promise: only the Rust you need. When some tutorial elsewhere drags you into async trait bounds, that's not this course, close the tab. Second, the weekly checkpoints were built for exactly this: show up with the error you're embarrassed about, we'll look at it together, you leave unstuck, and nobody is grading you on how confused you were when you walked in. Showing up stuck in week 3 is the intended use of a checkpoint, and honestly those are the ones I care most about.

## Start here

So, that's lesson 0. Module 1 is open: accounts, transactions, and programs, the three ideas the rest of the course is built from, no Rust in sight yet — see you at the first checkpoint.

Happy building! 🚀
