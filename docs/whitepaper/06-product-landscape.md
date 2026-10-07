# 06 - ServiceTitan Product Landscape

**Estimated reading time:** 7 minutes · **Facts as of:** September 27, 2026


> **Update (Pantheon 2026, October 6, 2026):** the press release says Max is now available to all residential in-home contractors (a keynote stated it more narrowly: plumbing, heating, electrical and garage-door customers with four or more technicians), with a limited commercial and roofing pilot; the company also announced the Atlas mobile app and Homh. See the [Pantheon 2026 AI roadmap brief](../pantheon-2026-ai-roadmap.md).

## Five Takeaways

1. The platform is organized as **Core** (the base system for all workflows), **FinTech**
   (payments and consumer financing) and **Pro** add-ons that deepen one area. [1]
2. The phone and contact-center stack is a product line of its own: Phones Pro (VoIP with
   call KPIs and transcripts), Contact Center Pro (omnichannel, multi-location) and AI
   Virtual Agents (overflow and after-hours booking). [1][2][3]
3. AI runs through the product rather than sitting beside it: Titan Intelligence, then
   Atlas (an agentic AI layer, fiscal 2026), then the Max program. [1][4]
4. Acquisitions extend the platform into specific trades and workflows: FieldRoutes,
   Aspire, Convex and Conduit Tech. [1][5]
5. Analysis: a voice agent is valuable here because it can *act* inside the system of
   record (customer, job, capacity), not because it can talk.

## Core, FinTech, Pro

| Layer | What it covers (per the 10-K) | Source |
|---|---|---|
| Core | Call tracking, scheduling, dispatching, end-customer communications, marketing automation, estimating, job costing, sales, inventory, payroll integration | [1] |
| FinTech | Payment processing and third-party consumer financing | [1] |
| Pro | Add-ons such as Phones Pro, Contact Center Pro, Marketing Pro and AI products. The website's Pro menu lists AI Virtual Agent, Marketing Pro, Contact Center Pro, Pricebook Pro, Fleet Pro, Scheduling Pro, Dispatch Pro and Field Pro (formerly Sales Pro) | [1][7][8] |

Office staff use the platform in a browser; technicians mainly use the mobile app. [1]

## Mapping products to the job lifecycle

| Lifecycle step (chapter 03) | Relevant public capabilities | Source |
|---|---|---|
| Lead and marketing | Marketing Pro (AI-powered email, direct mail, reputation management, ads measurement, Audience Builder); Convex for commercial prospecting | [1] |
| Inbound call | Phones Pro; Call Booking and Recording (auto-populates caller info and history for the CSR); Google Local Services Ads booking integration | [1] |
| Booking | Scheduling with capacity; AI Virtual Agents for overflow and after-hours; Contact Center Pro | [1][2][3] |
| Dispatch | Dispatching; technician on-the-way notifications with photo and tracking link | [1] |
| On site | Mobile app; customizable Pricebook with multiple pricing options, photos and warranties; Conduit Tech LiDAR design and load calculations for HVAC | [1] |
| Payment | FinTech payments and financing | [1] |
| Follow-up | Second Chance Leads (AI finds unbooked calls worth another try); memberships; reporting and Benchmark Insights | [1] |

## The phone stack in more detail

- **Phones Pro** is a VoIP phone system that routes calls through the platform, so the
  business knows which CSR took each call and can report KPIs like abandonment rate and
  average call duration. It provides call transcripts and automated escalation alerts. [1]
- **Call Booking and Recording** fills in customer details as a call arrives and shows the
  CSR property details and history, so booking is informed rather than blind. [1]
- **Contact Center Pro** is described as an omnichannel, multi-location, AI-powered cloud
  contact center for the trades, with a Universal Inbox across channels and businesses. [1]
- **AI Virtual Agents** use AI with the platform's data to handle overflow and after-hours
  calls: booking, rescheduling and confirming appointments. [1] The product page lists
  capabilities including capacity-aware booking by job type, location and skills;
  confirmations; rescheduling; membership greetings; recurring services; job-type
  selection; live escalation; transcripts and summaries; and AI call classification. [2]
- **Second Chance Leads** uses AI to review calls that did not produce a booking and flag
  the ones worth pursuing again. [1]

Analysis: this is the environment a voice agent lives in. It inherits customer records,
capacity rules and escalation paths from these products, and its failures surface in the
same reports CSR managers already use.

## AI across the platform

The 10-K describes three layers of AI activity: insights embedded in existing products,
purpose-built AI add-ons for the trades, and **Atlas**, introduced in fiscal 2026 as an
agentic AI layer and the next evolution of the **Titan Intelligence** engine. [1] The Atlas
page positions it as a conversational assistant for office and field work, with some
capabilities marked as coming soon. [6] **Max**, discussed in fiscal 2027 results, is the
company's "Agentic Operating System" program; management expects more than 700 enrolled
locations by the end of fiscal 2027. [4]

## Acquisitions as product extensions

- **FieldRoutes** (pest control and lawn care) and **Aspire** (commercial landscaping) are
  sold alongside the main ServiceTitan product for those verticals. [5]
- **Convex** gives contractors serving commercial buildings a view of properties, contacts,
  businesses and permits to find new work. [1]
- **Conduit Tech** uses LiDAR to build 3D models, permit-ready load calculations and
  visualizations on site for HVAC design and sales. [1]

## What this means for a voice-agent engineer

- Integration depth is the product. Knowing the data model (customer, location, job type,
  capacity, membership) matters as much as knowing the speech stack.
- The phone products already measure CSR performance. Voice-agent metrics should be
  comparable to them so managers can judge agents and humans side by side.
- Atlas and Max suggest the voice agent will increasingly be one surface of a broader agent
  system, which raises questions about shared tools, policies and evaluation.

## Questions to validate after joining

- Which of these products does the voice agent call directly, and through what interfaces?
- How are Virtual Agent calls reported alongside human CSR calls?
- How does Atlas share tools, policies or models with voice agents?

## Sources

1. ServiceTitan Form 10-K, fiscal 2026 (Business section): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
2. ServiceTitan, AI Virtual Agent product page: <https://www.servicetitan.com/features/pro/virtual-agent>
3. ServiceTitan, Contact Center Pro product page: <https://www.servicetitan.com/features/pro/contact-center>
4. ServiceTitan fiscal Q2 2027 results (September 8, 2026): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm>
5. ServiceTitan IPO prospectus (Form 424B4): <https://www.sec.gov/Archives/edgar/data/1638826/000119312524277099/d577298d424b4.htm>
6. ServiceTitan, Atlas product page: <https://www.servicetitan.com/features/atlas>
7. ServiceTitan, Scheduling Pro: <https://www.servicetitan.com/features/pro/scheduling>
8. ServiceTitan, Dispatch Pro: <https://www.servicetitan.com/features/pro/dispatch>
