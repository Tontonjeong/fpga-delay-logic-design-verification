#!/usr/bin/env python3
"""Run one or all portable RTL regressions."""

import argparse
import sys
from pathlib import Path

from verification_lib import executable, version_line
from verification_project3 import project3
from verification_projects import project1, project2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--project", choices=["1", "2", "3", "all"], default="all")
    args = parser.parse_args()
    repo = args.repo.resolve()
    iverilog, vvp = executable("iverilog"), executable("vvp")
    if not iverilog or not vvp:
        print("Icarus Verilog 13.0 is required.", file=sys.stderr)
        return 2
    print(f"SIMULATOR={version_line(iverilog)}")
    runners = {"1": project1, "2": project2, "3": project3}
    selected = runners if args.project == "all" else {args.project: runners[args.project]}
    for number, runner in selected.items():
        try:
            evidence = runner(repo, iverilog, vvp)
            print(f"PROJECT{number}={evidence['status']}")
        except Exception as exc:
            print(f"PROJECT{number}=FAIL: {exc}", file=sys.stderr)
            return 1
    print("VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
