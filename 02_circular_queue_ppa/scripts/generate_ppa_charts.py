#!/usr/bin/env python3
"""Generate PPA charts only from a complete Quartus result CSV."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "results" / "PPA_results.csv"
OUT = ROOT / "figures" / "ppa_results"

METRICS = {
    "ALMs/Logic Utilization": "alm_comparison.png",
    "Registers": "register_comparison.png",
    "Memory Bits": "memory_bits_comparison.png",
    "Fmax (MHz)": "fmax_comparison.png",
    "Core Dynamic Power (W)": "core_dynamic_power_comparison.png",
}


def load_rows() -> list[dict[str, str]]:
    if not CSV_PATH.exists():
        raise SystemExit(
            "PPA_results.csv is absent. Run Quartus and collect_ppa_results.py first."
        )
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 4:
        raise SystemExit(f"Expected four PPA rows, found {len(rows)}.")

    required = {
        "Architecture",
        "DEPTH",
        "Quartus Version",
        "FPGA Device",
        "Clock Constraint (MHz)",
        "Power Method",
        "Toggle Assumption",
        *METRICS,
    }
    missing_columns = required.difference(rows[0])
    if missing_columns:
        raise SystemExit("Missing columns: " + ", ".join(sorted(missing_columns)))

    for row in rows:
        missing_values = [name for name in required if not row.get(name, "").strip()]
        if missing_values:
            raise SystemExit(
                f"Incomplete row {row.get('Quartus Project', '?')}: "
                + ", ".join(sorted(missing_values))
            )
    return rows


def main() -> None:
    rows = load_rows()
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("matplotlib is required to generate PPA charts.") from exc

    versions = {row["Quartus Version"] for row in rows}
    devices = {row["FPGA Device"] for row in rows}
    clocks = {row["Clock Constraint (MHz)"] for row in rows}
    methods = {row["Power Method"] for row in rows}
    toggles = {row["Toggle Assumption"] for row in rows}
    if any(len(values) != 1 for values in (versions, devices, clocks, methods, toggles)):
        raise SystemExit("All four rows must use the same tool/device/power conditions.")

    labels = [f"{row['Architecture']}\nDEPTH={row['DEPTH']}" for row in rows]
    caption = (
        f"Quartus {next(iter(versions))} · {next(iter(devices))} · "
        f"{next(iter(clocks))} MHz · {next(iter(methods))} · "
        f"toggle {next(iter(toggles))}"
    )
    OUT.mkdir(parents=True, exist_ok=True)

    for metric, filename in METRICS.items():
        values = [float(row[metric].replace(",", "")) for row in rows]
        fig, ax = plt.subplots(figsize=(9.5, 5.4), dpi=160)
        bars = ax.bar(labels, values, color=["#5B78F6", "#16A394", "#5B78F6", "#16A394"])
        ax.set_title(metric)
        ax.set_ylabel(metric)
        ax.grid(axis="y", alpha=0.2)
        ax.bar_label(bars, padding=3)
        fig.text(0.5, 0.01, caption, ha="center", fontsize=8.5)
        fig.tight_layout(rect=(0, 0.04, 1, 1))
        fig.savefig(OUT / filename)
        plt.close(fig)
        print(f"Wrote {OUT / filename}")


if __name__ == "__main__":
    main()

