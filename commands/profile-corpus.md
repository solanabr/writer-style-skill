---
description: "Regenerate builder-internal evidence + card dials from a corpus"
---

Run the stylometric profiler to (re)generate the builder-internal evidence for one or more voices. This is
**build-time** tooling — its output feeds the persona-builder and the validator, never the writer directly.
Run it from a **clone**: the source corpus in `tone-lora/` is not shipped with the installed skill.

```bash
SKILL="skills/writer-style"   # in a clone, from the repo root

# all five secondaries from the standard <corpus>/<author>/raw layout:
python3 "$SKILL/tools/profile_corpus.py" --corpus tone-lora/corpus \
    --authors helius,vitalik,balaji,hayes,hotz --out "$SKILL/profiles/kaue/evidence"
# the primary, filtered to on-register files only:
python3 "$SKILL/tools/profile_corpus.py" --paths kaue=tone-lora/corpus/you/raw \
    --include 'defis-core|hackathon-zero|mcp-services|self-host' --out "$SKILL/profiles/kaue/evidence"
```

The profiler **cleans** the corpus first (strips HTML/`<center>`/`<br>` artifacts, newsletter/footer chrome,
and skips guest-reposts by other authors), then writes `<name>.profile.json` with:
- `meta` (counts, `paragraph_metric_valid`, warnings),
- `raw` (full forensic stylometry — builder-internal),
- `card_suggestions` (the writer-actionable dials, ready to curate into `<name>.card.yaml`).

After regenerating, **re-derive** any affected `*.card.yaml` from the new `card_suggestions` (hand-curating the
favor/avoid/move lists against the persona). Run `python3 "$SKILL/tools/test_tools.py"` to confirm the tools still pass.
