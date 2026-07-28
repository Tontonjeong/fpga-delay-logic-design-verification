# Design Decisions

## Data and valid are one transaction

Every architecture stores or shifts data and validity together. A delayed word is usable only when the validity state from the same time slot is asserted.

## Memory data is not reset

Projects 2 and 3 clear validity and pointer state but do not reset `data_mem`. This prevents stale data from becoming valid while avoiding a wide data reset network. Memory inference remains a possibility, not a claimed result, until Quartus Fit evidence exists.

## Delay range is explicit

Projects 2 and 3 accept `1..DEPTH`. Invalid delay values deassert `oDataEn`. The Project 1 interface remains the authored 3-bit baseline and its scenarios use 2, 3, and 5.

## Output semantics remain architecture-specific

Projects 1 and 2 force `oData=0` when invalid. Project 3 updates `oData` only on valid delayed samples, so invalid cycles hold the last valid word. This behavior is required by the supplied scenario 2 reference vector and is not normalized away.

## Reference and DUT evidence are separate

Python-generated vectors establish internal consistency. Only a ModelSim run of the SystemVerilog DUT and Checker can establish Simulation Verified status.

## PPA charts require complete data

The chart generator validates four rows, common tool/device/method metadata, and nonblank metrics. Without complete Quartus reports, the repository publishes the method matrix instead of numerical bars.

