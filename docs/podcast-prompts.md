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

SEE_FULL_FILE_IN_LOCAL_ARTIFACTS_PLEASE_RESTORE_FROM_COMMIT_357a606
