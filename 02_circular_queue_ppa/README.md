# Project 2 — Circular Queue and PPA Workflow

This project replaces whole-pipeline shifting with a circular time-slot store and prepares an apples-to-apples four-case Quartus PPA study.

![Circular queue write and read addressing](../docs/assets/en/architecture/circular_queue_block.svg)

## Problem

The shift-register baseline moves all stored data and valid bits every clock. The circular queue updates one slot per clock and reads the slot at `(write_ptr - iDelay) mod DEPTH`.

## Architecture

- 16-bit `data_mem` plus one `valid_mem` bit per slot
- circular `write_ptr`, wrapping at `DEPTH-1`
- `DELAY_WIDTH=$clog2(DEPTH+1)`
- valid delay range `1..DEPTH`
- invalid delay or invalid slot produces `oDataEn=0`, `oData=0`
- `data_mem` is not reset; reset clears `valid_mem` and `write_ptr`

The validity array prevents stale memory content from being exposed. Avoiding a data-array reset also removes a wide reset network and leaves memory inference available to Quartus, subject to the selected device and synthesis result.

## PPA Matrix

![Four-case PPA comparison matrix](../docs/assets/en/ppa/ppa_comparison_matrix.svg)

| Architecture | DEPTH | Top-level entity |
|---|---:|---|
| Shift Register | 10 | `shift_depth10` |
| Circular Queue | 10 | `circular_depth10` |
| Shift Register | 100 | `shift_depth100` |
| Circular Queue | 100 | `circular_depth100` |

Common constraints:

- Agilex 5 `A5ED065BB32AE6SR0`
- 100 MHz / 10 ns
- `BALANCED` optimization
- virtual pins
- vectorless power estimation
- 12.5% default toggle assumption

Collected fields include logic utilization/ALMs, registers, memory bits or blocks, Fmax, total power, core dynamic power, and static power.

## Current PPA Status

**PPA automation implemented · Numerical PPA BLOCKED because Quartus Fit/Timing/Power reports are unavailable.**

`results/PPA_results_template.csv` intentionally contains blank metric cells. No zero-filled chart, estimated improvement, or fabricated reduction percentage is published.

Structural expectations are not measurements:

- At `DEPTH=10`, pointer and address arithmetic may offset the circular queue's storage advantage.
- At `DEPTH=100`, shift-register switching and routing can grow substantially.
- If Quartus infers MLAB or another memory resource, register and ALM use may decrease.
- Only Fit, Timing Analyzer, and Power Analyzer reports can establish the actual result.

## Reproduce

Functional equivalence from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_project2.ps1
```

From a Quartus Prime Pro command prompt:

```bat
cd 02_circular_queue_ppa
scripts\run_all_ppa.bat
```

The batch flow compiles all four cases, runs vectorless Power Analyzer, and calls `scripts/collect_ppa_results.py`. After a complete CSV exists:

```text
python scripts/generate_ppa_charts.py
```

The chart script refuses incomplete data.

## Evidence and Limitations

| Evidence | Status |
|---|---|
| RTL and self-checking equivalence testbench | Source available |
| Four Quartus projects | Configured |
| Icarus Verilog 13.0 equivalence | **PASS — 26 checks, 0 errors** |
| Simulation evidence | [log](results/project2_simulation.log), [VCD](results/project2_waveform.vcd) |
| Quartus reports | **BLOCKED — Quartus unavailable** |
| Numerical PPA CSV | **BLOCKED** |

Expected-waveform PNGs are models of intended behavior, not ModelSim captures.
