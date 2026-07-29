# Source Provenance and Execution Boundary

This page separates the supplied archives, compatibility fixes, and supplemental verification. It prevents a generated regression from being presented as if it were the untouched assignment submission.

## Supplied archive audit

- Four ZIP packages were inspected with path-traversal, link, entry-count, member-size, and total-size guards.
- Result: 113 files, 3,125,872 uncompressed bytes, no nested ZIP.
- The public manifest omits local Windows paths and records archive/member SHA-256 values.
- The two Project 1 archives contain the same core RTL/testbench; the larger package also includes the final report and figures.

[Public source manifest](../results/source_manifest.csv)

## Evidence layers

| Layer | What ran | Meaning |
|---|---|---|
| Original archive | Untouched RTL and original testbench/batch scripts | Establishes whether the delivered package compiles and reaches the end of its stimulus |
| Compatibility patch | Original Project 3 testbench with one instance renamed from `checker` to `output_check` | Resolves a SystemVerilog reserved-word conflict; DUT, Driver, Checker, vectors, and expected data are unchanged |
| Supplemental self-check | Independent reference model and assertion-based regressions stored in this repository | Adds deterministic functional checks that the original Project 1/2 stimulus-only testbenches do not contain |
| Quartus implementation | Original Project 2 RTL/QSF/SDC under one device and one clock constraint | Provides measured synthesis, fit, timing, and power-estimation reports |

## Byte-level comparison

| Artifact | Supplied archive vs repository |
|---|---|
| Project 1 RTL | Identical — SHA-256 prefix `6F8EAB1FFEBA` |
| Project 1 original testbench | Identical — `ACD1C61F0CE2` |
| Project 2 RTL | Identical — `20A597E7B9C4` |
| Project 2 original testbench | Identical — `C79164129CF5` |
| Project 3 RTL | Identical — `B7AE8E17B796` |
| Project 3 Input Driver | Identical — `319215FCD646` |
| Project 3 Output Checker | Identical — `5771A6130AE4` |
| Project 3 top testbench | One-line compatibility difference only |

## Original-run findings

- Project 1 original testbench: ModelSim 10.5b compiled with 0 errors/0 warnings and reached `$finish` at 310 ns. It contains stimulus but no assertions, scoreboard, or PASS marker.
- Project 2 original testbench: ModelSim 10.5b compiled with 0 errors/0 warnings and reached `$finish` at 320 ns. It also contains stimulus but no functional checker.
- Project 3 original testbench: all three batch runs fail at compile time because `checker` is a reserved SystemVerilog keyword. The supplied `run_all_batch.bat` masks this failure and prints a completion message.
- Project 3 compatibility patch: scenarios 1–3 pass the original Driver/Checker and expected-vector comparisons.

The portfolio therefore labels Project 1/2 original runs as **COMPILE + STIMULUS COMPLETE**, not functional PASS. Functional PASS belongs to the supplemental self-check layer.

## Tool boundary

- Questa Intel FPGA Starter Edition 2024.1 is installed, but the local license environment does not initialize. Its failure is retained as a tool/license result.
- ModelSim Intel FPGA Starter Edition 10.5b is installed and runs the archive sources.
- Icarus Verilog 13.0 runs the supplemental portable regression.
- Quartus Prime Pro 24.3.1 runs synthesis, fitting, timing analysis, and power estimation.

Power Analyzer values are estimates under a fixed 12.5% default toggle assumption. They are not board measurements.
