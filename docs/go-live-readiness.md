# Northstar MVP Go-Live Readiness

## What Works

The final MVP successfully supports the planned customer-service flows that were tested during NS-15:

### Order Status
- Retrieve order status for a valid order.
- Confirm whether an order has shipped.
- Handle invalid order numbers.
- Provide a support option when the order cannot be found.

### Returns & Refunds
- Explain how to return an item.
- Check return eligibility for a valid order.
- Show refund processing status.

### Conversation Controls
- Start Over returns the user to the main menu.
- Contact Support routes the user to the support flow.

The MVP was tested against the defined NS-14 and NS-15 scenarios using the available test data.

---

## Known Broken / Limitations

The current build is a **prototype MVP** and has the following limitations:

- Uses **mock/test order data** rather than Northstar's production database.
- Only the available test order data can be executed; several scenarios could not be fully tested because matching test data was not present.
- Support escalation is provided through a **prototype support flow** rather than a live support integration.
- The application is a **prototype deployment** and is not production-ready.
- Refund processing information is simulated and is not connected to a real payment provider.

No undocumented requirements were added during QA testing.

---

## Northstar Handoff Requirements

To operate or extend this MVP, Northstar's team will need to:

- Connect the chatbot to **production order data**.
- Replace mock return and refund data with **live business data**.
- Configure the **real customer support channel** (email, ticketing system, or live chat).
- Review and finalize the **business rules** for returns, refunds, and escalation behavior.
- Deploy the application using Northstar's production infrastructure.
- Expand test data coverage to include processing, delayed, delivered, non-eligible, returned, non-refundable, and refund-issued scenarios.

---

## Readiness Summary

The MVP is suitable for **demonstration and evaluation purposes**. Core order-status and returns/refunds flows are functioning with the available test data, but production deployment requires integration with Northstar's operational systems and completion of the handoff items listed above.
