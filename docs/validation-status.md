# Validation Status

Four evidence states are used consistently:

1. **Documented** — source and specification are present.
2. **Reference Validated** — Python-generated vectors are internally consistent.
3. **Simulation Verified** — ModelSim executed DUT and Checker with PASS.
4. **Synthesized / PPA Analyzed** — Quartus compilation and Power Analyzer completed.

| Project | RTL Source | Simulation | Synthesis | PPA |
|---|---|---|---|---|
| Project 1 | Documented from supplied source | Not rerun | Not rerun | N/A |
| Project 2 | Documented from supplied source | Not rerun | Not rerun | Automation ready; numerical results pending |
| Project 3 | Documented from supplied source | Not run | Not rerun | N/A |

Project 3 reference consistency:

| Scenario | Cycles | Valid outputs | State |
|---:|---:|---:|---|
| 1 | 8 | 5 | Reference Validated |
| 2 | 14 | 4 | Reference Validated |
| 3 | 17 | 14 | Reference Validated |

Evidence files are mapped in [evidence-matrix.md](evidence-matrix.md).

