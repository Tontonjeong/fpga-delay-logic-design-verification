#!/usr/bin/env python3
"""Generate bilingual SVG diagrams redrawn from the three project briefs.

No source-slide pixels are copied. The diagrams combine the brief requirements
with repository RTL and evidence boundaries.
"""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).parents[1]
KO_DIR = ROOT / "docs/assets/ko/architecture"
EN_DIR = ROOT / "docs/assets/en/architecture"
PROVENANCE = ROOT / "docs/assets/architecture/diagram_provenance.yaml"

BG = "#07111f"
SURFACE = "#0f1d31"
SURFACE_2 = "#172943"
LINE = "#335273"
INK = "#f3f7ff"
MUTED = "#abc0d8"
CYAN = "#54c8ff"
MINT = "#5ee3c2"
AMBER = "#f7b84b"
VIOLET = "#a5a3ff"
RED = "#ff7187"


def text(x: int, y: int, value: str, size: int = 28, color: str = INK,
         weight: int = 500, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" '
        f'font-family="Inter,Pretendard,Malgun Gothic,Segoe UI,Arial,sans-serif">'
        f'{escape(value)}</text>'
    )


def multiline(x: int, y: int, lines: list[str], size: int = 24,
              color: str = MUTED, weight: int = 500, gap: int = 34,
              anchor: str = "start") -> str:
    parts = [
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" font-family="Inter,Pretendard,Malgun Gothic,Segoe UI,Arial,sans-serif">'
    ]
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else gap
        parts.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def box(x: int, y: int, w: int, h: int, title: str, body: list[str] | None = None,
        accent: str = CYAN, fill: str = SURFACE_2, title_size: int = 28) -> str:
    body = body or []
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" '
        f'stroke="{LINE}" stroke-width="2"/>',
        f'<rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{accent}"/>',
        text(x + 30, y + 48, title, title_size, INK, 750),
    ]
    if body:
        parts.append(multiline(x + 30, y + 86, body, 21, MUTED, 500, 31))
    return "".join(parts)


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = CYAN,
          label: str | None = None, dash: bool = False) -> str:
    dash_attr = ' stroke-dasharray="10 8"' if dash else ""
    parts = [
        f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="4" '
        f'fill="none" marker-end="url(#arrow)"{dash_attr}/>'
    ]
    if label:
        parts.append(text((x1 + x2) // 2, min(y1, y2) - 12, label, 20, color, 700, "middle"))
    return "".join(parts)


def base(title_value: str, subtitle: str, body: str, footer: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{escape(title_value)}</title>
<desc id="desc">{escape(subtitle)}</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#07111f"/><stop offset="1" stop-color="#0c1d34"/>
  </linearGradient>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{CYAN}"/>
  </marker>
  <filter id="shadow"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-opacity=".28"/></filter>
</defs>
<rect width="1600" height="900" fill="url(#bg)"/>
<circle cx="1450" cy="80" r="240" fill="#284f8c" opacity=".18"/>
<circle cx="80" cy="760" r="260" fill="#0b8f83" opacity=".11"/>
{text(70, 80, title_value, 45, INK, 850)}
{text(70, 120, subtitle, 22, MUTED, 500)}
<line x1="70" y1="148" x2="1530" y2="148" stroke="{LINE}" stroke-width="2"/>
{body}
<line x1="70" y1="846" x2="1530" y2="846" stroke="{LINE}" stroke-width="1"/>
{text(70, 878, footer, 18, MUTED, 500)}
</svg>
"""


def shift_datapath(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 1 · Shift Register 데이터패스" if ko else "Project 1 · Shift-Register Datapath"
    subtitle = "data와 valid가 같은 stage를 이동하고 iDelay가 출력 tap을 선택" if ko else "Data and valid advance together; iDelay selects the output tap"
    parts: list[str] = []
    parts.append(box(70, 230, 190, 190, "Input", ["iData[15:0]", "iDataEn", "iClk · iRsn"], MINT))
    stage_x = [360, 585, 810, 1035]
    for index, x in enumerate(stage_x):
        parts.append(box(x, 230, 170, 190, f"Stage {index}", ["data_q", "valid_q"], CYAN if index < 3 else VIOLET))
    parts.append(box(1280, 230, 240, 190, "Tap / MUX", ["oData", "oDataEn"], AMBER))
    parts.append(arrow(260, 325, 360, 325, MINT))
    for x1, x2 in zip(stage_x, stage_x[1:]):
        parts.append(arrow(x1 + 170, 325, x2, 325))
    parts.append(arrow(1205, 325, 1280, 325, VIOLET))
    parts.append(box(420, 480, 730, 160,
                     "Control Logic" if not ko else "제어 로직",
                     ["iDelay=N → tap[N−1]", "reset clears data_q and valid_q"],
                     VIOLET))
    parts.append(arrow(785, 480, 785, 430, VIOLET, "tap select"))
    note_title = "핵심 계약" if ko else "Core contract"
    note_body = (
        ["유효한 입력만 pipeline에 기록", "data/valid cycle alignment 유지", "iDelay 범위는 RTL parameter로 제한"]
        if ko else
        ["Only enabled inputs enter the pipeline", "Preserve cycle alignment of data and valid", "RTL parameters bound the legal iDelay range"]
    )
    parts.append(box(70, 670, 1450, 150, note_title, note_body, MINT, SURFACE, 24))
    footer = "Redrawn from Project 1 brief p.2 + repository RTL; not a source-slide capture."
    return base(title_value, subtitle, "".join(parts), footer)


def testbench_architecture(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 1 · Self-Checking 테스트벤치" if ko else "Project 1 · Self-Checking Testbench"
    subtitle = "동일 stimulus를 DUT와 독립 reference에 공급하고 cycle 단위로 비교" if ko else "Drive identical stimulus into DUT and an independent reference, then compare every cycle"
    p = [
        box(80, 265, 230, 180, "Stimulus", ["clock/reset", "data/valid", "dynamic delay"], MINT),
        box(475, 210, 300, 180, "Reference Model", ["cycle queue", "expected data", "expected valid"], VIOLET),
        box(475, 485, 300, 180, "RTL DUT", ["Shift Register", "data/valid pipe"], CYAN),
        box(955, 335, 300, 220, "Checker", ["expected vs actual", "count valid outputs", "fail on mismatch"], AMBER),
        box(1350, 350, 170, 190, "Result", ["PASS/FAIL", "log · VCD"], MINT),
        arrow(310, 330, 475, 300, MINT),
        arrow(310, 380, 475, 560, MINT),
        arrow(775, 300, 955, 405, VIOLET),
        arrow(775, 575, 955, 485, CYAN),
        arrow(1255, 445, 1350, 445, AMBER),
    ]
    note = (
        "강의안의 eye-checking 개념을 repository의 자동 self-checking regression 구조로 확장"
        if ko else
        "Extends the brief's eye-checking concept into the repository's automated self-checking regression"
    )
    p.append(box(170, 720, 1260, 90, "Evidence upgrade" if not ko else "검증 강화", [note], RED, SURFACE, 24))
    return base(title_value, subtitle, "".join(p),
                "Redrawn from Project 1 brief p.2; PASS claims require executed logs.")


def expected_timing(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 1 · 예상 타이밍 계약" if ko else "Project 1 · Expected Timing Contract"
    subtitle = "iDelay=3 예시: enable과 data가 같은 지연 후 출력에 정렬" if ko else "Example iDelay=3: enable and data emerge with identical latency"
    parts: list[str] = []
    x0, dx = 310, 120
    names = ["iClk", "iRsn", "iDataEn", "iData", "oDataEn", "oData"]
    y_rows = [240, 330, 420, 510, 600, 690]
    for name, y in zip(names, y_rows):
        parts.append(text(90, y + 10, name, 25, INK, 700))
        parts.append(f'<line x1="{x0}" y1="{y}" x2="1500" y2="{y}" stroke="{LINE}" stroke-width="2"/>')
    for i in range(10):
        x = x0 + i * dx
        parts.append(f'<line x1="{x}" y1="205" x2="{x}" y2="735" stroke="{LINE}" stroke-width="1" opacity=".6"/>')
        parts.append(text(x + 8, 195, str(i), 16, MUTED, 500))
    clock = [f"M{x0},{y_rows[0]}"]
    for i in range(10):
        x = x0 + i * dx
        clock.extend([f"L{x+dx//2},{y_rows[0]-30}", f"L{x+dx},{y_rows[0]}"])
    parts.append(f'<path d="{" ".join(clock)}" stroke="{CYAN}" stroke-width="4" fill="none"/>')
    parts.append(f'<path d="M{x0},{y_rows[1]-30} L{x0+dx},{y_rows[1]-30} L{x0+dx},{y_rows[1]} L1500,{y_rows[1]}" stroke="{RED}" stroke-width="4" fill="none"/>')
    def high_segment(row: int, start: int, end: int, color: str) -> str:
        y = y_rows[row]
        return f'<path d="M{x0},{y} L{x0+start*dx},{y} L{x0+start*dx},{y-34} L{x0+end*dx},{y-34} L{x0+end*dx},{y} L1500,{y}" stroke="{color}" stroke-width="4" fill="none"/>'
    parts.append(high_segment(2, 2, 5, MINT))
    parts.append(high_segment(4, 5, 8, AMBER))
    data_in = ["A", "B", "C"]
    data_out = ["A", "B", "C"]
    for idx, value in enumerate(data_in):
        x = x0 + (2 + idx) * dx
        parts.append(box(x + 6, y_rows[3] - 42, 105, 58, value, [], MINT, "#14382f", 22))
    for idx, value in enumerate(data_out):
        x = x0 + (5 + idx) * dx
        parts.append(box(x + 6, y_rows[5] - 42, 105, 58, value, [], AMBER, "#3c2b12", 22))
    parts.append(arrow(x0 + 2 * dx + 52, 475, x0 + 5 * dx + 52, 565, VIOLET, "3 cycles", True))
    note = (
        ["reset 동안 valid=0", "iDataEn pulse와 iData token이 3 cycle 뒤 함께 출력"]
        if ko else
        ["valid remains 0 during reset", "iDataEn pulses and data tokens reappear together three cycles later"]
    )
    parts.append(box(930, 690, 570, 140, "Interpretation" if not ko else "해석", note, VIOLET, SURFACE, 21))
    return base(title_value, subtitle, "".join(parts),
                "Conceptual timing redrawn from Project 1 requirements; executed VCD is published separately.")


def circular_queue(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 2 · Circular Queue 아키텍처" if ko else "Project 2 · Circular-Queue Architecture"
    subtitle = "한 슬롯 write + modulo read address로 programmable delay 구현" if ko else "Programmable delay using one-slot writes and a modulo read address"
    parts: list[str] = [
        box(70, 260, 250, 210, "Input", ["iData", "iDataEn", "iDelay"], MINT),
        box(430, 205, 590, 340, "data_mem / valid_mem", [], CYAN),
        box(1160, 260, 360, 210, "Output", ["oDataEn = valid_mem[read]", "oData updates only when valid"], AMBER),
        arrow(320, 350, 430, 350, MINT, "write"),
        arrow(1020, 350, 1160, 350, CYAN, "read"),
    ]
    cx, cy, r = 725, 375, 115
    for i in range(10):
        import math
        angle = -math.pi / 2 + i * 2 * math.pi / 10
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        parts.append(f'<circle cx="{x}" cy="{y}" r="28" fill="{SURFACE}" stroke="{CYAN}" stroke-width="2"/>')
        parts.append(text(x, y + 7, str(i), 18, INK, 700, "middle"))
    parts.append(text(cx, cy - 10, "DEPTH", 24, MUTED, 800, "middle"))
    parts.append(text(cx, cy + 28, "ring", 23, CYAN, 700, "middle"))
    parts.extend([
        box(240, 630, 480, 150, "Write pointer" if not ko else "쓰기 포인터",
            ["write_ptr = (write_ptr + 1) mod DEPTH", "one slot changes per cycle"], VIOLET),
        box(850, 630, 510, 150, "Read address" if not ko else "읽기 주소",
            ["read = (write_ptr - iDelay) mod DEPTH", "wrap-around is explicit"], AMBER),
        arrow(480, 630, 595, 525, VIOLET),
        arrow(1100, 630, 875, 525, AMBER),
    ])
    return base(title_value, subtitle, "".join(parts),
                "Project 2 brief p.1 + repository RTL; no synthesis result is implied.")


def architecture_comparison(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 2 · 구조 비교" if ko else "Project 2 · Architecture Comparison"
    subtitle = "같은 cycle contract, 다른 저장·선택 비용 구조" if ko else "Same cycle contract, different storage and selection cost structures"
    left_body = (
        ["DEPTH×(DATA+VALID) registers", "모든 stage가 shift", "tap mux로 iDelay 선택"]
        if ko else
        ["DEPTH×(DATA+VALID) registers", "Every stage shifts", "Tap mux selects iDelay"]
    )
    right_body = (
        ["DEPTH slots in data/valid memories", "cycle당 한 슬롯만 write", "modulo address로 read"]
        if ko else
        ["DEPTH slots in data/valid memories", "One slot written per cycle", "Modulo-addressed read"]
    )
    parts = [
        box(90, 220, 620, 390, "Shift Register", left_body, CYAN),
        box(890, 220, 620, 390, "Circular Queue", right_body, MINT),
    ]
    for i in range(5):
        x = 175 + i * 95
        parts.append(f'<rect x="{x}" y="440" width="68" height="68" rx="10" fill="{SURFACE}" stroke="{CYAN}" stroke-width="2"/>')
        parts.append(text(x + 34, 482, f"Q{i}", 18, INK, 700, "middle"))
        if i < 4:
            parts.append(arrow(x + 68, 474, x + 95, 474, CYAN))
    cx, cy = 1200, 475
    for i in range(8):
        import math
        a = i * 2 * math.pi / 8
        x, y = int(cx + 110 * math.cos(a)), int(cy + 110 * math.sin(a))
        parts.append(f'<circle cx="{x}" cy="{y}" r="28" fill="{SURFACE}" stroke="{MINT}" stroke-width="2"/>')
    comparison = (
        ["기능 등가성은 simulation으로 확인", "Area·Fmax·Power 우열은 Quartus report가 있어야 주장 가능"]
        if ko else
        ["Functional equivalence is checked in simulation", "Area, Fmax, and power advantages require Quartus reports"]
    )
    parts.append(box(230, 690, 1140, 120, "Evidence boundary" if not ko else "증거 경계",
                     comparison, AMBER, SURFACE, 24))
    return base(title_value, subtitle, "".join(parts),
                "Architecture redraw only. Numerical PPA remains BLOCKED because Quartus is unavailable.")


def ppa_matrix(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 2 · 4-Case PPA 매트릭스" if ko else "Project 2 · Four-Case PPA Matrix"
    subtitle = "동일 target·clock·optimization·toggle 가정에서 구조와 DEPTH만 비교" if ko else "Compare only architecture and DEPTH under identical constraints"
    parts: list[str] = []
    cols = [430, 910]
    rows = [270, 520]
    labels = [
        ("Shift Register · DEPTH 10", CYAN),
        ("Circular Queue · DEPTH 10", MINT),
        ("Shift Register · DEPTH 100", CYAN),
        ("Circular Queue · DEPTH 100", MINT),
    ]
    for index, (label, accent) in enumerate(labels):
        x = cols[index % 2]
        y = rows[index // 2]
        body = ["Logic / registers: BLOCKED", "Fmax / slack: BLOCKED", "Power: BLOCKED"]
        parts.append(box(x, y, 390, 180, label, body, accent))
    fixed = (
        ["Agilex 5 A5ED065BB32AE6SR0", "100 MHz · BALANCED · virtual pins", "Vectorless toggle assumption 12.5%"]
        if not ko else
        ["Agilex 5 A5ED065BB32AE6SR0", "100 MHz · BALANCED · virtual pins", "Vectorless toggle 가정 12.5%"]
    )
    parts.append(box(70, 270, 275, 430, "Fixed controls" if not ko else "고정 조건", fixed, VIOLET))
    parts.append(box(430, 745, 870, 72, "NUMERICAL RESULTS: BLOCKED — Quartus executables not found", [], RED, "#3a1721", 25))
    parts.append(box(1330, 320, 190, 360, "Required", ["Analysis & Synthesis", "Fitter", "Timing Analyzer", "Power Analyzer"], AMBER, SURFACE, 24))
    return base(title_value, subtitle, "".join(parts),
                "Project 2 brief p.1; this matrix records method readiness, not measured PPA.")


def file_driven_verification(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 3 · File-Driven Verification" if not ko else "Project 3 · 파일 기반 검증 구조"
    subtitle = "태그 기반 입력·레지스터·기대값을 Driver와 Checker가 소비" if ko else "Driver and Checker consume tagged stimulus, register, and expected-output files"
    parts = [
        box(70, 210, 235, 150, "input.txt", ["data records", "valid records"], MINT),
        box(70, 425, 235, 150, "register.txt", ["iDelay events"], VIOLET),
        box(70, 640, 235, 150, "output.txt", ["expected data", "expected valid"], AMBER),
        box(440, 300, 300, 250, "Input Driver", ["parse tags", "drive iData/iDataEn", "apply iDelay"], MINT),
        box(870, 300, 300, 250, "Memory DUT", ["data_mem", "valid_mem", "circular write_ptr"], CYAN),
        box(1290, 300, 240, 250, "Output Checker", ["cycle compare", "valid count", "deterministic errors"], AMBER),
        arrow(305, 285, 440, 360, MINT),
        arrow(305, 500, 440, 470, VIOLET),
        arrow(740, 425, 870, 425, CYAN),
        arrow(1170, 425, 1290, 425, CYAN),
        arrow(305, 715, 1290, 510, AMBER, "reference", True),
        box(520, 625, 650, 195, "Verdict" if not ko else "판정",
            ["expected == actual for every cycle", "valid-output count must also match", "[CHECKER][PASS] + [TEST PASS]"],
            MINT),
    ]
    return base(title_value, subtitle, "".join(parts),
                "Redrawn from Project 3 brief p.2 + implemented repository Driver/Checker.")


def scenario_flow(lang: str) -> str:
    ko = lang == "ko"
    title_value = "Project 3 · 시나리오 실행 흐름" if ko else "Project 3 · Scenario Execution Flow"
    subtitle = "동일 harness에서 reset, continuous enable, dynamic delay를 순차 검증" if ko else "One harness verifies reset release, continuous enable, and dynamic delay"
    items = [
        ("1", "Reset release" if not ko else "리셋 해제", ["clear state", "valid=0", "first delayed output"]),
        ("2", "Continuous enable" if not ko else "연속 enable", ["back-to-back tokens", "data/valid alignment", "no loss or duplication"]),
        ("3", "Dynamic delay" if not ko else "Delay 변경", ["register event", "new read address", "deterministic comparison"]),
    ]
    parts: list[str] = []
    xs = [100, 580, 1060]
    accents = [RED, CYAN, VIOLET]
    for (number, name, body), x, accent in zip(items, xs, accents):
        parts.append(f'<circle cx="{x+195}" cy="255" r="58" fill="{accent}" opacity=".95"/>')
        parts.append(text(x + 195, 270, number, 42, BG, 900, "middle"))
        parts.append(box(x, 345, 390, 280, name, body, accent))
    parts.extend([
        arrow(490, 485, 580, 485, CYAN),
        arrow(970, 485, 1060, 485, CYAN),
        box(315, 640, 970, 180, "Common checker" if not ko else "공통 Checker",
            ["cycle-by-cycle data/valid", "output count", "scenario-specific PASS marker"], MINT, SURFACE, 24),
    ])
    return base(title_value, subtitle, "".join(parts),
                "Project 3 brief pp.1–2; executed scenario counts are reported in verification_summary.json.")


GENERATORS = {
    "project1_shift_register_datapath.svg": shift_datapath,
    "project1_testbench_architecture.svg": testbench_architecture,
    "project1_expected_timing.svg": expected_timing,
    "project2_circular_queue_architecture.svg": circular_queue,
    "project2_architecture_comparison.svg": architecture_comparison,
    "project2_ppa_matrix.svg": ppa_matrix,
    "project3_file_driven_verification.svg": file_driven_verification,
    "project3_scenario_flow.svg": scenario_flow,
}

PROVENANCE_DATA = [
    ("project1_shift_register_datapath", "저전력 반도체 회로설계 - 프로젝트 1(상).pdf", "2",
     "Shift-register chain, iDelay tap, and data/valid interface redrawn against repository RTL."),
    ("project1_testbench_architecture", "저전력 반도체 회로설계 - 프로젝트 1(상).pdf", "2",
     "Brief testbench concept extended to the repository's automated Driver/reference/Checker evidence."),
    ("project1_expected_timing", "저전력 반도체 회로설계 - 프로젝트 1(상).pdf", "1-2",
     "Conceptual delay contract; executed timing evidence is the separately published VCD-derived waveform."),
    ("project2_circular_queue_architecture", "저전력 반도체 회로설계 - 프로젝트 2(상).pdf", "1",
     "Circular-queue requirement combined with implemented modulo-address RTL."),
    ("project2_architecture_comparison", "저전력 반도체 회로설계 - 프로젝트 2(상).pdf", "1",
     "Qualitative architecture comparison only; no numerical PPA claim."),
    ("project2_ppa_matrix", "저전력 반도체 회로설계 - 프로젝트 2(상).pdf", "1",
     "Four controlled cases from the brief; all numerical results remain BLOCKED without Quartus."),
    ("project3_file_driven_verification", "저전력 반도체 회로설계 - 프로젝트 3(상).pdf", "2",
     "input/register/output file roles redrawn against the implemented Driver and Checker."),
    ("project3_scenario_flow", "저전력 반도체 회로설계 - 프로젝트 3(상).pdf", "1-2",
     "Three required scenarios organized around the repository's common checker and PASS markers."),
]


def write_provenance() -> None:
    lines = [
        "# Architecture diagram provenance",
        "# Original lecture-slide images are not included in this public repository.",
        "# Every diagram is a clean-room redraw, not a source-slide capture.",
        "diagrams:",
    ]
    for stem, source, pages, note in PROVENANCE_DATA:
        lines.extend([
            f"  - id: {stem}",
            f'    source_document: "{source}"',
            f'    source_page: "{pages}"',
            f"    output_ko: ../ko/architecture/{stem}.svg",
            f"    output_en: ../en/architecture/{stem}.svg",
            "    transformation: clean-room redraw",
            f'    evidence_boundary: "{note}"',
            "    source_slide_pixels_published: false",
        ])
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    KO_DIR.mkdir(parents=True, exist_ok=True)
    EN_DIR.mkdir(parents=True, exist_ok=True)
    for filename, generator in GENERATORS.items():
        (KO_DIR / filename).write_text(generator("ko"), encoding="utf-8")
        (EN_DIR / filename).write_text(generator("en"), encoding="utf-8")
    write_provenance()
    print(f"LECTURE_DIAGRAMS=PASS bilingual={len(GENERATORS) * 2} provenance={PROVENANCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
