# AI agents don't have bank accounts. They won't need them.

Give an agent a real job and watch where it stalls. I shipped a production-ready crypto Telegram bot in one day with Claude and MCP (one day, honestly, that part still surprises me), and the bottleneck was never the intelligence. It was the moment the thing needed to buy something. A paid API here, a rate-limited data feed there, and suddenly my "autonomous" agent is standing at a counter with no wallet, waiting for a human — me — to come swipe a card it will never be allowed to hold.

So here's the thesis, stated up front so you can hold me to it: agents are becoming economic actors, the banking system structurally cannot serve them, and crypto rails can. Today. The rest of this piece earns that claim one pillar at a time, and I'll be explicit about which pillars are live right now and which ones are me projecting.

## The KYC wall

Start with the boring pillar, because everything else leans on it. A bank account, a card, a payment processor login: each one requires a legal person behind it. That's what KYC is. Less a form than a premise, the assumption that behind every balance sits a human (or a company full of humans) who can be identified, held liable, sued, sanctioned, made to answer for what the money does.

An autonomous agent cannot pass KYC. There's no clever integration coming to fix that, because the requirement is the system working as designed. Deterrence needs someone to deter.

Run the workarounds yourself. Hand the agent your credit card? That's you transacting with extra steps, plus your liability when it does something dumb. Provision it a virtual card? The card rides your identity; there is no "its name" to put on anything. Give it API access to your bank? Same arrangement in a different costume. You can dress the dependency up in nicer and nicer UX, but it stays a dependency: somewhere a person vouches, and the person is the account. Every path collapses to the same shape: the agent rides a human's credentials, with a human in the loop. Fine for a demo. Quietly fatal for autonomy, because an actor that must wake its owner to spend pennies isn't an economic actor, it's a shopping list with ambition.

I'm going to call this the KYC wall, and I want to be fair to it: it exists for decent reasons, fraud recourse and sanctions enforcement are real jobs. But a wall built to check persons doesn't bend for software. It just excludes it.

## A wallet is just a keypair

What does onboarding look like on crypto rails?

Generate a keypair. Done. That's the entire application process, and there was never a committee that could have rejected it, because a wallet was never an account in the first place: it's a number the agent generated, plus the signatures only that number can produce. An agent can hold one, sign with it, and spend from it, permissionlessly. This is live today, not a roadmap item. No pilot program, no waitlist.

The line I keep coming back to, and the one to keep if you keep nothing else: banks verify persons; chains verify signatures. A signature is something an agent produces natively, at machine speed, without asking permission from anyone. Personhood is something it will never produce at all. We keep trying to match this new actor to rails that authenticate the one thing it doesn't have, then acting surprised when a human ends up duct-taped into the middle of every flow.

The first time you watch a process you wrote sign a transaction on its own is a strange little moment, somewhere between "I automated a chore" and "I gave something an allowance." I recommend it.

## The protocols showed up

So the keypair gives an agent a hand to pay with. It still needs a counter to pay at, and subscriptions are the wrong counter: a subscription assumes an account, an email, a dashboard, a card on file, a human who might feel bad about churning. Person-shaped furniture, all of it.

What machine-to-machine commerce actually wants is closer to a vending machine than a storefront. Request the thing, see the price, pay, receive. No relationship, no memory.

That's x402. Coinbase shipped it in 2025: a payment protocol built on HTTP 402, where an agent requests a resource, gets back a price, and pays per call in stablecoins, with no account and no subscription anywhere in the loop. The whole signup flow collapses into the request itself.

And on the other side of the stack, MCP (the Model Context Protocol, an open standard out of Anthropic) is emerging as the standard for how agents attach to tools and services at all. Put the two next to each other and the fit is almost suspicious: MCP turns every service into something an agent calls per-request, x402 turns every request into something an agent can pay for per call, and pay-per-call APIs pair naturally with per-request micropayments. The tool call and the payment want to be the same gesture.

I'll admit my bias, I've been telling anyone who'll listen that if you're not wiring agents into MCP servers yet you're leaving real productivity on the table — so discount me accordingly. But the plumbing here is shipped and documented, which is more than most "AI x crypto" pitches can say for themselves.

## The rail underneath

For any of this to work at machine scale, settlement has to be faster than the conversation and cheaper than the thing being bought. On Solana, concretely: blocks land about every 400ms. The base fee is 5,000 lamports per signature, which puts fees at fractions of a cent. A stablecoin payment is a `transfer_checked` instruction, and optimistic confirmation lands in under a second.

