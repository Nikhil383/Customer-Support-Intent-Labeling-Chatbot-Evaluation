"""Generates the starter Jupyter notebooks for this project using nbformat."""

import nbformat as nbf
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
NB_DIR = BASE / "notebooks"
NB_DIR.mkdir(exist_ok=True)


def md(text):
    return nbf.v4.new_markdown_cell(text)


def code(text):
    return nbf.v4.new_code_cell(text)


# ---------------------------------------------------------------------------
# Notebook 1: Manual labeling workbook
# ---------------------------------------------------------------------------
nb1 = nbf.v4.new_notebook()
nb1.cells = [
    md("# 01 — Label Conversations\n\n"
       "Read each conversation and fill in your labels below, following "
       "`guidelines/labeling_guideline.md`. This notebook is intentionally "
       "manual — the point of the exercise is doing the labeling yourself, "
       "not automating it away."),
    code(
        "import json\n"
        "import pandas as pd\n"
        "from pathlib import Path\n\n"
        "conversations = json.loads(Path('../data/conversations.json').read_text())\n"
        "print(f'{len(conversations)} conversations loaded')"
    ),
    md("## Read a conversation\n\nRe-run this cell with a different index to read the next one."),
    code(
        "idx = 0\n"
        "conv = conversations[idx]\n"
        "print(conv['conversation_id'])\n"
        "for turn in conv['turns']:\n"
        "    print(f\"{turn['speaker']:>9}: {turn['text']}\")"
    ),
    md("## Record your label for this conversation\n\n"
       "Fill in the dict below for the conversation you just read, then run "
       "the cell to append it to `labels`. Repeat for every conversation."),
    code(
        "labels = []  # run this cell once at the start of a labeling session\n"
        "# labels = pd.read_csv('../data/my_labels.csv').to_dict('records')  # or resume a saved session"
    ),
    code(
        "labels.append({\n"
        "    'conversation_id': conv['conversation_id'],\n"
        "    'primary_intent': 'REPLACE_ME',       # billing_issue / delivery_delay / refund_request /\n"
        "                                            # account_access / product_complaint / general_inquiry\n"
        "    'sentiment': 'REPLACE_ME',             # negative / neutral / positive\n"
        "    'pii_present': False,                  # True/False — confirm against pii_flags.json\n"
        "    'pii_types': [],                       # e.g. ['email', 'phone']\n"
        "    'resolution_status': 'REPLACE_ME',     # resolved / unresolved / unclear\n"
        "    'low_confidence': False,\n"
        "})\n"
        "print(f'{len(labels)} conversations labeled so far')"
    ),
    md("## Save your labels"),
    code(
        "pd.DataFrame(labels).to_csv('../data/my_labels.csv', index=False)\n"
        "print('Saved to data/my_labels.csv')"
    ),
]

# ---------------------------------------------------------------------------
# Notebook 2: Agreement analysis
# ---------------------------------------------------------------------------
nb2 = nbf.v4.new_notebook()
nb2.cells = [
    md("# 02 — Inter-Annotator Agreement\n\n"
       "Label a ~20% sample twice (e.g. on two different days, without looking "
       "at your first pass) and compare here. This mirrors the guideline's "
       "agreement-checking process and the JD's quality-consistency requirement."),
    code(
        "import pandas as pd\n"
        "from sklearn.metrics import cohen_kappa_score\n\n"
        "pass1 = pd.read_csv('../data/labels_pass1.csv').sort_values('conversation_id').reset_index(drop=True)\n"
        "pass2 = pd.read_csv('../data/labels_pass2.csv').sort_values('conversation_id').reset_index(drop=True)\n\n"
        "assert pass1['conversation_id'].equals(pass2['conversation_id']), \\\n"
        "    'Both passes must cover the exact same conversation_id sample'"
    ),
    code(
        "kappa = cohen_kappa_score(pass1['primary_intent'], pass2['primary_intent'])\n"
        "agreement_rate = (pass1['primary_intent'] == pass2['primary_intent']).mean()\n\n"
        "print(f'Conversations compared: {len(pass1)}')\n"
        "print(f'Raw agreement rate:     {agreement_rate:.2%}')\n"
        "print(f\"Cohen's kappa:          {kappa:.3f}\")"
    ),
    md("## Review mismatches\n\nLook at cases where the two passes disagreed — these often reveal ambiguity in the guideline itself."),
    code(
        "mismatches = pass1[pass1['primary_intent'] != pass2['primary_intent']]['conversation_id']\n"
        "mismatches"
    ),
]

# ---------------------------------------------------------------------------
# Notebook 3: Model testing against labels
# ---------------------------------------------------------------------------
nb3 = nbf.v4.new_notebook()
nb3.cells = [
    md("# 03 — Test a Model's Intent Detection Against Your Labels\n\n"
       "Once `data/my_labels.csv` has real labels, use this notebook to test "
       "how well a simple classifier (or an LLM prompt, if you have API access) "
       "predicts intent — then audit and categorize the errors, mirroring the "
       "JD's 'test customer service models... to confirm intent detection works "
       "as intended' responsibility."),
    code(
        "import json\n"
        "import pandas as pd\n"
        "from pathlib import Path\n\n"
        "conversations = {c['conversation_id']: c for c in json.loads(Path('../data/conversations.json').read_text())}\n"
        "labels = pd.read_csv('../data/my_labels.csv')\n"
        "labels.head()"
    ),
    md("## Option A — Rule-based baseline (no API needed)\n\n"
       "A simple keyword baseline to compare your labels against, useful as a sanity check "
       "even without model/API access."),
    code(
        "KEYWORD_RULES = {\n"
        "    'billing_issue': ['charged', 'bill', 'billing'],\n"
        "    'delivery_delay': ['where is my', 'delivery', 'shipped', 'shipment', 'delayed'],\n"
        "    'refund_request': ['refund', 'money back'],\n"
        "    'account_access': ['log in', 'login', 'password', 'locked out'],\n"
        "    'product_complaint': ['broken', 'defective', 'damaged', 'cracked', 'wrong size', 'wrong item'],\n"
        "}\n\n"
        "def predict_intent(conv_id):\n"
        "    text = ' '.join(t['text'] for t in conversations[conv_id]['turns'] if t['speaker'] == 'customer').lower()\n"
        "    for intent, keywords in KEYWORD_RULES.items():\n"
        "        if any(kw in text for kw in keywords):\n"
        "            return intent\n"
        "    return 'general_inquiry'\n\n"
        "labels['predicted_intent'] = labels['conversation_id'].apply(predict_intent)\n"
        "labels[['conversation_id', 'primary_intent', 'predicted_intent']]"
    ),
    code(
        "accuracy = (labels['primary_intent'] == labels['predicted_intent']).mean()\n"
        "print(f'Baseline keyword-rule accuracy vs your labels: {accuracy:.2%}')\n\n"
        "errors = labels[labels['primary_intent'] != labels['predicted_intent']]\n"
        "errors[['conversation_id', 'primary_intent', 'predicted_intent']]"
    ),
    md("## Error analysis\n\n"
       "For each mismatch above, note *why* the baseline got it wrong — e.g. ambiguous "
       "phrasing, missing keyword, intent stated indirectly. This write-up is the "
       "'defect identification' deliverable — summarize the patterns you find."),
]

nbf.write(nb1, str(NB_DIR / "01_label_conversations.ipynb"))
nbf.write(nb2, str(NB_DIR / "02_agreement_analysis.ipynb"))
nbf.write(nb3, str(NB_DIR / "03_model_testing.ipynb"))
print("Notebooks written to notebooks/")
