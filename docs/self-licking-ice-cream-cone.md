# The Self-Licking Ice Cream Cone: History, Podcast, and Organizational Diagnostic

> **Purpose.** A source-grounded explainer and discussion aid for recognizing when an organization
> optimizes for preserving its own machinery instead of producing external value. The contemporary
> examples below are diagnostic patterns, not accusations about any named organization.

## Five takeaways

1. **The defining feature is circular justification.** The system's outputs justify the need for
   more of the system, while independent evidence of customer or mission value stays weak.
2. **The phrase is documented by 1991–1992, not securely attributable to a single first use.**
   Norman Friedman's 1991 *Desert Victory* and S. Pete Worden's 1992 paper are commonly cited.
3. **Worden's NASA example was a political-economy critique.** He argued that the Shuttle and
   Space Station architecture mutually reinforced cost, jobs, and congressional support. Treat
   the paper as a pointed contemporary critique, not as a neutral or complete history of NASA.
4. **Process is not automatically waste.** In safety-critical work, assurance, auditability, and
   coordination can be essential. The test is whether each control demonstrably reduces risk or
   improves outcomes enough to justify its cost.
5. **Break the loop with external outcome measures and real stop conditions.** Define the user,
   desired outcome, counter-metrics, decision owner, and kill/rollback criteria before adding more
   process or scaling a system.

## Historical grounding and caveats

