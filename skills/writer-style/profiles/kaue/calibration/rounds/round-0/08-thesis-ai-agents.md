# AI agents don't have bank accounts — and won't need them

Picture the dumbest bottleneck in modern software. An agent is halfway through a research job for you. It found the dataset it needs, the API is right there, and the price is, say, three cents a call. The agent can read the docs, write the query, and parse the response, but it cannot do the one thing a vending machine solved decades ago: accept that the item costs three cents, pay three cents, take the item. So it stops. It pings you and waits, or it fails the task outright, and a workflow that ran at machine speed now runs at whenever-you-check-your-notifications speed.

I want to make a bigger claim than "that's annoying," and I'll state it up front so you can shoot at it: agents are becoming economic actors, the banking system structurally cannot serve them, and crypto rails already can. Today, in production, with protocols you can go read.

How I argue it matters as much as the claim. Five pillars, each checkable on its own, then an honest ledger of what's live versus what's me projecting, because the blur between those two is where every bad AI-x-crypto thesis hides. If one pillar breaks for you, you'll know exactly which one, and how much of the thesis it takes down with it.

## Pillar 1: the person-shaped hole

Banks and card networks require a legal person behind every account. That's the entire KYC apparatus in one sentence: before the account exists, a human, or a company that resolves to humans, proves identity, and everything the account does afterward traces back to that person. The fraud and sanctions machinery assumes there is always someone to hold responsible.

An autonomous agent cannot pass KYC. There's no premium tier where this goes away, no enterprise plan with an "agents" checkbox. The best an agent can do on banking rails is ride on a human's credentials with a human in the loop, which means every "my AI pays for things" product you've seen is, underneath, a person's account with an allowance and an approval step bolted on top. Delegation, not agency. And delegation inherits the delegator: the agent can work at 3am, but it pays when you wake up, and it can only buy from whatever the platform holding your card decided to onboard.

I've been guilty of hand-waving this in the wrong direction, big time. For a while I assumed some fintech would eventually just issue accounts to agents, the way banks eventually issued cards to teenagers. Then you look at how the requirement actually works and the assumption dies: the legal person isn't a feature of the account. It IS the account. Remove the person and there's nothing left to open, which is why no bank roadmap fixes this — you'd be asking the rail to delete its own compliance model.

So the wall is structural. Hold that thought while we look at the other side of it.

## Pillar 2: a wallet doesn't ask who you are

A crypto wallet is a keypair. That's the whole pillar, honestly.

An agent can generate a keypair, hold it, sign with it, and spend from it, permissionlessly. Nobody approves the wallet into existence because there's nothing to approve; the chain never authenticates who is signing, it verifies that the signature matches the key. A bank asks "who are you, and are you allowed?" A chain asks "does the math check out?" An agent fails the first question forever and passes the second one all day long.

This is live today, not a roadmap item. No waitlist, no testnet asterisk.

It also inverts the economics of having an account at all. On banking rails, opening an account is an event: paperwork, review, a relationship. On-chain, a keypair is a variable in a program. An agent can hold one wallet or spin up a fresh one per task or per budget, and nobody files anything. Does that mean any script anywhere can just hold money now? Yup. Sit with how strange that is: the exact property that makes these rails terrifying to a compliance officer, that a keypair spends without anyone's permission, is the property that makes them the only rails an agent can natively use. Same fact, two readings. I'll come back to the terrifying reading in the constraints section, because it deserves more than a wink.

## Pillar 3: a price tag on every request

Now the vending machine stops being a metaphor.

x402, which Coinbase shipped in 2025, is a payment protocol built on HTTP 402, and the loop it defines is the vending loop, verbatim: the agent requests a resource, the server responds with a price, the agent pays per call in stablecoins, the server serves the resource. No account. No subscription. Nothing to sign up for, which means nothing to KYC, which means the person-shaped hole from Pillar 1 never opens in the first place. Push the vending analogy one step further and it keeps paying rent: a vending machine doesn't know your name, doesn't run a tab, and doesn't care whether a hand or a robot arm inserted the coin. It verifies the coin. That indifference is the entire feature.

