# 00 - Introduction

**Estimated reading time:** 6 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. ServiceTitan connects contractor workflows from customer intake through scheduling, field service, payments, and follow-up; its value proposition is broader than call handling.
2. The market is large, fragmented, seasonal, and constrained by technician availability. More demand does not automatically mean more completed jobs.
3. The phone is a revenue-critical entry point: an agent must qualify the need and book work into real capacity, not merely hold a convincing conversation.
4. PE-backed consolidation gives ServiceTitan a route to expand across acquired contractors when sponsors standardize portfolio operations on one platform.
5. Production success means a correctly booked, policy-compliant job that remains valid after the call. Tool authority, escalation, and defensible evaluation matter more than a raw booking-rate number.

## Executive Summary

ServiceTitan (Nasdaq: TTAN) sells cloud software that helps trades businesses manage work from the first customer call through scheduling, field service, and final payment. The company has been publicly traded since December 2024. In fiscal 2026, approximately 10,800 Active Customers invoiced $82.1 billion through the platform, while ServiceTitan reported about $961 million in revenue. The revenue figure is roughly 1.2% of that transaction volume, and the company guided to $1.14 billion in fiscal 2027 revenue. These figures describe different measures: platform transaction volume is not the same as accounting revenue. See [Chapter 01](01-company.md) for definitions and sources.

The market is large, fragmented, and shaped by seasonality. Annual spending on trades services in the United States and Canada is estimated at about $1.5 trillion. Demand can rise sharply with extreme heat or cold, while the availability of qualified technicians limits how much work a contractor can complete. The U.S. Bureau of Labor Statistics projects roughly 40,000 annual openings for HVAC technicians and 44,000 for plumbers through 2034, including openings caused by workers leaving or retiring. [Chapter 02](02-the-trades-industry.md) examines the market and its workforce constraints.

For a contractor, a phone call is often the beginning of a revenue-generating workflow. The business must answer the call, understand the customer's need, determine whether the work is appropriate, and book it into actual technician capacity. Those steps become harder during seasonal peaks and after hours, when staffing a customer service representative (CSR) team can be difficult. [Chapter 03](./03-how-a-contractor-works.md), [Chapter 04](./04-the-contact-center.md), and [Chapter 05](./05-pain-points.md) explain the contractor workflow and the role of the contact center.

ServiceTitan's platform includes Core, FinTech, and Pro offerings. Its phone-related products include Phones Pro, Contact Center Pro, and AI Virtual Agents. The company's public AI strategy also includes Atlas and Max, which it describes as an "Agentic Operating System" for the trades. [Chapter 06](./06-product-landscape.md) describes the product landscape, while [Chapter 07](./07-ai-voice-agents.md) examines the voice-agent offering.

Virtual Agents are designed to handle overflow and after-hours calls, including appointment booking, rescheduling, confirmations, membership-related interactions, and escalation to a human when needed. They operate in a competitive market that also includes AI-native vendors integrating with ServiceTitan from outside its platform. [Chapter 07](./07-ai-voice-agents.md), [Chapter 08](./08-technology-landscape.md), and [Chapter 09](./09-competitive-landscape.md) cover the product, the underlying technology, and the competitive landscape.

A production voice agent must follow the rules that govern the actions it takes and the data it handles. AI-generated outbound calls may require prior express consent under the Telephone Consumer Protection Act (TCPA); recording-consent requirements vary by state; and AI-disclosure laws are evolving. Payments and personal information introduce additional obligations. These requirements should be represented in the agent's policy and execution layers, not left to the model's discretion. [Chapter 10](10-regulation-and-compliance.md) discusses the relevant legal and compliance considerations.

The most useful measure of success is not simply whether a call ends or an appointment appears in a calendar. The outcome must be a correctly booked job that fits the contractor's capacity and remains valid after the call. Evaluation therefore needs a defensible denominator, honest baselines, and controls for seasonality. [Chapter 11](11-economics-and-metrics.md) discusses the economics and metrics needed to judge those outcomes.

For an engineer, the highest-leverage work often occurs at the boundaries where the agent changes business state or makes a claim to the customer. Tool validation, evidence grounding, escalation, and evaluation help ensure that the agent does what it is authorized to do and accurately communicates what happened. [Chapter 12](./12-risks-and-failure-modes.md), [Chapter 13](./13-future-directions.md), and [Chapter 14](./14-implications-and-open-questions.md) examine failure modes, future directions, and the open questions that follow from this analysis.

## How to Read This Paper

Readers who want a focused introduction can follow the essentials path—Chapters 00, 01, 02, 06, 07, 10, 11, and 14—which should take about two hours. This route covers the company, its market, the product, the voice-agent workflow, compliance, measurement, and the principal engineering implications.

Readers who want the full context should read [Chapter 00](./00-introduction.md) through [Chapter 17](./17-running-agents-in-production.md) in order and then consult the appendices. Each chapter builds on the terminology and assumptions introduced earlier.

## Sourcing Conventions

Every factual claim should be traceable to a public source, and numerical claims should include an "as of" date where relevant. The paper labels interpretation as **Analysis** and a testable but unconfirmed proposition as **Hypothesis**.

Company-reported and customer-reported results are attributed to their source. They should not be treated as general benchmarks unless independent evidence supports that interpretation. Primary sources, such as SEC filings, regulators, and the Bureau of Labor Statistics, are preferred; secondary sources are identified as such.

The marker `[unverified]` identifies claims that still need confirmation. The [claims ledger](claims-ledger.md) records those claims and their verification status.
