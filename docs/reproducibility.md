# Reproducibility

## Verified open-source flow

Tested environment:

- Windows PowerShell
- Icarus Verilog `13.0 (stable) (v13_0)`
- Python 3.11+

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_all_verification.ps1
```

The command:

1. compiles the Project 1 self-checking baseline;
2. compiles the Project 2 shift/circular/reference equivalence regression;
3. compiles the Project 3 DUT, Input Driver, and Output Checker;
4. executes Project 3 scenarios 1–3;
5. writes compile logs, simulation logs, VCD files, and `results/verification_summary.json`.

Expected markers:

```text
[P1][PASS] checks=20 errors=0
[P2][PASS] checks=26 errors=0
[CHECKER][PASS] Scenario 1
[CHECKER][PASS] Scenario 2
[CHECKER][PASS] Scenario 3
VERIFICATION=PASS
```

Individual wrappers:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_project1.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_project2.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_project3.ps1
```

## Reference and repository checks

```text
python 03_memory_based_dv/scripts/generate_reference_vectors.py
python scripts/validate_repository.py
python scripts/check_pages_assets.py
```

## ModelSim/Questa flow

ModelSim Intel FPGA Starter Edition 10.5b was used for the original-archive
reruns. Questa 2024.1 is installed but fails license initialization on this
host. Project 1/2 original testbenches have no checker, so their successful
stimulus completion is not labeled PASS. Project 3 passes its original
Driver/Checker after the documented one-line instance-name compatibility fix.

## Quartus Prime Pro

The public projects target Agilex 5 `A5ED065BB32AE6SR0`. With matching device support installed:

```bat
01_shift_register_baseline\quartus\run_quartus_compile.bat
02_circular_queue_ppa\scripts\run_all_ppa.bat
03_memory_based_dv\quartus\run_quartus_compile.bat
```

On the verified host, Quartus Prime Pro 24.3.1 completed Project 1/3 synthesis
and all four Project 2 Fit/Timing/Power runs. The CSV collector and dependency-
free SVG chart generator reproduce the published tables from committed reports.
