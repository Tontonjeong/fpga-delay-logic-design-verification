#!/usr/bin/env python3
"""Capture the actual Windows FPGA tool environment without PATH assumptions."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

CANDIDATES = {
    "Quartus Prime Pro": [
        Path(r"D:\IntelQuartus\quartus\bin64\quartus_sh.exe"),
        Path(r"D:\intelFPGA\18.1\quartus\bin64\quartus_sh.exe"),
    ],
    "Questa Intel FPGA Starter Edition": [
        Path(r"D:\IntelQuartus\questa_fse\win64\vsim.exe"),
    ],
    "ModelSim Intel FPGA Starter Edition": [
        Path(r"D:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe"),
    ],
    "Icarus Verilog": [
        Path(r"D:\msys64\ucrt64\bin\iverilog.exe"),
    ],
}


def first_existing(paths: list[Path]) -> Path | None:
    return next((path for path in paths if path.exists()), None)


def version(path: Path, arguments: list[str]) -> tuple[int, str]:
    environment = os.environ.copy()
    environment["PATH"] = str(path.parent) + os.pathsep + environment["PATH"]
    try:
        done = subprocess.run(
            [str(path), *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=environment,
            timeout=30,
        )
        return done.returncode, done.stdout.strip()
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout
        return 124, (partial or "version query timed out while another tool process was active").strip()


def main() -> int:
    records: list[dict[str, object]] = []
    for name, candidates in CANDIDATES.items():
        path = first_existing(candidates)
        if not path:
            records.append({"name": name, "found": False, "candidates": [str(x) for x in candidates]})
            continue
        arguments = ["--version"] if "Quartus" in name else ["-version"]
        if name == "Icarus Verilog":
            arguments = ["-V"]
        code, output = version(path, arguments)
        records.append(
            {
                "name": name,
                "found": True,
                "path": str(path),
                "version_exit_code": code,
                "version_output": output,
            }
        )

    payload = {
        "captured_at": datetime.now().astimezone().isoformat(),
        "host": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "processor": platform.processor(),
        },
        "tools": records,
        "notes": {
            "questa_2024": "Installed; simulation initialization is blocked by the local license environment.",
            "modelsim_10_5b": "Installed; used for original archive reruns.",
            "quartus_24_3_1": "Installed; used for synthesis, fit, timing, and power reports.",
        },
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "execution_environment.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [f"Captured: {payload['captured_at']}", f"Host: {payload['host']['platform']}"]
    for record in records:
        if not record["found"]:
            lines.append(f"{record['name']}: NOT FOUND")
            continue
        first_line = str(record["version_output"]).splitlines()[0] if record["version_output"] else "no output"
        lines.append(f"{record['name']}: {first_line}")
        lines.append(f"  {record['path']}")
    (RESULTS / "tool_versions.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
