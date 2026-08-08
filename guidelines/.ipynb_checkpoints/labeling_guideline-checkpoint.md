# Customer Support Intent Labeling Guideline v1.0

## Purpose
This guideline defines how to label customer support conversations for:
1. **Primary intent** — the main reason the customer contacted support
2. **Sentiment** — the customer's emotional tone
3. **PII presence** — whether personally identifiable information appears in the conversation
4. **Resolution status** — whether the conversation ends with the issue resolved

Consistent labeling matters more than "correct" labeling — when in doubt, follow the
decision rules below rather than intuition, so two annotators reach the same label
independently.

---

## 1. Primary Intent (choose exactly one)

| Label | Definition | Example trigger phrases |
|---|---|---|
| `billing_issue` | Customer disputes a charge, asks about a bill, or reports incorrect billing | "I was charged twice", "why is my bill higher" |
| `delivery_delay` | Customer asks about a late, missing, or delayed order/shipment | "where is my order", "it's been 2 weeks" |
| `refund_request` | Customer explicitly asks for money back | "I want a refund", "can I get my money back" |
| `account_access` | Customer cannot log in, reset password, or access their account | "I'm locked out", "forgot my password" |
| `product_complaint` | Customer reports a defective, wrong, or unsatisfactory product | "this arrived broken", "not what I ordered" |
| `general_inquiry` | Customer asks a question with no complaint or request for action | "do you ship to Canada" |

**Decision rule:** if a conversation could fit two labels, choose the intent tied to the
customer's **first explicit ask**, not background complaints mentioned in passing.

## 2. Sentiment (choose exactly one)

- `negative` — frustration, anger, or explicit dissatisfaction is present
- `neutral` — factual, no strong emotion either way
- `positive` — customer expresses satisfaction, gratitude, or relief

**Decision rule:** sentiment is judged on the customer's final message, not their first —
tone often shifts across a conversation.

## 3. PII Presence (yes/no + type)

Flag `pii_present: true` if the conversation contains any of:
- Full name paired with another identifier (email, phone, address, order ID)
- Payment card numbers or partial card numbers
- Home address
- Phone number
- Email address

Record the type(s) found in `pii_types`, e.g. `["email", "phone"]`.

**Decision rule:** a first name alone is NOT PII for this exercise. It must be paired with
at least one other identifying detail to count.

## 4. Resolution Status

- `resolved` — the agent's final message indicates the issue was fixed or answered
- `unresolved` — conversation ends without resolution (escalation, no reply, customer still waiting)
- `unclear` — cannot tell from the transcript alone

---

## Annotation Process
1. Read the full conversation once before labeling anything.
2. Apply labels in the order above (intent → sentiment → PII → resolution).
3. If uncertain between two intent labels after applying the decision rule, mark
   `low_confidence: true` so it can be reviewed separately — do not guess silently.
4. Do not use outside context; label only what is present in the transcript.

## Inter-Annotator Agreement
A random 20% sample of the dataset should be labeled independently by a second annotator
(or by the same annotator on a different day, blind to prior labels) to measure consistency
via Cohen's kappa on the `primary_intent` field. Kappa below 0.6 signals the guideline
needs revision before scaling up labeling.
