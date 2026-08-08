# Customer Support Intent Labeling & Chatbot Evaluation

A small annotation + evaluation project built to practice the core tasks in a
Machine Learning Data Associate role: intent/dialogue labeling, guideline-driven
annotation, inter-annotator agreement, model output testing, and PII/compliance
flagging.

## Status
Data and tooling are complete. Manual labeling (the actual annotation work)
is not done yet -- that's the part that has to be done by hand, on purpose,
since it's the skill this project exists to build and demonstrate. See
"Your Next Steps" below.

## Stack
- Python 3.11, managed with uv (https://docs.astral.sh/uv/)
- pandas, scikit-learn (Cohen's kappa), Jupyter notebooks

## Project Structure
```
.
├── main.py                          # pipeline entry point (data setup + PII first-pass)
├── guidelines/
│   └── labeling_guideline.md        # the annotation rubric -- read this first
├── data/
│   ├── conversations.json           # 20 hand-authored simulated support conversations
│   ├── pii_flags.json               # automated PII first-pass (needs manual confirmation)
│   ├── my_labels.csv                # <- your labels go here (notebook 1)
│   ├── labels_pass1.csv             # <- first agreement-check pass (notebook 2)
│   └── labels_pass2.csv             # <- second agreement-check pass (notebook 2)
├── notebooks/
│   ├── 01_label_conversations.ipynb # read conversations, enter labels
│   ├── 02_agreement_analysis.ipynb  # Cohen's kappa between two labeling passes
│   └── 03_model_testing.ipynb       # test a baseline classifier against your labels
├── scripts/
│   ├── generate_conversations.py    # authors the simulated conversation set
│   ├── pii_check.py                 # regex-based PII first-pass
│   ├── compute_agreement.py         # CLI version of the kappa calculation
│   └── make_notebooks.py            # regenerates the notebooks above
└── tests/
    └── test_fixture_*.csv           # dummy data used only to verify compute_agreement.py works
```

## Setup
```bash
uv sync
uv run python main.py        # generates data/conversations.json and data/pii_flags.json
uv run jupyter lab            # open notebooks/01_label_conversations.ipynb
```

## Your Next Steps (the real work)
1. Read `guidelines/labeling_guideline.md`.
2. Label all 20 conversations in `notebooks/01_label_conversations.ipynb` -> saves to `data/my_labels.csv`.
3. Re-label a ~4-conversation sample (20%) a second time, on a different day, without looking at your first-pass labels. Save the two passes as `data/labels_pass1.csv` and `data/labels_pass2.csv`, then run:
   ```bash
   uv run python scripts/compute_agreement.py data/labels_pass1.csv data/labels_pass2.csv
   ```
   This gives you a real Cohen's kappa score you can put on your resume.
4. Run the baseline classifier test in `notebooks/03_model_testing.ipynb` against your real labels, and write 2-3 sentences on the error patterns you find -- this is your "defect identification" writeup.
5. Update your resume with the real numbers this produces (annotated count, kappa score, baseline accuracy, PII flags confirmed) -- I'll write the bullets from your actual results once you have them.

## Notes on the dataset
The 20 conversations in `data/conversations.json` are simulated/hand-authored for this exercise (not scraped or sourced from a real company's data), which also mirrors the JD's "author simulated conversations" responsibility. The `tests/test_fixture_*.csv` files are dummy data used only to confirm `compute_agreement.py` computes kappa correctly -- they are not real annotation results and shouldn't be cited anywhere as such.
