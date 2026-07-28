# Limitations

- Questa/ModelSim and Quartus Prime Pro were not installed on the verification host.
- Functional regressions were executed with Icarus Verilog 13.0. The compiler emits a non-fatal constant-select sensitivity message for two `always_*` blocks; all self-checks completed with zero errors.
- No synthesis utilization, inferred-memory report, Fmax, timing-closure, or power value is published.
- Numerical Project 2 PPA is **BLOCKED** until complete Quartus Fit, Timing, and Power reports exist.
- Vectorless power, if later generated, is an estimate rather than board measurement.
- Project 1's 3-bit `iDelay` interface cannot represent all values of its default depth 10.
- The circular queue's asynchronous array read may map differently across device families and tool versions.
- Public CI does not replace local FPGA-tool execution.
- No open-source reuse license is granted.
