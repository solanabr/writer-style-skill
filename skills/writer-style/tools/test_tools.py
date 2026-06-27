#!/usr/bin/env python3
"""
test_tools.py — run every writer-style tool's selftest in one shot.

    python test_tools.py

Exits non-zero if any tool's selftest fails. Pure-Python, no network, no deps.
"""
from __future__ import annotations
import sys

import profile_corpus
import validate_voice
import style_lexicons


def main() -> int:
    rc = 0
    print("== profile_corpus ==")
    rc |= profile_corpus.selftest()
    print("\n== validate_voice ==")
    rc |= validate_voice.selftest()

    # cross-module sanity: lexicon helpers behave
    print("\n== style_lexicons ==")
    ok = True
    def check(c, m):
        nonlocal ok; print(("PASS" if c else "FAIL") + " - " + m); ok = ok and c
    check(style_lexicons.syllables("table") == 2, "syllables('table') == 2")
    check(style_lexicons.syllables("a") == 1, "syllables('a') == 1")
    fk = style_lexicons.flesch_kincaid_grade(["the", "cat", "sat"], 1)
    check(isinstance(fk, float), "flesch_kincaid_grade returns a float")
    check(style_lexicons.count_markers("for example, suppose you stake", style_lexicons.EXAMPLE_MARKERS) >= 2,
          "count_markers finds example markers")
    print("\n" + ("STYLE_LEXICONS SELFTESTS PASSED" if ok else "FAILURES ABOVE"))
    rc |= (0 if ok else 1)

    print("\n" + ("ALL TOOL SELFTESTS PASSED" if rc == 0 else "SOME TOOL SELFTESTS FAILED"))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
