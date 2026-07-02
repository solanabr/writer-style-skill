# From `anchor init` to devnet: your first program, deployed

My first Solana program never left my laptop. The code was fine (well, fine-ish); what killed the evening was everything around it: three separate toolchains, each pinned to a version the other two hated, and me re-running the same install command like persistence was a strategy. If you're starting today instead, good news: Anchor 1.0 bundles the Solana toolchain, so the full prerequisite list is Rust and Anchor. That's it. No separate `solana` CLI install, no version matrix, no lost evening.

So here's the deal for this session: one terminal, `anchor init my_program` at the start, a program live on devnet at the end. We'll scaffold the project, poke at what actually got generated, build it, test it, point the config at devnet, fund a wallet with free fake money, deploy, and then prove the thing is really out there instead of taking the tooling's word for it. Exact commands where a step is interesting, zero ceremony where it isn't. If you can open a terminal without flinching, you're qualified. No prior Anchor required.

## One command, a whole workspace

```bash
anchor init my_program
```

cd in and look around. Four things matter today:

```text
my_program/
├── Anchor.toml                        # cluster + wallet config (we'll be back)
├── programs/my_program/src/lib.rs     # the program itself
├── tests/
└── migrations/
```

`programs/my_program/src/lib.rs` is where the program lives, and it's where you'll spend most of your Anchor life; everything else in the tree is scaffolding around that one file. `Anchor.toml` is the control panel: which cluster you're talking to, which wallet pays for things. Underrated file; it decides where every command in this guide actually aims, and it stars in one of the three classic failures we'll cover at the end. `tests/` and `migrations/` do what they sound like, and you can leave both alone today.

I lied a little, though. The most important file isn't in that tree, because it doesn't exist yet: `target/deploy/my_program-keypair.json` only appears once you build for the first time. It deserves its own section, so let's go create it.

## Build once, meet your program's identity

```bash
anchor build
```

Three artifacts fall out. The compiled `.so` lands in `target/deploy/`; that binary is what will actually live on-chain. The IDL lands in `target/idl/` (a JSON description of your program's instructions and accounts; clients read it so they know how to call you). And on this first build only, Anchor generates `target/deploy/my_program-keypair.json`.

That keypair isn't a build artifact, it's your program's identity. Its public key is your program ID: the address the program will occupy on whatever cluster you deploy to, the handle every client, every test, and every integration will use to find you. Which explains the `declare_id!()` sitting at the top of `lib.rs`: the program stating, in source code, what address it believes it lives at.

Here's the catch, and it is the #1 first-deploy failure: the program ID in `declare_id!()` must match the deploy keypair. I think of it as the identity handshake. `declare_id!()` is the program introducing itself; the keypair is the ID card it shows at the door; if they disagree, no entry. Why would they ever disagree? Easy: fork any Anchor repo. The source ships with the author's `declare_id!()`, your machine mints a brand-new keypair on your first build, and now the code claims one address while your keypair proves another. Same story if you delete or regenerate keys. (Ask me how I know. My first deploy died right here, twice, before I slowed down enough to read what the error was actually telling me.)

The fix is one command:

```bash
anchor keys sync
```

It reads the keypair you actually have and rewrites `declare_id!()` to match. A godsend the first time the mismatch bites you, cheap insurance every run after. Forked something? Regenerated anything? Not sure? Run it. Takes a second.

## Test without the theater

`anchor test` runs the generated suite. Two things changed in Anchor 1.0 that are worth knowing even on day one, mostly because every tutorial older than the release will confidently tell you otherwise. First, the default test template is LiteSVM: Rust tests that execute in-process, no local network to boot before you can check your work. Second, when `anchor test` does need a cluster, it runs against Surfpool, not `solana-test-validator`. If a guide tells you to open a second terminal and babysit a validator while your tests run, that guide is describing a previous era. The practical effect is a tighter loop. You edit, you run, tests pass or they don't, nothing to keep alive in the background.

We're not touching the test contents today. The generated suite exists to prove your pipeline works end to end, and that's exactly the job we need it to do before spending devnet SOL on a build that was broken all along.

Green? Moving on.

## Point it at devnet and fund it

Devnet is a real, public Solana cluster where the SOL is worthless. Real network, real latency, fake money — which makes it the rehearsal stage, the place where a botched first deploy costs you nothing but pride. Nothing technically stops you from deploying straight to mainnet. Please don't; first deploys have a way of containing surprises, and mainnet charges real money for them. Devnet runs the same deploy flow with zero stakes, so every step you practice here transfers as-is.

Open `Anchor.toml` and set the provider block:

```toml
[provider]
cluster = "devnet"
```

While you're in there, confirm that `wallet` in the same provider block points at your local keypair. That wallet is about to do two jobs: pay for the deploy, and (as you'll see shortly) hold a surprising amount of power over the result.

