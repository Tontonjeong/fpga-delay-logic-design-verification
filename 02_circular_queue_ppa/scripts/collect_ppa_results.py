#!/usr/bin/env python3
"""Collect Quartus fit/timing/power values from all four PPA projects.

The Quartus report wording varies by version and device. The parser therefore
tries several label patterns and leaves a cell blank rather than inventing a
value when a label cannot be found.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

CASES = [
    ("Shift Register", 10, "shift_depth10"),
    ("Circular Queue", 10, "circular_depth10"),
    ("Shift Register", 100, "shift_depth100"),
    ("Circular Queue", 100, "circular_depth100"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def first_match(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).replace(",", "").strip()
    return ""


def report_path(case: str, suffix: str) -> Path:
    base = ROOT / "quartus" / case
    direct = base / f"{case}.{suffix}.rpt"
    if direct.exists():
        return direct
    output_direct = base / "output_files" / f"{case}.{suffix}.rpt"
    if output_direct.exists():
        return output_direct
    matches = sorted(base.glob(f"*.{suffix}.rpt"))
    matches.extend(sorted((base / "output_files").glob(f"*.{suffix}.rpt")))
    return matches[0] if matches else direct


def parse_case(architecture: str, depth: int, case: str) -> dict[str, str | int]:
    fit_path = report_path(case, "fit")
    sta_path = report_path(case, "sta")
    pow_path = report_path(case, "pow")

    fit = read_text(fit_path)
    sta = read_text(sta_path)
    power = read_text(pow_path)
    qsf = read_text(ROOT / "quartus" / case / f"{case}.qsf")

    quartus_version = first_match(fit + sta + power, [
        r"Quartus\s+Prime(?:\s+Version)?\s*[:;]?\s*([0-9]+(?:\.[0-9]+)+)",
        r"Version\s+([0-9]+(?:\.[0-9]+)+)\s+Build",
    ])
    device = first_match(qsf, [
        r"set_global_assignment\s+-name\s+DEVICE\s+(\S+)",
    ])

    alms = first_match(fit, [
        r"(?:Total\s+ALMs|ALMs\s+needed|Logic\s+utilization\s*\(in\s+ALMs\))[^;\n]*;\s*([0-9,]+)",
        r"Total\s+logic\s+utilization[^;\n]*;\s*([0-9,]+)",
    ])
    registers = first_match(fit, [
        r"Dedicated\s+logic\s+registers[^;\n]*;\s*([0-9,]+)",
        r"Total\s+registers[^;\n]*;\s*([0-9,]+)",
    ])
    memory_bits = first_match(fit, [
        r"Total\s+(?:block\s+)?memory\s+bits[^;\n]*;\s*([0-9,]+)",
        r"Memory\s+bits[^;\n]*;\s*([0-9,]+)",
    ])
    memory_blocks = first_match(fit, [
        r"(?:M20K|M10K|MLAB)\s+blocks[^;\n]*;\s*([0-9,]+)",
        r"Total\s+RAM\s+Blocks[^;\n]*;\s*([0-9,]+)",
    ])

    fmax = first_match(sta, [
        r"iClk[^\n;]*;\s*([0-9.]+)\s*MHz",
        r"([0-9.]+)\s*MHz[^\n]*iClk",
        r"Fmax[^\n]*?([0-9.]+)\s*MHz",
    ])

    total_power = first_match(power, [
        r"Total\s+Thermal\s+Power\s+Dissipation[^\n;]*;\s*([0-9.]+)\s*W",
        r"Total\s+Thermal\s+Power\s+Dissipation[^\n]*?([0-9.]+)\s*W",
    ])
    dynamic_power = first_match(power, [
        r"Core\s+Dynamic\s+Thermal\s+Power\s+Dissipation[^\n;]*;\s*([0-9.]+)\s*W",
        r"Dynamic\s+Thermal\s+Power\s+Dissipation[^\n;]*;\s*([0-9.]+)\s*W",
    ])
    static_power = first_match(power, [
        r"Static\s+Thermal\s+Power\s+Dissipation[^\n;]*;\s*([0-9.]+)\s*W",
        r"Device\s+Static[^\n;]*;\s*([0-9.]+)\s*W",
    ])
    io_power = first_match(power, [
        r"I/O\s+Thermal\s+Power\s+Dissipation[^\n;]*;\s*([0-9.]+)\s*W",
    ])

    return {
        "Architecture": architecture,
        "DEPTH": depth,
        "Quartus Project": case,
        "Quartus Version": quartus_version,
        "FPGA Device": device,
        "Clock Constraint (MHz)": "100",
        "Power Method": "Vectorless estimation",
        "Toggle Assumption": "12.5%",
        "ALMs/Logic Utilization": alms,
        "Registers": registers,
        "Memory Bits": memory_bits,
        "Memory Blocks": memory_blocks,
        "Fmax (MHz)": fmax,
        "Total Power (W)": total_power,
        "Core Dynamic Power (W)": dynamic_power,
        "Static Power (W)": static_power,
        "I/O Power (W)": io_power,
        "Fit Report": str(fit_path.relative_to(ROOT)),
        "Timing Report": str(sta_path.relative_to(ROOT)),
        "Power Report": str(pow_path.relative_to(ROOT)),
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = [parse_case(*case) for case in CASES]
    missing_report_sets = [
        row["Quartus Project"]
        for row in rows
        if not Path(ROOT / row["Fit Report"]).exists()
        or not Path(ROOT / row["Timing Report"]).exists()
        or not Path(ROOT / row["Power Report"]).exists()
    ]
    if missing_report_sets:
        print("Numerical PPA results pending.")
        print("Missing Quartus report sets: " + ", ".join(missing_report_sets))
        raise SystemExit(2)

    out = RESULTS / "PPA_results.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote: {out}")
    for row in rows:
        missing = [k for k in ("ALMs/Logic Utilization", "Fmax (MHz)", "Total Power (W)") if not row[k]]
        if missing:
            print(f"WARNING: {row['Quartus Project']} missing: {', '.join(missing)}")


if __name__ == "__main__":
    main()
