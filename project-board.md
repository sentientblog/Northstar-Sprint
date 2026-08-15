# Northstar Support Deflection MVP — Project Board

## Project Goal
Build a simple chatbot MVP for Northstar Retail Co. that reduces manual
support handling for at least two repetitive ticket categories:

1. Order Status
2. Returns & Refunds

## Board Rules
- Every task must be ≤4 hours.
- Every task must have an owner, priority, status, and Definition of Done.
- Definitions of Done must be one clear, checkable outcome.
- Split tasks if they exceed 4 hours.
- Update task status on the same day work occurs.
- Work must be traceable: Task → Owner → Commit/Edit → Artifact.
- Commit format: `<type>: <what changed> - <why it matters>`.
- `wip`, `updates`, `stuff`, etc. are not valid commit messages.
- Zero visible activity for 2+ days triggers the Team Charter escalation path.
- Do not create artificial work or commits to inflate contribution.

---

## NS-01 — Define MVP Scope
**Owner:** Jonah | **Priority:** High | **Estimate:** ≤2h | **Status:** Done

Define supported ticket categories, chatbot behaviour, MVP boundaries and
out-of-scope functionality.

**Deliverable:** `docs/mvp-scope.md`

**DoD:** MVP scope clearly defines supported categories, behaviour,
boundaries and out-of-scope functionality.

---

## NS-02 — Define Order Status Conversation Flow
**Owner:** Jonah | **Priority:** High | **Estimate:** ≤3h | **Status:** Done

Define user inputs, chatbot options, required order information, order
states, responses, invalid inputs, retries and escalation.

**Deliverable:** `docs/order-status-flow.md`

**DoD:** Developers can implement the Order Status flow without inventing
additional business logic.

---

## NS-03 — Define Returns & Refunds Conversation Flow
**Owner:** Jonah | **Priority:** High | **Estimate:** ≤3h | **Status:** Done

Define eligibility, 7-day rule, returned/not-returned states, refund
not-available, refund-in-transit, retry limit and escalation behaviour.

**Deliverable:** `docs/returns-refunds-flow.md`

**DoD:** Every supported Returns & Refunds state has a defined chatbot response.

---

## NS-04 — Define Mock Data & Business Rules
**Owner:** Jonah | **Priority:** High | **Estimate:** ≤3h | **Status:** Done

Create/document order and return data, status codes, date calculations and
edge-case data required by developers.

**Deliverable:** Mock data and supporting documentation in `data/`.

**DoD:** Developers have all approved data, status codes and business rules
required to implement the flows.

---

## NS-05 — Set Up Chatbot Frontend
**Owner:** Frontend Developer | **Priority:** High | **Estimate:** ≤4h | **Status:** Done

Build the chatbot interface using the existing MVP scope, flows and data
specifications.

**DoD:** Users can select Order Status or Returns & Refunds and proceed
through the chatbot interface.

---

## NS-06 — Implement Order Status Backend
**Owner:** Backend Developer | **Priority:** High | **Estimate:** ≤4h | **Status:** Done

Implement Order Status logic using the approved flow, mock data and status codes.

**DoD:** Backend returns the correct response for each supported order state.

---

## NS-07 — Implement Returns & Refunds Backend
**Owner:** Backend Developer | **Priority:** High | **Estimate:** ≤4h | **Status:** Done

Implement Returns & Refunds logic using the approved flow, data and rules.

**DoD:** Backend returns the correct response for each documented eligibility
and refund state.

---

## NS-08 — Connect Mock Data to Backend
**Owner:** Backend Developer | **Priority:** High | **Estimate:** ≤3h | **Status:** Done

Connect the approved mock datasets to backend logic.

**DoD:** Backend responses correctly reflect the approved mock data and states.

---

## NS-09 — Implement Conversation & Response Logic
**Owner:** Backend Developer | **Priority:** High | **Estimate:** ≤4h | **Status:** Done

Implement decision logic using the approved flowcharts and business rules.

**DoD:** The chatbot selects the correct next response/state for each supported
user interaction.

---

## NS-10 — Connect Frontend to Backend
**Owner:** Frontend + Backend | **Priority:** High | **Estimate:** ≤4h | **Status:** Done

Connect the chatbot interface to backend functionality.

**DoD:** Users can complete Order Status or Returns & Refunds interactions
through the frontend and receive backend responses.

---

## NS-11 — Implement Error, Retry & Escalation Handling
**Owner:** Frontend + Backend | **Priority:** Medium | **Estimate:** ≤3h | **Status:** Done

Implement invalid-input, retry, Start Over and escalation behaviour.

**DoD:** Error and recovery behaviour matches the approved conversation flows.

---

## NS-12 — Finalize Order Status Flowchart
**Owner:** Jonah | **Priority:** Medium | **Estimate:** ≤3h | **Status:** Done

