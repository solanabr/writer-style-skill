# From `anchor init` to devnet: your first program, deployed

Last lesson we set up Rust and you fought the borrow checker to something like a respectable draw. This is the lesson where that effort starts paying rent: by the end of it you'll have a program with a real address, live on devnet, that anyone with an internet connection can look up and call. Not a localhost demo you tear down after the screenshot — an actual deployed artifact. Tag along, terminal open, and we'll go end to end.

The route, so you know where we are at every step: scaffold a project, read what Anchor generated (five minutes now, hours saved later), build, test, point the config at devnet, fund a wallet, deploy, then verify it's live. The interesting steps carry their why, because deployment is one of those topics where understanding two or three decisions saves you from an entire genre of confusing errors; the routine ones we just run and move on.

One prerequisite check. You need the Rust toolchain and Anchor installed, which you have from last lesson. What you do NOT need is a separate Solana CLI install: Anchor 1.0 bundles the whole Solana toolchain, which honestly is a godsend if you ever lived through the old days of pinning Anchor and Solana releases against each other by hand and praying the matrix held.

## Scaffolding the project

```bash
anchor init my_program
cd my_program
```

Before you touch anything, take the tour. `anchor init my_program` generated a full workspace, and four pieces of it matter today:

- **`programs/my_program/src/lib.rs`**: the program itself. All the Rust from last lesson lives here.
- **`tests/`**: where your tests go.
- **`migrations/`**: deploy scripts. You won't edit these today.
- **`Anchor.toml`**: the workspace config, which cluster you're pointed at and which wallet pays. This one file decides where your deploys land, so keep it in your head.

There's a fifth piece that doesn't exist yet, and it's the most important one: `target/deploy/my_program-keypair.json`. It appears on your first build, and it's the program's identity, the keypair whose public key becomes your program's address on every cluster you ever deploy it to, which also means that casually deleting `target/` between builds has consequences beyond a slower compile. We'll hit exactly that failure in a second.

## The program ID, and the #1 first-deploy failure

Open `lib.rs` and look at the top. There's a `declare_id!()` macro with an address in it, and that address must match the public key of the deploy keypair, because it gets baked into the compiled binary and checked at runtime; your program literally asserts its own address from inside itself, which sounds circular until you realize it's what lets clients and other programs trust that the code at that address is the code that claims to live there.

Here's the catch: those two things drift apart all the time, and nothing warns you until the deploy blows up. Clone someone's repo and the code carries *their* `declare_id!()` while your machine generates a fresh keypair on first build. Delete `target/` and rebuild, same story, new keypair, stale ID. This exact mismatch is the number one first-deploy failure, and it produces the kind of error that makes beginners quietly question whether they're cut out for this. You are. It's one command.

That command is `anchor keys sync`. It reads your actual deploy keypair, rewrites `declare_id!()` to match, and the mismatch is gone. It has never once made anything worse, so run it after cloning any Anchor repo, after regenerating keys, whenever a deploy error smells like an identity problem.

## Build and test

```bash
anchor build
```

