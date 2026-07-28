"""Shared process and evidence helpers for portable RTL regression."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def executable(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for root in (Path(r"D:\msys64\ucrt64\bin"), Path(r"C:\msys64\ucrt64\bin")):
        candidate = root / f"{name}.exe"
        if candidate.exists():
            return str(candidate)
    return None


def run_logged(
    command: list[str],
    cwd: Path,
    log_path: Path,
    markers: tuple[str, ...] = (),
) -> str:
    environment = os.environ.copy()
    environment["PATH"] = str(Path(command[0]).parent) + os.pathsep + environment["PATH"]
    done = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=environment,
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(done.stdout, encoding="utf-8")
    print(done.stdout, end="")
    if done.returncode:
        raise RuntimeError(f"exit {done.returncode}; see {log_path}")
    missing = [marker for marker in markers if marker not in done.stdout]
    if missing:
        raise RuntimeError(f"missing PASS marker(s) {missing}; see {log_path}")
    return done.stdout


def compile_design(
    iverilog: str,
    project: Path,
    top: str,
    sources: list[str],
    output_name: str,
    log_name: str,
) -> Path:
    (project / "build").mkdir(exist_ok=True)
    (project / "results").mkdir(exist_ok=True)
    output = project / "build" / output_name
    run_logged(
        [
            iverilog,
            "-g2012",
            "-Wall",
            "-s",
            top,
            "-o",
            str(output.relative_to(project)),
            *sources,
        ],
        project,
        project / "results" / log_name,
    )
    return output


def version_line(path: str) -> str:
    environment = os.environ.copy()
    environment["PATH"] = str(Path(path).parent) + os.pathsep + environment["PATH"]
    done = subprocess.run(
        [path, "-V"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=environment,
    )
    return done.stdout.splitlines()[0] if done.stdout else "version unavailable"


def git_commit(repo: Path) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        check=True,
    )
    return done.stdout.strip()


def tool_scan() -> list[dict[str, object]]:
    names = [
        "vsim", "vlog", "vlib", "vmap",
        "quartus_sh", "quartus_map", "quartus_fit", "quartus_sta", "quartus_pow",
        "iverilog", "vvp", "verilator", "yosys",
    ]
    return [
        {"name": name, "found": bool(executable(name)), "path": executable(name)}
        for name in names
    ]
