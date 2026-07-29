# Limitations

- Questa 2024.1 is installed, but local license initialization fails. ModelSim
  Intel FPGA Starter Edition 10.5b runs the supplied sources.
- Supplemental functional regressions use Icarus Verilog 13.0. Its
  constant-select sensitivity message is non-fatal; all self-checks complete
  with zero errors.
- Quartus Prime Pro 24.3.1 produces Project 1/3 synthesis and complete Project 2
  Fit/Timing/Power reports.
- Agilex 5 vectorless estimation is unsupported in this tool build. The four
  power runs therefore use a fixed 12.5% default toggle assumption and have Low
  estimation confidence; they are not board measurements.
- Timing and power models are marked preliminary in the Agilex 5 reports.
- Project 1's 3-bit `iDelay` interface cannot represent all values of its default depth 10.
- The circular queue's asynchronous array read may map differently across device families and tool versions.
- Public CI does not replace local FPGA-tool execution.
- No open-source reuse license is granted.
