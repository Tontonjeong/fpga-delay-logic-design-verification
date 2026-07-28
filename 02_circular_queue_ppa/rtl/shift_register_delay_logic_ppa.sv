`timescale 1ns/1ps

// -----------------------------------------------------------------------------
// Parameterized Shift Register delay logic used only for Project 1 vs Project 2
// PPA comparison. The functional behavior and stimulus are kept equivalent to
// circular_queue_delay_logic.
// -----------------------------------------------------------------------------
module shift_register_delay_logic_ppa #(
    parameter int DATA_WIDTH  = 16,
    parameter int DEPTH       = 10,
    parameter int DELAY_WIDTH = (DEPTH <= 1) ? 1 : $clog2(DEPTH + 1)
)(
    input  logic                   iClk,
    input  logic                   iRsn,
    input  logic                   iDataEn,
    input  logic [DATA_WIDTH-1:0]  iData,
    input  logic [DELAY_WIDTH-1:0] iDelay,
    output logic                   oDataEn,
    output logic [DATA_WIDTH-1:0]  oData
);

    logic [DATA_WIDTH-1:0] data_shift [0:DEPTH-1];
    logic [DEPTH-1:0]      valid_shift;
    integer stage;

    // Every stored word shifts each clock. This is the main source of the
    // dynamic-power difference compared with the circular queue architecture.
    always_ff @(posedge iClk or negedge iRsn) begin
        if (!iRsn) begin
            valid_shift <= '0;
            for (stage = 0; stage < DEPTH; stage = stage + 1) begin
                data_shift[stage] <= '0;
            end
        end else begin
            for (stage = DEPTH-1; stage > 0; stage = stage - 1) begin
                data_shift[stage]  <= data_shift[stage-1];
                valid_shift[stage] <= valid_shift[stage-1];
            end
            data_shift[0]  <= iDataEn ? iData : '0;
            valid_shift[0] <= iDataEn;
        end
    end

    always_comb begin
        oDataEn = 1'b0;
        oData   = '0;

        if (iRsn && (iDelay >= 1) && (iDelay <= DEPTH)) begin
            oDataEn = valid_shift[iDelay-1];
            oData   = valid_shift[iDelay-1] ? data_shift[iDelay-1] : '0;
        end
    end

endmodule
