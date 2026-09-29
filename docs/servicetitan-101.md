# ServiceTitan 101

This is a public-source orientation, not an account of any internal architecture or
roadmap. Product names and positioning change; revisit the linked pages before using
this as current company research.

## What The Company Does

ServiceTitan describes its platform as cloud software for the trades, including
contractors in plumbing, HVAC, electrical, and related home and commercial services.
Its public product pages group capabilities around customer acquisition, field service
operations, financial workflows, and business intelligence. Start with the [company
overview](https://www.servicetitan.com/company) and [platform overview](https://www.servicetitan.com/features).

The important mental model is not "a chatbot for a consumer." The paying customer is
typically a contractor business. That business uses software to turn demand into
scheduled work, send the right technician, complete the job, collect payment, and
retain the customer. A voice agent therefore sits inside an operational workflow where
an apparently small conversational error can create a missed lead, a bad appointment,
or unnecessary CSR work.

## Who Uses It

Public product material distinguishes residential and commercial contractors and
describes workflows involving office staff, technicians, and business owners. Do not
infer the exact workflows, permissions, or systems used by any particular customer.
The public [industries page](https://www.servicetitan.com/industries) is a useful starting point.

## Product Vocabulary

These are public product references, not claims about an internal implementation:

- [Contact Center Pro](https://www.servicetitan.com/features/pro/contact-center) addresses contact-center workflows.
- [Scheduling Pro](https://www.servicetitan.com/features/pro/scheduling) addresses scheduling and booking workflows.
- [Dispatch Pro](https://www.servicetitan.com/features/pro/dispatch) addresses dispatch operations.
- [Atlas](https://www.servicetitan.com/features/atlas) is presented publicly as an AI assistant for the trades.
- [AI Voice Agents](https://www.servicetitan.com/features/pro/virtual-agent) is the public product page for voice-agent capabilities.

Read the pages as product context. They do not reveal private system boundaries,
production metrics, customer data, or team ownership. Those are questions to ask after
joining, under the relevant access and privacy policies.

## How AI Fits The Learning Problem

The useful engineering question is: which parts of a customer interaction can be
handled conversationally, and which actions require authoritative business state,
policy checks, auditability, or human escalation? The labs model this boundary with a
fictional contractor and a mock backend. They do not model ServiceTitan's internal
systems.

For pre-start study, focus on four outcomes:

1. Understand the contractor's economic unit: a completed, profitable customer job.
2. Trace how an inbound request becomes a scheduled operational commitment.
3. Separate natural-language interpretation from authorization and transaction logic.
4. Measure customer-visible outcomes such as correct booking, appropriate escalation,
   and dead-air latency rather than optimizing model metrics in isolation.

## Public Sources

- [ServiceTitan company](https://www.servicetitan.com/company)
- [ServiceTitan platform](https://www.servicetitan.com/features)
- [ServiceTitan industries](https://www.servicetitan.com/industries)
- [ServiceTitan products](https://www.servicetitan.com/products)
