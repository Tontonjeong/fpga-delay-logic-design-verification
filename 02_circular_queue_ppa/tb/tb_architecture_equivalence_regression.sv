`timescale 1ns/1ps

// Portable equivalence regression for Project 2. Both implementations are
// checked against an independent transaction-history model.
module tb_architecture_equivalence_regression;
    localparam integer DATA_WIDTH = 16;
    localparam integer DEPTH = 10;
    localparam integer DELAY_WIDTH = 4;
    localparam time CLK_PERIOD = 10ns;

    logic iClk = 1'b0;
    logic iRsn = 1'b0;
    logic iDataEn = 1'b0;
    logic [DATA_WIDTH-1:0] iData = '0;
    logic [DELAY_WIDTH-1:0] iDelay = 4'd3;
    logic shift_oDataEn;
    logic [DATA_WIDTH-1:0] shift_oData;
    logic circular_oDataEn;
    logic [DATA_WIDTH-1:0] circular_oData;

    logic [DATA_WIDTH-1:0] reference_data [0:DEPTH-1];
    logic [DEPTH-1:0] reference_valid;
    integer checks = 0;
    integer errors = 0;
    integer stage;

    shift_register_delay_logic_ppa #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH),
        .DELAY_WIDTH(DELAY_WIDTH)
    ) shift_dut (
        .iClk(iClk), .iRsn(iRsn), .iDataEn(iDataEn), .iData(iData),
        .iDelay(iDelay), .oDataEn(shift_oDataEn), .oData(shift_oData)
    );

    circular_queue_delay_logic #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH),
        .DELAY_WIDTH(DELAY_WIDTH)
    ) circular_dut (
        .iClk(iClk), .iRsn(iRsn), .iDataEn(iDataEn), .iData(iData),
        .iDelay(iDelay), .oDataEn(circular_oDataEn), .oData(circular_oData)
    );

    always #(CLK_PERIOD/2) iClk = ~iClk;

    task automatic drive(
        input logic en,
        input logic [DATA_WIDTH-1:0] data,
        input logic [DELAY_WIDTH-1:0] delay_value
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
        if (iRsn) begin : CHECK_OUTPUTS
            logic expected_valid;
            logic [DATA_WIDTH-1:0] expected_data;
            expected_valid = ((iDelay >= 1) && (iDelay <= DEPTH)) ?
                             reference_valid[iDelay-1] : 1'b0;
            expected_data = expected_valid ? reference_data[iDelay-1] : '0;
            checks = checks + 1;

            if ((shift_oDataEn !== expected_valid) ||
                (shift_oData !== expected_data) ||
                (circular_oDataEn !== expected_valid) ||
                (circular_oData !== expected_data)) begin
                errors = errors + 1;
                $display(
                    "[P2][ERROR] check=%0d delay=%0d expected=%0b/%04h shift=%0b/%04h circular=%0b/%04h",
                    checks, iDelay, expected_valid, expected_data,
                    shift_oDataEn, shift_oData, circular_oDataEn, circular_oData
                );
            end
        end
    end

    initial begin
        $dumpfile("results/project2_waveform.vcd");
        $dumpvars(0, tb_architecture_equivalence_regression);

        repeat (3) @(negedge iClk);
        iRsn = 1'b1;

        drive(1'b1, 16'h1101, 4'd3);
        drive(1'b1, 16'h1102, 4'd3);
        drive(1'b1, 16'h1103, 4'd3);
        drive(1'b0, 16'h0000, 4'd3);
        drive(1'b1, 16'h2201, 4'd3);
        drive(1'b0, 16'h0000, 4'd3);

        // Exercise changing delays and a full-depth wrap.
        drive(1'b1, 16'h3301, 4'd2);
        drive(1'b1, 16'h3302, 4'd2);
        drive(1'b1, 16'h4401, 4'd5);
        drive(1'b0, 16'h0000, 4'd5);
        drive(1'b1, 16'h5501, 4'd10);
        drive(1'b1, 16'h5502, 4'd10);
        repeat (13) drive(1'b0, 16'h0000, 4'd10);

        @(posedge iClk);
        #2;
        if (errors == 0)
            $display("[P2][PASS] checks=%0d errors=0; shift and circular implementations match the reference model", checks);
        else
            $display("[P2][FAIL] checks=%0d errors=%0d", checks, errors);
        $finish_and_return(errors == 0 ? 0 : 1);
    end
endmodule
