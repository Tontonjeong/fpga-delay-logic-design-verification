#!/usr/bin/env python3
"""Render compact, reviewable PNG timing diagrams from committed VCD evidence."""

from __future__ import annotations

import os
from bisect import bisect_right
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parents[1]
WIDTH, LEFT, RIGHT = 1500, 215, 42
ROW_HEIGHT, TOP, BOTTOM = 78, 118, 58
BG, PANEL, GRID = "#071020", "#111a30", "#2e3b5d"
INK, MUTED, CYAN, MINT, AMBER = "#eef2ff", "#aeb9d5", "#4cc9f0", "#38dcc9", "#f7b84b"


def font(size: int, bold: bool = False, korean: bool = False) -> ImageFont.FreeTypeFont:
    if korean:
        name = "malgunbd.ttf" if bold else "malgun.ttf"
    else:
        name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(Path(os.environ["WINDIR"]) / "Fonts" / name), size)


def parse_vcd(path: Path) -> tuple[dict[str, str], dict[str, list[tuple[int, str]]], int]:
    ids: dict[str, str] = {}
    changes: dict[str, list[tuple[int, str]]] = {}
    scopes: list[str] = []
    in_definitions = True
    current_time = 0
    maximum_time = 0
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if in_definitions:
            if line.startswith("$scope"):
                scopes.append(line.split()[2])
            elif line.startswith("$upscope") and scopes:
                scopes.pop()
            elif line.startswith("$var") and len(scopes) == 1:
                parts = line.split()
                ids[parts[4]] = parts[3]
                changes.setdefault(parts[3], [])
            elif line.startswith("$enddefinitions"):
                in_definitions = False
            continue
        if line.startswith("#"):
            current_time = int(line[1:])
            maximum_time = max(maximum_time, current_time)
        elif line and line[0] in "01xz":
            changes.setdefault(line[1:], []).append((current_time, line[0]))
        elif line.startswith("b"):
            value, identifier = line[1:].split(maxsplit=1)
            changes.setdefault(identifier, []).append((current_time, value))
    return ids, changes, maximum_time


def normalized(value: str) -> int | None:
    if not value or any(bit in value.lower() for bit in "xz"):
        return None
    return int(value, 2)


def value_at(events: list[tuple[int, str]], when: int) -> str:
    times = [event[0] for event in events]
    index = bisect_right(times, when) - 1
    return events[index][1] if index >= 0 else "x"


def render(
    source: Path,
    destination: Path,
    title: str,
    subtitle: str,
    labels: list[tuple[str, str, str]],
    korean: bool,
) -> None:
    ids, all_changes, maximum = parse_vcd(source)
    height = TOP + ROW_HEIGHT * len(labels) + BOTTOM
    image = Image.new("RGB", (WIDTH, height), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((22, 22, WIDTH - 22, height - 22), radius=24, fill=PANEL, outline=GRID, width=2)
    draw.text((LEFT, 42), title, font=font(34, True, korean), fill=INK)
    draw.text((LEFT, 83), subtitle, font=font(18, False, korean), fill=MUTED)

    plot_width = WIDTH - LEFT - RIGHT
    for tick in range(0, 11):
        x = LEFT + round(plot_width * tick / 10)
        draw.line((x, TOP, x, height - BOTTOM), fill=GRID, width=1)
        ns = maximum * tick / 10 / 1000
        draw.text((x - 15, height - BOTTOM + 13), f"{ns:.0f}", font=font(15), fill=MUTED)
    draw.text((WIDTH - 76, height - BOTTOM + 13), "ns", font=font(15, True), fill=MUTED)

    for row, (signal, label, kind) in enumerate(labels):
        y0 = TOP + row * ROW_HEIGHT
        center = y0 + ROW_HEIGHT // 2
        draw.text((42, center - 13), label, font=font(18, True, korean), fill=INK)
        draw.line((LEFT, y0 + ROW_HEIGHT, WIDTH - RIGHT, y0 + ROW_HEIGHT), fill=GRID, width=1)
        identifier = ids[signal]
        events = all_changes.get(identifier, [])
        points = sorted(set([0, maximum] + [time for time, _ in events]))
        color = CYAN if kind == "bit" else MINT
        for start, end in zip(points, points[1:]):
            x1 = LEFT + round(plot_width * start / maximum)
            x2 = LEFT + round(plot_width * end / maximum)
            value = value_at(events, start)
            if kind == "bit":
                level = normalized(value)
                y = center - 17 if level == 1 else center + 17 if level == 0 else center
                draw.line((x1, y, x2, y), fill=color if level is not None else AMBER, width=3)
                next_value = value_at(events, end)
                next_level = normalized(next_value)
                if next_level != level and end != maximum:
                    next_y = center - 17 if next_level == 1 else center + 17 if next_level == 0 else center
                    draw.line((x2, y, x2, next_y), fill=color, width=3)
            else:
                draw.line((x1, center, x2, center), fill=color, width=4)
                integer = normalized(value)
                if x2 - x1 > 43:
                    if integer is None:
                        text = "X"
                    elif kind == "hex":
                        text = f"0x{integer:04X}"
                    else:
                        text = str(integer)
                    draw.text((x1 + 5, center - 27), text, font=font(14, True), fill=INK)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "PNG", optimize=True)


