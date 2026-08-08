"""
Computes Cohen's kappa inter-annotator agreement on the `primary_intent` field
between two label sets, per the labeling guideline's agreement process.

Expects two CSV files with columns: conversation_id, primary_intent
(one row per conversation, produced by labeling the same 20% sample twice —
see notebooks/02_agreement_analysis.ipynb for the labeling workflow).

Run: uv run python scripts/compute_agreement.py labels_pass1.csv labels_pass2.csv
"""

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score


def compute_agreement(path_a: str, path_b: str) -> None:
    df_a = pd.read_csv(path_a).sort_values("conversation_id").reset_index(drop=True)
    df_b = pd.read_csv(path_b).sort_values("conversation_id").reset_index(drop=True)

    if not df_a["conversation_id"].equals(df_b["conversation_id"]):
        raise ValueError(
            "Label files cover different conversation_id sets — "
            "both passes must label the exact same sample to compute agreement."
        )

    kappa = cohen_kappa_score(df_a["primary_intent"], df_b["primary_intent"])
    agreement_rate = (df_a["primary_intent"] == df_b["primary_intent"]).mean()

    print(f"Conversations compared: {len(df_a)}")
    print(f"Raw agreement rate:     {agreement_rate:.2%}")
    print(f"Cohen's kappa:          {kappa:.3f}")

    if kappa < 0.6:
        print("\n⚠ Kappa below 0.6 — guideline likely needs revision before scaling up labeling.")
    else:
        print("\n✓ Kappa at or above 0.6 — guideline is holding up reasonably well.")

    mismatches = df_a[df_a["primary_intent"] != df_b["primary_intent"]]["conversation_id"].tolist()
    if mismatches:
        print(f"\nMismatched conversation_ids to review: {mismatches}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: uv run python scripts/compute_agreement.py <labels_pass1.csv> <labels_pass2.csv>")
        sys.exit(1)
    compute_agreement(sys.argv[1], sys.argv[2])
