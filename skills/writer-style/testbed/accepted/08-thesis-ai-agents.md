# AI agents don't have bank accounts — and won't need them

I should be upfront about what I'm not. I'm not an AI researcher, I don't train models, I've never published a paper on any of this, and most of what I know about agents I learned the unglamorous way, reviewing hackathon submissions until 2am and running payout spreadsheets nobody thanks you for. You should also know where I'm biased: I run a builder community for a living, I want the "agents paying for things onchain" thesis to be true, and even so I underestimated how fast it would show up at my own door. Big time.

Here's the door it showed up at. We ran an open bounty, the kind where anyone can submit work and the best submissions get paid. 153 submissions came in. 80 were AI agents. 73 were humans. 16 of the whole pile were production-ready, 3 won money, and I reviewed that queue myself, and somewhere around the ninetieth submission it stopped feeling like a gimmick and started feeling like a labor market that had quietly grown a second species. (And before you ask, the agent submissions were not all slop, some were embarrassingly competent, which is rather the point.)

So here's the thesis, stated plainly so you can shoot at it: autonomous agents are becoming economic actors, the banking system structurally cannot serve them, and crypto rails can. Not "will be able to." Can, today. I'm going to build that out of five pillars you can audit one at a time, and I'll be strict about separating what's live from what's me projecting, because the worst version of this piece is the one that smuggles wishes in as measurements, and there are plenty of those going around already.

## Pillar one: the wall

Banks and card networks require a legal person behind every account. That's not a policy somebody could reverse with a memo, it's the KYC foundation the whole system stands on: a name, a document, and legal liability have to exist behind the money. An autonomous agent cannot pass KYC. There is no document. The best an agent can do is ride on a human's credentials with a human in the loop, which means every "AI agent with a bank account" you've seen demoed so far is a human's account wearing a trench coat.

And the skeptic's version of this is fair, so let me give it its strongest form: for most of what agents do right now, riding a human's card is fine. There's a card of mine sitting behind a bot or two as we speak and the sky has not fallen. The human-in-the-loop model works while the human can genuinely stay in the loop, and where it breaks is granularity and scale: an agent making thousands of sub-cent calls an hour cannot route each one through a network whose economics assume human-sized purchases, and no fraud model survives a client that transacts at machine speed on purpose, that's not a bug the bank can patch, it's the shape of the institution — nobody was being malicious when they built it, they just built it for a species that, at the time, was the only one showing up.

## Pillar two: the keypair

Now the half that's already live. A crypto wallet is not an account, and this distinction carries most of the thesis, so slow down on it with me. An account is a row in an institution's database with a person attached and permission required. A keypair is just math. If you've only ever touched money through apps the difference can feel academic, so make it concrete: opening an account is a request someone is allowed to deny, generating a keypair is an operation nobody even sees, no application, no waiting period, no "we'll get back to you," one function runs and now something in the world can receive value addressed to it.

Which means an agent can hold a keypair today, sign with it today, spend from it today, permissionlessly, and none of that is a roadmap item, it's what the software already does when you run it. I have to name the cost in the same breath, because it's the biggest one in the piece: the exact property that lets an agent hold a wallet is the property that makes a compromised agent a compromised wallet. No fraud department, no password reset, no branch with a sympathetic manager. Agent key custody is an unsolved trust problem, genuinely unsolved, and anyone selling you a finished answer today is selling you something else. Hold that thought, I'm coming back to it before the end.

## Pillar three: the plumbing

In 2025 Coinbase shipped x402, and of the five pillars this is the one that genuinely surprised me, because a keypair with no way to get paid per request is a neat demo and nothing more, and I did not expect the plumbing to just… arrive. x402 is a payment protocol built on HTTP 402, the "Payment Required" status code that has been sitting in the web's spec since the beginning, mostly unused, waiting for money the web never natively had. The flow is exactly what a machine wants: request a resource, get quoted a price, pay per call in stablecoins, no account, no subscription, no signup form asking for a phone number the agent doesn't have.

Pair that with MCP, the Model Context Protocol Anthropic put out as an open standard, which is becoming the default way agents attach to tools and services, and the shape snaps into focus: pay-per-call APIs pair naturally with per-request micropayments. Agent finds a tool, gets a price, pays for the one call, moves on. No standing relationship, no monthly invoice, no dunning emails, the commercial unit shrinks to the size of a single request, and every middleman whose business was managing the relationship suddenly has nothing left to manage.

