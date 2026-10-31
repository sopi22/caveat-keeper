# caveat-keeper scanner

The scanner reads a repo's own README and research notes, finds the rules that repo set
for itself (banned words, limits, test grades), and checks the rest of the repo against
them. Python standard library only; no network.

Each result is a flag for a person to review, with notes on why it might be a false alarm.

## Setup

```bash
cd scanner
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
pytest                                     # run the test suite
caveat-keeper <path-to-target-repo>         # scan a repo
caveat-keeper <path-to-target-repo> -o out.json
```

The report is a single JSON file: the rules found in the target repo's own docs, and the
list of flags, each with file, line, matched text and notes.

## Example

```bash
caveat-keeper examples/synthetic_violations
```

`examples/synthetic_violations/` is a small fake project with deliberately planted
mistakes, used to check that every one gets caught. It is not a real project.

## Scope (v0.1)

Four checks: banned words, limits, test grade, dropped warnings. No AI-based review, no
GUI, no multi-repo support. Local files only, no background processes.
