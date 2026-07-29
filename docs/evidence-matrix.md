# Evidence Matrix

| Claim | Primary evidence | State |
|---|---|---|
| Project 1 aligns data and valid at a selected tap | [`delay_logic.sv`](../01_shift_register_baseline/rtl/delay_logic.sv) | Documented |
| Project 1 passes fixed, sparse-valid, and dynamic-delay traffic | [simulation log](../01_shift_register_baseline/results/project1_simulation.log), [VCD](../01_shift_register_baseline/results/project1_waveform.vcd) | **PASS — 20 checks** |
| Project 2 uses one-slot circular writes | [`circular_queue_delay_logic.sv`](../02_circular_queue_ppa/rtl/circular_queue_delay_logic.sv) | Documented |
| Project 2 shift and circular architectures match an independent history model | [equivalence log](../02_circular_queue_ppa/results/project2_simulation.log), [VCD](../02_circular_queue_ppa/results/project2_waveform.vcd) | **PASS — 26 checks** |
| Project 2 contains four common-condition Quartus cases | [`quartus/`](../02_circular_queue_ppa/quartus/) | **Fit complete — 4/4** |
| Project 2 numerical PPA exists | [CSV](../02_circular_queue_ppa/results/PPA_results.csv), [raw reports](../02_circular_queue_ppa/quartus/) | **COMPLETE** |
| Project 3 holds last valid data on invalid output cycles | [`memory_delay_logic.sv`](../03_memory_based_dv/rtl/memory_delay_logic.sv) | Documented |
| Project 3 parses input/config files | [`input_driver.sv`](../03_memory_based_dv/tb/input_driver.sv) | Documented |
| Project 3 checks data, valid, and count | [`output_checker.sv`](../03_memory_based_dv/tb/output_checker.sv) | Documented |
| Project 3 scenario 1 passes 8 cycles / 5 valid outputs | [console log](../03_memory_based_dv/results/scenario1_console.log) | **PASS** |
| Project 3 scenario 2 passes 14 cycles / 4 valid outputs | [console log](../03_memory_based_dv/results/scenario2_console.log) | **PASS** |
| Project 3 scenario 3 passes 17 cycles / 14 valid outputs | [console log](../03_memory_based_dv/results/scenario3_console.log), [VCD](../03_memory_based_dv/results/scenario3_waveform.vcd) | **PASS** |
| Quartus synthesis completed | [summary](../results/synthesis_summary.csv) and project reports | **SUCCESS — Projects 1–3** |

The consolidated machine-readable record is [`results/verification_summary.json`](../results/verification_summary.json).
