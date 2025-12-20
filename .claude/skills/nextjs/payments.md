
---

# ✅ `payments.md`

```md
# Payments Skill

## 🎯 Role
Handle secure Stripe integration, payment flows, subscriptions, and webhook event processing.

---

## 🚀 Core Expertise
- Stripe Checkout
- Payment Intents
- Webhooks
- Subscription billing
- Order lifecycle
- Secure server-side handling

---

## 🔥 Rules
- Never process Stripe on client
- Use server-side API
- Verify webhook signatures
- Store transactions safely
- Handle failures properly

---

## 🧠 Example Webhook

```ts
export async function POST(req: Request) {
  const body = await req.text();
  // verify event -> process -> update DB
}
