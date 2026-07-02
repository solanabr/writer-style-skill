# From anchor init to devnet: your first program, deployed

I've lost count of the intro Anchor tutorials that end the same way: tests pass, the terminal goes green, everybody celebrates. And your program still exists exactly nowhere. No address, no cluster, nothing a friend could hit from a wallet. Just a binary on your laptop, which is a strange thing to call "shipped."

Here's the part that trips people up: the jump from green tests to a live devnet address is small, and almost none of it is Rust. First deploys rarely die in the program itself; they die in the plumbing around it, and plumbing is quick to fix once you know which pipe burst. A mismatched program ID. An underfunded wallet. A config quietly pointing at the wrong cluster. So today we walk the whole road: init a project, understand what the generator handed you, build, test, deploy to devnet, and prove it's live. By the end you'll have a program ID you can hand to a friend, and they can call it from their machine. I'll keep the routine steps terse and slow down where things bite. Terminal open, tag along.

## Two prerequisites, one command

We only need two installs here: the Rust toolchain and Anchor itself. That's the entire list. Anchor 1.0 bundles the Solana toolchain, so the separate `solana` CLI install (and the version-matching dance that used to come with it) is gone. If you never suffered that dance, lucky you; it was its own little saga.

With both in place, run `anchor init my_program`:

```bash
anchor init my_program
```

Pick a name you can live with, you'll be typing it constantly. Anchor scaffolds the folder and drops you at the starting line. No wallet setup, no cluster choice yet; all of that lives in one config file we'll touch in a minute.

## What `anchor init` actually handed you

So what did that command generate? Four things in this folder matter today:

```text
my_program/
├── Anchor.toml
├── programs/
│   └── my_program/
│       └── src/
│           └── lib.rs
├── tests/
└── migrations/
```

`programs/my_program/src/lib.rs` is the program itself, all of it in one file for now. `tests/` holds a TypeScript test that will double as your first client later on. `migrations/` you can ignore today. And `Anchor.toml` is mission control: which cluster you're talking to, which wallet pays for it. We'll be back in there soon.

The most important file isn't in the tree yet. On your first build, Anchor generates `target/deploy/my_program-keypair.json`, and that keypair is your program's identity. Its public key is your program ID: the address the tests use, the client uses, and eventually the one you hand to other people's wallets. Everything finds you through it. (That file is a real keypair, so treat it like one.)

Now open `lib.rs`. Right at the top sits `declare_id!()`, the same address declared in code, and it must match the deploy keypair. Two sources of truth for one identity, and they drift: clone someone's repo, or regenerate your keys, and suddenly the code claims one address while the keypair answers to another, and nothing warns you until the deploy itself falls over. That mismatch is the #1 first-deploy failure. It ate a whole afternoon of mine once, and the worst part is that the program was never the problem — the config was lying about who it was.

The silver bullet? `anchor keys sync`. It reads your actual keypair and rewrites the declaration to match. One command. Run it after any clone, any key regeneration, any deploy failure you can't otherwise explain.

## Build, then test

Time to compile:

```bash
anchor build
```

The build drops two artifacts: the compiled `.so` in `target/deploy/` (the binary that will live on-chain) and the IDL in `target/idl/`, a JSON description of your program's interface that generated clients read. Keep that IDL in mind; it's how we'll prove the deploy worked at the end. This first build is also the moment `my_program-keypair.json` gets minted, so if `anchor keys sync` is going to matter, now it has something to sync against.

Then comes `anchor test`:

```bash
anchor test
```

Anchor 1.0 changed what happens under this command. Tests run against Surfpool now, not `solana-test-validator`, and the default test template is LiteSVM: Rust, in-process. If an older tutorial ever told you to keep `solana-test-validator` running in a second terminal, that ritual is gone — the template's tests execute inside the test process itself instead of round-tripping to a separate node, and the feedback loop tightens accordingly.

Run it. Watch it pass. It's template code, sure, but a passing run proves the toolchain agrees with your program before any real network gets involved, and that's the thing you want settled before money (even fake money) enters the picture. If something fails here, fix it here; a test that can't pass in-process has no business being sent to a cluster.

