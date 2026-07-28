#!/usr/bin/env python3
"""Validate bilingual lecture-brief redraws without third-party packages."""

from __future__ import annotations

import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


STEMS = (
    "project1_shift_register_datapath",
    "project1_testbench_architecture",
    "project1_expected_timing",
    "project2_circular_queue_architecture",
    "project2_architecture_comparison",
    "project2_ppa_matrix",
    "project3_file_driven_verification",
    "project3_scenario_flow",
)


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"invalid PNG header: {path}")
    return struct.unpack(">II", header[16:24])


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    expected: list[Path] = []

    for language in ("ko", "en"):
        asset_dir = repo / "docs" / "assets" / language / "architecture"
        for stem in STEMS:
            svg = asset_dir / f"{stem}.svg"
            png = asset_dir / f"{stem}.png"
            expected.extend((svg, png))
            for path in (svg, png):
                if not path.is_file() or path.stat().st_size < 1_000:
                    errors.append(f"missing or unexpectedly small asset: {path.relative_to(repo)}")
            if svg.is_file():
                try:
                    root = ET.parse(svg).getroot()
                    if root.tag.rsplit("}", 1)[-1] != "svg":
                        errors.append(f"not an SVG root: {svg.relative_to(repo)}")
                except ET.ParseError as exc:
                    errors.append(f"invalid SVG XML {svg.relative_to(repo)}: {exc}")
            if png.is_file():
                try:
                    if png_size(png) != (1600, 900):
                        errors.append(f"unexpected PNG dimensions: {png.relative_to(repo)}")
                except ValueError as exc:
                    errors.append(str(exc))

    provenance = repo / "docs" / "assets" / "architecture" / "diagram_provenance.yaml"
    if not provenance.is_file():
        errors.append("missing diagram provenance manifest")
    else:
        text = provenance.read_text(encoding="utf-8")
        for stem in STEMS:
            if stem not in text:
                errors.append(f"provenance missing stem: {stem}")
        if "not a source-slide capture" not in text.lower():
            errors.append("provenance must state that redraws are not source-slide captures")

    pages = {
        "ko": repo / "docs" / "index.html",
        "en": repo / "docs" / "en" / "index.html",
    }
    for language, page in pages.items():
        html = page.read_text(encoding="utf-8")
        if 'id="brief-redraws"' not in html:
            errors.append(f"missing brief-redraws section: {page.relative_to(repo)}")
        for stem in STEMS:
            hits = len(re.findall(re.escape(stem), html))
            if hits < 2:
                errors.append(
                    f"{page.relative_to(repo)} must reference SVG and PNG for {stem}"
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "LECTURE_DIAGRAMS=PASS "
        f"bilingual_assets={len(expected)} pages={len(pages)} provenance=present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
