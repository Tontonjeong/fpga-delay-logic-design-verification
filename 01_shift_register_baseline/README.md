# Project 1 — Shift Register Baseline

This baseline implements a programmable delay as parallel data and valid shift pipelines. It establishes the cycle semantics later preserved by the circular-addressed designs.

![Shift-register data and valid paths](../docs/assets/en/architecture/shift_register_block.svg)

## Problem

Delay a 16-bit input by a runtime-selected number of clocks while preserving exact alignment between the data word and its validity.

## Architecture

- `DATA_WIDTH=16`, `DEPTH=10`
- 3-bit `iDelay`, as defined by the supplied baseline interface
- active-low asynchronous reset `iRsn`
- `data_shift[0:DEPTH-1]` and `enable_shift[DEPTH-1:0]`
- `iDelay=N` selects stage `N-1`
- invalid outputs use `oDataEn=0` and `oData=0`

Every stage shifts on every enabled clock edge; the design is intentionally simple and serves as the architectural baseline.

## Key RTL

```systemverilog
for (stage = DEPTH-1; stage > 0; stage = stage - 1) begin
    data_shift[stage]   <= data_shift[stage-1];
    enable_shift[stage] <= enable_shift[stage-1];
end

oDataEn = enable_shift[iDelay-1];
oData   = enable_shift[iDelay-1] ? data_shift[iDelay-1] : '0;
```

## Verification

The supplied testbench drives:

1. asserted reset followed by release;
2. `16'h1001` through `16'h1006` with `iDelay=3`;
3. a runtime delay transition from 2 to 5.

The original testbench remains available for manual review. A separate portable self-checking regression now drives fixed delay, sparse valid traffic, and runtime tap changes against an independent reference pipeline.

| Evidence | Status |
|---|---|
| Supplied RTL/testbench | SHA-256 matched to the submitted ZIP |
| Original ModelSim 10.5b run | **COMPILE + STIMULUS COMPLETE** — 0 errors, 0 warnings, `$finish` at 310 ns |
| Icarus Verilog 13.0 functional regression | **PASS — 20 checks, 0 errors** |
| Original-run evidence | [transcript](../results/archive_rerun/project1_modelsim_original.log), [VCD](../results/archive_rerun/project1_original.vcd) |
| Supplemental self-check evidence | [log](results/project1_simulation.log), [VCD](results/project1_waveform.vcd) |
| Quartus Prime Pro 24.3.1 synthesis | **SUCCESS** — 0 errors, 1 warning, 85 estimated ALMs, 119 registers |

The original testbench contains stimulus but no assertion, scoreboard, or PASS marker.
Its run is therefore not relabeled as a functional PASS. The 20-check verdict
belongs to the separate repository regression and is presented as supplemental
verification.

## Reproduce

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_project1.ps1
```

From `01_shift_register_baseline/quartus` in a Quartus Prime Pro command prompt:

```bat
run_quartus_compile.bat
```

The supplied QSF uses Agilex 5 with `DEVICE AUTO`. Quartus 24.3 reports that
auto-selection is unsupported for this family and selects
`A5EC065BB32AE4S`; the untouched project then synthesizes successfully. This
device differs from Project 2, so the Project 1 estimates are not used in the
four-case PPA comparison.

## Limitations

- The 3-bit baseline interface cannot select delays above 7 even though `DEPTH` defaults to 10.
- The supplied scenarios use delays 2, 3, and 5; `iDelay=0` is not part of the baseline contract.
- Original and supplemental runs are kept as separate evidence layers.
- The synthesis report is evidence of RTL elaboration/resource estimation, not
  a board implementation or hardware measurement.

See [provenance](PROVENANCE.md) and the [expected waveform table](results/expected_waveform_table.csv).
