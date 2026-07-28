#!/usr/bin/env python3
"""Validate public structure, evidence states, links, and sensitive-file rules."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "README.ko.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "CHANGELOG_PORTFOLIO.md",
    "assets/hero/fpga_delay_logic_hero.svg",
    "assets/hero/github_social_preview.png",
    "docs/assets/en/architecture/architecture_evolution.svg",
    "docs/assets/en/architecture/shift_register_block.svg",
    "docs/assets/en/architecture/circular_queue_block.svg",
    "docs/assets/en/architecture/memory_delay_block.svg",
    "docs/assets/en/verification/file_driven_dv_flow.svg",
    "docs/assets/en/ppa/ppa_comparison_matrix.svg",
    "docs/assets/ko/architecture/architecture_evolution.svg",
    "docs/assets/ko/verification/file_driven_dv_flow.svg",
    "01_shift_register_baseline/rtl/delay_logic.sv",
    "02_circular_queue_ppa/rtl/circular_queue_delay_logic.sv",
    "03_memory_based_dv/rtl/memory_delay_logic.sv",
    "03_memory_based_dv/tb/input_driver.sv",
    "03_memory_based_dv/tb/output_checker.sv",
    "03_memory_based_dv/results/reference_summary.csv",
    "docs/index.html",
]

FORBIDDEN_SUFFIXES = {".zip", ".docx", ".wlf", ".qdb"}
FORBIDDEN_DIRS = {"db", "incremental_db", "output_files", "work", "__pycache__"}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".sv",
    ".sdc",
    ".tcl",
    ".do",
    ".bat",
    ".py",
    ".csv",
    ".qsf",
    ".qpf",
    ".html",
    ".svg",
    ".yml",
    ".yaml",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}", errors)


def validate_public_scope(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part.lower() in FORBIDDEN_DIRS for part in relative.parts):
            fail(f"forbidden generated directory: {relative}", errors)
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden public file: {relative}", errors)


def iter_local_targets(path: Path, text: str):
    markdown = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    html = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
    for target in [*markdown.findall(text), *html.findall(text)]:
        target = target.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#", "data:", "/")):
            continue
        yield unquote(target.split("#", 1)[0].split("?", 1)[0])


def validate_links_and_paths(errors: list[str]) -> None:
    windows_absolute = re.compile(r"(?i)(?:^|[\s\"'`(])(?:[a-z]:\\|[a-z]:/)")
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="strict")
        relative = path.relative_to(ROOT)
        if windows_absolute.search(text):
            fail(f"machine-specific absolute path: {relative}", errors)
        for target in iter_local_targets(path, text):
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"link escapes repository: {relative} -> {target}", errors)
                continue
            if not resolved.exists():
                fail(f"broken relative link: {relative} -> {target}", errors)


def parse_tagged(path: Path) -> tuple[list[int], list[int]]:
    data: list[int] = []
    valid: list[int] = []
    section = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("tag:"):
            match = re.search(r"data_type=([A-Za-z_]+)", line)
            section = match.group(1) if match else ""
        elif re.fullmatch(r"[-+]?\d+", line):
            if section == "data":
                data.append(int(line))
            elif section == "valid":
                valid.append(1 if int(line) else 0)
    return data, valid


def validate_reference_summary(errors: list[str]) -> None:
    expected = {
        1: (8, 5),
        2: (14, 4),
        3: (17, 14),
    }
    summary_path = ROOT / "03_memory_based_dv/results/reference_summary.csv"
    with summary_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 3:
        fail(f"reference summary has {len(rows)} rows, expected 3", errors)
        return
    for row in rows:
        scenario = int(row["scenario"])
        actual = (int(row["reference_cycles"]), int(row["expected_valid_outputs"]))
        if actual != expected.get(scenario):
            fail(f"scenario {scenario} summary mismatch: {actual}", errors)
        vector_dir = ROOT / f"03_memory_based_dv/vectors/scenario{scenario}"
        out_data, out_valid = parse_tagged(vector_dir / "output.txt")
        if len(out_data) != actual[0] or len(out_valid) != actual[0]:
            fail(f"scenario {scenario} output vector length mismatch", errors)
        if sum(out_valid) != actual[1]:
            fail(f"scenario {scenario} valid-output count mismatch", errors)


def validate_ppa(errors: list[str]) -> None:
    result_path = ROOT / "02_circular_queue_ppa/results/PPA_results.csv"
    if not result_path.exists():
        return
    with result_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metrics = [
        "ALMs/Logic Utilization",
        "Registers",
        "Memory Bits",
        "Memory Blocks",
        "Fmax (MHz)",
        "Total Power (W)",
        "Core Dynamic Power (W)",
        "Static Power (W)",
    ]
    if len(rows) != 4:
        fail("PPA_results.csv must contain exactly four configurations", errors)
    for row in rows:
        for metric in metrics:
            if not row.get(metric, "").strip():
                fail(
                    f"incomplete PPA result: {row.get('Quartus Project', '?')} / {metric}",
                    errors,
                )


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_public_scope(errors)
    validate_links_and_paths(errors)
    validate_reference_summary(errors)
    validate_ppa(errors)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository structure: PASS")
    print("Relative links and machine paths: PASS")
    print("Project 3 reference summary: PASS")
    print("PPA evidence policy: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