Two artifacts come out of `anchor build`, and both matter. The compiled program, a `.so` file, lands in `target/deploy/`, and the IDL lands in `target/idl/`. The IDL (interface definition language, a JSON description of your program's instructions and accounts) is how clients talk to your program without anyone hand-writing serialization code on either side, and it's the reason a TypeScript frontend can call a Rust program and get the argument types right. Lesson 4 leans on it heavily, so it's worth knowing where it lives now.

```bash
anchor test
```

Anchor 1.0 changed the testing story: `anchor test` runs against Surfpool rather than the old `solana-test-validator`, and the default test template is LiteSVM, meaning Rust tests running in-process with no separate validator to spin up, warm up, and babysit while it eats a CPU core. Today that means the scaffolded test just runs, fast, and it should pass out of the box because you haven't changed anything yet. Run it, watch it go green, move on.

## Pointing at devnet

So far everything has been local. Time to aim at the real (well, real-ish) world. Open `Anchor.toml` and set the provider:

```toml
[provider]
cluster = "devnet"
wallet = "~/.config/solana/id.json"
```

Cluster says where, wallet says who pays (a local keypair on your machine; the path `anchor init` wrote is usually right already). I'll confess why I'm making you stare at this file instead of just handing you the deploy command. On one of my own early deploys I skipped this check, deployed, then spent the better part of an evening pasting my program ID into the devnet explorer, refreshing, getting nothing, slowly building a conspiracy theory about devnet eating my program, drafting a message to a friend about a "possible explorer indexing issue." The program was fine. It was on localnet. The terminal had printed exactly where it went, and I had scrolled right past that line to go stare at the wrong network for an hour. Read your `Anchor.toml`; the config always wins.

Now, funding. Devnet SOL is free, that's the whole point of devnet, but it's rate-limited:

```bash
solana airdrop 2
```

Requests are typically capped around 2 SOL each, and the CLI faucet will start refusing you if you hammer it. When that happens, faucet.solana.com is the fallback.

How much do you actually need? Deployment makes your program account rent-exempt for roughly 2× the binary size (headroom for future upgrades), which for a typical starter program works out to a few SOL of devnet balance; my last starter deploy ate a bit under 3. Airdrop until you're comfortably above that, and remember none of this is real money, so there's nothing to optimize here.

## The deploy

```bash
anchor deploy --provider.cluster devnet
```

That's it! One command, a short wait while the binary streams up to the cluster in chunks (this is where those airdropped SOL actually go, into making the program account rent-exempt), and your program is live on a public network.

It's worth understanding what just happened, though, because it shapes how you ship changes for the rest of your time on Solana. The deploy went through Solana's upgradeable loader, and the wallet that paid (yours) became the program's upgrade authority. The upside: when you fix a bug next week, you run `anchor upgrade` and ship new code to the same address, no redeploy, no new program ID, clients don't even notice. The cost: whoever holds that wallet can replace your program's code wholesale. On devnet that's a shrug. On mainnet the upgrade authority is one of the most sensitive secrets you own, and lesson 6 will treat it with the paranoia it deserves. For today, just register the trade: upgradeable programs are convenient precisely because someone holds the power to change them, and right now that someone is you.

## Prove it's live

So is it actually up there, or are we taking a terminal's word for it? Verify:

```bash
solana program show <PROGRAM_ID> --url devnet
```

Your program ID was printed at the end of the deploy, and it's the pubkey of that keypair file from earlier (same address — told you it was the identity). The output shows the owner, the ProgramData address, the authority, which should be your wallet, and the slot of the last deploy. If that command comes back with real data, your program exists on a public cluster, and anyone in the world can run the same command against the same address and see the same answer, which is a strangely satisfying thing the first time it lands.

The stronger proof is calling it, and you already have the tool for that: the generated TS test talks to your program through the IDL, so pointing it at devnet exercises the real deployed program instead of a local one. We'll do that properly next lesson when we build an actual client.

Before we close, the three failures that catch almost everyone on their first deploy, so future-you can skip the panic:

1. **Insufficient devnet balance**: the deploy dies partway through. Airdrop more, or use faucet.solana.com when the CLI faucet is rate-limiting you.
2. **`declare_id!` mismatch**: you cloned a repo or regenerated keys. `anchor keys sync`, rebuild, redeploy.
3. **Wrong cluster**: everything "works" but nothing is where you're looking. Check `Anchor.toml`. Ask me how I know.

## Where you are now

Three lessons down, three to go, and you've crossed the line that matters most psychologically: your code is no longer a local experiment — it's a live program on a public network, at an address you can send to a friend, and the distance between "I'm learning Solana" and "I have a program on Solana" turns out to be about eight commands. Build, test, sync, fund, deploy, verify. Pretty soon you'll be running that loop without thinking, the way you stopped thinking about `git push` at some point.

Next lesson we build the other half: client development with TypeScript and the wallet adapter, where that IDL file finally earns its keep and your program gets a front door humans can actually use. Happy deploying! 🚀
