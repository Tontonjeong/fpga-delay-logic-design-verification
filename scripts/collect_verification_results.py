#!/usr/bin/env python3
"""Collect current regression logs into a concise evidence manifest."""

import json
import subprocess
from datetime import datetime
from pathlib import Path

from verification_lib import executable, tool_scan, version_line


ROOT = Path(__file__).parents[1]


def contains(relative: str, marker: str) -> bool:
    return marker in (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    simulator = executable("iverilog")
    if not simulator:
        raise SystemExit("Icarus Verilog not found")
    commit = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()
    p1 = contains(
        "01_shift_register_baseline/results/project1_simulation.log", "[P1][PASS]"
    )
    p2 = contains(
        "02_circular_queue_ppa/results/project2_simulation.log", "[P2][PASS]"
    )
    scenarios = []
    for number in (1, 2, 3):
        log = f"03_memory_based_dv/results/scenario{number}_console.log"
        passed = contains(log, "[CHECKER][PASS]") and contains(log, "[TEST PASS]")
        scenarios.append({"scenario": number, "status": "PASS" if passed else "FAIL", "log": log})
    evidence = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "git_commit_tested": commit,
        "simulator": "Icarus Verilog",
        "simulator_version": version_line(simulator),
        "projects": {
            "project1": {"status": "PASS" if p1 else "FAIL", "checks": 20},
            "project2": {"status": "PASS" if p2 else "FAIL", "checks": 26},
            "project3": {
                "status": "PASS" if all(x["status"] == "PASS" for x in scenarios) else "FAIL",
                "scenarios": scenarios,
            },
        },
        "synthesis": {
            "status": "BLOCKED",
            "reason": "Quartus Prime executables were not found on this Windows host.",
        },
        "ppa": {
            "status": "BLOCKED",
            "reason": "Fit, Timing, and Power reports were unavailable; no numbers claimed.",
        },
        "tools": tool_scan(),
    }
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    (results / "verification_summary.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "FPGA Delay Logic - Verification Evidence",
        f"Generated: {evidence['generated_at']}",
        f"Commit tested: {commit}",
        f"Simulator: {evidence['simulator_version']}",
        f"Project 1: {evidence['projects']['project1']['status']} (20 checks)",
        f"Project 2: {evidence['projects']['project2']['status']} (26 checks)",
        f"Project 3: {evidence['projects']['project3']['status']} (3 scenarios)",
        "Synthesis: BLOCKED (Quartus not installed)",
        "Numerical PPA: BLOCKED (Fit/Timing/Power reports unavailable)",
    ]
    (results / "verification_summary.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    (results / "tool_environment.json").write_text(
        json.dumps(evidence["tools"], indent=2) + "\n", encoding="utf-8"
    )
    print("\n".join(lines))
    return 0 if all((p1, p2, evidence["projects"]["project3"]["status"] == "PASS")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