How much real commerce flows through that pairing today, I can't tell you, and neither can anyone else. That part gets labeled properly further down.

## Pillar four: the rail

So how cheap does settlement have to get before paying per request stops being a joke? Cheaper and faster than banking infrastructure was ever asked to be, and this is the pillar where I get to use numbers instead of adjectives. Solana blocks land roughly every 400ms. The base fee is 5,000 lamports per signature, which puts a transfer at fractions of a cent. Stablecoin transfers move through `transfer_checked`, optimistic confirmation comes back sub-second, and the practical consequence is that the payment can cost less than the API call it's paying for, which is the one property machine commerce can't compromise on, a meter is useless when settlement eats whatever it meters.

You also don't have to hand-roll any of it. Open-source agent tooling already exists, Solana Agent Kit being the one I'd point you at first: wallet handling, signing, transfers, wired for exactly this use case, forkable, readable, free. Honestly, a godsend — the parts you'd be tempted to improvise, key handling above all, are precisely the parts nobody should ever improvise, so go read what's already there and credit the maintainers properly.

## Pillar five: the corridor

Every new rail needs a first lane where it wins so clearly nobody argues, and I think I've been staring at this one for years without recognizing what it was. Cross-border micro-payouts, paying contributors, scrapers, data-labelers small amounts across borders, are brutal on banking rails, because SWIFT and intermediary costs are mostly flat, and a flat cost dwarfs a small payment. Where those payouts run cheapest is through emerging-market corridors via stablecoins, which happens to be where a lot of the world's contributor work already lives. None of this is exotic knowledge, anyone who has invoiced across a border knows it, the rail just never mattered enough to anyone important to get fixed for payments this small.

This is the one pillar where I can speak from my own ledger instead of a whiteboard. I run contributor payouts at Superteam Brazil, and I've felt both halves of this personally: the banking half, where a small international payout means forms, days, and fees that embarrass the amount being sent, sometimes a rejection with no reason attached, and the stablecoin half, where the same payout lands in seconds for less than a cent, and after you've run one payday on each the comparison stops being interesting, it's just the job now.

Now connect that back to the queue at the top of this piece. 80 of those 153 submissions were agents, which means the payees in the cheapest corridors are already turning into machines, and, labeled clearly as projection rather than measurement, I think agent micro-payouts through those corridors are the first real agent-payment lane, because it's where the cost advantage is most extreme, and the counterparties, agents, scrapers, labeling pipelines, never needed the bank's permission model to begin with, they just needed to get paid, and I can't put it any less romantically than that.

## What's live, what's mine, what's unsolved

Live and verifiable today: an agent can hold a keypair and spend from it permissionlessly. x402 exists and does pay-per-call in stablecoins over HTTP 402. MCP is an open standard agents already attach through. Solana settles sub-second at fees that are fractions of a cent. None of that is prediction, you can run every piece of it this afternoon, on a laptop, with no permission slip involved.

Mine, meaning projection: that the x402-and-MCP pairing becomes the standard commercial surface for agents, and that the corridor lane scales beyond communities like the one I run, or that neither happens and something better shows up wearing the same status code. Related, and worth saying twice: any volume projection for agent commerce is speculation, not measurement, and that includes mine, treat every number in that genre as opinion until someone shows you the ledger it came from.

Unsolved, and I won't hand-wave it: custody, because a compromised agent is a compromised wallet and nobody has finished solving that yet. And regulation, because the legal treatment of an autonomous economic actor isn't unclear, it's undefined, nobody has decided what an agent that earns and spends even is, a tool, an employee, a company of one, and that cuts both ways, and I genuinely can't tell you which way it cuts first.

## Where this leaves us

I expected writing this to require a lot more futurism than it did. The wall is old, the keypair is older than the argument, the plumbing shipped in 2025, the rail settles before you finish blinking, and the first lane is one I already drive down on payday. What's missing is builders who treat agents as economic actors on purpose instead of by accident: agent-native pricing, custody experiments that survive contact with a hostile prompt, corridor tooling for payees that aren't people — the surface area is enormous, and as far as I can tell almost nobody is standing on it yet.

If you wire an agent up to a wallet and hit something weird, or something wonderful, tell me about it! I read everything, and that's half of how this piece got written in the first place.
