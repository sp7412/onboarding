# How A Contractor Works

This is a simplified, fictional workflow for learning. Individual contractors differ
by trade, geography, staffing, pricing, and operating policy.

## The Job Lifecycle

1. **Demand arrives.** A customer calls, submits a web request, or responds to a
   reminder. The office needs enough information to identify the customer and classify
   the request.
2. **Triage happens.** The office determines the trade, urgency, service area, and
   whether the request is safe for routine scheduling. A gas smell, fire, flooding, or
   another hazard may require immediate safety guidance and escalation.
3. **The job is booked.** The scheduler offers eligible windows. The customer confirms
   the address and a window. The system creates one job, safely handling retries.
4. **The job is dispatched.** An office team assigns work based on availability,
   geography, skills, and operating policy. The technician receives the job details.
5. **The visit occurs.** The technician diagnoses the issue, performs authorized work,
   and may prepare an estimate for additional work.
6. **The job is completed.** The business records labor/materials, presents the invoice,
   and collects payment according to its policy.
7. **The relationship continues.** A customer may join or renew a maintenance
   membership, receive reminders, or call again for a related issue.

## Where A Voice Agent Fits

The voice agent is most useful at the front door: answering, identifying, gathering
structured facts, booking eligible work, and transferring calls it should not handle.
It should not become the system of record for customers, schedules, prices, jobs, or
payments. Those actions belong behind authenticated tools and application policy.

```mermaid
flowchart TD
    A[Inbound call] --> B[Identify caller and address]
    B --> C{Safe and in scope?}
    C -- no --> D[Safety guidance or human transfer]
    C -- yes --> E[Triage trade and job type]
    E --> F[Find eligible windows]
    F --> G[Read back address and window]
    G --> H{Explicit confirmation?}
    H -- no --> D
    H -- yes --> I[Create idempotent job]
    I --> J[Dispatch technician]
    J --> K[Visit, estimate, work]
    K --> L[Invoice and payment]
    L --> M[Membership or follow-up]
    style A fill:#e7f0ff
    style D fill:#ffe8e8
    style I fill:#e8f7ed
```

## Trade-Specific Lifecycles

The generic lifecycle above is the shared primer. Real work diverges after triage:
trade-specific questions affect urgency, technician qualifications, diagnostic work,
authorization, parts, and what counts as a verified completion. These examples are
fictional and intentionally omit contractor-specific pricing and policies.

### HVAC: service, repair, and replacement

An HVAC call may be a no-cooling/no-heating complaint, an unusual noise, a seasonal
maintenance visit, or a request to replace aging equipment. For a breakdown, the
technician typically diagnoses the system before the customer approves repairs or
replacement. A replacement adds sizing, installation, commissioning, and warranty steps;
a maintenance visit follows a checklist and may create a separately authorized repair
recommendation.

```mermaid
flowchart TD
    A[Customer reports no cooling or heating] --> B[Confirm address, system type, and symptoms]
    B --> C{Immediate hazard?}
    C -- yes --> D[Give safety guidance and escalate]
    C -- no --> E[Book diagnostic visit]
    E --> F[Dispatch HVAC technician]
    F --> G[Inspect system and diagnose]
    G --> H{Repair feasible and authorized?}
    H -- yes --> I[Repair and verify operation]
    H -- no --> J[Present options and estimate]
    J --> K{Customer approves?}
    K -- no --> L[Document decision and schedule follow-up]
    K -- yes --> M[Repair or replace, then commission]
    I --> N[Invoice, warranty, and maintenance follow-up]
    M --> N
    style D fill:#ffe8e8
    style I fill:#e8f7ed
    style M fill:#e7f0ff
```

**Important completion checks:** verify heating/cooling operation, record findings and
parts, distinguish completed repairs from recommended work, and capture warranty or
maintenance follow-up. Replacing equipment generally needs more planning than a routine
diagnostic or repair appointment.

### Plumbing: urgent repair, drain, fixture, and water-heater work

Plumbing intake must distinguish an active leak or flooding from a routine clog, fixture
installation, or water-heater issue. The affected location, whether water can be shut
off, access constraints, and the job's scope influence urgency and who should be sent.
A larger repair may require explicit approval, a return visit, or a qualified specialist.

```mermaid
flowchart TD
    A[Leak, clog, fixture, or water-heater request] --> B[Confirm location, symptoms, and affected fixtures]
    B --> C{Active flooding or safety hazard?}
    C -- yes --> D[Give immediate safety or shutoff guidance and escalate]
    C -- no --> E[Book by urgency and required skill]
    E --> F[Dispatch qualified plumber]
    F --> G[Inspect, locate cause, and assess access]
    G --> H{Repair within scope and approved?}
    H -- yes --> I[Repair or clear blockage]
    H -- no --> J[Explain options and estimate]
    J --> K{Customer authorizes work?}
    K -- no --> L[Record decision and next steps]
    K -- yes --> M[Repair, replace, or arrange specialist]
    I --> N[Test for leaks, flow, and safe operation]
    M --> N
    N --> O[Invoice, cleanup, warranty, and follow-up]
    style D fill:#ffe8e8
    style I fill:#e8f7ed
    style M fill:#e7f0ff
```

**Important completion checks:** test the repaired fixture or line, verify leaks have
stopped and flow is restored, document any remaining limitations, and leave the work
area safe. An emergency response may stabilize the situation first and defer permanent
repair until the customer approves the scope.

## Engineering Questions At Each Boundary

| Boundary | Questions |
|---|---|
| Call to identity | What is authoritative: caller ID, account lookup, or caller-provided information? |
| Triage to safety | Which signals require immediate escalation, and how are false negatives reviewed? |
| Availability to booking | Is the slot still available at commit time? What is the idempotency key? |
| Booking to dispatch | Which facts are required by the field team, and what may be edited later? |
| Visit to invoice | Which decisions are technician-owned, office-owned, or policy-controlled? |
| Completion to retention | Which follow-up is useful, consented, and measurable? |

The fictional backend in `labs/stlab/backend.py` intentionally stops at customers,
slots, and jobs.
