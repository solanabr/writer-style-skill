# Anchor 1.0 is out. Should you upgrade?

New toolchain? Renamed packages? A breaking change at every CPI call site? Yes, yes, and yes. Anchor 1.0 shipped, and the list of breaking changes is long enough that you want ten minutes with it before your next `anchor build`, so let's rip the band-aid off.

What actually changed:

- **Self-contained toolchain:** 1.0 targets Solana 3.x / Agave and bundles its own toolchain, which means no external `solana` CLI dependency and one less version matrix to babysit.
- **Renamed TS client:** `@coral-xyz/anchor` is now `@anchor-lang/core`, so the first casualty of the upgrade is every import line in your tests and frontend.
- **CPIs take a `Pubkey`:** `CpiContext::new(...)` and `new_with_signer(...)` now want the program's `Pubkey` (`.key()`) instead of an `AccountInfo`, and this is the one that touches every single CPI call site you have, so budget for it.
- **Checked token transfers:** plain `transfer` is deprecated, and SPL token CPIs now go through `transfer_checked`, which takes the mint and decimals alongside the amount.
- **Space math:** account space is now `T::DISCRIMINATOR.len() + T::INIT_SPACE`, no more magic `8`, and good riddance!
- **Stricter accounts:** duplicate mutable accounts are disallowed by default, which is one of those changes that only hurts if your program was already doing something questionable.
- **One `#[error_code]` enum per program,** and the legacy on-chain IDL instructions are gone — external programs get consumed through `declare_program!()` + Program Metadata now.
- **Testing moved in-process:** the default test template is LiteSVM (Rust), and `anchor test` / `anchor localnet` run against Surfpool instead of `solana-test-validator`.

The migrate-or-wait call depends on where you're standing. New project: start on 1.0, no hesitation, writing fresh code against a version that's already legacy buys you nothing. Production program: every change above is mechanical (a rename, a new signature, a space recalc), but mechanical and broad is exactly the combination where a tired reviewer waves through the one call site that wasn't quite like the others. Migrate behind a branch, not in place, and let CI chew on the whole surface before anything touches a deploy path.

I'll admit my bias here: major releases make me want to upgrade the same afternoon, and afternoon-me has eaten enough broken builds to finally accept the boring branch-first routine.

Go read your CPI call sites.

lfb
