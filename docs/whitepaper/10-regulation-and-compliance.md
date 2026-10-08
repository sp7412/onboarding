# 10 - Regulation And Compliance

> **General education, not legal advice.** Requirements vary by jurisdiction, channel,
> role, contract and facts, and they change. Counsel and compliance owners must validate
> any design. Facts as of September 27, 2026.

**Estimated reading time:** 10 minutes · **Facts as of:** September 27, 2026

## Five Takeaways

1. **AI voices count as "artificial" under the TCPA.** Since February 2024 the FCC has
   treated AI-generated human voices as artificial voices, so *outbound* calls that use
   them need prior express consent unless an emergency purpose or exemption applies. [1]
2. **Call recording consent varies by state.** Federal law and most states allow recording
   with one party's consent, but about a dozen states require all parties to consent, and
   the list has edge cases. [2][3]
3. **AI disclosure laws are emerging.** Utah requires a business using generative AI with
   consumers to disclose it when clearly asked, and gives a safe harbor for disclosing up
   front. [4]
4. **Payments and personal data carry their own regimes:** PCI DSS for card data and
   state privacy laws such as the CCPA. [5][6]
5. ServiceTitan's own 10-K names the TCPA and related rules as a business risk. [7]
   Analysis: compliance should be designed into the agent's policy layer (per call,
   per jurisdiction), not left to the prompt.

## 1. Outbound calls and AI voices (TCPA)

The Telephone Consumer Protection Act restricts calls using an artificial or prerecorded
voice to residential lines and to mobile numbers without the called party's prior express
consent. In Declaratory Ruling FCC 24-17 (adopted February 2, released February 8, 2024),
the FCC confirmed that these restrictions cover current AI technologies that generate
human voices, so such calls require prior express consent absent an emergency purpose or
exemption. [1] Legal commentary notes the FCC also said the TCPA has no carve-out for
technologies that claim to be the equivalent of a live agent. [8]

ServiceTitan's 10-K describes the TCPA, the Telemarketing Sales Rule as implemented by the
FCC, and related rules as imposing significant restrictions on calls and texts without prior
consent, and lists them among its regulatory risks. [7]

**Analysis for design.** Inbound answering (the customer called the business) is a different
situation from the business initiating a call. Outbound reminders, confirmations, missed-call
callbacks and review requests are where TCPA risk concentrates. An agent platform needs a
consent record per contact and per purpose, and a policy check before any AI-voiced outbound
call. Marketing-type calls face stricter rules than purely informational ones; that line
must be drawn by counsel.

## 2. Recording and transcription consent

Federal law (the Wiretap Act, part of the Electronic Communications Privacy Act) allows a
party to a call to record it with one party's consent. Most states follow that one-party
rule, and a smaller group requires every party to consent. [2][3] Commonly cited all-party
states for phone calls include California, Connecticut, Delaware, Florida, Illinois,
Maryland, Massachusetts, Montana, Nevada, New Hampshire, Pennsylvania and Washington, but
published lists run from roughly 11 to 13 states because several are edge cases. [3]
Justia's 50-state survey notes that some states apply the rule only where there is a
reasonable expectation of privacy, and that courts disagree about which state's law applies
to interstate calls. [2]

**Analysis for design.** Voice agents record, transcribe and summarize by nature. The safest
default is an up-front recording notice on every call, with the notice text and behavior
configurable per business and jurisdiction. Downstream uses (training, quality review,
model evaluation) may need their own consent and retention rules.

## 3. Telling callers they are talking to AI

Utah's Artificial Intelligence Policy Act, as amended by SB 226 effective May 7, 2025,
requires a business using generative AI in a consumer transaction to disclose that the
consumer is interacting with AI if the consumer clearly and unambiguously asks. It gives a
safe harbor to businesses that disclose AI use clearly at the start and throughout the
interaction, and allows fines of up to $2,500 per violation. [4] Stricter disclosure applies
to regulated occupations in "high-risk" interactions. [4]

**Analysis for design.** Even where not required, answering honestly when a caller asks "am I
talking to a robot?" is both the low-risk and the trust-preserving choice. A standard
opening disclosure also satisfies the Utah safe harbor. Other states have bot-disclosure or
AI laws with different scopes; track them centrally.

