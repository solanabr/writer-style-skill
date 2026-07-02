# Anchor 1.0 is out. Should you upgrade?

It shipped. And if you run an Anchor program in production, I know which part of the release notes you opened first, and it wasn't the features list.

Fair. Breaking changes first, verdict after.

- **The toolchain is bundled.** 1.0 targets Solana 3.x / Agave and ships its own toolchain, so there's no external `solana` CLI to version-match anymore.
- **The TS package moved.** `@coral-xyz/anchor` is now `@anchor-lang/core`.
- **`CpiContext::new(...)` and `new_with_signer(...)` now take the program `Pubkey`** (`.key()`), not an `AccountInfo`. This touches every CPI call site you have. Every one.
- **SPL token CPIs use `transfer_checked`** (mint + decimals). Plain `transfer` is deprecated.
- **Space is `T::DISCRIMINATOR.len() + T::INIT_SPACE`.** The magic `8` is gone (good riddance — mine went in on autopilot for years).
- **Duplicate mutable accounts are disallowed by default.**
- **One `#[error_code]` enum per program.** Legacy on-chain IDL instructions are removed; external programs are consumed via `declare_program!()` + Program Metadata.
- **The test stack changed too.** The default template is LiteSVM (Rust), and `anchor test` / `anchor localnet` now run against Surfpool instead of `solana-test-validator`.

Notice what's *not* on that list? A redesign. Nothing up there makes you rethink your accounts or your architecture. Renames, signatures, defaults. Mechanical. The catch here is: the blast radius is wide anyway (every CPI call site, every space calculation, plus the package rename in every client), and mechanical-but-broad is exactly the kind of migration where nothing is hard and one missed call site still slips through review.

So, should you upgrade?

New project: start on 1.0, no debate. Fresh code on a deprecated API surface helps nobody, least of all you in six months.

Production program: migrate, but behind a branch, not in place. Branch it, then let the compiler march you through every `CpiContext` it just broke, fix the space calculations while you're in there, swap the client to `@anchor-lang/core`, and let the Surfpool-backed `anchor test` tell you when the whole thing is green again. Merge on green. Not before.

That's the whole decision, honestly. The changelog reads scarier than the diff will feel — branch it this week and see for yourself. It's not that hard.

cya 👋
