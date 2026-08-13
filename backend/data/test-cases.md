| Test ID  | Scenario                   | Input                          | Expected Result                                        | Actual Result     | Pass/Fail | Notes        |
|----------|----------------------------|--------------------------------|--------------------------------------------------------|-------------------|-----------|--------------|
| TC-OS-01 | Processing order           | Valid processing order         | Bot shows order is being processed                     | Pending execution | PENDING   | Order Status |
| TC-OS-02 | In transit order           | Valid in_transit order         | Bot shows order is in transit                          | Pending execution | PENDING   | Order Status |
| TC-OS-03 | Delayed order              | Valid delayed order            | Bot shows delay message                                | Pending execution | PENDING   | Order Status |
| TC-OS-04 | Delivered order            | Valid delivered order          | Bot confirms delivery                                  | Pending execution | PENDING   | Order Status |
| TC-OS-05 | Delivered but not received | Delivered order with complaint | Bot provides support or escalation guidance            | Pending execution | PENDING   | Order Status |
| TC-OS-06 | Invalid order              | Invalid order number           | Bot shows invalid order message                        | Pending execution | PENDING   | Order Status |
| TC-OS-07 | Five failed attempts       | Invalid order entered 5 times  | Bot offers support or safely handles repeated failures | Pending execution | PENDING   | Order Status |
| TC-RT-01 | Return eligible            | Eligible item                  | Bot confirms eligibility                               | Pending execution | PENDING   | Returns      |
| TC-RT-02 | Return not eligible        | Non-eligible item              | Bot explains why item is not eligible                  | Pending execution | PENDING   | Returns      |
| TC-RT-03 | Item not returned          | Refund requested before return | Bot requests item return first                         | Pending execution | PENDING   | Returns      |
| TC-RT-04 | Item returned              | Returned item                  | Bot confirms return received                           | Pending execution | PENDING   | Returns      |
| TC-RF-01 | Refund not available       | Non-refundable order           | Bot explains refund is not available                   | Pending execution | PENDING   | Refunds      |
| TC-RF-02 | Refund in transit          | Refund processing              | Bot shows refund is being processed                    | Pending execution | PENDING   | Refunds      |
| TC-RF-03 | Refund issued              | Completed refund               | Bot confirms refund issued                             | Pending execution | PENDING   | Refunds      |
| TC-GN-01 | Unsupported request        | Unsupported text or option     | Bot offers supported options                           | Pending execution | PENDING   | General      |
| TC-GN-02 | Unavailable data           | Missing backend data           | Bot shows graceful unavailable message                 | Pending execution | PENDING   | General      |
| TC-GN-03 | Start Over                 | Select Start Over              | Conversation returns to main menu                      | Pending execution | PENDING   | General      |
| TC-GN-04 | Contact Support            | Select Contact Support         | Escalation or support message appears                  | Pending execution | PENDING   | General      |