Payment is only half the pairing, though. The other half is how agents find tools at all, and that's MCP, the Model Context Protocol, Anthropic's open standard, now the emerging standard for how agents attach to tools and services. (MCP is also why half my desktop tooling can talk to Claude these days, but that's a different post.) Pay-per-call APIs pair naturally with per-request micropayments, and the fit is worth spelling out. Subscriptions assume a persistent customer with a name and predictable usage. An agent is the opposite kind of customer: it might call one tool ten thousand times this week and never again, and touch a hundred other tools exactly once each. Nobody subscribes to a hundred services to use each one once, and no serious operator wants to manage a hundred logins for a bot either. Per-call pricing is how an agent actually consumes. MCP is the socket the agent plugs into; x402 is the meter on the socket.

## Pillar 4: a rail where the fee is a rounding error

For per-call machine payments, the settlement layer has one job: be fast and cheap enough that neither machine has to think about it. This is where numbers argue better than prose, so let me keep this stretch flat and just lay them out.

Solana produces blocks roughly every 400ms. The base fee is 5,000 lamports per signature, which lands at fractions of a cent. Stablecoin transfers move through `transfer_checked`. Optimistic confirmation arrives sub-second, and yes, "optimistic" is a qualifier doing real work in that sentence; the stronger guarantee trails behind it.

Run those numbers against the vending loop. A payment of a few cents needs a fee that's a rounding error on the payment itself, and fractions of a cent under a cents-sized purchase clears that bar with room to spare. The payment also needs to settle inside the window a machine expects a response in, and sub-second confirmation fits inside an ordinary request timeout. On rails where a transfer takes days and carries flat costs in dollars, a three-cent purchase makes no sense. Here it's a log line.

You also don't need to build the plumbing yourself, and you shouldn't. Open-source agent tooling already exists, Solana Agent Kit being the obvious example; fork first, write second. For getting an agent from "holds a keypair" to "transacts" without hand-rolling everything, honestly, a godsend.

## Pillar 5: the corridor where it lands first

Every thesis needs a first lane, so here's my candidate, and I'm flagging now that the candidacy itself is a projection.

Start with the live half. Cross-border micro-payouts, paying contributors, scrapers, data-labelers, are brutal on banking rails, because SWIFT and intermediary costs are flat while the payments are small: the fee doesn't shrink with the amount, so on a small payout the plumbing can be worth more than the payment it moves. Those same payouts are already cheapest in emerging-market corridors via stablecoins. None of that involves an agent; it's just how the cost table looks today. I've signed off on enough contributor payout runs at Superteam Brazil to have felt both halves personally, the wire that costs more than the line item it carries, and the stablecoin transfer that just… arrives. Builders in these corridors aren't waiting for this thesis; they already live on the rails it needs, which is exactly why I'd bet the first real agent payments show up here rather than in some bank's innovation lab.

Now the projected half, labeled as such: if agents become payers, this is a plausible early lane. The scraping pipeline that pays its labelers per task. The research agent that pays contributors per accepted item. Small, cross-border, cost-sensitive: everything banking rails price worst and these rails price best. I believe it. It is still a projection, not a measurement.

## What's live, what's projection, and what could kill it

I promised auditable, so let's do the ledger.

**Live today:** an agent holding a keypair, signing, spending, permissionlessly. x402 pricing and settling machine-to-machine calls in stablecoins, no account or subscription required. MCP as the emerging standard for attaching agents to tools. A settlement rail at ~400ms blocks and fractions of a cent in fees. Stablecoin corridors undercutting flat SWIFT costs on small cross-border payouts.

**Projection:** agents becoming a payer class that matters. The corridor as the first big lane. Any volume projection for agent commerce, and I mean any, mine included, is speculation, not measurement. Nobody can measure a market that barely exists yet.

And two constraints, stated at full strength, because a thesis you refuse to stress isn't a thesis.

First: custody. A compromised agent is a compromised wallet. Take the skeptic's version, which is fair: "you've described the ideal rail for a hijacked bot to drain funds in 400ms increments, with no bank to call and no chargeback to file." Grant all of it. Agent custody of keys is an unsolved trust problem, and I won't pretend the ecosystem has an answer, because it doesn't yet. The only honest mitigation I know today is keeping agent wallets small enough that a drain is a bad day rather than a catastrophe, and that's damage control rather than a solution. Well, does the thesis survive the concession? I think so, and here's the shape of why: the claim was never "this is safe." The claim is that banks structurally can't serve agents and these rails structurally can. Custody decides how much value we dare put behind that capability, not whether the capability exists.

Second: the law. Regulatory treatment of autonomous economic actors is undefined, and undefined cuts both ways: nothing forbids an agent's wallet today, and nothing protects it either. The person requirement I spent Pillar 1 calling a wall exists because societies want someone accountable, and when regulators eventually define who answers for an agent's transactions, that answer could narrow this thesis or switch parts of it off in some jurisdictions. I have no prediction there, and I'm suspicious of anyone who does.

## The short version

Banks authenticate persons. Chains verify signatures. An agent has a signature and will never have personhood, and that asymmetry doesn't age: no bank roadmap closes it, because the person requirement is the compliance model itself, and no crypto breakthrough needs to arrive, because the keypair side already works.

Maybe agent commerce stays small for years. That outcome is fully compatible with every pillar above; the rails don't need the traffic to justify themselves, they're live either way. But if you'd rather feel the thesis than debate it, it's not that hard: give an agent a wallet with a couple of dollars on it, point it at an x402-priced endpoint, and watch a piece of software buy something with no human in the loop. The first time it happens on your own machine, this stops being abstract.

If you build one, or you think Pillar 5 is the wrong first lane, my DMs are open. Happy building! 🚀
