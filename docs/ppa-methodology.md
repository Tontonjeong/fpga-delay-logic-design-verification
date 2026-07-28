# PPA Methodology

## Comparison matrix

![PPA comparison matrix](../assets/ppa/ppa_comparison_matrix.svg)

| Case | Architecture | DEPTH |
|---|---|---:|
| `shift_depth10` | Shift Register | 10 |
| `circular_depth10` | Circular Queue | 10 |
| `shift_depth100` | Shift Register | 100 |
| `circular_depth100` | Circular Queue | 100 |

## Controlled conditions

- FPGA family/device: Agilex 5 / `A5ED065BB32AE6SR0`
- clock: 100 MHz
- optimization: `BALANCED`
- I/O: virtual pins
- Power Analyzer: vectorless estimation
- default input and internal toggle assumption: 12.5%

All four cases must use the same installed device, Quartus version, and power method. Results from different devices are not placed in one comparison table.

## Metrics

The collector looks for logic utilization/ALMs, registers, memory bits, memory blocks, Fmax, total power, core dynamic power, static power, and I/O power. It records report paths plus tool/device/method metadata.

## Current state

Quartus Prime Pro is not available in the portfolio assembly environment. `PPA_results.csv` is therefore absent and `PPA_results_template.csv` remains blank. Numerical PPA results are pending.

## Interpretation boundary

The circular queue may update fewer storage bits per clock and may map to FPGA memory. Pointer/address logic can offset this at small depth. These are structural expectations only. Actual claims require Fit, Timing Analyzer, and Power Analyzer reports.