Create the final visual Order Status conversation flow.

**Deliverable:** Order Status flowchart in `docs/`.

**DoD:** Flowchart accurately represents the approved logic and implementation.

---

## NS-13 — Finalize Returns & Refunds Flowchart
**Owner:** Jonah | **Priority:** Medium | **Estimate:** ≤3h | **Status:** Done

Create the final visual Returns & Refunds flow.

**Deliverable:** Returns & Refunds flowchart in `docs/`.

**DoD:** Flowchart accurately represents eligibility, returned/not-returned,
refund states, retries and escalation.

---

## NS-14 — Create Functional Test Cases
**Owner:** QC | **Priority:** High | **Estimate:** ≤3h | **Status:** Done

Create tests covering supported functionality and defined edge cases.

**DoD:** Test cases cover the primary Order Status and Returns & Refunds paths
and their relevant edge cases.

---

## NS-15 — Execute MVP Testing
**Owner:** QC | **Priority:** High | **Estimate:** ≤4h | **Status:** Done

Execute the approved functional tests against the completed MVP.

**DoD:** Every defined test has a recorded pass, fail or blocked result.

---

## NS-16 — Verify & Document Test Results
**Owner:** QC | **Priority:** High | **Estimate:** ≤3h | **Status:** Done

Consolidate testing results and document unresolved defects/limitations.

**Deliverable:** Test-results documentation.

**DoD:** Final results clearly identify every test outcome and unresolved issue
or accepted limitation.

---

## NS-17 — Create Go-Live Readiness Note
**Owner:** Jonah | **Priority:** High | **Estimate:** ≤2h | **Status:** Done

Create the required one-page Northstar handoff note.

**Deliverable:** `docs/go-live-readiness.md`

Must cover:
- What works.
- Known limitations/broken functionality.
- What Northstar needs to do to take over.
- Production integration requirements.
- Handoff requirements.

**DoD:** A one-page note clearly communicates MVP capabilities, limitations
and requirements for moving toward production.

---

## NS-18 — Audit Contribution & Traceability
**Owner:** Entire Team | **Priority:** High | **Estimate:** ≤4h | **Status:** Finalize

Review task ownership, board timestamps, commits, PRs, edits and resulting
artifacts; identify missing evidence and prepare the raw audit evidence/export.

**DoD:** Completed work can be traced from task → contributor → repository
activity → resulting artifact.

---

## NS-19 — Final Delivery & Demo Package
**Owner:** Entire Team | **Priority:** High | **Estimate:** ≤4h | **Status:** Finalize

Verify MVP, documentation, flowcharts, mock data, testing evidence, go-live
note, audit evidence and demo path.

**DoD:** MVP and required Assignment 2 artifacts are complete and ready for
submission and presentation.

---

## NS-20 — Repository & Documentation Review
**Owner:** Member 5 | **Priority:** Medium | **Estimate:** ≤3h | **Status:** In Progress

Review repository structure, README, documentation, links, data, source code,
duplicates/obsolete files and consistency between scope, flows, data and tests.

**Deliverable:** Documentation/repository improvements and review findings.

**DoD:** A new team member or Northstar representative can navigate the
repository and locate the information needed to understand the MVP.

---

## NS-21 — MVP Integration & Presentation Readiness Review
**Owner:** Member 5 | **Priority:** High | **Estimate:** ≤4h | **Status:** In Progress

Independently run the MVP and test Order Status, Returns & Refunds,
frontend/backend integration, mock data, retries, Start Over, escalation,
flowchart consistency, dead ends and obvious UI issues.

**Deliverable:** `docs/presentation-readiness-review.md`

Record significant findings as:
- Finding
- Severity: Low / Medium / High
- Recommended Action
- Status: Open / Resolved / Accepted

**DoD:** MVP has been independently reviewed for presentation readiness and
all significant findings are documented and communicated.

---

# Assessment / Audit Requirements

## Assignment 1 — Team Working Agreement & Board
Board must demonstrate:
- 10+ granular tasks.
- Tasks ≤4 hours.
- Owner assigned to every task.
- Priority assigned to every task.
- Clear, checkable Definition of Done.
- Signed Team Charter stored in the repository.
- Same-day board status updates.

## Assignment 2 — Collaborative Delivery & Audit Log
Required:
- Working multi-author MVP.
- Version-controlled repository.
- Individual activity/commit/edit evidence.
- Task → contribution → artifact traceability.
- Commit/edit naming discipline.
- Raw audit log export.
- 1-page Go-Live Readiness Note.

Evaluation focus:
- 40% Balance of Contribution.
- 30% Process Discipline.
- 30% Quality of Work.

## Assignment 3
Individual Day-5 requirements:
- Confidential Peer Reliability Index.
- Final self-assessment against Day-1 baseline.

Do not place individual Peer Reliability responses in the shared repository.
