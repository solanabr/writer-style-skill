# Anchor 1.0 is out

Tired of pinning a `solana` CLI to match your Anchor version, of CPI contexts demanding a whole `AccountInfo` when all they ever read was the key, of that magic `8` in every space calc you stopped questioning around your third program? Anchor 1.0 shipped, and it goes after all three!

The shape of the release: it targets Solana 3.x / Agave and bundles its own toolchain, so the external `solana` CLI dependency is gone entirely, no more matching framework version to CLI version and praying, which in my own setups was quietly the top source of works-on-my-machine bugs. Oh, and the TS client got renamed, `@coral-xyz/anchor` is now `@anchor-lang/core`, so your frontend imports churn along with the program.

What breaks is broader. `CpiContext::new(...)` and `new_with_signer(...)` now take the program's `Pubkey` (a `.key()`) instead of an `AccountInfo`, and that touches every CPI call site you have. Plain `transfer` is deprecated in favor of `transfer_checked`, which now wants the mint and the decimals alongside the amount, and space calculations drop the magic `8` for `T::DISCRIMINATOR.len() + T::INIT_SPACE`. Duplicate mutable accounts are disallowed by default now, you get exactly one `#[error_code]` enum per program, and the legacy on-chain IDL instructions are gone; external programs are consumed through `declare_program!()` plus Program Metadata. Even the testing story moved: the default template is LiteSVM in Rust, and `anchor test` / `anchor localnet` run against Surfpool instead of `solana-test-validator`.

I migrated a two-program escrow setup last weekend to feel out how bad it actually gets, and the honest answer is: less bad than the changelog reads. ripgrep counted 17 `CpiContext` call sites across both programs, and the edits took me about an hour because the compiler does the navigating for you, every stale call site is a loud type error instead of a silent behavior change. The space calcs took ten minutes; the thing that actually cost me the evening was the package rename, which rippled into a pile of client tests I had honestly forgotten existed.

As for migrating: new project, start on 1.0 and don't look back. Production program, the changes are mechanical but they are everywhere — every CPI call site, every space calc, a package rename across your whole client — so do it behind a branch, not in place, and let CI catch what your eyes skim past. Yes, that's a noisy week of diffs, but you come out the other side with a toolchain that finally stops fighting you.

lfb
