# Obsidian as a personal knowledge base, with Grok Bot as a maintainer

This guide describes a practical way to preserve useful knowledge from ChatGPT conversations, the ServiceTitan onboarding study repository, research, project notes, and other approved sources. Obsidian is the human-facing interface; ordinary Markdown files are the durable data layer; Git provides history and rollback; an LLM helps retrieve, summarize, link, and propose updates.

The goal is not to copy every conversation into a giant prompt or to let an agent silently rewrite everything. The goal is a searchable, source-linked knowledge base that remains useful without any particular AI provider.

## Recommended architecture

- **Original sources:** ChatGPT data export, GitHub repositories and pull requests, documents, notes, and public references. Keep originals or stable source links.
- **Obsidian vault:** a local folder of Markdown notes, attachments, and links. It is readable without Obsidian and can be edited by ordinary tools.
- **Curated knowledge:** concise project summaries, decisions, concepts, research notes, and open questions that link back to source evidence.
- **LLM assistant:** retrieves relevant notes, drafts summaries, identifies stale information, and proposes diffs. It is not the authority for facts.
- **Git and backup:** track changes and allow recovery. Do not treat Git as the only backup if the vault contains important personal material.
- **Optional semantic search:** add an embedding/RAG layer only when ordinary Obsidian search and links stop being sufficient.

Keep the published onboarding repository separate from the broader personal vault. The repository is a public-safe, reviewed deliverable; the vault can contain private personal knowledge. Do not sync private notes into a public repository.

## Why Obsidian

Obsidian stores notes as local Markdown files with internal links and backlinks. That makes it a good long-lived knowledge layer: notes can be inspected, searched, versioned, moved, and used by other tools without a proprietary database export.

Use Obsidian for browsing and human curation, not as a requirement for every automation. The underlying vault folder is the interface that matters. Start with built-in search, links, tags, and properties. Add community plugins only when a specific need justifies their maintenance and security cost.

## A starter vault structure

Create a new vault named Personal Knowledge. Start small:

- 00 Inbox — unprocessed conversation extracts, reading notes, and candidate updates.
- 10 Projects — one note or folder per project, with current status, key links, risks, and next steps.
- 20 Knowledge — durable concepts such as voice-agent architecture, evaluation, computer vision, software engineering, and personal workflows.
- 30 Decisions — decisions with date, context, evidence, rationale, status, and superseding decision.
- 40 Sources — source records and bibliographic notes; prefer links over duplicating entire source documents.
- 50 Reviews — periodic summaries, audits, and maintenance reports.
- 90 System — templates, vault conventions, and the home index.
- Attachments — images, PDFs, and other files that genuinely need to be stored locally.

Create a Home note that links to active projects, recent decisions, unresolved questions, and the inbox. Avoid elaborate folder taxonomies until repeated use shows where the boundaries should be.

## Separate raw archive from curated knowledge

Use two layers:

1. **Archive:** original ChatGPT export, downloaded repository snapshot, original files, or source URLs. Preserve provenance and do not rewrite originals during summarization.
2. **Curated vault:** short notes that answer recurring questions, capture durable decisions, and link to the archive or canonical source.

A raw conversation is evidence that a topic was discussed; it is not automatically proof that every claim in it is correct. Mark AI-generated summaries as proposed until checked. If two sources conflict, preserve the disagreement and point to the newer or more authoritative source rather than silently choosing one.

For ChatGPT, use the account's data-export flow to obtain an archive. Keep the export outside the curated notes, then selectively extract useful conversations. Exporting is an archive operation, not a way to recreate those conversations as live ChatGPT chats. Do not ingest everything before deciding what should be retained and where it may be stored.

For the onboarding guide, start with the GitHub repository's Markdown, notebooks, diagrams, and source links. Preserve the repository URL, path, branch or commit, and pull-request link where relevant. A ZIP is convenient for a snapshot; a Git clone is better for ongoing change tracking. Neither contains all conversation history or every PR discussion unless those are captured separately.

