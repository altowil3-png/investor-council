#!/usr/bin/env python3
"""
Generated-summary sync & drift check (v4)
=========================================
Single source of truth = `inputs/TICKER.json` -> `os-modules/valuation_engine.py`.
This tool writes the engine's numbers into marked blocks in the markdown files and,
in `--check` mode, fails (exit 1) when any markdown has drifted from the engine.

Blocks:
  analysis file (from JSON `analysis_path`):  <!-- AUTO-SUMMARY:<TICKER>:START --> ... <!-- AUTO-SUMMARY:<TICKER>:END -->
  README.md:                                  <!-- AUTO-SUMMARY:README:START --> ... <!-- AUTO-SUMMARY:README:END -->
  analyses/INDEX.md:                          <!-- AUTO-SUMMARY:INDEX:START -->  ... <!-- AUTO-SUMMARY:INDEX:END -->

Extra rules enforced by --check:
  * every inputs/*.json passes the engine's provenance validator;
  * a v4 analysis file may only be referenced from README/INDEX inside the generated blocks
    (no hand-written verdicts that can go stale);
  * every analysis without an inputs/*.json is a legacy file: its own header and every README/INDEX
    line that links to it must carry the LEGACY tag below.

Usage:
  python3 tools/sync_summaries.py --write       # regenerate blocks
  python3 tools/sync_summaries.py --check       # CI: fail on drift / rule violations
  python3 tools/sync_summaries.py --self-test   # unit tests for this tool
"""

from __future__ import annotations

import glob
import importlib.util
import json
import os
import re
import sys
import tempfile
from typing import Dict, List, Tuple

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGACY_TAG = "[LEGACY v1 — Pending v4 Re-audit]"
README = os.path.join(REPO, "README.md")
INDEX = os.path.join(REPO, "analyses", "INDEX.md")