## 4. Business texting (A2P 10DLC)

Voice agents often send follow-up texts: confirmations, technician-on-the-way messages,
links. In the U.S., application-to-person texts sent over standard 10-digit numbers (A2P
10DLC) generally require the sending business to register its brand and messaging campaigns
through its messaging provider, and unregistered traffic can be filtered or blocked. [9]
Exact requirements and exceptions depend on the provider and carriers, so confirm them with
the platform actually sending the messages. Texting also falls under
the TCPA's consent rules noted in the 10-K. [7]

## 5. Payments over the phone (PCI DSS)

PCI DSS sets baseline technical and operational requirements for protecting payment account
data and applies to entities that store, process or transmit cardholder data or could
affect its security. [5] **Analysis:** card numbers should never enter free-form model
context, transcripts or logs. Use a separate secure capture path (a payment link, DTMF
masking or a PCI-scoped payment flow) and keep the agent out of scope.

## 6. Privacy and data rights

The California Consumer Privacy Act gives covered consumers rights to know, delete,
correct, opt out of sale or sharing and limit use of sensitive personal information, and
places responsibilities on covered businesses. [6] Call audio, transcripts and summaries
are personal information. **Analysis:** support deletion and retention limits across every
copy, including evaluation datasets and traces (see lab 07's redaction section).

## 7. Trade-specific rules the agent must not overstep

HVAC work touches EPA Section 608, which covers technician certification, refrigerant
handling and recordkeeping for covered equipment. [10] BLS notes that most states require plumbers
to be licensed and that HVAC technicians may need a license or certification. [11][12] **Analysis:** the agent should never give do-it-yourself repair
guidance on regulated or dangerous work beyond basic safety instructions (for example,
leaving a home that smells of gas), and should route technical questions to qualified staff.

## Compliance as system design

| Concern | Control in the agent platform |
|---|---|
| Outbound AI-voice calls | Consent store per contact and purpose; pre-call policy check |
| Recording | Jurisdiction-aware notice; configurable text; retention policy per use |
| AI disclosure | Standard opening disclosure; honest answer when asked |
| Texting | Registered brands and campaigns; consent and opt-out handling |
| Payments | Out-of-band secure capture; redaction in transcripts and logs |
| Privacy | Deletion and retention across recordings, transcripts, traces, eval sets |
| Regulated advice | Tool and prompt limits; escalation to licensed staff |

## Questions to validate after joining

- Who owns voice-agent compliance policy (legal, product, platform), and where are rules
  enforced in code?
- Is outbound AI calling in scope today, and how is consent captured?
- What are the retention rules for recordings and transcripts used for model evaluation?

## Sources

1. FCC, Declaratory Ruling FCC 24-17, CG Docket No. 23-362 (released February 8, 2024): <https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf>
2. Justia, "Recording Phone Calls and Conversations: 50-State Survey": <https://www.justia.com/50-state-surveys/recording-phone-calls-and-conversations/>
3. Viirtue, "Call Recording Consent Laws by State (2026 Guide)": <https://viirtue.com/call-recording-consent-laws-by-state-2026-guide/>
4. Orrick, "Utah enacts AI disclosure law for consumer transactions" (April 25, 2025): <https://infobytes.orrick.com/2025-04-25/utah-enacts-ai-disclosure-law-for-consumer-transactions>
5. PCI Security Standards Council, PCI DSS: <https://www.pcisecuritystandards.org/standards/pci-dss/>
6. California Department of Justice, CCPA: <https://oag.ca.gov/privacy/ccpa>
7. ServiceTitan Form 10-K, fiscal 2026 (Government Regulation; Risk Factors): <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm>
8. Wilson Sonsini, "FCC Rules AI-Generated Voices Are 'Artificial' Under the TCPA": <https://wsgr.com/en/insights/fcc-rules-ai-generated-voices-are-artificial-under-the-tcpa.html>
9. Twilio, A2P 10DLC documentation: <https://www.twilio.com/docs/messaging/compliance/a2p-10dlc>
10. U.S. EPA, Section 608: <https://www.epa.gov/section608>
11. BLS Occupational Outlook Handbook, plumbers (licensing): <https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm>
12. BLS Occupational Outlook Handbook, HVAC mechanics and installers: <https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm>
