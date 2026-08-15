# Northstar Support Deflection Chatbot
## About the Project
Northstar is a Support Deflection Chatbot MVP developed for Northstar Retail Co. The purpose of the project is to help reduce repetitive customer support requests by guiding customers through predefined options and providing relevant information before they need to contact a human support agent.The chatbot uses a guided conversation and decision-tree approach rather than advanced AI. Users select options based on their support problem and are guided through the appropriate conversation flow.
## Core Features
The MVP focuses on two required support categories:
### 1. Order Status
Customers can select options such as:
- Where is my order?
- Has my order shipped?
- My order hasn't arrived
- Something else
Where necessary, the chatbot can request an order number and use mock Northstar data to provide the relevant response.
### 2. Returns & Refunds
Customers can select options such as:
- How do I return an item?
- Is my item eligible for return?
- When will I receive my refund?
- My refund hasn't arrived
- Something else
The chatbot also provides appropriate fall-back options when a customer's issue is not covered by the available choices.
### Stretch Goal
Stock Availability is a stretch feature and should only be considered after Order Status and Returns & Refunds are stable and working reliably.
## Project Documentation
The detailed project documentation is available in the docs. It includes information about the MVP Scope, [View order status flowchart](order-satus-flowchart.drawio), [View return status flowchart](returns-refunds-flowchart), [View general chat function flowchart](general-chatbot-flowchart.png), testing information[View test results](test-results.md)[View retest results](retest-results.md), and known limitations. [Go-live readiness](go-live-readiness.md) – Provides information about the project's readiness, known issues, testing results, and handover requirements. 
[MVP scope](backend/docs/NS-01-mvp-scope)
[The order status flow](order-status-flow.md)
[Returns & Refunds Flow](docs/go-live-readiness.md)
[Returns Refunds flowcharts](order-status-flowchart.drawio)
[Order status Rough Flow-chart](order-status-flow-rough-flowchart)
[Flow chart](general-chatbot-flowchart.png)
[Test Results](data/test-results.md) 
[Retest Results](data/retest-results.md)
## Running the Application
To run the project locally:
1. Clone this repository.
2. Open the project folder in your code editor or terminal.
3. Install the project dependencies using the command provided in the project's configuration.
4. Start the application using the project's development/run command.
5. Open the local address provided by the application in your browser.
## Live Demo
The deployed chatbot can be accessed here:
**[Northstar Live Demo] (https://northstar-sprint.vercel.app/)
The live version can be used to test the Order Status and Returns & Refunds user journeys.
## Project Scope
This project is an MVP demonstration of the support-deflection approach. It does not aim to build a production customer-service platform, sophisticated AI model, production database, real payment or shipping integrations, authentication, or advanced analytics. The main goal is to demonstrate a simple, functional chatbot that can handle repetitive support requests through guided options and appropriate responses.