The fee math is the entire ballgame. If the resource being bought costs cents, the rail cannot charge cents to move cents; a fee that amounts to a rounding error on the price is what makes per-call payment thinkable at all, and nothing else in this piece works without that property holding.

Speed is the quieter half of the same argument. An agent's whole loop runs in seconds, so a settlement layer that clears in minutes would leave every tool call idling behind its own payment. A block time measured in milliseconds keeps the paying inside the rhythm of the doing.

You also don't have to start from a blank file: open-source agent tooling already exists, and Solana Agent Kit is where I'd point you first.

Scope this honestly, though. The rail settles value: it doesn't decide whether the agent should have paid, it doesn't meter the quality of what came back, and it won't arbitrate the dispute when a data feed sells your agent garbage, all of that lives a layer up. Settlement is narrow. Narrow is fine.

## Where it lands first (my best guess)

I owe you a register shift here. Everything above this line is live and checkable; this section is a projection, my read on where agent payments actually start. The earlier pillars you can verify, this one you can only argue with.

The corridor I keep staring at is cross-border micro-payouts: paying contributors, scrapers, data-labelers. Lots of small payments, often across borders, and on banking rails that profile is quietly brutal, because the flat SWIFT and intermediary costs don't shrink just because the payment is small. On a micro-payout, the fees dwarf the payment itself. Stablecoins invert that, and the inversion is sharpest in emerging-market corridors, where they're already the cheapest way to move small amounts. I live on one end of those corridors, so let me say it plainly: the places everyone frames as underserved are, for this particular future, ahead of the curve. The cheap lane got built here first.

I've also run this math in real life, paying out bounty contributors in stablecoins because the banking route would have eaten the small payouts whole. Now run the projection forward: if agents start commissioning piecework, labeling runs, scraping jobs, verification passes, from humans (and, weirder, from other agents), they inherit exactly this payment profile, tiny, frequent, borderless, on rails that already win that corridor for humans today.

Plausible early lane. That's the strongest honest phrasing I can give you: plausible, not proven, and I'd watch it before anything else in this space.

## The part where I argue against myself

A thesis you can't attack is marketing. Here are the three strongest counters I know, in the shape a skeptic would give them.

**Custody is unsolved.** A compromised agent is a compromised wallet. Full stop. Prompt-inject the agent, exfiltrate the key, and the same permissionlessness that let it spend without asking anyone lets the attacker spend without asking anyone; the wall that wasn't there to slow the agent down isn't there to slow the thief down either. I don't have a clean answer, and I distrust anyone who claims one. My working posture is the one I hold for AI everywhere: it's a sidekick you manage, never the architect. Scoped keys, small balances, spending caps, a human above it in the org chart. That contains the damage; it doesn't solve the trust problem.

**Regulation is undefined.** Nobody can tell you, today, how an autonomous economic actor gets treated the moment it becomes a legal question instead of a payments demo, because the regulatory treatment simply doesn't exist yet. The KYC wall could get rebuilt in new places. Some of the rebuild might even be reasonable. My honest guess, and it's only a guess: the answers arrive late and unevenly, jurisdiction by jurisdiction, so build like ambiguity is part of the spec.

**The market size is vibes.** Any volume projection for agent commerce is speculation, not measurement. Nobody has measured it because there isn't much to measure yet, and that includes whatever enthusiasm is leaking out of my own paragraphs.

If those three don't slow you down a little, you read them too fast. For me they change the slope of my confidence, not the direction.

## Keys, not accounts

Zoom out once. Every economic actor we've ever built rails for came with a person attached, so we built rails that authenticate persons, and those rails work exactly as long as the actor at the counter is, somewhere underneath, a person. Agents are the first actors showing up without one. No market size fixes that mismatch; it lives in the design. Banks verify persons; chains verify signatures. That one sentence is the whole piece, everything else was me showing you the load it carries.

What's live: the keypair, the signing, the spending, x402, MCP, a rail settling in under a second for fractions of a cent. What's projection: which corridor lights up first, how fast, how big. I've labeled the guesses as guesses so you can grade me later.

If you build agents, give one a wallet on devnet this weekend, it's not that hard! And if you think I'm wrong, especially about the corridor, tell me where; my DMs are open 🤝

What a time to be alive!
