`timescale 1ns/1ps

module tb_delay_logic;

    localparam int DATA_WIDTH = 16;
    localparam int DEPTH      = 10;
    localparam time CLK_PERIOD = 10ns;

    logic                  iClk;
    logic                  iRsn;
    logic                  iDataEn;
    logic [DATA_WIDTH-1:0] iData;
    logic [2:0]            iDelay;
    logic                  oDataEn;
    logic [DATA_WIDTH-1:0] oData;

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

    initial iClk = 1'b0;
    always #(CLK_PERIOD/2) iClk = ~iClk;

    task automatic drive_cycle(
        input logic                  en,
        input logic [DATA_WIDTH-1:0] data,
        input logic [2:0]            delay_value
    );
        begin
            @(negedge iClk);
            iDataEn = en;
            iData   = data;
            iDelay  = delay_value;
        end
    endtask

    initial begin
        iRsn    = 1'b0;
        iDataEn = 1'b0;
        iData   = '0;
        iDelay  = 3'd3;

        // Scenario 1: reset asserted and then released
        repeat (3) @(negedge iClk);
        iRsn = 1'b1;
        drive_cycle(1'b0, 16'h0000, 3'd3);
        drive_cycle(1'b0, 16'h0000, 3'd3);

        // Scenario 2: continuous Enable input, fixed iDelay=3
        drive_cycle(1'b1, 16'h1001, 3'd3);
        drive_cycle(1'b1, 16'h1002, 3'd3);
        drive_cycle(1'b1, 16'h1003, 3'd3);
        drive_cycle(1'b1, 16'h1004, 3'd3);
        drive_cycle(1'b1, 16'h1005, 3'd3);
        drive_cycle(1'b1, 16'h1006, 3'd3);
        drive_cycle(1'b0, 16'h0000, 3'd3);
        drive_cycle(1'b0, 16'h0000, 3'd3);
        drive_cycle(1'b0, 16'h0000, 3'd3);
        drive_cycle(1'b0, 16'h0000, 3'd3);

        // Scenario 3: change the delay value during operation (optional scenario)
        drive_cycle(1'b1, 16'h2001, 3'd2);
        drive_cycle(1'b1, 16'h2002, 3'd2);
        drive_cycle(1'b1, 16'h2003, 3'd2);
        drive_cycle(1'b1, 16'h2004, 3'd2);
        drive_cycle(1'b1, 16'h3001, 3'd5);
        drive_cycle(1'b1, 16'h3002, 3'd5);
        drive_cycle(1'b1, 16'h3003, 3'd5);
        drive_cycle(1'b1, 16'h3004, 3'd5);
        drive_cycle(1'b0, 16'h0000, 3'd5);
        drive_cycle(1'b0, 16'h0000, 3'd5);
        drive_cycle(1'b0, 16'h0000, 3'd5);
        drive_cycle(1'b0, 16'h0000, 3'd5);
        drive_cycle(1'b0, 16'h0000, 3'd5);
        drive_cycle(1'b0, 16'h0000, 3'd5);

        #20;
        $finish;
    end

endmodule
