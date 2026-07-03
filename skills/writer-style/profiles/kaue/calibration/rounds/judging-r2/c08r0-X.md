# AI agents don't have bank accounts — and won't need them

I'm no AI researcher. I don't train models, I can't tell you when the next capability jump lands, and I won't pretend otherwise. What I have instead is a review queue. Over the last year I've watched agents show up in open bounties with working submissions, I've wired agents into my own workflow over MCP and let them run jobs while I sleep, and I've slowly made peace with a strange fact: some of the contributors I evaluate are not people. They produce real work. Occasionally they win.

And every time one of them earns something, we slam into the same wall. The money layer assumes a human is standing there.

So let me put the thesis up front where you can shoot at it: autonomous agents are becoming economic actors, the banking system structurally cannot serve them, and crypto rails can serve them today. That's a narrower claim than "crypto wins because decentralization is good", and I want to build it out of four pillars you can kick one at a time: a key, a meter, a rail, and a corridor. Three of them are live right now. The fourth is partly a projection, and I'll flag it loudly when we get there.

## The membership and the key

Start with why banks are out of this game, because it's not the reason people usually reach for.

It's not that banks are slow or expensive (they're both, but that's survivable). The real problem is that a bank account is a membership. Behind every account and every card network sits a hard requirement for a legal person: a name, a document, a KYC file, someone a court can reach. An autonomous agent cannot pass KYC. Not "struggles to". Cannot, structurally, because there is no legal person in there to verify. The best an agent can do today is ride on a human's credentials, with a human in the loop clicking the approvals, which means it isn't an economic actor at all. It's autocomplete with a spending limit.

Run through the workarounds and watch them all collapse into the same thing. Give the agent a virtual card and it's your card, your name, your liability. List the agent as a "user" on a corporate account and a human still owns the account and approves the spend. Sign it up with some agent-banking startup promising friendlier onboarding and the onboarding is friendlier for the human filling in the forms. Every version reduces to a human vouching, holding, and approving, because the system's unit of trust is the legal person, and no amount of better UX changes the unit.

A wallet is a different kind of object entirely. A crypto wallet is a keypair. An agent can hold one, sign with it, and spend from it, permissionlessly, with no application form, because there is nothing to apply to. A key doesn't ask who's holding it.

To be precise about what's live: an agent holding a keypair can transact today. This is boring, deployed infrastructure, not a roadmap slide. Banking requires personhood; a wallet requires only the ability to compute a signature, and computing signatures is the one thing software has never once struggled with.

Pillar one, the key. Kick it if you like. I don't think it moves.

## Pillar two: the meter

Can an agent actually transact the way agents need to, though? Holding money is one thing; machine commerce doesn't look like buying sneakers. It looks like thousands of tiny purchases of requests, data, and compute, most of them worth fractions of a cent, none of them worth a signup flow.

Notice also what agents are not: durable customers. An agent might exist for the length of one job, spun up, run, torn down. Subscriptions assume a persistent identity to bill; accounts assume a relationship worth maintaining. A meter assumes nothing except that whoever is calling can pay for this call, right now, which happens to be a perfect description of the customer an API actually has when that customer is software.

This is where x402 comes in. In 2025, Coinbase shipped it: a payment protocol for machine-to-machine payments built on HTTP 402, the "Payment Required" status code that (as far as I can tell) spent decades sitting in the spec mostly unused, like the web reserved a parking spot for machine money before anyone knew what would park in it. The flow is exactly the shape a machine wants: request a resource, get back a price, pay per call in stablecoins, receive the resource. No account, no subscription, nothing that assumes a creature with an email address.

Now pair that with MCP, the Model Context Protocol: Anthropic's open standard, and the emerging default for how agents attach to tools and services. MCP standardizes the plugging-in; x402-style payments standardize the paying. Pay-per-call APIs pair naturally with per-request micropayments, and I'll admit my bias openly here: half my own tooling runs through MCP servers at this point, so when I look at this pairing I'm not evaluating a whitepaper, I'm describing my own terminal.

That's pillar two, the meter, and it's just as live as the key.

## Pillar three: the rail

Micropayments kept getting announced and kept dying, and the disease was always the same: when settling a payment costs more than the payment itself, the economics collapse back into subscriptions and accounts, which drags you right back into memberships and KYC. The meter is worthless without a rail cheap enough to run it on.

