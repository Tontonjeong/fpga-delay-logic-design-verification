# Codex handoff

Reactivation prompt: Read this file, inspect the simulator available on the machine, then rerun repository and HDL verification.

- Base branch/commit: `main` / `c6ad33984642281664b93f6208d8880467343ce5`.
- Migration branch: `migration/portable-contract-20260801`.
- Fresh-clone verification: repository PASS; Icarus project 1/2/3 PASS.
- Known warning: Icarus reports constant-select sensitivity limitations in two `always_*` processes.
- Next: retain warnings as evidence; use licensed simulator only when configured.