def load_engine():
    path = os.path.join(REPO, "os-modules", "valuation_engine.py")
    spec = importlib.util.spec_from_file_location("valuation_engine", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["valuation_engine"] = mod
    spec.loader.exec_module(mod)
    return mod


def markers(name: str) -> Tuple[str, str]:
    return f"<!-- AUTO-SUMMARY:{name}:START -->", f"<!-- AUTO-SUMMARY:{name}:END -->"


def extract_block(text: str, name: str) -> str | None:
    start, end = markers(name)
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0 or j < i:
        return None
    return text[i + len(start):j].strip("\n")


def replace_block(text: str, name: str, body: str) -> str:
    start, end = markers(name)
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0 or j < i:
        raise ValueError(f"markers for {name} not found")
    return text[:i + len(start)] + "\n" + body + "\n" + text[j:]


def strip_blocks(text: str) -> str:
    return re.sub(r"<!-- AUTO-SUMMARY:([A-Z0-9_.-]+):START -->.*?<!-- AUTO-SUMMARY:\1:END -->", "", text, flags=re.S)


def collect(engine) -> Tuple[List[Dict[str, object]], List[str]]:
    summaries, errors = [], []
    for path in sorted(glob.glob(os.path.join(REPO, "inputs", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
        errs = engine.validate_company_json(raw)
        if errs:
            errors += [f"{os.path.relpath(path, REPO)}: {e}" for e in errs]
            continue
        d = engine.company_dict_from_json(raw, source_path=path)
        if not d.get("analysis_path"):
            errors.append(f"{os.path.relpath(path, REPO)}: analysis_path is required")
            continue
        summaries.append(engine.build_summary(d))
    return summaries, errors


def expected_blocks(engine, summaries) -> Dict[str, Tuple[str, str]]:
    """file path -> list of (block name, body)"""
    out: Dict[str, List[Tuple[str, str]]] = {}
    for s in summaries:
        out.setdefault(os.path.join(REPO, str(s["analysis_path"])), []).append((str(s["ticker"]), engine.render_summary_block(s)))
    out.setdefault(README, []).append(("README", engine.render_readme_items(summaries)))
    out.setdefault(INDEX, []).append(("INDEX", engine.render_index_rows(summaries)))
    return out


def legacy_files(summaries) -> List[str]:
    v4 = {os.path.normpath(os.path.join(REPO, str(s["analysis_path"]))) for s in summaries}
    files = []
    for p in sorted(glob.glob(os.path.join(REPO, "analyses", "**", "*.md"), recursive=True)):
        if os.path.basename(p) == "INDEX.md" or os.path.normpath(p) in v4:
            continue
        files.append(p)
    return files


def check_rules(summaries) -> List[str]:
    errors: List[str] = []
    readme, index = open(README, encoding="utf-8").read(), open(INDEX, encoding="utf-8").read()
    for s in summaries:
        fname = os.path.basename(str(s["analysis_path"]))
        for label, text in (("README.md", readme), ("analyses/INDEX.md", index)):
            if fname in strip_blocks(text):
                errors.append(f"{label}: links to v4 analysis {fname} outside the generated block (hand-written verdicts go stale)")
    for p in legacy_files(summaries):
        fname = os.path.basename(p)
        head = "".join(open(p, encoding="utf-8").readlines()[:15])
        if LEGACY_TAG not in head:
            errors.append(f"{os.path.relpath(p, REPO)}: legacy analysis must carry {LEGACY_TAG} in its first 15 lines")
        for label, text in (("README.md", readme), ("analyses/INDEX.md", index)):
            lines = [ln for ln in text.splitlines() if fname in ln]
            if not lines:
                errors.append(f"{label}: legacy analysis {fname} is not listed")
            for ln in lines:
                if LEGACY_TAG not in ln:
                    errors.append(f"{label}: line linking {fname} must carry {LEGACY_TAG}")
    return errors


def run(write: bool) -> int:
    engine = load_engine()
    summaries, errors = collect(engine)
    drift: List[str] = []
    if not errors:
        for path, blocks in expected_blocks(engine, summaries).items():
            rel = os.path.relpath(path, REPO)
            if not os.path.exists(path):
                errors.append(f"{rel}: file not found")
                continue
            text = open(path, encoding="utf-8").read()
            new_text = text
            for name, body in blocks:
                current = extract_block(new_text, name)
                if current is None:
                    errors.append(f"{rel}: missing markers {markers(name)[0]} / END")
                    continue
                if current != body.strip("\n"):
                    drift.append(f"{rel}: block {name} differs from engine output")
                    new_text = replace_block(new_text, name, body)
            if write and new_text != text:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
        errors += check_rules(summaries)

    for s in summaries:
        unv = s["facts_unverified"]
        if unv:
            print(f"[WARN] {s['ticker']}: {len(unv)} unverified facts: {', '.join(unv)}")
    if write:
        for d in drift:
            print(f"[WROTE] {d}")
        drift = []
    for e in errors:
        print(f"[ERROR] {e}")
    for d in drift:
        print(f"[DRIFT] {d} — run: python3 tools/sync_summaries.py --write")
    if errors or drift:
        return 1
    print(f"OK: {len(summaries)} v4 input file(s) in sync; {len(legacy_files(summaries))} legacy analyses correctly tagged.")
    return 0


def self_test() -> int:
    body = "| a | b |\n| 1 | 2 |"
    doc = "x\n<!-- AUTO-SUMMARY:T:START -->\nold\n<!-- AUTO-SUMMARY:T:END -->\ny\n"
    assert extract_block(doc, "T") == "old"
    new = replace_block(doc, "T", body)
    assert extract_block(new, "T") == body and new.startswith("x\n") and new.endswith("y\n")
    assert extract_block(new, "MISSING") is None
    assert "old" not in strip_blocks(doc) and "x" in strip_blocks(doc)
    # Drift detection on a real file round-trip
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "a.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(new)
        txt = open(p, encoding="utf-8").read()
        assert extract_block(txt, "T") == body                     # in sync
        assert extract_block(txt.replace("| 1 |", "| 9 |"), "T") != body  # hand edit = drift
    print("sync_summaries self-test passed.")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    if "--write" in sys.argv:
        sys.exit(run(write=True))
    sys.exit(run(write=False))
