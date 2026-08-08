"""
Entry point for the Customer Support Intent Labeling & Chatbot Evaluation project.

Running this sets up the dataset and runs the automated PII first-pass.
The actual annotation work (the real point of this project) happens in
notebooks/01_label_conversations.ipynb -- see README.md for the full workflow.
"""

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def run(script: str) -> None:
    print(f"\n--- Running {script} ---")
    subprocess.run([sys.executable, str(BASE / "scripts" / script)], check=True)


def main():
    run("generate_conversations.py")
    run("pii_check.py")
    print(
        "\nSetup complete.\n"
        "Next steps:\n"
        "  1. Open notebooks/01_label_conversations.ipynb and label each conversation.\n"
        "  2. Label a 20% sample a second time, save as data/labels_pass1.csv and "
        "data/labels_pass2.csv, and run scripts/compute_agreement.py (or notebook 02).\n"
        "  3. Once data/my_labels.csv has real labels, open notebook 03 to test a "
        "baseline classifier against them and write up the error analysis.\n"
        "See README.md for full details."
    )


if __name__ == "__main__":
    main()
