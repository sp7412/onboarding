# 10 - Regulation And Compliance

> General education, not legal advice. Requirements vary by jurisdiction, channel, role,
> contract, and facts. Counsel and compliance owners must validate any design.

**Estimated reading time:** 7 minutes

## Five Takeaways

1. A voice workflow should model consent, disclosure, retention, access, and jurisdiction
   explicitly.
2. EPA Section 608 establishes certification and refrigerant-management obligations for
   covered work. [1]
3. PCI DSS is a baseline of technical and operational requirements for payment-account
   data security. [2]
4. The California DOJ describes CCPA rights including know, delete, opt out, correct, and
   limit rights for covered consumers. [3]
5. This chapter makes no universal conclusion about recording, calling, texting, or state
   law because the verified source set is incomplete.

## Engineering Inputs

Before a call is recorded, transcribed, summarized, retained, or transferred, the system
needs an applicable policy. The policy may depend on jurisdiction, caller, channel,
purpose, notice, consent, and contract. The voice agent should not improvise a legal
disclosure or claim that a requirement is satisfied.

For payments, the simplest design is to avoid collecting card data in free-form model
context. PCI SSC says PCI DSS protects payment account data and applies to entities that
store, process, transmit, or could affect the security of the cardholder-data
environment. [2] Scope and validation must be determined by the responsible compliance
program.

For privacy, the California DOJ describes consumer rights and business responsibilities
under the CCPA. [3] A system handling caller data should support purpose limitation,
access controls, deletion or retention exceptions, correction workflows, and auditable
request handling where applicable.

For HVAC and refrigeration workflows, EPA Section 608 prohibits intentional venting of
certain refrigerants and describes certification, recordkeeping, and reporting topics.
[1] A voice agent should route technical or compliance-sensitive questions to authorized
people and avoid presenting generic conversational guidance as a work authorization.

## Unverified Legal Areas

Recording consent, TCPA and outbound calling, A2P messaging, AI-voice treatment,
bot disclosure, accessibility, retention periods, and state-specific rules need a second
verification pass and legal review. They are not stated as conclusions here.

## Sources

1. U.S. EPA, Section 608: <https://www.epa.gov/section608>
2. PCI Security Standards Council, PCI DSS: <https://www.pcisecuritystandards.org/standards/pci-dss/>
3. California DOJ, CCPA: <https://oag.ca.gov/privacy/ccpa>
