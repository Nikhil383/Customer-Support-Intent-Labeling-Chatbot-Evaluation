"""
Lightweight rule-based PII scanner for the conversation dataset.

This is a *first-pass* automated flag, not a replacement for manual review —
the labeling guideline requires a human to confirm PII presence and type.
This script exists to speed up that manual pass, matching the JD's
"flag exposure of personally identifiable information" responsibility.

Run: uv run python scripts/pii_check.py
Writes: data/pii_flags.json
"""

import json
import re
from pathlib import Path

PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    "phone": re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "card_partial": re.compile(r"\b(?:card|ending in)\s*(?:number\s*)?\d{4}\b", re.IGNORECASE),
    "address": re.compile(r"\b\d{1,5}\s+\w+(\s\w+)*\s(Street|St|Avenue|Ave|Terrace|Road|Rd|Lane|Ln)\b", re.IGNORECASE),
}

NAME_HINT_PATTERN = re.compile(r"\bmy name is ([A-Z][a-z]+ [A-Z][a-z]+)\b")


def scan_conversation(conv: dict) -> dict:
    full_text = " ".join(turn["text"] for turn in conv["turns"])
    found = {}
    for label, pattern in PATTERNS.items():
        matches = pattern.findall(full_text)
        if matches:
            found[label] = len(matches) if isinstance(matches[0], str) else len(matches)

    name_matches = NAME_HINT_PATTERN.findall(full_text)
    if name_matches:
        found["name_self_declared"] = len(name_matches)

    return {
        "conversation_id": conv["conversation_id"],
        "pii_flag": bool(found),
        "pii_types_detected": sorted(found.keys()),
        "match_counts": found,
    }


def main():
    base = Path(__file__).resolve().parent.parent
    conversations = json.loads((base / "data" / "conversations.json").read_text())

    results = [scan_conversation(c) for c in conversations]

    out_path = base / "data" / "pii_flags.json"
    out_path.write_text(json.dumps(results, indent=2))

    flagged = sum(r["pii_flag"] for r in results)
    print(f"Scanned {len(results)} conversations, {flagged} flagged for potential PII.")
    print(f"Results written to {out_path}")
    print("\nReminder: this is an automated first pass. Confirm each flag manually")
    print("against the labeling guideline before recording it as a final label.")


if __name__ == "__main__":
    main()
