`timescale 1ns/1ps

module tb_circular_queue_delay_logic;

    localparam int DATA_WIDTH  = 16;
    localparam int DEPTH       = 10;
    localparam int DELAY_WIDTH = 4;
    localparam time CLK_PERIOD = 10ns;

    logic                   iClk;
    logic                   iRsn;
    logic                   iDataEn;
    logic [DATA_WIDTH-1:0]  iData;
    logic [DELAY_WIDTH-1:0] iDelay;
    logic                   oDataEn;
    logic [DATA_WIDTH-1:0]  oData;

    circular_queue_delay_logic #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH),
        .PTR_WIDTH(4),
        .DELAY_WIDTH(DELAY_WIDTH)
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
        input logic [DELAY_WIDTH-1:0] delay_value
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
        iDelay  = 4'd3;

        // Scenario 1: reset asserted and then released
        repeat (3) @(negedge iClk);
        iRsn = 1'b1;
        drive_cycle(1'b0, 16'h0000, 4'd3);
        drive_cycle(1'b0, 16'h0000, 4'd3);

        // Scenario 2: continuous Enable input, fixed iDelay=3
        drive_cycle(1'b1, 16'h1001, 4'd3);
        drive_cycle(1'b1, 16'h1002, 4'd3);
        drive_cycle(1'b1, 16'h1003, 4'd3);
        drive_cycle(1'b1, 16'h1004, 4'd3);
        drive_cycle(1'b1, 16'h1005, 4'd3);
        drive_cycle(1'b1, 16'h1006, 4'd3);
        drive_cycle(1'b0, 16'h0000, 4'd3);
        drive_cycle(1'b0, 16'h0000, 4'd3);
        drive_cycle(1'b0, 16'h0000, 4'd3);
        drive_cycle(1'b0, 16'h0000, 4'd3);

        // Scenario 3: change delay during operation (iDelay=2 -> 5)
        drive_cycle(1'b1, 16'h2001, 4'd2);
        drive_cycle(1'b1, 16'h2002, 4'd2);
        drive_cycle(1'b1, 16'h2003, 4'd2);
        drive_cycle(1'b1, 16'h2004, 4'd2);
        drive_cycle(1'b1, 16'h3001, 4'd5);
        drive_cycle(1'b1, 16'h3002, 4'd5);
        drive_cycle(1'b1, 16'h3003, 4'd5);
        drive_cycle(1'b1, 16'h3004, 4'd5);
        repeat (7) drive_cycle(1'b0, 16'h0000, 4'd5);

        #20;
        $finish;
    end

endmodule
