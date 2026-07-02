---
slot: derivation
register: written-longform
length_words: 131
topic: bridge security / challenge-response design
fk_grade: 11
demonstrates: [plain-competent-body, mechanism-carries-the-weight, zero-markers, serious-register]
source: on-register (2025-03-bitvmy-bridge, technical explainer)
---
The most significant innovation in BitVMY is a fundamental change to the challenge-response mechanism. In BitVM2, if a withdrawal is challenged but the challenge fails, the operator can proceed with the withdrawal and take funds from the vault. In BitVMY, a successful challenge permanently cancels the withdrawal attempt. The challenge game only determines who receives the bond amounts, not whether the vault can be accessed.

This seemingly small change has profound security implications. Even if an attacker successfully executes a 51% attack on Syscoin, they cannot extract the Bitcoin in the vault. The worst they can do is win bond amounts from challengers. Since the cost of executing a 51% attack on a merge-mined chain like Syscoin would significantly exceed potential bond gains, this removes the economic incentive for such attacks.

<!-- MOVE TRACE: the RESTRAINT exemplar — note what is NOT here. No catchphrase, no identity beat, no analogy, no joke: a serious security topic carried entirely by the mechanism ("the challenge game only determines who receives the bond amounts") and a cost-vs-reward argument. The verdict is implicit in the economics, not a token ("a godsend" would be tone-deaf here). This is the voice AT REST — the plainness-quota sections of a long piece read like this, and on security topics the whole body does. Kaue when the topic is serious IS this register. -->