## Slack and email ingestion are core requirements

Treat Slack and email as first-class inputs, not as an afterthought. They often contain the rationale behind decisions, commitments, corrections, project history, and links to the canonical work. The aim is to make that material findable from Obsidian without turning the vault into an unstructured dump of every message.

Use a **two-layer ingestion design**:

1. **Preserved source archive:** retain authorized exports or source-system records in a restricted archive location, with the original structure intact. Keep large exports and attachments out of the curated vault unless there is a concrete reason to store them there.
2. **Obsidian knowledge layer:** create concise Markdown notes for meaningful threads, decisions, meetings, project updates, and action candidates. Include stable links back to the original Slack message/thread or email, where available.

### Slack: preserve the thread, not just the one message

For a Slack capture, include the original message and enough surrounding thread context to understand what it responds to. Preserve, where available:

- Workspace/team, channel, message timestamp, author, and stable permalink.
- Thread/reply relationships and relevant parent message.
- Message timestamps and edit/deletion indicators when the source exposes them.
- Referenced files, documents, pull requests, and follow-up messages as links.
- Export or ingestion batch identifier and capture timestamp.

A channel export may not preserve the same navigable permalink behavior as live Slack, and a connector may only expose conversations the authorized account can access. Test the actual output rather than assuming an export contains every private channel, DM, file, or historical message. Use an approved export or scoped connector; do not bypass workspace permissions.

### Email: preserve message identity and conversation context

For an email capture, retain enough metadata to distinguish messages and reconstruct the conversation:

- From, To, Cc, sent timestamp, subject, and mailbox/folder where available.
- Message-ID and In-Reply-To/References headers when available.
- A stable source URL or connector reference if the provider supports one.
- Attachment names and links or archive paths; do not silently discard attachment context.
- Whether the message is inbound, sent, forwarded, or part of a larger thread.

Email exports may not contain working web links back to the mailbox. When no stable source link exists, store the export filename/path and message identifier so the original can still be found. Keep attachments in the preserved archive or a controlled attachment folder and link to them from the note.

### Normalize both sources into a shared record

Use one schema across Slack and email so search and review can work consistently. Example frontmatter:

```yaml
---
type: correspondence
source_system: slack # or email
source_id: "provider message/thread identifier"
source_url: "canonical permalink when available"
project: []
participants: []
sent_at: "YYYY-MM-DDTHH:MM:SSZ"
captured_at: "YYYY-MM-DDTHH:MM:SSZ"
ingestion_batch: "YYYY-MM-DD-source-name"
status: captured # captured, reviewed, promoted, superseded
sensitivity: review # public, personal, work-restricted, review
---
```

Use only metadata the source actually supplies. The example values are placeholders, not facts. Do not place secrets, sensitive personal data, or restricted employer/customer information in a personal vault. If classification is uncertain, quarantine the item and ask before processing it further.

### What should become a durable note?

Do not make a permanent standalone note for every message by default. Instead:

- Preserve the source record in the archive.
- Create a short thread/conversation note when the exchange contains meaningful context, a decision, a commitment, or useful technical reasoning.
- Promote durable decisions into `30 Decisions/` and link the evidence note.
- Put candidate follow-ups in `00 Inbox/` with an explicit proposed status; do not treat extracted actions as approved commitments.
- Update a project summary only when the evidence materially changes project status, scope, risks, or next steps.
- Keep opinions, hypotheses, and confirmed decisions clearly distinct.

### Incremental ingestion, deduplication, and corrections

Prefer incremental sync or date-bounded export batches after the initial import. Track a source identifier plus a content hash or equivalent deduplication key so reruns do not create duplicate notes. Record the last successful sync watermark, the time range checked, and any permission or API failures. A failed run must be reported as incomplete; it must not be interpreted as "no new messages."

