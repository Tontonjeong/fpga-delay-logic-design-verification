#!/usr/bin/env python3
"""Maintain Korean SVG variants from the canonical English Pages assets."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
EN = ROOT / "docs/assets/en"
KO = ROOT / "docs/assets/ko"

EVIDENCE_UPDATES = {
    "architecture/architecture_evolution.svg": {
        "RTL + expected waveform": "Icarus regression · 20 checks PASS",
        "4-case Quartus workflow; data pending": "Equivalence PASS · Quartus PPA blocked",
        "3 reference scenarios validated": "3 DUT + Checker scenarios PASS",
    },
    "verification/file_driven_dv_flow.svg": {
        "Current evidence: Python Reference Vector Consistency PASS · DUT ModelSim execution pending":
            "Current evidence: Icarus Verilog 13.0 · Scenarios 1–3 · DUT + Checker PASS",
    },
    "ppa/ppa_comparison_matrix.svg": {
        "Method configured; numerical Quartus results pending. This is not a result chart.":
            "Workflow configured · Quartus unavailable on verification host · Numerical PPA BLOCKED",
    },
}

TRANSLATIONS = {
    "architecture/architecture_evolution.svg": {
        "Architecture evolution": "아키텍처 발전 과정",
        "Shift-register baseline evolves to circular queue PPA workflow and then memory-based file-driven verification.":
            "시프트 레지스터 기준 설계에서 순환 큐 PPA 흐름과 메모리 기반 파일 검증으로 발전합니다.",
        "Architecture Evolution": "아키텍처 발전 과정",
        "One delay contract, three engineering questions": "하나의 지연 규약, 세 가지 엔지니어링 질문",
        "01 · BASELINE RTL": "01 · 기준 RTL",
        "Shift Register": "시프트 레지스터",
        "02 · SCALABILITY / PPA": "02 · 확장성 / PPA",
        "Circular Queue": "순환 큐",
        "03 · FEATURED DV": "03 · 핵심 DV",
        "Memory-Based": "메모리 기반",
        "Driver + Checker": "Driver + Checker",
        "Question": "질문",
        "Evidence": "근거",
        "How do data and valid remain": "선택한 탭에서 데이터와 valid를",
        "cycle-aligned at a selected tap?": "어떻게 같은 사이클로 정렬하는가?",
        "Can one-entry updates scale better": "한 엔트리 갱신이 전체 stage 이동보다",
        "than whole-stage shifting?": "더 효율적으로 확장되는가?",
        "Can scenarios produce deterministic": "시나리오가 데이터·valid·개수·오류를",
        "data, valid, count, and errors?": "결정적으로 검증할 수 있는가?",
        "Icarus regression · 20 checks PASS": "Icarus 회귀 · 20개 체크 PASS",
        "Equivalence PASS · Quartus PPA blocked": "등가성 PASS · Quartus PPA 차단",
        "3 DUT + Checker scenarios PASS": "DUT + Checker 3개 시나리오 PASS",
    },
    "architecture/shift_register_block.svg": {
        "Shift-register delay logic block diagram": "시프트 레지스터 지연 로직 블록도",
        "Parallel DATA and VALID pipelines with an iDelay-selected tap.":
            "DATA와 VALID 병렬 파이프라인에서 iDelay로 탭을 선택합니다.",
        "Shift Register Baseline": "시프트 레지스터 기준 설계",
        "DATA": "데이터",
        "VALID": "유효",
        "stage 0": "단계 0",
        "stage 1": "단계 1",
        "stage N-1": "단계 N-1",
        "stage DEPTH-1": "단계 DEPTH-1",
        "valid 0": "valid 0",
        "valid 1": "valid 1",
        "valid N-1": "valid N-1",
        "valid DEPTH-1": "valid DEPTH-1",
        "Tap Select": "탭 선택",
        "Data and valid move through identical stage depth on every clock.":
            "데이터와 valid는 매 클록 동일한 단계 깊이로 이동합니다.",
    },
    "architecture/circular_queue_block.svg": {
        "Circular queue delay logic": "순환 큐 지연 로직",
        "One-slot write, modulo read address, and parallel valid memory.":
            "한 슬롯 쓰기, 모듈로 읽기 주소, 병렬 valid 메모리 구조입니다.",
        "Circular Queue Architecture": "순환 큐 아키텍처",
        "WRITE PORT": "쓰기 포트",
        "One slot updated per clock; pointer wraps.": "클록마다 한 슬롯을 갱신하고 포인터가 순환합니다.",
        "READ ADDRESS": "읽기 주소",
        "Valid range: 1..DEPTH": "유효 범위: 1..DEPTH",
        "Reset policy": "리셋 정책",
        "Reset valid_mem + write_ptr; do not reset data_mem.":
            "valid_mem과 write_ptr만 리셋하고 data_mem은 리셋하지 않습니다.",
        "Invalid slot: oDataEn=0 and oData=0 · stale data is blocked by valid_mem.":
            "무효 슬롯: oDataEn=0, oData=0 · valid_mem이 오래된 데이터를 차단합니다.",
    },
    "architecture/memory_delay_block.svg": {
        "Memory-based delay logic block diagram": "메모리 기반 지연 로직 블록도",
        "Synchronous write and read paths with output hold behavior on invalid cycles.":
            "동기식 쓰기/읽기 경로와 무효 사이클의 출력 유지 동작을 나타냅니다.",
        "Memory-Based Delay Logic": "메모리 기반 지연 로직",
        "INPUT": "입력",
        "SIMPLE DUAL-PORT STORE": "단순 듀얼 포트 저장소",
        "ADDRESS CONTROL": "주소 제어",
        "write_ptr advances every clock": "write_ptr은 매 클록 증가",
        "REGISTERED OUTPUT": "레지스터 출력",
        "if valid: oData ← data_mem": "valid이면: oData ← data_mem",
        "if invalid: hold last valid oData": "invalid이면: 마지막 유효 oData 유지",
        "Reset": "리셋",
        "clear valid state and pointers": "valid 상태와 포인터 초기화",
        "leave data_mem unreset": "data_mem은 리셋하지 않음",
    },
    "verification/file_driven_dv_flow.svg": {
        "File-driven digital verification flow": "파일 기반 디지털 검증 흐름",
        "Input and register files feed a driver, the DUT feeds a checker, and the output reference provides expected data and valid values.":
            "입력·레지스터 파일이 Driver를 구동하고, DUT 출력과 참조 파일을 Checker가 비교합니다.",
        "File-Driven Verification Architecture": "파일 기반 검증 아키텍처",
        "INPUT DRIVER": "입력 DRIVER",
        "parse → align → drive": "파싱 → 정렬 → 구동",
        "reset + scenario control": "리셋 + 시나리오 제어",
        "OUTPUT CHECKER": "출력 CHECKER",
        "data + valid + count": "데이터 + valid + 개수",
        "location / expected / actual": "위치 / 기대값 / 실제값",
        "Reference Vector": "참조 벡터",
        "Deterministic verdict": "결정적 판정",
        "Every reference cycle matches data and valid": "모든 참조 사이클의 데이터와 valid 비교",
        "Actual valid count equals expected valid count": "실제 valid 개수와 기대 개수 비교",
        "Final markers: [CHECKER][PASS] and [TEST PASS]": "최종 표식: [CHECKER][PASS], [TEST PASS]",
        "Current evidence: Icarus Verilog 13.0 · Scenarios 1–3 · DUT + Checker PASS":
            "현재 근거: Icarus Verilog 13.0 · 시나리오 1–3 · DUT + Checker PASS",
    },
    "ppa/ppa_comparison_matrix.svg": {
        "PPA comparison matrix": "PPA 비교 매트릭스",
        "Four Quartus configurations compare shift register and circular queue at depths 10 and 100 under common settings.":
            "동일 조건에서 깊이 10·100의 시프트 레지스터와 순환 큐 4개 구성을 비교합니다.",
        "Four-Case PPA Comparison": "4개 구성 PPA 비교",
        "Shift Register": "시프트 레지스터",
        "Circular Queue": "순환 큐",
        "baseline scale": "기준 규모",
        "routing / switching scale": "라우팅 / 스위칭 규모",
        "pointer overhead visible": "포인터 오버헤드 확인",
        "memory inference opportunity": "메모리 추론 가능성",
        "Common setup:": "공통 조건:",
        "Workflow configured · Quartus unavailable on verification host · Numerical PPA BLOCKED":
            "흐름 구성 완료 · 검증 호스트에 Quartus 없음 · 수치 PPA BLOCKED",
    },
}


def replace_all(text: str, replacements: dict[str, str]) -> str:
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def main() -> None:
    for relative, replacements in EVIDENCE_UPDATES.items():
        path = EN / relative
        path.write_text(replace_all(path.read_text(encoding="utf-8"), replacements), encoding="utf-8")
    for relative, replacements in TRANSLATIONS.items():
        source = EN / relative
        destination = KO / relative
        text = replace_all(source.read_text(encoding="utf-8"), replacements)
        text = text.replace(
            "Segoe UI, Arial, sans-serif",
            "Malgun Gothic, Apple SD Gothic Neo, sans-serif",
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        print(relative)


if __name__ == "__main__":
    main()
