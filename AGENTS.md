# Project rules

- Purpose: reproducible verification of three FPGA delay-logic designs.
- Main directories: project folders, `rtl`, `tb`, `vectors`, `scripts`, `results`.
- Preserve source-first evidence and simulator warnings; do not invent synthesis/PPA results.
- Verify with `python scripts/validate_repository.py` and `python scripts/run_verification.py`.
- Current base: `main` at `c6ad33984642281664b93f6208d8880467343ce5`.
