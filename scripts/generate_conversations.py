"""
Authors a set of simulated multi-turn customer support conversations.

This mirrors the JD task "Author simulated conversations used for testing and
training." Conversations are hand-authored (not pulled from a real dataset) so
there are no licensing/privacy concerns, and cover a spread of intents,
sentiment, PII presence, and resolution outcomes for labeling practice.

Run: uv run python scripts/generate_conversations.py
Writes: data/conversations.json
"""

import json
from pathlib import Path

CONVERSATIONS = [
    {
        "conversation_id": "conv_001",
        "turns": [
            {"speaker": "customer", "text": "Hi, I was charged twice for my order #4471 this month."},
            {"speaker": "agent", "text": "I'm sorry about that! Let me check your billing history."},
            {"speaker": "customer", "text": "Thanks, it's really frustrating, I need that money back."},
            {"speaker": "agent", "text": "I can see the duplicate charge. I've issued a refund, it'll post in 3-5 business days."},
            {"speaker": "customer", "text": "Okay, appreciate you sorting it quickly."},
        ],
    },
    {
        "conversation_id": "conv_002",
        "turns": [
            {"speaker": "customer", "text": "Where is my package? It's been two weeks since I ordered."},
            {"speaker": "agent", "text": "Let me pull up your tracking info. Can you confirm your order number?"},
            {"speaker": "customer", "text": "It's 88213-A."},
            {"speaker": "agent", "text": "I see it's still in transit, stuck at a regional facility. I'll escalate this with the carrier."},
            {"speaker": "customer", "text": "This is unacceptable, I needed it last week."},
        ],
    },
    {
        "conversation_id": "conv_003",
        "turns": [
            {"speaker": "customer", "text": "I can't log into my account, it keeps saying invalid password."},
            {"speaker": "agent", "text": "No problem, I can send a password reset link. Is your email still john.doe@example.com?"},
            {"speaker": "customer", "text": "Yes that's right."},
            {"speaker": "agent", "text": "Sent! Let me know once you're back in."},
            {"speaker": "customer", "text": "Got it, I'm in now, thank you!"},
        ],
    },
    {
        "conversation_id": "conv_004",
        "turns": [
            {"speaker": "customer", "text": "The blender I ordered arrived cracked."},
            {"speaker": "agent", "text": "I'm really sorry to hear that. Can you send a photo of the damage?"},
            {"speaker": "customer", "text": "Attached."},
            {"speaker": "agent", "text": "Thanks, I've started a replacement order, no charge, arriving in 4-6 days."},
            {"speaker": "customer", "text": "Great, thank you for the quick help."},
        ],
    },
    {
        "conversation_id": "conv_005",
        "turns": [
            {"speaker": "customer", "text": "Do you ship to Canada?"},
            {"speaker": "agent", "text": "Yes, we ship to Canada with standard delivery of 7-10 business days."},
            {"speaker": "customer", "text": "Perfect, thanks."},
        ],
    },
    {
        "conversation_id": "conv_006",
        "turns": [
            {"speaker": "customer", "text": "I want a refund for order 55210, it's not what I expected."},
            {"speaker": "agent", "text": "Understood. Can you tell me more about what was wrong with it?"},
            {"speaker": "customer", "text": "The color is completely different from the pictures."},
            {"speaker": "agent", "text": "I'll process a full refund to your original payment method."},
            {"speaker": "customer", "text": "Thank you."},
        ],
    },
    {
        "conversation_id": "conv_007",
        "turns": [
            {"speaker": "customer", "text": "My card ending in 4432 was billed for something I didn't buy."},
            {"speaker": "agent", "text": "That's concerning, let's look into it. Can I confirm your name and phone number for verification?"},
            {"speaker": "customer", "text": "Sarah Kim, 555-201-8890."},
            {"speaker": "agent", "text": "Thanks Sarah, I've flagged this as potential fraud and reversed the charge."},
            {"speaker": "customer", "text": "Okay, please make sure this doesn't happen again."},
        ],
    },
    {
        "conversation_id": "conv_008",
        "turns": [
            {"speaker": "customer", "text": "My order still hasn't shipped after 5 days."},
            {"speaker": "agent", "text": "Let me check the status for you."},
            {"speaker": "customer", "text": "I've been waiting on hold for 20 minutes already, this is ridiculous."},
            {"speaker": "agent", "text": "I apologize for the wait. I don't see an update yet, I'll follow up over email within 24 hours."},
            {"speaker": "customer", "text": "Fine, I guess I'll wait."},
        ],
    },
    {
        "conversation_id": "conv_009",
        "turns": [
            {"speaker": "customer", "text": "I forgot my password and the reset email isn't coming through."},
            {"speaker": "agent", "text": "Let's try resending it. What's the email on file?"},
            {"speaker": "customer", "text": "mike.chen88@mailhost.com"},
            {"speaker": "agent", "text": "Resent — please check spam folder as well."},
            {"speaker": "customer", "text": "Found it, thanks!"},
        ],
    },
    {
        "conversation_id": "conv_010",
        "turns": [
            {"speaker": "customer", "text": "The jacket I received is the wrong size even though I ordered a medium."},
            {"speaker": "agent", "text": "Sorry about that mix-up. Would you like an exchange or a refund?"},
            {"speaker": "customer", "text": "An exchange for the correct size please."},
            {"speaker": "agent", "text": "Done, the correct size ships out today at no extra cost."},
            {"speaker": "customer", "text": "Appreciate it."},
        ],
    },
    {
        "conversation_id": "conv_011",
        "turns": [
            {"speaker": "customer", "text": "I was charged a subscription fee I didn't sign up for."},
            {"speaker": "agent", "text": "Let me look into your account for any active subscriptions."},
            {"speaker": "customer", "text": "This is the second time this has happened, I'm getting really annoyed."},
            {"speaker": "agent", "text": "I understand the frustration. I've cancelled the subscription and refunded the charge."},
            {"speaker": "customer", "text": "Thank you, please make sure it doesn't auto-renew again."},
        ],
    },
    {
        "conversation_id": "conv_012",
        "turns": [
            {"speaker": "customer", "text": "My delivery says delivered but I never got it."},
            {"speaker": "agent", "text": "I'm sorry to hear that. Can you confirm your delivery address?"},
            {"speaker": "customer", "text": "742 Evergreen Terrace, apartment 3B."},
            {"speaker": "agent", "text": "Thanks, I've opened a missing package investigation with the carrier."},
            {"speaker": "customer", "text": "How long will that take?"},
        ],
    },
    {
        "conversation_id": "conv_013",
        "turns": [
            {"speaker": "customer", "text": "Can I change the email on my account?"},
            {"speaker": "agent", "text": "Sure, what would you like it updated to?"},
            {"speaker": "customer", "text": "newemail@example.com"},
            {"speaker": "agent", "text": "Updated! You'll get a confirmation email shortly."},
            {"speaker": "customer", "text": "Perfect, thanks."},
        ],
    },
    {
        "conversation_id": "conv_014",
        "turns": [
            {"speaker": "customer", "text": "The headphones I bought stopped working after 3 days."},
            {"speaker": "agent", "text": "Sorry to hear that. Since it's within the return window, I can send a replacement."},
            {"speaker": "customer", "text": "I'd rather just get a refund honestly."},
            {"speaker": "agent", "text": "That's fine, refund issued to your original payment method."},
            {"speaker": "customer", "text": "Thanks for not making this difficult."},
        ],
    },
    {
        "conversation_id": "conv_015",
        "turns": [
            {"speaker": "customer", "text": "What are your customer service hours?"},
            {"speaker": "agent", "text": "We're available Monday to Saturday, 8am to 9pm."},
            {"speaker": "customer", "text": "Got it, thank you."},
        ],
    },
    {
        "conversation_id": "conv_016",
        "turns": [
            {"speaker": "customer", "text": "I locked myself out of my account after too many failed logins."},
            {"speaker": "agent", "text": "I can unlock that for you. Can you verify your registered phone number?"},
            {"speaker": "customer", "text": "555-822-1190"},
            {"speaker": "agent", "text": "Verified and unlocked, please try logging in again."},
            {"speaker": "customer", "text": "Still not working, this is really annoying."},
        ],
    },
    {
        "conversation_id": "conv_017",
        "turns": [
            {"speaker": "customer", "text": "I received someone else's order instead of mine."},
            {"speaker": "agent", "text": "I apologize for the mix-up, that shouldn't happen. Can you share the order number on the package?"},
            {"speaker": "customer", "text": "It says #90213, mine was #90215."},
            {"speaker": "agent", "text": "Thank you, I've arranged for your correct order to be shipped and a pickup for this one."},
            {"speaker": "customer", "text": "Alright, appreciate the quick fix."},
        ],
    },
    {
        "conversation_id": "conv_018",
        "turns": [
            {"speaker": "customer", "text": "Is the warranty on the coffee machine one year or two?"},
            {"speaker": "agent", "text": "It's a two-year manufacturer warranty."},
            {"speaker": "customer", "text": "Great, thanks for confirming."},
        ],
    },
    {
        "conversation_id": "conv_019",
        "turns": [
            {"speaker": "customer", "text": "My refund still hasn't shown up after 10 days."},
            {"speaker": "agent", "text": "I'm sorry for the delay, let me check the transaction."},
            {"speaker": "customer", "text": "I've already contacted support twice about this."},
            {"speaker": "agent", "text": "I see the delay was on our end, escalating for immediate processing today."},
            {"speaker": "customer", "text": "This is really disappointing service."},
        ],
    },
    {
        "conversation_id": "conv_020",
        "turns": [
            {"speaker": "customer", "text": "The shoes I got are damaged, the sole is coming apart."},
            {"speaker": "agent", "text": "That's not right at all. Could you share a photo?"},
            {"speaker": "customer", "text": "Sent, my name is David Ortiz if that helps look up the order."},
            {"speaker": "agent", "text": "Thanks David, replacement pair shipping out today free of charge."},
            {"speaker": "customer", "text": "Appreciated, thank you."},
        ],
    },
]


def main():
    out_path = Path(__file__).resolve().parent.parent / "data" / "conversations.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(CONVERSATIONS, indent=2))
    print(f"Wrote {len(CONVERSATIONS)} conversations to {out_path}")


if __name__ == "__main__":
    main()
