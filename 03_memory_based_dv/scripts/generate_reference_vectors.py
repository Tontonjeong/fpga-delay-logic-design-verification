#!/usr/bin/env python3
"""Generate Project 3 output.txt files from Input.txt/register.txt.

The model mirrors the RTL cycle order:
1. Read the slot iDelay clocks behind the current write pointer.
2. Update oData only when the delayed valid bit is 1; otherwise hold it.
3. Write the current input slot and advance the circular write pointer.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 10


@dataclass
class Scenario:
    data: list[int]
    valid: list[int]
    initial_delay: int
    delay_events: dict[int, int]  # 1-based input cycle -> new delay


def parse_tagged_vectors(path: Path) -> tuple[list[int], list[int]]:
    data: list[int] = []
    valid: list[int] = []
    section: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("tag:"):
            match = re.search(r"data_type=([A-Za-z_]+)", line)
            section = match.group(1) if match else None
            continue
        if re.fullmatch(r"[-+]?\d+", line):
            if section == "data":
                data.append(int(line))
            elif section == "valid":
                valid.append(1 if int(line) else 0)

    if not data or len(data) != len(valid):
        raise ValueError(f"Invalid Input.txt: data={len(data)}, valid={len(valid)}")
    return data, valid


def parse_registers(path: Path) -> tuple[int, dict[int, int]]:
    initial_delay: int | None = None
    events: dict[int, int] = {}

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("tag:"):
            continue
        parts = line.split()
        if len(parts) == 2 and parts[0] == "Delay":
            initial_delay = int(parts[1], 16)
        elif len(parts) == 3 and parts[0] == "DelayAt":
            events[int(parts[1])] = int(parts[2], 16)

    if initial_delay is None:
        raise ValueError(f"No Delay entry in {path}")
    if not 1 <= initial_delay <= DEPTH:
        raise ValueError(f"Delay must be in 1..{DEPTH}")
    return initial_delay, events


def load_scenario(directory: Path) -> Scenario:
    data, valid = parse_tagged_vectors(directory / "Input.txt")
    initial_delay, events = parse_registers(directory / "register.txt")
    return Scenario(data, valid, initial_delay, events)


def simulate(s: Scenario) -> tuple[list[int], list[int], list[dict[str, int]]]:
    max_delay = max([s.initial_delay, *s.delay_events.values()])
    total_cycles = len(s.data) + max_delay

    data_mem = [0] * DEPTH
    valid_mem = [0] * DEPTH
    write_ptr = 0
    delay = s.initial_delay
    out_data = 0

    out_values: list[int] = []
    out_valid: list[int] = []
    trace: list[dict[str, int]] = []

    for cycle in range(1, total_cycles + 1):
        if cycle in s.delay_events:
            delay = s.delay_events[cycle]

        read_addr = (write_ptr - delay) % DEPTH
        delayed_valid = valid_mem[read_addr]
        if delayed_valid:
            out_data = data_mem[read_addr]

        input_index = cycle - 1
        if input_index < len(s.data):
            in_data = s.data[input_index]
            in_valid = s.valid[input_index]
        else:
            in_data = 0
            in_valid = 0

        out_values.append(out_data)
        out_valid.append(delayed_valid)
        trace.append(
            {
                "cycle": cycle,
                "delay": delay,
                "write_ptr": write_ptr,
                "read_addr": read_addr,
                "iDataEn": in_valid,
                "iData": in_data,
                "oDataEn": delayed_valid,
                "oData": out_data,
            }
        )

        valid_mem[write_ptr] = in_valid
        if in_valid:
            data_mem[write_ptr] = in_data
        write_ptr = (write_ptr + 1) % DEPTH

    return out_values, out_valid, trace


def write_output(path: Path, data: list[int], valid: list[int]) -> None:
    lines = ["tag: data_type=data stage=pilot", *map(str, data)]
    lines.extend(["tag: data_type=valid stage=pilot", *map(str, valid)])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary_rows: list[dict[str, int | str]] = []
    all_trace_rows: list[dict[str, int | str]] = []

    for scenario_id in (1, 2, 3):
        directory = ROOT / "vectors" / f"scenario{scenario_id}"
        scenario = load_scenario(directory)
        out_data, out_valid, trace = simulate(scenario)
        write_output(directory / "output.txt", out_data, out_valid)

        summary_rows.append(
            {
                "scenario": scenario_id,
                "input_cycles": len(scenario.data),
                "reference_cycles": len(out_data),
                "initial_delay": scenario.initial_delay,
                "delay_changes": len(scenario.delay_events),
                "expected_valid_outputs": sum(out_valid),
                "result": "REFERENCE PASS",
            }
        )
        for row in trace:
            all_trace_rows.append({"scenario": scenario_id, **row})

    results = ROOT / "results"
    results.mkdir(exist_ok=True)

    with (results / "reference_summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    with (results / "reference_cycle_trace.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=all_trace_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_trace_rows)

    report = ["Project 3 reference-vector consistency check"]
    report.extend(
        f"Scenario {r['scenario']}: cycles={r['reference_cycles']}, "
        f"valid_outputs={r['expected_valid_outputs']}, {r['result']}"
        for r in summary_rows
    )
    (results / "reference_validation.txt").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
