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

## Optional ModelSim/Questa flow

If `vsim`, `vlog`, `vlib`, and `vmap` are available, the original per-project ModelSim wrappers remain in each `modelsim/` directory. The committed PASS evidence in this repository was generated with Icarus Verilog, not ModelSim.

## Quartus Prime Pro

The public projects target Agilex 5 `A5ED065BB32AE6SR0`. With matching device support installed:

```bat
01_shift_register_baseline\quartus\run_quartus_compile.bat
02_circular_queue_ppa\scripts\run_all_ppa.bat
03_memory_based_dv\quartus\run_quartus_compile.bat
```

On the verified host, all queried Quartus executables were absent. The PPA batch and chart gate are present, but synthesis and numerical PPA remain **BLOCKED** until reports are generated.