Edits and deletions need an explicit policy. If a source message changes, update the captured record with provenance and retain an audit trail where appropriate. If a source is deleted, do not automatically erase derived notes without considering retention requirements and the reason for deletion; flag affected notes for review. Respect provider retention, organization policy, legal holds, and user deletion requests.

## Scheduled Slack and email ingestion with Grok Bot Routines

For recurring capture, prefer a supported Grok Bot cloud **Routine** over building a second scheduler, provided Routines are available in the account and can access the required sources and destination. A schedule only initiates work; it does not itself guarantee complete source coverage, persistent state, or access to a local Obsidian vault. Verify the actual account capabilities and run history before relying on it. See the official [Grok Bot overview](https://docs.x.ai/grok-bot/overview), [connectors and apps](https://docs.x.ai/grok-bot/computer-and-apps), [files and results](https://docs.x.ai/grok-bot/files-and-results), and [security and approvals](https://docs.x.ai/grok-bot/approvals-security-and-privacy) documentation.

### Suggested first schedule

Start with one daily run at **9:00 PM America/Chicago**, then adjust frequency once the pilot proves reliable. Run against one authorized Slack channel and one mailbox/folder before broadening scope. Keep the schedule, timezone, source scope, destination, and last successful run visible in the runbook.

### Routine contract

Use this as a starting instruction for the scheduled Routine; adapt it to the actual connected apps and available file tools:

> Every day at 9:00 PM America/Chicago, synchronize newly available, authorized Slack and email correspondence into my Obsidian knowledge base.
>
> 1. Read only the explicitly approved channels and mailboxes. Report source access or history limitations; do not imply complete coverage unless verified.
> 2. Retrieve changes since the last successful checkpoint, with a small overlap window where supported to avoid gaps. Preserve stable source IDs, timestamps, authors/recipients, thread context, permalinks, and attachment references where available.
> 3. Deduplicate by stable source ID and content hash. Make reruns safe. Detect edits and handle deletions only to the extent supported by the source; preserve an audit trail and flag derived notes for review when needed.
> 4. Separate preserved source evidence from curated notes. Extract meaningful decisions, project updates, unresolved questions, and candidate actions. Label candidate actions as proposed, not confirmed commitments, unless the source explicitly confirms them.
> 5. Link each material claim to source evidence. Update existing notes instead of generating duplicates. Do not invent missing metadata.
> 6. Do not send messages, modify source correspondence, delete source records, publish notes, or push changes. Do not overwrite existing knowledge notes without validating and reporting the diff.
> 7. If a source or destination is unavailable, stop the affected write path and report the run as incomplete. Never treat a failed source query as proof that no new items exist.
> 8. Record the run timestamp, sources checked, time range, items read/changed/skipped, notes proposed or written, errors, and checkpoint status. Preserve enough state to retry safely.
> 9. Quarantine uncertain classifications and exclude restricted employer/customer information from a personal vault unless retention and storage are explicitly authorized.
>
> Begin in dry-run mode: show proposed notes and diffs without applying changes. After review, enable writes only to the approved vault location and low-risk destinations.

### Verify before enabling unattended writes

- Confirm the Routine actually saved the intended schedule and timezone, and inspect its execution history after a test run.
- Confirm whether it runs in a cloud workspace or on a machine with access to the vault. A local-only vault is not automatically visible to a cloud Routine; use only a supported, approved sync or filesystem bridge.
- Confirm the connected Slack and email accounts expose the required history, threads, metadata, and attachment references.
- Run the same sample twice and verify that the second run creates no duplicates.
- Simulate an inaccessible source and a failed write; both must be reported as incomplete, not successful empty runs.
- Review sensitive-data handling, diffs, and restore behavior before permitting unattended writes.

Treat scheduled automation as a staged rollout: **dry run → reviewed writes → limited unattended writes → broader coverage**. Keep destructive actions, decisions with material consequences, and external side effects behind explicit approval.

### A safe pilot for both sources

1. Choose one low-risk Slack channel and one mailbox/folder you are authorized to process.
2. Export or retrieve a small, date-bounded sample, including a multi-message Slack thread and a multi-message email conversation.
3. Verify author/recipient, timestamps, thread relationships, attachments, links, and source IDs against the original systems.
4. Run ingestion twice and confirm it does not create duplicates.
5. Confirm that restricted channels, unrelated mailboxes, and inaccessible records are not pulled in.
6. Review the generated notes for correct summaries, explicit uncertainty, source links, and false action items.
7. Only then expand scope or schedule recurring ingestion.

A practical first milestone is **reliable, repeatable export and traceability**, not full automation. A second milestone can add scheduled incremental ingestion once permissions, coverage, deduplication, and recovery behavior have been tested.

## Note conventions and provenance

Use a small, consistent metadata set. For example, a project note can begin with:

- type: project
- status: active
- created: YYYY-MM-DD
- updated: YYYY-MM-DD
- source: canonical URL or file path
- confidence: verified, supported, or unverified

For decisions, record the decision statement, date, decision owner only when known, rationale, evidence links, status, and what it supersedes. For research, distinguish direct source claims from interpretation and recommendations. Use explicit status labels such as draft, reviewed, verified, and superseded.

Every important factual claim should be traceable to a source. Include stable URLs, repository paths, commit SHAs, PR numbers, timestamps, or page references where available. Do not invent missing metadata. A note without a reliable source should say so.

Prefer links between notes over repeated copies. If a decision changes, update the decision record and link the older record as superseded instead of deleting the history.

## What Grok Bot can and cannot do

Grok Bot may help maintain the vault, but it will not automatically keep a local Obsidian vault current merely because you created one. First determine where the Bot runs and which file operations and connectors are actually available in your account.

- **Cloud workspace only:** the Bot can work with files in its own workspace and return downloadable Markdown. The local vault is a separate location; you must import the output or use a supported bridge.
- **Approved connected drive or sync bridge:** the Bot may be able to work with a shared folder, depending on the supported connector, permissions, and sync behavior. Test a small round trip before relying on it.
- **Local filesystem access:** if a trusted local agent can access the vault directory, it may propose or apply changes locally. Give it access only to the intended folder and retain version history.
- **Scheduled routines:** a scheduled task is not the same as continuous monitoring. It needs an actual trigger, source access, and permission to read the changed material. Verify the last-run time and sources checked.

Treat product capabilities and UI labels as changeable. Confirm current behavior in the official [Grok Bot documentation](https://docs.x.ai/grok-bot/overview), especially its [connectors and apps](https://docs.x.ai/grok-bot/computer-and-apps), [files and results](https://docs.x.ai/grok-bot/files-and-results), and [security and approvals](https://docs.x.ai/grok-bot/approvals-security-and-privacy) pages.

Do not assume that a cloud Bot can read local files, that a connector can monitor every event, or that a routine has fresh data. If the source cannot be checked, the Bot should report that limitation instead of treating missing data as an empty result.

## A staged maintenance workflow

### Stage 1 — Create and verify the vault

1. Install Obsidian and create the Personal Knowledge vault in a stable local folder.
2. Create the starter folders and Home note.
3. Put a few manually written notes in the vault and link them to each other.
4. Confirm that the files exist as ordinary Markdown and that a backup can restore them.
5. Keep confidential employer information, credentials, customer data, and restricted recordings out of a personal vault unless explicitly authorized by policy.

### Stage 2 — Import one bounded source

Use the onboarding repository as the first pilot because it already has a clear source of truth and public-safe documentation. Add a project note linking to the repository, the deployed guide, important chapters, and relevant PRs. Import only the Markdown and supporting assets you actually want searchable; do not blindly duplicate the whole repository into the vault if links are enough.

Then test one ChatGPT export subset or a handful of conversation notes. Preserve original export files separately. Include the conversation title/date and a source reference when available.

### Stage 3 — Ask the LLM to propose, not silently mutate

Use a prompt like this:

> Review only the files and sources I explicitly provide. Identify durable facts, decisions, project changes, unresolved questions, and links that would improve the knowledge base.
>
> For each proposed change, provide the target note, the source evidence, why the change is useful, and a unified diff or complete replacement text. Distinguish source facts from interpretation and recommendation. Do not invent dates, owners, URLs, or confidence. Do not delete or merge existing notes. Do not change verified decisions without showing the conflicting evidence. Do not publish or push changes.
>
> Return a short report of sources inspected, sources unavailable, proposed changes, possible conflicts, and items needing my review.

Review the output and apply only useful changes. The first success criterion is a correct, source-linked note—not automation.

### Stage 4 — Add change detection

After manual curation is dependable, define specific sources and events that should trigger a review:

- A pull request merges or a key repository document changes.
- A project decision is explicitly recorded in a conversation or meeting note.
- A new approved document or transcript is added to a monitored folder.
- A scheduled audit finds broken links, stale project summaries, duplicate notes, or conflicting decisions.

For GitHub changes, capture the repository, commit, file paths, PR number, merge date, and links. Ask the LLM which notes may be affected and produce proposed diffs. A merged PR should trigger review of related notes, not an automatic claim that every PR statement is a permanent fact.

For ChatGPT, an export is usually a snapshot rather than a live event stream. Until an authorized integration exists, treat new exports or manually selected conversation notes as explicit ingestion batches. Do not describe this as continuous synchronization.

### Stage 5 — Validate and version every write

Before changes become durable:

1. Check that each source URL resolves and points to the intended material.
2. Check internal Obsidian links and required metadata.
3. Confirm that a proposed update does not erase a prior decision or contradict a more authoritative source.
4. Review the diff for unexpected changes and sensitive content.
5. Commit the reviewed change to Git, or use another versioned backup method.
6. Record the commit or change identifier in the maintenance report.

Start with read-only analysis and approval-gated writes. Only consider automatic writes to low-risk index or status files after repeated successful tests. Keep deletion, decision changes, publishing, and external actions behind explicit approval.

## When to add semantic search or RAG

Do not begin with a vector database. First try Obsidian search, tags, backlinks, and a well-maintained Home/index note. Add a retrieval layer when a concrete test shows that keyword search and links are insufficient.

A retrieval system should return the source note and relevant excerpt alongside every answer. Evaluate it against a small set of realistic questions: whether it finds the right note, cites the correct source, distinguishes current from superseded decisions, and admits when the vault lacks evidence. An answer that sounds plausible but cannot show its evidence is a retrieval failure.

A desktop LLM workspace such as AnythingLLM can be evaluated as an optional search interface, but keep the Markdown vault portable and authoritative. Do not let an index or embedding store become the only copy of the knowledge.

## Practical first-week plan

- **Day 1:** create the vault, Home note, starter folders, and backup.
- **Day 2:** add the onboarding project note and links to the repository and guide index.
- **Day 3:** curate five to ten useful conversation outcomes with source references.
- **Day 4:** ask an LLM to propose links, tags, and stale-note candidates; review all changes.
- **Day 5:** test Git history or another restore path and write down the recovery procedure.
- **After the pilot:** check whether Grok Bot has local filesystem access or only cloud workspace access, then choose the simplest supported bridge.

## Acceptance checklist

- [ ] Notes remain readable as ordinary Markdown without Obsidian or a particular LLM.
- [ ] Original sources are preserved or linked, and important claims have traceable provenance.
- [ ] Draft summaries are visibly distinguished from reviewed or verified knowledge.
- [ ] The vault has a tested backup and recovery path.
- [ ] Grok Bot's actual access model is verified rather than assumed.
- [ ] A failed or inaccessible source is reported as a gap, not treated as empty.
- [ ] Proposed changes include evidence and a reviewable diff.
- [ ] Sensitive data, deletion, durable decision changes, and publishing remain approval-gated.
- [ ] Semantic search is added only after a measurable retrieval need is demonstrated.
