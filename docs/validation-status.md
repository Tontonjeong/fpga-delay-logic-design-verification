# Validation Status

Evidence is reported as **PASS**, **FAIL**, **BLOCKED**, or **N/A**. A functional PASS requires an executed log; a configured project is not a synthesis or PPA result.

| Project | Functional simulation | Synthesis | Numerical PPA |
|---|---|---|---|
| Project 1 | **PASS** — Icarus Verilog 13.0, 20 checks | **BLOCKED** — Quartus unavailable | N/A |
| Project 2 | **PASS** — shift/circular/reference equivalence, 26 checks | **BLOCKED** — Quartus unavailable | **BLOCKED** — no Fit/Timing/Power reports |
| Project 3 | **PASS** — file scenarios 1–3, Checker + Test markers | **BLOCKED** — Quartus unavailable | N/A |

Project 3 executed counts:

| Scenario | Compared cycles | Valid outputs | State |
|---:|---:|---:|---|
| 1 | 8 | 5 | PASS |
| 2 | 14 | 4 | PASS |
| 3 | 17 | 14 | PASS |

Simulator: `Icarus Verilog version 13.0 (stable) (v13_0)`

Execution date: `2026-07-29`

Source commit tested: `c356ade3998e36a76255b573aa9f93bbf274be3e`

See [evidence-matrix.md](evidence-matrix.md) and [`results/verification_summary.json`](../results/verification_summary.json).
