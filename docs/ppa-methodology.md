# PPA Methodology

## Comparison matrix

![PPA comparison matrix](assets/en/ppa/ppa_comparison_matrix.svg)

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
- Power Analyzer: fixed default toggle method (`vectorless=off`)
- default input and internal toggle assumption: 12.5%

All four cases must use the same installed device, Quartus version, and power method. Results from different devices are not placed in one comparison table.

## Metrics

The collector looks for logic utilization/ALMs, registers, memory bits, memory blocks, Fmax, total power, core dynamic power, static power, and I/O power. It records report paths plus tool/device/method metadata.

## Current state

Quartus Prime Pro 24.3.1 is installed on the verified Windows host. The four cases are rerun from their QSF/SDC sources and only completed Fit, Timing Analyzer, and Power Analyzer reports are collected.

The supplied batch command combined `--use_vectorless_estimation=on` with `--default_toggle_rate`, which Quartus 24.3 rejects. Agilex 5 also reports that vectorless estimation is unsupported. The rerun therefore uses a controlled 12.5% default toggle rate with vectorless estimation disabled for every case.

[The machine-readable result table](../02_circular_queue_ppa/results/PPA_results.csv)
contains the exact values and report paths. All four builds meet the 100 MHz
constraint with positive setup and hold slack. Neither Circular Queue build
maps storage into a RAM block; its register-count advantage at depth 100 is
offset by higher ALM use and lower restricted Fmax.

## Interpretation boundary

The reports establish the implementation result for this RTL, device, and tool
version. They do not establish a universal architecture ranking. In particular:

- Project 2 uses an asynchronous indexed read and modulo-address expression,
  which did not infer RAM in these builds.
- Project 3 uses a different simple dual-port coding style and Quartus
  synthesis does infer `altdpram` as LUTRAM; that supports the conclusion that
  coding style matters, not that Project 3 and Project 2 are directly
  PPA-comparable.
- The Agilex 5 timing and power models are marked preliminary in the reports.
- Power values use fixed default activity and have Low estimation confidence;
  they are tool estimates, not measured board power.
