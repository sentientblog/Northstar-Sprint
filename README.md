# Northstar MVP Mock Data

This directory contains mock data used by the Support Deflection
Chatbot MVP.

## Files

### orders.json

Contains mock order records used by the Order Status flow.

Supported order states:

- processing
- in_transit
- delayed
- delivered

### returns.json

Contains mock return and refund records used by the Returns & Refunds
flow.

Return states:

- not_returned
- returned

Refund states:

- not_available
- in_transit
- issued

## Return Eligibility

An item is eligible for return if it was purchased within the
previous 7 days.

Eligibility should be calculated from `purchase_date`; it should
not be stored as a static field.

## Testing

`NS9999` can be used as a nonexistent order number to test the
five-attempt retry and escalation behaviour.

This data is fictional and intended only for the MVP prototype.
