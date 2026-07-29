# Validation Status

Evidence is reported as **PASS**, **FAIL**, **BLOCKED**, or **N/A**. A functional PASS requires an executed log; a configured project is not a synthesis or PPA result.

| Project | Functional simulation | Synthesis | Numerical PPA |
|---|---|---|---|
| Project 1 | **PASS** — supplemental Icarus 13.0, 20 checks | **SUCCESS** — Quartus 24.3.1, 85 estimated ALMs | N/A |
| Project 2 | **PASS** — shift/circular/reference equivalence, 26 checks | **SUCCESS** — four Fits | **COMPLETE** — timing + power reports |
| Project 3 | **PASS** — original Checker after one-line compatibility change | **SUCCESS** — `altdpram` inferred as LUTRAM | N/A |

Project 3 executed counts:

| Scenario | Compared cycles | Valid outputs | State |
|---:|---:|---:|---|
| 1 | 8 | 5 | PASS |
| 2 | 14 | 4 | PASS |
| 3 | 17 | 14 | PASS |

Simulators: `ModelSim Intel FPGA Starter Edition 10.5b`, `Icarus Verilog 13.0`

Execution date: `2026-07-29–30`

See [evidence-matrix.md](evidence-matrix.md) and [`results/verification_summary.json`](../results/verification_summary.json).
