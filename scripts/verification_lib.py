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
    roots: list[Path] = []
    if os.environ.get("MSYS2_ROOT"):
        roots.append(Path(os.environ["MSYS2_ROOT"]) / "ucrt64/bin")
    roots.extend(Path(f"{drive}:/") / "msys64/ucrt64/bin" for drive in "CDE")
    drive_root = Path("D:" + os.sep)
    roots.extend(
        [
            drive_root / "IntelQuartus/quartus/bin64",
            drive_root / "IntelQuartus/questa_fse/win64",
            drive_root / "IntelQuartus/questa_fe/win64",
            drive_root / "intelFPGA/18.1/modelsim_ase/win32aloem",
        ]
    )
    for root in roots:
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
    command_text = subprocess.list2cmdline(command)
    log_text = f"$ {command_text}\n{done.stdout}\n[exit_code={done.returncode}]\n"
    log_path.write_text(log_text, encoding="utf-8")
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
        {"name": name, "found": bool(executable(name))}
        for name in names
    ]
