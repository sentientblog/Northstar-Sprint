# Northstar Support Chatbot — Order Status Flow

## Purpose

Define the chatbot behaviour for customers who need information
about an existing order.

## Supported Scenarios

The MVP supports three Order Status scenarios:

1. Where is my order?
2. Has my order shipped?
3. My order hasn't arrived.

## Entry Point

When the customer selects **Order Status**, the chatbot presents
the three supported scenarios.

## Required Input

All three scenarios require the customer to provide an order number.

The order number is used to retrieve the corresponding order from
the mock order data.

## Order Number Validation

If the order number is not found:

- Inform the customer that the order number could not be found.
- Allow the customer to try again.
- Provide an option to contact support.

## Scenario 1 — Where Is My Order?

The chatbot retrieves the order's:

- Current status
- Estimated delivery date

The chatbot presents this information to the customer.

### Example

> Your order NS1001 is currently in transit and is expected to
> arrive on August 14.

## Scenario 2 — Has My Order Shipped?

The chatbot checks the order's shipping status.

If shipped:

> Your order NS1001 has shipped and is currently in transit.

If not shipped:

> Your order NS1002 has not shipped yet and is currently being processed.

## Scenario 3 — My Order Hasn't Arrived

The chatbot checks the order's delivery status.

Possible states:

- In transit
- Delayed
- Delivered

If the order is delayed or still in transit, the chatbot provides
the available delivery information.

If the order is marked as delivered but the customer reports that
they have not received it, the chatbot should offer human-support
escalation.

## Resolution

After providing an answer, the chatbot should offer:

- **Start Over**
- **Contact Support**

## Escalation

The chatbot should provide a human-support option when:

- The order cannot be found after retrying.
- The customer's issue is not covered by the available options.
- An order is marked as delivered but the customer reports it missing.
- The customer indicates that the provided information did not resolve
  their issue.

## Required Data

The Order Status flow requires:

| Field | Purpose |
|---|---|
| `order_id` | Identify the order |
| `status` | Current order state |
| `shipped` | Determine whether the order has shipped |
| `estimated_delivery` | Provide expected delivery information |

## Definition of Done

A customer can select Order Status, choose one of the supported
scenarios, provide an order number, receive an appropriate response,
and access an escalation path when the chatbot cannot resolve the issue.

## Flowchart

See `order-status-flow.png`.
