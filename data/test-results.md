# NS-15 Execution Results

| Test ID  | Result                                                                            | Status  |
|----------|-----------------------------------------------------------------------------------|---------|
| TC-OS-01 | No valid processing order available                                               | BLOCKED |
| TC-OS-02 | NS1025 showed In Transit with delivery date and last update                       | PASS    |
| TC-OS-03 | No delayed order available                                                        | BLOCKED |
| TC-OS-04 | No delivered order available                                                      | BLOCKED |
| TC-OS-05 | Bot advised contacting support if delivery date had passed                        | PASS    |
| TC-OS-06 | NS9999 returned order not found                                                   | PASS    |
| TC-OS-07 | Contact Support remained available after repeated invalid attempts                | PASS    |
| TC-RT-01 | NS1025 eligible for return within 30 days                                         | PASS    |
| TC-RT-02 | No non-eligible return order available                                            | BLOCKED |
| TC-RT-03 | Refund-before-return flow not available                                           | BLOCKED |
| TC-RT-04 | No returned-item order available                                                  | BLOCKED |
| TC-RF-01 | No non-refundable order available                                                 | BLOCKED |
| TC-RF-02 | Refund status showed Processing (3-5 business days)                               | PASS    |
| TC-RF-03 | No refund-issued order available                                                  | BLOCKED |
| TC-GN-01 | Unsupported path handled with 'I couldn't find an option that matches your issue' | PASS    |
| TC-GN-02 | Free-text unavailable-data request not supported                                  | BLOCKED |
| TC-GN-03 | Start Over returned to the welcome screen                                         | PASS    |
| TC-GN-04 | Contact Support showed escalation and business hours                              | PASS    |
## Summary

- Total test cases: 18
- Passed: 9
- Failed: 0
- Blocked: 9

## Notes

- Order status for NS1025 was successfully retrieved.
- Invalid order handling and support escalation worked correctly.
- Return eligibility and refund-processing responses worked correctly.
- Several scenarios could not be fully executed because the current MVP does not contain test data for processing, delayed, delivered, returned, non-eligible, non-refundable, and refund-issued orders.