S. Pete Worden's paper, “On Self-Licking Ice Cream Cones,” appeared in the *Astronomical Society of
the Pacific Conference Series*, volume 26 (1992), pp. 599–603. The paper is available via
[ResearchGate](https://www.researchgate.net/publication/234554226_On_Self-Licking_Ice_Cream_Cones)
and is catalogued under Bibcode [1992ASPC...26..599W](https://ui.adsabs.harvard.edu/abs/1992ASPC...26..599W/abstract).
The phrase is also commonly traced to Norman Friedman's 1991 book
[*Desert Victory: The War for Kuwait*](https://books.google.com/books?q=Norman+Friedman+Desert+Victory+The+War+for+Kuwait); therefore,
say it was **in circulation by 1991–1992** rather than confidently declaring Worden the sole inventor.

Worden's core example was the Space Shuttle–Space Station relationship. His argument was that the
Station's design depended on the Shuttle, while the Shuttle program was justified in part by the
Station; maintaining the linked architecture protected a large employment and congressional
constituency and made it difficult to redirect funding toward alternatives. The paper also criticized
the way congressional appropriations incentives could dominate NASA's program choices. The details
and figures in the paper reflect Worden's argument at the time and should be attributed to him, not
repeated as timeless facts.

Related language subsequently appeared in military and intelligence contexts. A U.S. Air Force
Academy professional-development article, for example, applies the metaphor to performance-rating
and physical-training processes that continue even when they fail to improve the people they are
supposed to develop ([PDF](https://www.usafa.af.mil/Portals/21/documents/10ABW/10ABW_Documents/DEC2017_Self-licking%20Ice%20Cream%20Cones.pdf?ver=2017-12-19-121225-727)).
A 2021 analysis of the Afghanistan war used the concept to discuss institutional incentives and
misleading progress metrics ([Responsible Statecraft](https://responsiblestatecraft.org/2021/10/04/how-the-self-licking-ice-cream-cone-prolonged-the-20-year-war/)).
These are applications of the metaphor, not proof that every large institution behaves this way.

The related “Iron Law of Bureaucracy” is often associated with Jerry Pournelle: in simplified form,
organizations can drift toward serving the interests of the people who control them rather than the
mission they were created to accomplish. It is a useful parallel, but not the same claim and not a
substitute for evidence.

### A careful diagnostic

A process or program is not a self-licking ice cream cone merely because it is expensive, slow, or
bureaucratic. Look for a **reinforcing loop**:

1. The organization creates a process, program, platform, committee, or metric.
2. The system produces artifacts that demonstrate its own activity (reports, approvals, dashboards,
   meetings, model outputs, tickets, or headcount).
3. Those artifacts are treated as evidence that the system is valuable and needs more resources.
4. External outcomes are weak, ambiguous, or never measured independently.
5. Criticism or termination is framed as a threat to the system, rather than as a normal response to
   evidence.

Ask whether the system would still be funded or operated if the outputs it generates were no longer
counted as success. Then ask what independent evidence would change the decision.

## Refined NotebookLM prompt

Use the prompt below with the source list. The key changes from a generic “bureaucracy is bad” prompt
are: distinguish documented history from interpretation; avoid asserting motives without evidence;
use contemporary examples as patterns unless sourced; and give the hosts a recurring test for external
value.

**Suggested sources for NotebookLM**

- Worden, S. Pete (1992), [“On Self-Licking Ice Cream Cones”](https://www.researchgate.net/publication/234554226_On_Self-Licking_Ice_Cream_Cones).
- Norman Friedman (1991), [*Desert Victory: The War for Kuwait*](https://books.google.com/books/about/Desert_Victory.html?id=).
- [U.S. Air Force Academy professional-development article (PDF)](https://www.usafa.af.mil/Portals/21/documents/10ABW/10ABW_Documents/DEC2017_Self-licking%20Ice%20Cream%20Cones.pdf?ver=2017-12-19-121225-727).
- [Responsible Statecraft: Afghanistan and institutional incentives](https://responsiblestatecraft.org/2021/10/04/how-the-self-licking-ice-cream-cone-prolonged-the-20-year-war/).
- [The New Yorker, “The Intelligence Gap” (1999)](https://www.newyorker.com/magazine/1999/12/06/the-intelligence-gap), for an example of the phrase in an intelligence-community critique.

**Copy/paste prompt**

Create a 12–18 minute, two-host conversational podcast titled “The Self-Licking Ice Cream Cone:
When Organizations Start Serving Themselves.” One host is historically minded and analytical; the
other focuses on practical modern examples. Let them sound curious and natural, with occasional
light humor, but do not imitate any specific existing podcast or host.

Audience: smart general listeners. Define the phrase as a system whose activity and continued
existence become its own justification, displacing its original mission or external customer value.
Use the ice-cream image to make the circular logic memorable.

Structure:
1. **Cold open (30–45 seconds):** a vivid analogy for a machine that manufactures proof of its own
   usefulness.
2. **Definition (2 minutes):** distinguish a self-perpetuating system from a merely large, expensive,
   regulated, or inefficient one.
3. **History (3–4 minutes):** explain that the phrase is documented by 1991–1992. Discuss Norman
   Friedman's 1991 *Desert Victory* and S. Pete Worden's 1992 paper, “On Self-Licking Ice Cream
   Cones” (ASP Conference Series 26, pp. 599–603). Attribute the Shuttle–Space Station argument to
   Worden: he argued the two programs were mutually reinforcing and that employment and congressional
   incentives made the architecture difficult to escape. Explain that this is a pointed critique, not
   a neutral full history. Mention later military/intelligence uses and the related, but distinct,
   Iron Law of Bureaucracy.
4. **Mechanism (2–3 minutes):** incentives, concentrated benefits and diffuse costs, sunk costs,
   risk aversion, proxy metrics, and the danger of rewarding visible activity instead of mission
   outcomes.
5. **Modern patterns (4–5 minutes):** cover government/defense, corporate initiatives, academia or
   nonprofits, and AI programs. Use sourced named examples only when the sources support the claims.
   Otherwise label scenarios as illustrative patterns, not allegations about named organizations.
   Discuss the human logic and the legitimate value the process may provide, as well as its costs.
6. **Counterexample and remedies (2 minutes):** contrast a tightly controlled, outcome-measured
   experiment with a process that scales its own bureaucracy. Discuss commercial space only with
   nuance: different contracting and iteration models can help, but do not imply that newer firms
   are free of subsidies, politics, safety constraints, or failure.
7. **Close (1 minute):** ask what evidence would show that a system should be stopped, simplified,
   or redesigned.

Keep the conversation balanced. Explain that controls can be essential in safety-critical systems.
Use a recurring diagnostic: Who benefits externally? What outcome changed? What evidence could
falsify the success story? What would make us stop? Do not invent quotations, dates, motives, or
statistics. If sources disagree or the historical origin is uncertain, say so. Distinguish documented
facts, the original author's argument, and the hosts' own interpretation. End reflectively, not with
forced optimism or cynicism.

## Full two-host podcast script

*Approximate runtime: 12–15 minutes at a conversational pace. This is an original script informed by
the sources above, not a verbatim transcript of any source.*

### Cold open: the machine that feeds itself

**HOST 1 — ANALYTICAL:** Imagine a machine that makes reports proving the machine is necessary. The
reports trigger a committee. The committee creates a task force. The task force produces a dashboard
showing how much work the committee and task force have completed. The dashboard is presented at a
review, and the review concludes that the machine needs more funding.

**HOST 2 — PRACTICAL:** And somewhere in the middle of all that, somebody asks, “Did we fix the
problem?” Everyone looks at the dashboard. The dashboard says 100 percent of the reports were
delivered on time.

**HOST 1:** Which is an answer to a different question.

**HOST 2:** Congratulations to the machine. It has achieved operational excellence at operating
itself.

**HOST 1:** That is the idea behind the wonderfully absurd phrase “self-licking ice cream cone.” A
system has become so good at sustaining itself that it no longer needs to demonstrate much value
outside its own boundaries.

### What the phrase means

**HOST 2:** The picture is ridiculous by design. An ice cream cone cannot lick itself. The thing that
should be the object of enjoyment becomes a little closed loop, consuming its own output.

**HOST 1:** In organizations, the loop is institutional. A department exists to solve a problem. It
creates processes, reports, software, governance, and roles to solve it. Over time, the processes
become the product. The department points to the activity as proof of importance, then uses that
importance to justify more activity.

**HOST 2:** But let's make a distinction before we start accusing every committee of being a dessert
with a budget. Some systems need a lot of process. Aviation safety, medical-device approval, nuclear
operations, and defense systems cannot be run on “move fast and hope.”

**HOST 1:** Exactly. Complexity isn't proof of dysfunction. The test is whether the machinery improves
the external result enough to justify its cost. A safety review that catches a catastrophic defect is
not waste. A review that exists because the last review requires another review, without reducing
risk or improving a decision, deserves scrutiny.

**HOST 2:** So we're not asking, “Is there paperwork?” We're asking, “What would be worse if this
paperwork disappeared?” And can anyone answer with evidence?

### The origin story: NASA, the Shuttle, and the Station

**HOST 1:** The phrase is in print by the early 1990s. Norman Friedman's 1991 book *Desert Victory:
The War for Kuwait* is often cited as an early appearance. Then in 1992, S. Pete Worden published a
paper called “On Self-Licking Ice Cream Cones” in the Astronomical Society of the Pacific Conference
Series.

**HOST 2:** Worden was making a pointed argument about NASA. His example was the relationship between
the Space Shuttle and the proposed Space Station. In his telling, the Station was designed around
being built by the Shuttle, while the Shuttle was defended in part as the vehicle needed to build the
Station.

**HOST 1:** That's the loop: each program helps justify the other. Worden argued that the combined
architecture also sustained a large network of jobs and political support. If employment and
contracts are distributed across congressional districts, then the benefits of continuing a program
are concentrated and visible, while the cost to taxpayers is spread broadly.

**HOST 2:** Which makes the politics asymmetric. The people who might lose a facility or contract know
exactly what they're losing. A taxpayer who might benefit from a cheaper alternative usually doesn't
have a lobbyist calling about it.

**HOST 1:** Worden also argued that the arrangement made it difficult to redirect resources toward a
more cost-effective launch system. We should be careful here: these are Worden's claims in a
particular historical debate, not a complete history of NASA or proof that every Shuttle or Station
decision was irrational.

**HOST 2:** And the phrase's exact first use isn't certain. The safe statement is that it was in
circulation by 1991–1992, with Worden's paper becoming an influential articulation of the concept.

**HOST 1:** The broader idea is older than the phrase. Bureaucracies can develop interests in budgets,
staffing, authority, and continuity. The related “Iron Law of Bureaucracy,” often associated with
Jerry Pournelle, captures a similar concern: people who control an organization can end up prioritizing
their own interests over its founding mission. They're related ideas, not interchangeable laws of
nature.

### Why the loop forms

**HOST 2:** How does a group of competent people end up building a system that seems to serve itself?
Nobody has to show up on Monday and announce, “Let's waste the next five years.”

**HOST 1:** Usually it begins with rational local decisions. A manager wants to avoid a failure. A
program lead wants stable funding. A regulator wants evidence. An engineer wants a clean interface.
A team creates a review to catch mistakes. Another review is added after an incident. A metric is
introduced because leadership needs visibility.

**HOST 2:** All reasonable in isolation.

**HOST 1:** Yes. But then the measures of success can drift. Instead of asking whether customers are
better served, the organization counts reviews completed, people trained, documents delivered, model
calls made, or projects launched. Those measures are easy to count and report. Actual outcomes may
take longer, be harder to attribute, or reveal uncomfortable trade-offs.

**HOST 2:** And once a metric is tied to funding or promotion, people naturally optimize for it. If
the dashboard rewards the number of issues closed, teams may close easy issues. If it rewards calls
handled, the system may rush callers. If it rewards the number of AI agents deployed, somebody will
find a way to deploy more agents.

**HOST 1:** Another force is sunk cost. “We've already spent five years and a billion dollars” sounds
like a reason to continue, even though the relevant question is whether the next dollar is better
spent continuing or switching. Past spending cannot be recovered. It should inform what we've learned,
not dictate the next decision.

**HOST 2:** And there is a social cost to stopping. People may lose jobs, status, influence, or a
career-defining project. Those are real human stakes. Understanding them is not the same as saying
they should determine whether the program works.

**HOST 1:** The most dangerous loops are self-sealing: failure creates the rationale for more of the
same. A project misses a milestone, so it gets another steering committee. The committee requests
more reporting. The reports show the project is now being managed more rigorously. But no one asks
whether the underlying approach should be abandoned.

### The modern versions

**HOST 2:** Let's take government and defense first. A program can begin with a legitimate national
security need. Then the budget, contractors, facilities, promotion paths, and political coalitions
become entangled with the chosen solution. Changing direction becomes harder than continuing.

**HOST 1:** Defense also illustrates why the diagnosis must be evidence-based. Long development cycles,
redundancy, testing, and rigorous configuration control can be essential when failure is dangerous.
The warning sign isn't that a program is expensive or has delays. It's when continued funding is
justified mainly by the number of jobs at stake, the amount already spent, or activity metrics that
do not establish capability or mission impact.

**HOST 2:** A corporate version is the endless initiative cycle. A company announces a transformation,
forms a central office, appoints workstream leads, and launches a dashboard. Six months later, the
dashboard is green because every workstream submitted its deliverable. But the customer journey is no
better, the sales cycle hasn't shortened, and employees have added three recurring meetings.

**HOST 1:** There may be good reasons for the initiative. The problem is using completion of the
initiative's machinery as a proxy for its objective. “We rolled out the new workflow” is not the same
as “the workflow reduced errors or helped customers finish faster.”

**HOST 2:** Academia and nonprofits can face the same pressure. A grant funds a program, the program
creates reports to demonstrate impact, and the reports become the evidence used to win the next
grant. Measurement is necessary. But if the organization chooses metrics primarily because they are
easy to report, it may reward what can be counted rather than what matters.

**HOST 1:** AI is especially vulnerable because the activity is so legible. You can count agents,
tools, tokens, evaluations, prototypes, and demos. You can publish an impressive architecture diagram.
But the business question is still: did a real workflow get more reliable, faster, safer, or less
expensive? Did a person get a better outcome?

**HOST 2:** Imagine a team deploying five agents to handle a scheduling call. One classifies intent,
one retrieves customer context, one checks availability, one proposes a slot, and one summarizes the
interaction. That architecture might be justified. Or it might be five services and four handoffs
wrapped around a deterministic task that one well-designed workflow could handle.

**HOST 1:** The number of agents is not the measure of success. Neither is the elegance of the
orchestration graph. The measure is whether the architecture improves end-to-end performance under
realistic conditions, including failures, uncertainty, latency, cost, and recovery.

**HOST 2:** And if an evaluation suite becomes the goal, it can become a cone too. A team optimizes
for its benchmark, the benchmark stops representing production, and the score improves while users
continue to struggle. The fix isn't to stop evaluating. It's to keep holdout cases, examine failures,
and test outcomes independently of the system that claims success.

### Different operating systems, different outcomes

**HOST 1:** This is why two teams with similarly talented people and similar resources can produce
dramatically different results. One team's operating system rewards evidence, candid disagreement,
small experiments, and stopping work that isn't paying off. Another rewards visible activity,
predictable narratives, and avoiding bad news.

**HOST 2:** Commercial space is often used as a contrast with traditional aerospace. Some newer
approaches emphasize iterative development, integrated teams, and repeated tests. Those methods can
shorten feedback loops. But the fair comparison isn't “old companies bad, new companies good.” New
entrants still operate within public policy, infrastructure, safety, and capital constraints; they
also have failures. Different programs have different mission and risk requirements.

**HOST 1:** The useful question is: how quickly does evidence change the plan? Can a team run a bounded
test, learn something meaningful, and revise the design? Does it have permission to retire an
approach that isn't working? Can leadership tell the difference between an honest failed experiment
and a program that has learned to hide failure?

**HOST 2:** A healthy process should make it easier to stop, not harder. If a governance mechanism
never produces a “no,” a rollback, a scope reduction, or a decision to simplify, ask what decisions
it is actually governing.

### A practical test

**HOST 1:** Here's a short test you can apply to a program, department, or AI initiative. First:
who is the external beneficiary? Name the person, customer, operator, or mission that should be better
off.

**HOST 2:** Second: what observable outcome should change? Not “more visibility,” unless visibility
is explicitly the outcome. Something like fewer incorrect bookings, lower time to resolve a call,
fewer safety incidents, or a decision made with better evidence.

**HOST 1:** Third: what would count as evidence that the program is not working? If no result could
change the team's view, the success claim isn't falsifiable.

**HOST 2:** Fourth: what would make us stop, simplify, or redesign it? A threshold, a date, a
comparison against a baseline, or a review by someone who doesn't own the program.

**HOST 1:** And fifth: do the measures create incentives to game them? Pair the headline metric with
counter-metrics. If you improve speed, check correctness and customer satisfaction. If you improve
automation, check escalation quality and the cost of errors. If you increase coverage, check whether
the new coverage solves meaningful cases.

**HOST 2:** There is also a human question. Can people tell the truth about a failure without
destroying their standing? When bad news is punished, the organization will eventually be rich in
green dashboards and poor in reality.

### Closing

**HOST 1:** The self-licking ice cream cone isn't fundamentally a story about stupid people. It's a
story about incentives and feedback. Smart, conscientious people can maintain a system that no longer
serves its original purpose if the system rewards them for maintaining it.

**HOST 2:** And the solution isn't to eliminate process. It's to reconnect process to outcomes. Keep
the controls that catch real risks. Remove the ones that only create artifacts. Fund the work that
helps the customer or mission. Give teams a way to learn—and a way to stop.

**HOST 1:** So next time you see a busy organization producing an impressive amount of evidence about
its own activity, ask one simple question: if all that activity disappeared tomorrow, what external
outcome would get worse?

**HOST 2:** If the answer is clear, the process may be doing important work. If nobody can answer,
you may have found the cone.

## Application to a voice-agent / AI product team

This section translates the metaphor into a neutral engineering diagnostic. It is a learning framework,
not a claim about any particular company's internal operations.

### The likely failure loop

1. A business identifies a real customer problem, such as missed inbound calls or avoidable booking
   friction.
2. The team creates agents, orchestration, dashboards, evals, governance, and rollout processes.
3. The team begins reporting outputs it directly controls: agents launched, intents covered, tool calls,
   prompts reviewed, evals passed, or calls processed.
4. Those outputs become the headline evidence for investment.
5. Harder questions—booking correctness, caller trust, recovery from bad data, incremental value,
   and total cost—receive less attention because they are harder to measure.
6. Weak outcomes lead to more agents, prompts, dashboards, or committees instead of reconsidering the
   architecture or product hypothesis.

This is a failure mode to guard against, not a prediction that it will happen.

### A healthier operating model

| Layer | Better question | Example evidence |
|---|---|---|
| Customer outcome | Did the caller's task get completed correctly? | Authoritative booking state; correct service type, time, address, and caller intent |
| Trust and safety | Did the agent avoid unsupported claims and unsafe actions? | False-confirmation rate; authorization failures; appropriate handoff/defer rate |
| Reliability | Did the system recover from realistic faults? | Tool timeout recovery, idempotent retries, stale-state handling, graceful escalation |
| Experience | Did the interaction work for people? | Turn-taking, interruption recovery, repeat rate, caller abandonment, reviewed call quality |
| Economics | Is the result worth its cost? | Cost per successfully completed task, human follow-up cost, incremental booking value |
| Delivery system | Does each process improve the above? | Decision latency, escaped defects, review yield, rework, time from failure discovery to fix |

Do not collapse these into one score too early. A system can improve booking rate while degrading trust, or lower latency while increasing incorrect actions. Use guardrails and segmented analysis.

### Example: the AC-not-cooling playbook

Suppose a fictional AI-assisted workflow helps a contractor respond to a caller whose air conditioner is not cooling.

A self-referential success metric might be: “We created 40 diagnostic steps, deployed three agents, and achieved 98% completion on the internal checklist.” Those numbers say little about whether the workflow helps the technician or homeowner.

A better evaluation asks whether the playbook captures the right symptom and urgency, avoids presenting uncertain diagnosis as fact, collects the information the technician actually needs, and hands off when the issue is unsafe or outside scope. Evidence could include a structured technician-feedback record, adjudicated missing-step labels, downstream rework, safety-related omissions, and field validation against a reviewed reference set.

A feedback record should separate observation from proposed change:

- **Observed issue:** Missing diagnostic step.
- **Source:** Technician feedback, call/visit identifier pseudonymized in the approved system, playbook version, and timestamp.
- **Evidence:** What step was missing, what the technician needed, and what downstream consequence occurred. Do not invent these details when none were supplied.
- **Proposal:** Candidate step, insertion point, prerequisites, and expected benefit.
- **Evaluation:** Replay on a frozen regression set; check for false confidence, unsafe instructions, redundant steps, and regressions on adjacent scenarios.
- **Approval:** Domain expert and product/safety owner review; versioned release; canary; rollback threshold.
- **Outcome:** Whether the change improved the targeted result and whether any counter-metric worsened.

If technician feedback says “missing diagnostic step” but provides no actual details, the correct state is **insufficient evidence to author a specific step**. Request the missing context rather than fabricate a plausible HVAC procedure. The feedback pipeline must not reward itself for turning every comment into a shipped change.

### Five questions for design reviews

1. What external user or operational outcome is this component supposed to improve?
2. What is the simplest baseline we are comparing against?
3. Which failure modes and counter-metrics could make the headline metric misleading?
4. What evidence would cause us to remove a component, narrow its autonomy, or stop the rollout?
5. Who independent of the component owner reviews the evidence, and where is the decision recorded?

**Bottom line:** model proposes; the application harness controls; evaluations test whether the system helps; authorized owners decide whether it should ship. The goal is not to maximize process, agent count, or evaluation volume. The goal is reliable external value with evidence strong enough to justify the complexity.
