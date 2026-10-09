# Podcast Prompts (NotebookLM Audio Overviews)

Seven technical episodes, three company-and-context episodes built on the
[background whitepaper](whitepaper/README.md), and four coaching episodes. Each episode below is **one
self-contained block**: copy it, then follow the steps. Listen **after** the matching readings,
not instead of them. The hosts are good at concepts, weaker on exact API names, config values and
numbers, so treat the [reading guide](reading-guide.md) and labs as the source of truth.

> **Public sources only.** Every source below is a public URL or a file from this public repo.
> Once employed, don't put ServiceTitan internal material into NotebookLM unless the company
> approves it.

## How to use a block
1. Create a **new notebook** in NotebookLM.
2. **Add source → Website** (or **YouTube** for video links): paste the URLs from the block's
   SOURCES list. You can paste several URLs at once, one per line. Repo files use
   `raw.githubusercontent.com` links so NotebookLM gets clean text.
3. **Audio Overview → Customize:** choose the format and length shown, and paste the block's
   CUSTOMIZE PROMPT.
4. If a site refuses to import (OpenAI's pages sometimes do), open it in your browser,
   **Print → Save as PDF**, and upload the PDF instead.
5. If the customize box truncates the prompt, trim its last sentence.
6. Listen, check the box, and add one line to your onboarding log.

Episodes are listed in **listening order**; numbers match references elsewhere in the repo.

For a **5–10 minute** episode on a single concept (instead of a full numbered episode), use the
[reusable short-episode template](#reusable-template-510-minute-source-grounded-episode) at the end of this file.
That template is for manual NotebookLM use; `scripts/podcasts_to_nlm.py` only reads the numbered episode blocks.

## Optional: create episodes from the command line

`scripts/podcasts_to_nlm.py` reads the blocks below and, for each episode, creates a notebook,
adds its sources and requests the Audio Overview with the block's format, length and prompt,
using the unofficial [`nlm` CLI](https://github.com/jacob-bd/notebooklm-mcp-cli).

```bash
pipx install notebooklm-mcp-cli      # provides `nlm`
nlm login                            # personal Google account only
python scripts/podcasts_to_nlm.py                # dry run: prints every command
python scripts/podcasts_to_nlm.py --run --episodes 1
```

- Consumer NotebookLM has no public API. `nlm` drives its internal interface with your saved
  browser session, so it can break without notice. Use a personal account on a personal
  machine, never a work account or work laptop.
- Sites that block automated imports (OpenAI's pages often do) are reported as failed; save
  those pages as PDFs and add them with `nlm source add <notebook-id> --file page.pdf --wait`.
- Progress is saved in `.nlm-podcasts.json` (gitignored). Reruns reuse each episode's
  notebook, add only missing sources, and retry only the audio request.
- NotebookLM limits how many Audio Overviews an account can generate per day. When the limit
  is hit (`RESOURCE_EXHAUSTED`), the script stops requesting audio; run it again later.

### Put the finished audio in this guide

```bash
gh auth login                                    # once
python scripts/podcasts_to_nlm.py --publish      # download, upload, add Listen links
python scripts/podcasts_to_nlm.py --publish --share   # also link each public notebook
```

`--publish` downloads each finished episode, uploads it to a GitHub release named
`podcasts`, and adds a **Listen:** line under that episode below. The site turns those links
into audio players. Commit and push the updated file to publish them. Release assets in this
public repo are public; the audio is AI-generated from public sources.

---

## Episode 1: The Business: ServiceTitan, Contractors, and AI Voice Agents
- [ ] Generated · [ ] Listened · **When:** Week of Sept 28, after reading-guide items 1–3 and whitepaper chapters 01–03

```text
EPISODE 1: THE BUSINESS: SERVICETITAN, CONTRACTORS, AND AI VOICE AGENTS
Format: Deep Dive · Length: Default

SOURCES (NotebookLM → Add source → Website / YouTube):
https://www.servicetitan.com/features/pro/virtual-agent
https://www.servicetitan.com/blog/webinar-recap-ai-virtual-agents-call-booking
https://www.servicetitan.com/press/servicetitan-introducing-the-next-evolution-of-ai-at-pantheon-2025-keynote
https://www.servicetitan.com/blog/pantheon-2025-vahe-keynote-atlas
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/01-company.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/02-the-trades-industry.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/03-how-a-contractor-works.md
https://raw.githubusercontent.com/sp7412/onboarding/main/docs/whitepaper/05-pain-points.md
https://raw.githubusercontent.com/sp7412/onboarding/main/notes/glossary.md

CUSTOMIZE PROMPT (Audio Overview → Customize):
The listener is a senior ML engineer from the defense industry who starts as a Senior AI Engineer on ServiceTitan's voice-agent team in a few weeks. He knows ML deeply but not the trades industry or SaaS. Explain how a residential HVAC/plumbing contractor runs: the inbound call, booking, capacity, dispatch, memberships, and why missed calls cost revenue. Then explain what ServiceTitan's AI Voice Agents do, how they escalate to human CSRs, and how they fit the Atlas AI strategy. End with 5 questions he should ask his new team. Stick to the sources.
```