Now, about paying. Why does deploying an empty starter program cost anything at all? Rent. A program account has to be rent-exempt (funded upfront to cover its on-chain footprint), and for programs that footprint is roughly 2× the binary size. For a typical starter program this works out to a few SOL of devnet balance.

```bash
solana airdrop 2
```

(There's the bundled `solana` binary earning its keep, told you the prerequisites were done.) Devnet SOL is free but rate-limited, typically ≤2 SOL per request, so "a few SOL" means asking more than once; space the requests out, the limiter is real. And when the CLI faucet starts refusing you entirely (it will, usually at the least convenient moment), faucet.solana.com hands out the same devnet SOL from a browser. I keep it bookmarked. Not proud, not sorry.

## Deploy. For real this time

```bash
anchor deploy --provider.cluster devnet
```

Watch it go. If it dies immediately complaining about your balance, that's the rent math from a minute ago; airdrop again and rerun. Under the hood, your `.so` ships to the cluster through the upgradeable loader, the piece of Solana that allows a deployed program's binary to be replaced later. And that enables the part I want you to actually register, because it follows you all the way to mainnet: the wallet that deploys (the one from your provider block) becomes the upgrade authority, the key that's allowed to swap the binary.

Upgradability is why iterating on Solana feels sane. Change the code, run `anchor upgrade`, and the new binary lands at the same address; no client re-integrates, no user migrates, nobody even has to know. On the flip side, whoever holds the upgrade authority's keypair can replace your program's behavior wholesale. On devnet that's a shrug. On mainnet that keypair becomes the most dangerous file you own, so start respecting it now, while it guards nothing. Fake money today, real responsibility later.

## Prove it's live

The deploy finished without complaint? Don't take its word for it.

```bash
solana program show <PROGRAM_ID> --url devnet
```

Swap in your program ID, the same address sitting in your `declare_id!()`. If devnet answers with the program account's details, you are, technically, already live. But details on a screen never quite feels like proof, at least for me. The real proof is a call: the generated TS test/client already knows how to talk to your program (it picks up the IDL from `target/idl/` and aims at your address), so point it at devnet and run it. Send the program ID to a friend and their client can build against the same IDL and call you too. That's what an address on a public cluster means.

Take a second with what just happened. Your instruction executed on a cluster you don't run, triggered from your laptop, at an address that now belongs to you. Anyone on the planet can call it. No app store, no deploy review, nobody to ask permission. The first time I watched that happen it quietly rewired what "publishing software" meant to me — honestly, it still does a little.

## The three ways first deploys die

In my experience it's almost always one of these, and all three are sub-minute fixes:

- **Insufficient balance.** The deploy wants a few SOL and airdrops arrive 2 SOL at a time. Run `solana airdrop 2` again, or grab more from faucet.solana.com.
- **The identity handshake fails.** `declare_id!` doesn't match the deploy keypair, usually because you forked a repo or regenerated keys. `anchor keys sync`, then deploy again.
- **Wrong cluster.** `Anchor.toml` still points somewhere else; it needs `[provider] cluster = "devnet"`. Fix the file, or stay explicit every time like we did with `anchor deploy --provider.cluster devnet`.

## You're on-chain. Now what?

From here the loop is the one you'll actually live in: edit `lib.rs`, `anchor build`, `anchor upgrade`, same address, and everyone calling your program simply gets the new behavior. That tight loop between an idea and a live address is the entire game, and you now own every step of it. Honestly, it's not that hard — you just did it once, and the second time is muscle memory.

So ship something small this week. Add an instruction, change a string, anything; the point is to run the upgrade loop once while it's all fresh. Break devnet; breaking things is what devnet is for. And if a deploy refuses to explain itself, my DMs are open. Happy building! 🚀
