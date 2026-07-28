<p align="center">
  <img src="assets/hero/fpga_delay_logic_hero.svg" alt="시프트 레지스터에서 순환 큐와 메모리 기반 파일 검증으로 발전하는 FPGA Delay Logic 포트폴리오" width="100%">
</p>

# FPGA Programmable Delay Logic

[![Validate portfolio](https://github.com/Tontonjeong/fpga-delay-logic-design-verification/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/Tontonjeong/fpga-delay-logic-design-verification/actions/workflows/validate.yml)

**RTL Architecture · PPA Methodology · File-Driven Digital Verification**

Shift Register → Circular Queue → Memory-Based DUT
SystemVerilog · Icarus Verilog 13.0 · Quartus Project Automation · Python

[English README](README.md) · [한국어 Portfolio](https://tontonjeong.github.io/fpga-delay-logic-design-verification/) · [English Portfolio](https://tontonjeong.github.io/fpga-delay-logic-design-verification/en/) · [검증 Manifest](results/verification_summary.json)

## 결과 요약

하나의 programmable delay 규약을 세 단계로 발전시킨 FPGA RTL/DV 포트폴리오입니다.

1. **Shift Register Baseline** — data와 valid를 같은 깊이로 이동하고 `iDelay-1` 탭을 선택합니다.
2. **Circular Queue and PPA** — 매 클록 한 entry만 갱신하고 모듈로 읽기 주소를 계산합니다.
3. **Memory-Based File-Driven DV** — Input Driver, DUT, Output Checker로 data·valid·출력 개수를 검증합니다.

2026-07-29에 세 프로젝트를 **Icarus Verilog 13.0으로 실제 컴파일·실행**했습니다. Project 1은 20개 self-check, Project 2는 26개 아키텍처 등가성 체크, Project 3은 파일 시나리오 1–3에서 모두 PASS했습니다.

검증 호스트에는 Quartus가 없었습니다. 합성과 수치 PPA는 추정하지 않고 **BLOCKED**로 명시합니다.

## 핵심 수치

| 항목 | 실행 또는 문서 근거 |
|---|---|
| Architecture | 3단계: Shift Register, Circular Queue, Memory-Based DV |
| Functional Regression | 3/3 프로젝트 PASS |
| Self-check | Project 1 20개 + Project 2 26개 |
| File-driven DV | Project 3 3개 시나리오, 8/14/17 cycle 비교 |
| PPA Method | 동일 조건 4개 Quartus 구성, DEPTH 10/100 |
| Evidence | compile/simulation log, VCD, 파형 PNG, JSON manifest |

## Architecture Evolution

<picture>
  <source srcset="docs/assets/ko/architecture/architecture_evolution.svg" type="image/svg+xml">
  <img src="docs/assets/ko/architecture/architecture_evolution.png" alt="시프트 레지스터에서 순환 큐와 메모리 기반 파일 검증으로 이어지는 아키텍처 발전 과정" width="100%">
</picture>

| 단계 | 엔지니어링 초점 | 현재 근거 |
|---|---|---|
| [01 — Shift Register Baseline](01_shift_register_baseline/README.md) | cycle semantics, data/valid 정렬 | **PASS**, 20 checks, log + VCD |
| [02 — Circular Queue and PPA](02_circular_queue_ppa/README.md) | one-slot update, pointer wrap, 규모 비교 | **PASS**, 26 equivalence checks, log + VCD |
| [03 — Memory-Based File-Driven DV](03_memory_based_dv/README.md) | Driver/Checker, 동적 delay event | **PASS**, scenario 1–3, logs + VCD |

## 과제 브리프 재도식화

강의자료 5페이지를 해석해 한·영 8종 엔지니어링 구조도로 새로 그렸습니다. 원본 슬라이드 이미지는 공개하지 않았으며, 그림별 출처 매핑과 증거 경계는 [provenance manifest](docs/assets/architecture/diagram_provenance.yaml)에 기록했습니다.

<picture>
  <source srcset="docs/assets/ko/architecture/project1_shift_register_datapath.svg" type="image/svg+xml">
  <img src="docs/assets/ko/architecture/project1_shift_register_datapath.png" alt="Project 1 시프트 레지스터 데이터패스와 제어 로직 및 핵심 계약" width="100%">
</picture>

| Project | 검토용 구조도 |
|---|---|
| 1 | [데이터패스](docs/assets/ko/architecture/project1_shift_register_datapath.svg) · [self-checking TB](docs/assets/ko/architecture/project1_testbench_architecture.svg) · [예상 timing](docs/assets/ko/architecture/project1_expected_timing.svg) |
| 2 | [순환 큐](docs/assets/ko/architecture/project2_circular_queue_architecture.svg) · [아키텍처 비교](docs/assets/ko/architecture/project2_architecture_comparison.svg) · [통제 PPA matrix](docs/assets/ko/architecture/project2_ppa_matrix.svg) |
| 3 | [파일 기반 검증](docs/assets/ko/architecture/project3_file_driven_verification.svg) · [시나리오 실행 흐름](docs/assets/ko/architecture/project3_scenario_flow.svg) |

## 검증 상태

| Project | 기능 시뮬레이션 | 합성 | 수치 PPA | 근거 |
|---|---|---|---|---|
| Project 1 | **PASS** — Icarus 13.0, 20 checks | **BLOCKED** — Quartus 없음 | N/A | [log](01_shift_register_baseline/results/project1_simulation.log), [VCD](01_shift_register_baseline/results/project1_waveform.vcd) |
| Project 2 | **PASS** — 두 구현 + 독립 참조, 26 checks | **BLOCKED** — Quartus 없음 | **BLOCKED** — Fit/Timing/Power 보고서 없음 | [log](02_circular_queue_ppa/results/project2_simulation.log), [VCD](02_circular_queue_ppa/results/project2_waveform.vcd) |
| Project 3 | **PASS** — scenario 1–3, DUT + Checker | **BLOCKED** — Quartus 없음 | N/A | [results](03_memory_based_dv/results/), [manifest](results/verification_summary.json) |

Project 3 실제 실행 결과:

| Scenario | 비교 cycle | Valid output | 결과 |
|---:|---:|---:|---|
| 1 | 8 | 5 | `[CHECKER][PASS]` + `[TEST PASS]` |
| 2 | 14 | 4 | `[CHECKER][PASS]` + `[TEST PASS]` |
| 3 | 17 | 14 | `[CHECKER][PASS]` + `[TEST PASS]` |

근거 실행의 소스 대상은 커밋 `c356ade3998e36a76255b573aa9f93bbf274be3e`입니다.

## 실제 실행 파형

<p align="center">
  <img src="docs/assets/ko/results/project3_scenario3_waveform.png" alt="Project 3에서 delay가 3에서 5로 바뀌는 파일 기반 검증 PASS 파형" width="100%">
</p>

파형 PNG는 예상값을 다시 그린 그림이 아니라 커밋된 VCD에서 직접 렌더링했습니다. Project 1·2 파형은 [한국어 포트폴리오](https://tontonjeong.github.io/fpga-delay-logic-design-verification/)에서 함께 확인할 수 있습니다.

## 파일 기반 검증 구조

<picture>
  <source srcset="docs/assets/ko/verification/file_driven_dv_flow.svg" type="image/svg+xml">
  <img src="docs/assets/ko/verification/file_driven_dv_flow.png" alt="입력 파일과 레지스터 파일, Input Driver, DUT, Output Checker 검증 흐름" width="100%">
</picture>

Checker는 모든 참조 cycle의 data와 valid를 비교하고 실제 valid 출력 개수를 계산합니다. 오류가 있으면 sample 위치, 기대값, 실제값을 기록하며 최종 verdict를 차단합니다.

## PPA 경계

<picture>
  <source srcset="docs/assets/ko/ppa/ppa_comparison_matrix.svg" type="image/svg+xml">
  <img src="docs/assets/ko/ppa/ppa_comparison_matrix.png" alt="4개 구성 PPA 방법과 수치 결과 BLOCKED 상태" width="92%">
</picture>

Agilex 5 `A5ED065BB32AE6SR0`, 100 MHz, `BALANCED`, virtual pin, vectorless Power Analyzer, 12.5% toggle 가정으로 4개 구성을 준비했습니다. 하지만 호스트에서 Quartus 실행 파일을 찾지 못해 utilization, Fmax, timing closure, power, 아키텍처 우위 수치를 주장하지 않습니다.

## 재현

Icarus Verilog 13.0을 설치한 Windows PowerShell에서 저장소 루트 기준으로 실행합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_all_verification.ps1
```

세 프로젝트를 다시 컴파일·실행하고 로그, VCD, JSON manifest를 생성합니다. 세부 전제조건은 [재현 가이드](docs/reproducibility.md)를 참고하십시오.

## 공개 근거 원칙

- PASS는 실제 실행 로그에 해당 marker가 있을 때만 표시합니다.
- 리뷰 가능한 VCD와 파형 PNG를 함께 유지합니다.
- Icarus의 constant-select sensitivity 메시지는 비치명 경고이며 모든 checker가 error 0으로 종료했습니다.
- Quartus Fit/Timing/Power 보고서가 생기기 전까지 합성과 수치 PPA는 BLOCKED입니다.
- vectorless power는 향후 생성되더라도 보드 실측값이 아닙니다.

## 작성자

**Hyeongrok Ryu · 류형록**  
FPGA RTL Design and Digital Verification Portfolio
