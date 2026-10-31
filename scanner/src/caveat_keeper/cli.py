"""caveat-keeper command-line entry point."""

from __future__ import annotations

import argparse
import sys

from caveat_keeper.report import write_report
from caveat_keeper.scan import scan_repo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="caveat-keeper",
        description=(
            "Scan a git repo's own docs for pattern matches against that "
            "repo's own stated vocabulary lock, entropy budget, "
            "reproducibility ladder, and closing-section language. Every "
            "result is a flag for human review, not a finding of fact."
        ),
    )
    parser.add_argument("repo", help="path to the target repo")
    parser.add_argument(
        "-o", "--out", default="caveat-keeper-report.json",
        help="path to write the JSON report (default: caveat-keeper-report.json)",
    )
    args = parser.parse_args(argv)

    result = scan_repo(args.repo)
    write_report(result, args.out)

    if result.caveat_survival_rate is not None:
        print(f"caveat-keeper: caveat survival rate {result.caveat_survival_rate:.2f}")
    print(f"caveat-keeper: {len(result.flags)} pattern flag(s) written to {args.out}")
    print("Each flag is a pattern match for human review -- see notes in the report.")
    by_check: dict[str, int] = {}
    for flag in result.flags:
        by_check[flag.check] = by_check.get(flag.check, 0) + 1
    for check, count in sorted(by_check.items()):
        print(f"  {check}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
