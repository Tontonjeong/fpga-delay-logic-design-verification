# Evidence Matrix

| Claim | Source | Evidence state |
|---|---|---|
| Project 1 uses parallel data/valid shift stages | [`delay_logic.sv`](../01_shift_register_baseline/rtl/delay_logic.sv) | Documented |
| Project 1 covers reset, fixed delay, and delay change | [`tb_delay_logic.sv`](../01_shift_register_baseline/tb/tb_delay_logic.sv) | Documented |
| Project 1 waveform figure is expected behavior | [`expected_waveform_scenario1_2.png`](../01_shift_register_baseline/figures/expected_waveform_scenario1_2.png) | Expected waveform |
| Project 2 uses one-slot circular writes | [`circular_queue_delay_logic.sv`](../02_circular_queue_ppa/rtl/circular_queue_delay_logic.sv) | Documented |
| Project 2 contains four identical-condition Quartus cases | [`quartus/`](../02_circular_queue_ppa/quartus/) | Configured |
| Project 2 numerical PPA exists | No complete result CSV | Pending |
| Project 3 holds last valid data on invalid cycles | [`memory_delay_logic.sv`](../03_memory_based_dv/rtl/memory_delay_logic.sv) | Documented |
| Project 3 parses input/config files | [`input_driver.sv`](../03_memory_based_dv/tb/input_driver.sv) | Documented |
| Project 3 checks data, valid, and count | [`output_checker.sv`](../03_memory_based_dv/tb/output_checker.sv) | Documented |
| Scenario 1 has 8 cycles and 5 valid outputs | [`reference_summary.csv`](../03_memory_based_dv/results/reference_summary.csv) | Reference Validated |
| Scenario 2 has 14 cycles and 4 valid outputs | [`reference_summary.csv`](../03_memory_based_dv/results/reference_summary.csv) | Reference Validated |
| Scenario 3 has 17 cycles and 14 valid outputs | [`reference_summary.csv`](../03_memory_based_dv/results/reference_summary.csv) | Reference Validated |
| Project 3 ModelSim PASS | No local simulation log | Pending |
| Project 3 Quartus compilation | No local Quartus report | Pending |

