`timescale 1ns/1ps

// Four fixed-parameter top-level wrappers for identical Quartus/PPA flows.

module circular_depth10 (
    input  logic        iClk,
    input  logic        iRsn,
    input  logic        iDataEn,
    input  logic [15:0] iData,
    input  logic [3:0]  iDelay,
    output logic        oDataEn,
    output logic [15:0] oData
);
    circular_queue_delay_logic #(
        .DATA_WIDTH(16), .DEPTH(10), .PTR_WIDTH(4), .DELAY_WIDTH(4)
    ) u_dut (.*);
endmodule

module circular_depth100 (
    input  logic        iClk,
    input  logic        iRsn,
    input  logic        iDataEn,
    input  logic [15:0] iData,
    input  logic [6:0]  iDelay,
    output logic        oDataEn,
    output logic [15:0] oData
);
    circular_queue_delay_logic #(
        .DATA_WIDTH(16), .DEPTH(100), .PTR_WIDTH(7), .DELAY_WIDTH(7)
    ) u_dut (.*);
endmodule

module shift_depth10 (
    input  logic        iClk,
    input  logic        iRsn,
    input  logic        iDataEn,
    input  logic [15:0] iData,
    input  logic [3:0]  iDelay,
    output logic        oDataEn,
    output logic [15:0] oData
);
    shift_register_delay_logic_ppa #(
        .DATA_WIDTH(16), .DEPTH(10), .DELAY_WIDTH(4)
    ) u_dut (.*);
endmodule

module shift_depth100 (
    input  logic        iClk,
    input  logic        iRsn,
    input  logic        iDataEn,
    input  logic [15:0] iData,
    input  logic [6:0]  iDelay,
    output logic        oDataEn,
    output logic [15:0] oData
);
    shift_register_delay_logic_ppa #(
        .DATA_WIDTH(16), .DEPTH(100), .DELAY_WIDTH(7)
    ) u_dut (.*);
endmodule
