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
