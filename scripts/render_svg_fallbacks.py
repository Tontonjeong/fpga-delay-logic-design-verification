#!/usr/bin/env python3
"""Render localized SVG Pages assets to same-name PNG fallbacks with Edge."""

import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parents[1]
EDGE = Path(os.environ.get("ProgramFiles(x86)", "")) / "Microsoft/Edge/Application/msedge.exe"


def render(svg: Path, profile: Path) -> None:
    header = svg.read_text(encoding="utf-8").splitlines()[0]
    width = int(re.search(r'width="(\d+)"', header).group(1))
    height = int(re.search(r'height="(\d+)"', header).group(1))
    destination = svg.with_suffix(".png")
    temporary = svg.with_suffix(".full.png")
    if temporary.exists():
        temporary.unlink()
    command = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--user-data-dir={profile}",
        f"--window-size={width},{height + 120}",
        f"--screenshot={temporary}",
        svg.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for _ in range(100):
        if temporary.exists() and temporary.stat().st_size:
            break
        time.sleep(0.1)
    else:
        raise RuntimeError(f"Edge did not create {temporary}")
    with Image.open(temporary) as image:
        image.crop((0, 0, width, height)).save(destination, "PNG", optimize=True)
    temporary.unlink()
    print(destination.relative_to(ROOT))


def main() -> None:
    if not EDGE.exists():
        raise SystemExit("Microsoft Edge was not found")
    with tempfile.TemporaryDirectory(prefix="fpga-svg-render-") as temporary_profile:
        profile = Path(temporary_profile)
        for language in ("ko", "en"):
            for svg in sorted((ROOT / f"docs/assets/{language}").rglob("*.svg")):
                render(svg, profile)


if __name__ == "__main__":
    main()