## Point it at devnet, then fund it

We're done rehearsing locally. Devnet is Solana's public practice cluster: real validators, real deploys, worthless SOL. Open `Anchor.toml` and set the provider:

```toml
[provider]
cluster = "devnet"
```

The wallet entry in the same section points at a local keypair. That wallet is about to pay for everything, so it needs a balance first.

Devnet SOL is free but rate-limited. `solana airdrop 2` gets you going (typically 2 SOL per request, tops), and when the CLI faucet decides you've had enough, faucet.solana.com is the fallback. Do the math before you start, honestly: a deploy that needs a few SOL, fed by a faucet that hands out 2 at a time, means more than one request; and the limiter has a talent for kicking in at the exact moment you're mid-deploy.

Why does a hello-world need a few SOL at all? Rent. The program account must be rent-exempt (funded well enough that the cluster keeps it around) for roughly 2× the binary size, and a typical starter program lands at a few SOL of devnet balance to deploy. Bigger binary, bigger deposit. Free money, yes, but you still have to go collect it before the deploy will clear.

## The deploy itself 🚀

Say your wallet's funded and the build is fresh. Everything from here is one line:

```bash
anchor deploy --provider.cluster devnet
```

Anchor takes the `.so` from `target/deploy/`, ships it through Solana's upgradeable loader, and prints your program ID. Somewhere on a devnet validator, your code now exists. The first time I watched that line print it felt disproportionately good, and I'd argue the feeling is earned: the gap between "compiles on my machine" and "callable by strangers" is the entire point of the exercise.

Two things happened in the background there. Deploying through the upgradeable loader means the program isn't carved into the chain forever; later changes ship to the same address with `anchor upgrade`, and every client keeps working against the address it already knows, because the identity you synced earlier never changed. And the wallet that ran the deploy is now the upgrade authority — the one key allowed to make that happen.

The catch here is: authority cuts both ways. Whoever holds that keypair can swap out your program's logic wholesale, so the moment anything real depends on this address, that wallet stops being a throwaway file in your home directory and starts being infrastructure. Back it up, and keep it out of the repo. On devnet, shrug. On mainnet, it's the thing you plan around before deploying, not after.

## Don't trust, verify

The deploy command says it worked. Check anyway:

```bash
solana program show <PROGRAM_ID> --url devnet
```

If devnet knows your program, this prints its details back from the cluster itself, not from anything cached on your machine, which makes it the first confirmation in this pipeline you didn't have to take on faith. Don't trust, verify. Even (especially) when the tool already said yes.

Then the real test: call it. The generated TS test in `tests/` already builds a client from the IDL, the same one `anchor build` wrote earlier, so point it at devnet and invoke your instruction against the live deployment. Same code that passed locally, now answered by a cluster you don't control. A green test on your own machine is a claim; an instruction executed on a public cluster is proof. When that call lands, you're deployed in the way that counts.

And if the deploy blew up instead, it's almost always one of three things:

- **Insufficient devnet balance.** Back to the faucet; deploys cost a few SOL, and airdrops are rate-limited, so this one loves to strike halfway through.
- **`declare_id!` mismatch.** The classic from earlier. `anchor keys sync`, rebuild, redeploy.
- **Wrong cluster in `Anchor.toml`.** You deployed somewhere, just not where you're looking. Check `[provider]` before checking anything else.

Three failures, three one-line fixes, and between them they cover most first deploys that go sideways.

## Where this leaves you

So what's in your hands now? A program you wrote, live at an address anyone on the internet can call. That's the loop, and you now own every step of it: init, build, test, fund, deploy, verify. The same loop carries a program all the way to mainnet; only the stakes change.

Don't stop at deployed-once, though. Change something small in `lib.rs` and ship it to the same address with `anchor upgrade`. Watching an address keep its identity while its logic changes will teach you more about how Solana treats programs than another tutorial would, and it's not that hard. And if you hit an error this guide didn't cover, ask. First-deploy failures are a genre; someone has almost certainly catalogued yours.

lfb