def main() -> None:
    common_en = [
        ("iClk", "Clock", "bit"),
        ("iRsn", "Reset_n", "bit"),
        ("iDataEn", "Input valid", "bit"),
        ("iData", "Input data", "hex"),
        ("iDelay", "Delay", "bus"),
        ("oDataEn", "Output valid", "bit"),
        ("oData", "Output data", "hex"),
    ]
    common_ko = [
        ("iClk", "클록", "bit"),
        ("iRsn", "리셋_n", "bit"),
        ("iDataEn", "입력 유효", "bit"),
        ("iData", "입력 데이터", "hex"),
        ("iDelay", "지연값", "bus"),
        ("oDataEn", "출력 유효", "bit"),
        ("oData", "출력 데이터", "hex"),
    ]
    cases = [
        (
            "01_shift_register_baseline/results/project1_waveform.vcd",
            "project1_waveform.png",
            "Project 1 · Shift-register regression",
            "Project 1 · 시프트 레지스터 회귀 검증",
            "Icarus Verilog 13.0 · 20 checks · PASS",
            "Icarus Verilog 13.0 · 20개 체크 · PASS",
        ),
        (
            "02_circular_queue_ppa/results/project2_waveform.vcd",
            "project2_waveform.png",
            "Project 2 · Architecture equivalence",
            "Project 2 · 아키텍처 등가성 검증",
            "Shift register = circular queue = reference · 26 checks · PASS",
            "시프트 레지스터 = 순환 큐 = 독립 참조 모델 · 26개 체크 · PASS",
        ),
        (
            "03_memory_based_dv/results/scenario3_waveform.vcd",
            "project3_scenario3_waveform.png",
            "Project 3 · Dynamic-delay file-driven DV",
            "Project 3 · 동적 지연 파일 기반 검증",
            "Scenario 3 · delay changes 3 → 5 · Checker PASS",
            "시나리오 3 · 지연값 3 → 5 변경 · Checker PASS",
        ),
    ]
    for source, name, en_title, ko_title, en_sub, ko_sub in cases:
        labels_en, labels_ko = common_en, common_ko
        if source.startswith("02_"):
            labels_en = common_en[:5] + [
                ("shift_oDataEn", "Shift valid", "bit"),
                ("shift_oData", "Shift data", "hex"),
                ("circular_oDataEn", "Queue valid", "bit"),
                ("circular_oData", "Queue data", "hex"),
            ]
            labels_ko = common_ko[:5] + [
                ("shift_oDataEn", "시프트 유효", "bit"),
                ("shift_oData", "시프트 데이터", "hex"),
                ("circular_oDataEn", "순환 큐 유효", "bit"),
                ("circular_oData", "순환 큐 데이터", "hex"),
            ]
        render(ROOT / source, ROOT / "docs/assets/en/results" / name, en_title, en_sub, labels_en, False)
        render(ROOT / source, ROOT / "docs/assets/ko/results" / name, ko_title, ko_sub, labels_ko, True)
        print(name)


if __name__ == "__main__":
    main()
