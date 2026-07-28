`timescale 1ns/1ps

// Common activity generator for optional VCD-based power analysis.
// Compile with one of the following macros:
//   PPA_CIRCULAR_D10, PPA_CIRCULAR_D100, PPA_SHIFT_D10, PPA_SHIFT_D100
module tb_ppa_activity;
    logic        iClk;
    logic        iRsn;
    logic        iDataEn;
    logic [15:0] iData;
    logic        oDataEn;
    logic [15:0] oData;

`ifdef PPA_CIRCULAR_D10
    logic [3:0] iDelay;
    circular_depth10 dut (.*);
`elsif PPA_CIRCULAR_D100
    logic [6:0] iDelay;
    circular_depth100 dut (.*);
`elsif PPA_SHIFT_D10
    logic [3:0] iDelay;
    shift_depth10 dut (.*);
`elsif PPA_SHIFT_D100
    logic [6:0] iDelay;
    shift_depth100 dut (.*);
`else
    initial $error("Select one PPA_* macro when compiling tb_ppa_activity.sv");
`endif

    initial iClk = 1'b0;
    always #5 iClk = ~iClk; // 100 MHz

    int unsigned cycle_count;
    logic [15:0] lfsr;

    initial begin
        iRsn       = 1'b0;
        iDataEn    = 1'b0;
        iData      = 16'h0001;
        cycle_count = 0;
        lfsr       = 16'h1ACE;
`ifdef PPA_CIRCULAR_D100
        iDelay = 7'd50;
`elsif PPA_SHIFT_D100
        iDelay = 7'd50;
`else
        iDelay = 4'd5;
`endif
        repeat (5) @(negedge iClk);
        iRsn = 1'b1;

        // 2,000 equivalent clock cycles with identical activity for all designs.
        repeat (2000) begin
            @(negedge iClk);
            cycle_count = cycle_count + 1;
            // 75% valid activity, including regular idle slots.
            iDataEn = ((cycle_count % 4) != 0);
            lfsr = {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
            iData = lfsr;
        end

        repeat (120) begin
            @(negedge iClk);
            iDataEn = 1'b0;
            iData   = '0;
        end
        #20;
        $finish;
    end
endmodule
