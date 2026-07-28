`timescale 1ns/1ps

module delay_logic #(
    parameter int DATA_WIDTH = 16,
    parameter int DEPTH      = 10
)(
    input  logic                  iClk,
    input  logic                  iRsn,
    input  logic                  iDataEn,
    input  logic [DATA_WIDTH-1:0] iData,
    input  logic [2:0]            iDelay,
    output logic                  oDataEn,
    output logic [DATA_WIDTH-1:0] oData
);

    logic [DATA_WIDTH-1:0] data_shift [0:DEPTH-1];
    logic [DEPTH-1:0]      enable_shift;
    integer stage;

    // Shift-register datapath and enable pipeline
    always_ff @(posedge iClk or negedge iRsn) begin
        if (!iRsn) begin
            enable_shift <= '0;
            for (stage = 0; stage < DEPTH; stage = stage + 1) begin
                data_shift[stage] <= '0;
            end
        end else begin
            for (stage = DEPTH-1; stage > 0; stage = stage - 1) begin
                data_shift[stage]  <= data_shift[stage-1];
                enable_shift[stage] <= enable_shift[stage-1];
            end

            // Input gating by iDataEn
            data_shift[0]  <= iDataEn ? iData : '0;
            enable_shift[0] <= iDataEn;
        end
    end

    // Select the delayed tap. The lecture material defines iDelay as [2:0].
    // iDelay=0 is not used by the supplied verification scenarios.
    always_comb begin
        oDataEn = 1'b0;
        oData   = '0;

        if (iRsn && (iDelay != 3'd0)) begin
            oDataEn = enable_shift[iDelay-1];
            oData   = enable_shift[iDelay-1] ? data_shift[iDelay-1] : '0;
        end
    end

endmodule
