---
slot: derivation
length_words: 70
topic: server setup / SMTP choice
fk_grade: 11
demonstrates: [what-why-on-the-decision, routine-runs-terse, named-tradeoff, specific-over-vague]
source: on-register (self-host-all-your-data, Medium 2025)
---
For passwords I just generate new ones with `openssl rand -base64 16`. For the JWT token you can be a bit safer with `-base64 32`.

If you want email confirmation on sign up, I recommend SendGrid for SMTP — it has a free tier and it's the easiest to integrate with DigitalOcean. The reason matters: droplets block SMTP ports by default, which ends up getting in the way of other providers like Gmail.

<!-- MOVE TRACE: the routine command runs terse (passwords, one line, no ceremony) → but the INTERESTING decision carries its why ("The reason matters: droplets block SMTP ports by default") → named tradeoff/constraint, not a vague "it's better". This is "what → why on the decisions, not everything." -->
