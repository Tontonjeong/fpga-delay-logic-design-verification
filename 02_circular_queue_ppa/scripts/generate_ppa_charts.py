#!/usr/bin/env python3
"""Generate dependency-free SVG PPA charts from the completed Quartus CSV."""
from __future__ import annotations

import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "results" / "PPA_results.csv"
OUT = ROOT / "figures" / "ppa_results"

METRICS = {
    "ALMs/Logic Utilization": "alm_comparison.svg",
    "Registers": "register_comparison.svg",
    "Restricted Fmax (MHz)": "restricted_fmax_comparison.svg",
    "Setup Slack (ns)": "setup_slack_comparison.svg",
    "Dynamic Power (W)": "dynamic_power_comparison.svg",
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
    versions = {row["Quartus Version"] for row in rows}
    devices = {row["FPGA Device"] for row in rows}
    clocks = {row["Clock Constraint (MHz)"] for row in rows}
    methods = {row["Power Method"] for row in rows}
    toggles = {row["Toggle Assumption"] for row in rows}
    if any(len(values) != 1 for values in (versions, devices, clocks, methods, toggles)):
        raise SystemExit("All four rows must use the same tool/device/power conditions.")

    labels = [
        ("Shift Register" if row["Architecture"] == "Shift Register" else "Circular Queue")
        + f" · DEPTH={row['DEPTH']}"
        for row in rows
    ]
    caption = (
        f"Quartus {next(iter(versions))} · {next(iter(devices))} · "
        f"{next(iter(clocks))} MHz · {next(iter(methods))} · "
        f"toggle {next(iter(toggles))}"
    )
    OUT.mkdir(parents=True, exist_ok=True)

    for metric, filename in METRICS.items():
        values = [float(row[metric].replace(",", "")) for row in rows]
        maximum = max(values) or 1.0
        width, height = 1200, 660
        left, top, plot_w, plot_h = 135, 110, 980, 380
        bar_w, gap = 150, 85
        colors = ["#5B78F6", "#16A394", "#5B78F6", "#16A394"]
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            "<style>text{font-family:Arial,'Noto Sans',sans-serif}.title{font-size:31px;font-weight:700;fill:#eef3ff}.label{font-size:18px;fill:#c3cee8}.value{font-size:21px;font-weight:700;fill:#fff}.note{font-size:15px;fill:#97a6c6}.grid{stroke:#32405f;stroke-width:1}</style>",
            '<rect width="1200" height="660" rx="28" fill="#091426"/>',
            f'<text x="60" y="62" class="title">{escape(metric)}</text>',
        ]
        for step in range(6):
            y = top + plot_h - (plot_h * step / 5)
            tick = maximum * step / 5
            parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" class="grid"/>')
            parts.append(f'<text x="{left - 18}" y="{y + 6:.1f}" text-anchor="end" class="note">{tick:.2f}</text>')
        for index, (label, value, color) in enumerate(zip(labels, values, colors)):
            x = left + 65 + index * (bar_w + gap)
            bar_h = plot_h * value / maximum
            y = top + plot_h - bar_h
            display = f"{value:.3f}".rstrip("0").rstrip(".")
            parts.extend([
                f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" rx="10" fill="{color}"/>',
                f'<text x="{x + bar_w / 2:.1f}" y="{max(top + 25, y - 12):.1f}" text-anchor="middle" class="value">{display}</text>',
                f'<text x="{x + bar_w / 2:.1f}" y="{top + plot_h + 34}" text-anchor="middle" class="label">{escape(label.split(" · ")[0])}</text>',
                f'<text x="{x + bar_w / 2:.1f}" y="{top + plot_h + 60}" text-anchor="middle" class="note">{escape(label.split(" · ")[1])}</text>',
            ])
        parts.extend([
            f'<text x="600" y="614" text-anchor="middle" class="note">{escape(caption)}</text>',
            "</svg>",
        ])
        destination = OUT / filename
        destination.write_text("\n".join(parts) + "\n", encoding="utf-8")
        print(f"Wrote {destination}")


if __name__ == "__main__":
    main()
