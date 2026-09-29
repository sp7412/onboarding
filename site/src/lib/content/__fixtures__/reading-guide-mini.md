# Reading Guide: ranked by priority

A curated list, ranked in the order to consume them.

- **Tier 1** (before day 1, must-do): the business, and the core mental models
- **Tier 2** (before day 1 if possible): the stack in depth

---

## Tier 1: Must-do before day 1

### 1. Example AI Voice Agent product page
- [ ] <https://example.com/features/virtual-agent> · product page · 15 min
- **Why:** this is the product you're joining. Read it as a spec of what customers
were promised.
- **Look for:**
  1. Booking is driven by capacity rules, so the agent is a front end to scheduling logic.
  2. There's an explicit escalation path to a live CSR.
  3. It works with Contact Center Pro or third-party phone systems.
  4. Customers review recordings and metrics, so there's a quality loop.
- **Pairs with:** lab 02 (tools and guardrails)

### 2. Example webinar recap
- [ ] <https://example.com/blog/webinar-recap> · blog · 15 min
- **Why:** more detail on the feature set and configuration knobs.
- **Look for:**
  1. The call types handled beyond booking.
  2. Membership awareness.
  3. Policy living in configuration, not in the prompt.
  4. Which phone systems are supported.
- **Pairs with:** lab 00 (mock backend), lab 06 (workflow)

## Tier 2: The stack in depth (before day 1 if possible)

### Official documentation quick reference

Use these official pages for API behavior and pair them with the labs.

| Read | Why | Time | Pair with |
|---|---|---:|---|
| [Realtime overview](https://example.com/realtime) | Session model, audio turns, streaming, and tool calling | 30 min | Lab 01 |
| [Turn handling](https://example.com/turns) | VAD, endpointing, interruptions, and semantic detection | 25 min | Lab 03 |

### 9. Building Effective Agents
- [ ] <https://example.com/effective-agents> · essay · 30 min
- **Why:** the clearest framework for how much agency to give an LLM.
- **Look for:**
  1. Workflows versus agents.
  2. Start simple.
  3. The patterns and which ones a booking call needs.
  4. Tool design as an engineered interface.
- **Pairs with:** labs 05 and 06

## Tier 3: First 30 days

### 15. A Field Guide to Rapidly Improving AI Products
- [ ] <https://example.com/field-guide> · blog · 45 min
- **Why:** error analysis as the core loop.

## Tier 4: As needed

### 26. A speech-text foundation model
- [ ] <https://example.com/moshi> · paper · 1 h
- **Why:** background on full-duplex speech models.
