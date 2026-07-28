`timescale 1ns/1ps

// Portable, self-checking regression for the supplied Project 1 RTL.
// The reference pipeline below is intentionally independent of the DUT state.
module tb_delay_logic_regression;
    localparam integer DATA_WIDTH = 16;
    localparam integer DEPTH = 10;
    localparam time CLK_PERIOD = 10ns;

    logic iClk = 1'b0;
    logic iRsn = 1'b0;
    logic iDataEn = 1'b0;
    logic [DATA_WIDTH-1:0] iData = '0;
    logic [2:0] iDelay = 3'd3;
    logic oDataEn;
    logic [DATA_WIDTH-1:0] oData;

    logic [DATA_WIDTH-1:0] reference_data [0:DEPTH-1];
    logic [DEPTH-1:0] reference_valid;
    integer checks = 0;
    integer errors = 0;
    integer stage;

    delay_logic #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH)
    ) dut (
        .iClk(iClk),
        .iRsn(iRsn),
        .iDataEn(iDataEn),
        .iData(iData),
        .iDelay(iDelay),
        .oDataEn(oDataEn),
        .oData(oData)
    );

    always #(CLK_PERIOD/2) iClk = ~iClk;

    task automatic drive(
        input logic en,
        input logic [DATA_WIDTH-1:0] data,
        input logic [2:0] delay_value
    );
        begin
            @(negedge iClk);
            iDataEn = en;
            iData = data;
            iDelay = delay_value;
        end
    endtask

    always @(posedge iClk) begin
        if (!iRsn) begin
            reference_valid = '0;
            for (stage = 0; stage < DEPTH; stage = stage + 1)
                reference_data[stage] = '0;
        end
        else begin
            for (stage = DEPTH-1; stage > 0; stage = stage - 1) begin
                reference_data[stage] = reference_data[stage-1];
                reference_valid[stage] = reference_valid[stage-1];
            end
            reference_data[0] = iDataEn ? iData : '0;
            reference_valid[0] = iDataEn;
        end

        #1;
        if (iRsn) begin
            checks = checks + 1;
            if ((iDelay == 0) ||
                (oDataEn !== reference_valid[iDelay-1]) ||
                (oData !== (reference_valid[iDelay-1] ?
                            reference_data[iDelay-1] : '0))) begin
                errors = errors + 1;
                $display(
                    "[P1][ERROR] check=%0d delay=%0d en=%0b data=%04h expected_en=%0b expected_data=%04h",
                    checks, iDelay, oDataEn, oData,
                    (iDelay == 0) ? 1'b0 : reference_valid[iDelay-1],
                    (iDelay == 0) ? 16'h0000 :
                        (reference_valid[iDelay-1] ? reference_data[iDelay-1] : '0)
                );
            end
        end
    end

    initial begin
        $dumpfile("results/project1_waveform.vcd");
        $dumpvars(0, tb_delay_logic_regression);

        repeat (3) @(negedge iClk);
        iRsn = 1'b1;

        // Fixed delay with continuous data.
        drive(1'b1, 16'h1001, 3'd3);
        drive(1'b1, 16'h1002, 3'd3);
        drive(1'b1, 16'h1003, 3'd3);
        drive(1'b1, 16'h1004, 3'd3);

        // Sparse valid traffic.
        drive(1'b0, 16'hDEAD, 3'd3);
        drive(1'b1, 16'h2001, 3'd3);
        drive(1'b0, 16'hBEEF, 3'd3);
        drive(1'b1, 16'h2002, 3'd3);

        // Runtime tap changes.
        drive(1'b1, 16'h3001, 3'd2);
        drive(1'b1, 16'h3002, 3'd2);
        drive(1'b1, 16'h4001, 3'd5);
        drive(1'b0, 16'h0000, 3'd5);
        repeat (7) drive(1'b0, 16'h0000, 3'd5);

        @(posedge iClk);
        #2;
        if (errors == 0)
            $display("[P1][PASS] checks=%0d errors=0", checks);
        else
            $display("[P1][FAIL] checks=%0d errors=%0d", checks, errors);
        $finish_and_return(errors == 0 ? 0 : 1);
    end
endmodule
