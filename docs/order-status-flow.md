# Order Status Conversation Flow

## Purpose

Defines the chatbot behaviour for Northstar Order Status queries.

## Supported Scenarios

1. Where is my order?
2. Has my order shipped?
3. My order hasn't arrived.

## Required Input

Order number.

## Validation

Invalid order numbers result in a retry option.

## Resolution

The chatbot retrieves the relevant mock order data and provides
the appropriate status information.

## Escalation

If the chatbot cannot resolve the customer's issue, the customer
is offered a human-support escalation path.

## Flowchart

![Order Status Flow](order-status-flow.png)
