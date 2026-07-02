# Anchor 1.0 is out — should you upgrade?

You bump a program to Anchor 1.0, hit build, and the compiler hands back a wall of red. Every CPI call site. Nothing you broke. That's just the release, and the real decision is when you eat it, so let's make that call quick.

What actually changed:

- Anchor 1.0 targets Solana 3.x / Agave and bundles its own toolchain. The external `solana` CLI dependency is gone.
- The TS client is renamed: `@coral-xyz/anchor` → `@anchor-lang/core`.
- `CpiContext::new(...)` and `new_with_signer(...)` now take the program `Pubkey` (`.key()`), not an `AccountInfo`. This is the one that touches every CPI call site.
- SPL token CPIs use `transfer_checked` (mint + decimals). Plain `transfer` is deprecated.
- Space is `T::DISCRIMINATOR.len() + T::INIT_SPACE`. No more magic `8`.
- Duplicate mutable accounts are disallowed by default.
- Only one `#[error_code]` enum per program now, and legacy on-chain IDL instructions are removed; external programs are consumed via `declare_program!()` + Program Metadata.
- The default test template is LiteSVM (Rust), and `anchor test` / `anchor localnet` run against Surfpool instead of `solana-test-validator`.

None of this is conceptually hard. The cost is surface area: every CPI call site in the codebase, every space calc, a package rename rippling through every client import you own. Mechanical, but broad. And honestly, I've been the guy who leaves a version bump rotting in a branch for months because "we'll do it right after this feature," and with a break this wide that habit just means paying the same bill later, with interest.

So, do you migrate today? Depends which side of the repo you're on. Starting a new project: go 1.0 from the first commit; there's no reason to write CPI call sites you'll just rewrite. If it's a production program already earning its keep, migrate behind a branch, not in place: port it there, let the full suite chew on it under Surfpool, and only point main at the new stack once everything comes back green.

The upgrade itself is grunt work: broad, mechanical, a little boring. Take the branch route and it stays boring, which is exactly what you want from a migration. Save the excitement for what you ship on top of it.

Happy building! 🚀
