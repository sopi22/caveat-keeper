# caveat-keeper

**Catches the warnings that quietly disappear from project notes.**

When an AI helper writes a project's notes, two kinds of mistakes are easy to miss:

- a warning ("this only worked on one phone", "not tested on Windows") is written in the
  log, but **dropped from the final summary**, so the summary sounds more certain than the
  work really was;
- a word the project said it would **never use** (or a limit it set for itself, like "two
  probe types maximum") shows up anyway.

caveat-keeper reads a project's own README and research notes, picks up the rules the
project set for itself, and checks the rest of the project against them. It uses plain
text and structure checks, no AI model judging the text, so every result can be traced to
an exact file and line.

Every result is a **flag for a person to look at**, not a verdict.

## Why I built it

I wanted to know whether this kind of slip can be caught with simple, repeatable checks
instead of asking another AI model "does this look right?". I wrote down what would count
as success and failure before running anything.

**Result so far: partly yes.** On a test project with mistakes planted on purpose, it
catches all of them. On real open-source projects it raises almost no false alarms, but
real projects rarely write their rules in the format it understands yet (details below).

## What it checks

| Check | Looks for |
|---|---|
| Word list | Words the project banned for itself appearing anyway |
| Limits | More items than the project's own stated maximum (e.g. "probe types: 2 maximum") |
| Test grade | A reproducibility grade (R0–R3) stated higher than the logged runs support |
| Dropped warnings | A warning in the log or notes that is missing from the closing summary |

## Run it

Requires Python 3.11+. No outside services, no network.

```bash
git clone https://github.com/sopi22/caveat-keeper.git
cd caveat-keeper/scanner
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest                                          # run the 52 tests
caveat-keeper examples/synthetic_violations     # scan the built-in test project
caveat-keeper <path-to-a-repo> -o report.json   # scan any repo, save the report
```

The report is one JSON file: the rules it found in the project's own docs, and every flag
with its file, line, what matched, and notes on why it might be a false alarm.

## What I found (short version)

- **Planted mistakes:** a small fake project with known, deliberately planted slips. All
  were caught.
- **Real projects** (openai/whisper, microsoft/vscode, stan-dev/httpstan, OpenAI CLIP and
  my own repos): almost no false alarms, but also little to check, because their rules are
  written in ordinary prose, not in a format the tool can pick up.
- **Fixed along the way:** it now reads standard Markdown headings (`#`, `##`, `###`), looks
  in more files (CONTRIBUTING.md, model-card.md, LIMITATIONS.md, docs/), and can check
  dropped warnings even when a project has no "summary" section.
- **Still open:** understanding rules written in everyday language. That isn't started yet.

The full lab notebook (every run, what I expected beforehand, what actually happened) is
in [RESEARCH.md](RESEARCH.md).

## What it is not

Not an AI-text detector, not an AI-based reviewer, not a dashboard and not a CI plug-in.
It never says something is "proven" or "verified"; it only points at text worth a second look.

## Tech

Python standard library only (plus pytest for tests). Local files only.

## Author

Jhoana Sophia Munar ([@sopi22](https://github.com/sopi22))

## License

MIT, see [LICENSE](LICENSE).