So let's name numbers instead of adjectives. Solana produces blocks roughly every 400ms. The base fee is 5,000 lamports per signature, which lands at fractions of a cent. Stablecoin transfers go through `transfer_checked`, and optimistic confirmation arrives sub-second. For a human tapping a card, sub-second versus three seconds is a shrug, for an agent making a thousand metered calls an hour it decides whether metering is an architecture or a joke.

And you don't have to wire any of this from scratch, open-source agent tooling already exists (Solana Agent Kit is the obvious example), so do the unglamorous right thing: fork what's there, credit the people who built it, and spend your originality on the product instead of the plumbing.

One boundary, to keep the claim honest: none of this makes Solana the only conceivable rail, and I'm not arguing that. The claim is smaller and harder to dodge. A rail this fast and this cheap exists right now, which means the meter has something real to run on.

## Pillar four: the corridor

Every new payment rail needs a first lane where it isn't just better but embarrassingly better. For agent payments I think that lane is already visible, and I should tell you up front why I'm not neutral about this one.

Cross-border micro-payouts, paying contributors, scrapers, data-labelers, are quietly brutal on banking rails: the flat SWIFT and intermediary fees dwarf the small payments they carry. A flat fee is a regressive tax on payment size, it disappears inside a large transfer and swallows a small one whole. The same transfers are cheapest in emerging-market corridors via stablecoins, and that is exactly where I live, professionally speaking. I run contributor payout rounds at Superteam Brazil, and I've felt both halves of this personally, I've been the person a cross-border payment crawled toward and the person trying to push a batch of small payouts through rails that were never built for them, and both ends teach you the same lesson. Watching a stablecoin payout settle in seconds, for less than a cent, after years of flat fees eating small payments alive — honestly, a godsend.

Now the flag I promised. The fact is that these corridors are the cheap lane today. The projection (mine, and I'm labeling it as one) is that this becomes the early lane for agent payments specifically: a scraping agent in one country paying data-labelers in another (agents or humans! the corridor doesn't care), per task, in stablecoins, with no bank in the loop because no bank could be in the loop. I'd bet on it. I can't prove it yet.

## Where the argument gets weaker

Now the uncomfortable part. I'd rather hand you three honest holes than one smooth story, so here they are, in descending order of how much they worry me.

Custody. Remember the key that doesn't ask who's holding it? That indifference cuts both ways, big time. A compromised agent is a compromised wallet: no fraud department, no chargeback, no password reset, no branch to walk into. Agent custody of keys is an unsolved trust problem, genuinely unsolved, and every mitigation I've seen so far (small hot wallets, spending caps, a human co-signing above a threshold) is a way of shrinking the blast radius rather than removing it. The same property that lets an agent hold money is the property that makes robbing one clean. (Completely unrelated: halfway through this section I got up to check where my own hardware wallet was. It was exactly where it always is. Great use of everyone's afternoon.)

Regulation. The regulatory treatment of autonomous economic actors is undefined, and I mean that word literally: if an agent pays for something it shouldn't have, nobody can tell you today whether the developer, the operator, the model provider, or the keyholder is liable. Serious people will have to answer that, and I have no prediction to offer beyond the observation that undefined states don't stay undefined forever: sooner or later someone writes the rule, and the answer will reshape what agent wallets are allowed to touch.

Volume. Any number I could give you for the size of agent commerce would be speculation dressed up as measurement, so I'm not giving you one. The pillars above argue that the door is open. They say nothing about how many walk through it, or when.

## What I'd do with this

Assemble the pillars and the shape is hard to unsee. The key works today. The meter works today. The rail works today. The corridor is where I'd place the first real bet, and it is a bet; I've labeled what's live and what's projection, and I'd rather you hold me to those labels than quote the optimistic half back at me.

If you're building here, start embarrassingly small. One agent, one keypair holding ten dollars in stablecoins, one metered API behind x402, and a hard spending cap you set while re-reading the custody paragraph. That's a weekend, not a company. But it puts you on the right side of the door while the banking system is still asking your agent for a passport it will never have.

Keep building. And if you wire one of these up and it breaks somewhere interesting, I genuinely want to hear about it.
