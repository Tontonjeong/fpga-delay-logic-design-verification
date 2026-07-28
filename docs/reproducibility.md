# Reproducibility

## Open checks

Run from the repository root:

```text
python 03_memory_based_dv/scripts/generate_reference_vectors.py
python scripts/validate_repository.py
git diff --exit-code
```

The final `git diff` makes vector drift visible.

## ModelSim

Requirements:

- ModelSim available as `vsim` in `PATH`
- working directory preserved by the supplied batch wrappers

Commands:

```bat
01_shift_register_baseline\modelsim\run_modelsim_batch.bat
02_circular_queue_ppa\modelsim\run_modelsim_batch.bat
03_memory_based_dv\modelsim\run_all_batch.bat
```

For Project 3, inspect `results/scenario*_simulation.log` and the console for both PASS markers.

## Quartus Prime Pro

The public projects target Agilex 5 `A5ED065BB32AE6SR0`. The matching device support package must be installed.

Project 1:

```bat
01_shift_register_baseline\quartus\run_quartus_compile.bat
```

Project 2 four-case flow:

```bat
02_circular_queue_ppa\scripts\run_all_ppa.bat
```

Project 3:

```bat
03_memory_based_dv\quartus\run_quartus_compile.bat
```

The PPA batch creates reports first, then writes `PPA_results.csv`. Chart generation refuses missing or blank metrics.

