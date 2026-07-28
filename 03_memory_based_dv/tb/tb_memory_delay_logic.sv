`timescale 1ns/1ps

// -----------------------------------------------------------------------------
// Top-level verification environment
//   Input Driver -> DUT -> Output Checker
// -----------------------------------------------------------------------------
module tb_memory_delay_logic;

    localparam integer DATA_WIDTH  = 16;
    localparam integer DEPTH       = 10;
    localparam integer DELAY_WIDTH = $clog2(DEPTH + 1);
    localparam time    CLK_PERIOD  = 10ns;  // 100 MHz

    logic                   iClk;
    logic                   iRsn;
    logic                   iDataEn;
    logic [DATA_WIDTH-1:0]  iData;
    logic [DELAY_WIDTH-1:0] iDelay;
    logic                   oDataEn;
    logic [DATA_WIDTH-1:0]  oData;

    logic   driver_done;
    logic   checker_done;
    integer driven_cycle_count;
    integer error_count;
    integer compared_sample_count;
    integer actual_valid_count;
    integer scenario_id;

    initial begin
        iClk = 1'b0;
        forever #(CLK_PERIOD/2) iClk = ~iClk;
    end

    memory_delay_logic #(
        .DATA_WIDTH (DATA_WIDTH),
        .DEPTH      (DEPTH)
    ) dut (
        .iClk    (iClk),
        .iRsn    (iRsn),
        .iDataEn (iDataEn),
        .iData   (iData),
        .iDelay  (iDelay),
        .oDataEn (oDataEn),
        .oData   (oData)
    );

    input_driver #(
        .DATA_WIDTH (DATA_WIDTH),
        .DEPTH      (DEPTH)
    ) driver (
        .iClk               (iClk),
        .iRsn               (iRsn),
        .iDataEn            (iDataEn),
        .iData              (iData),
        .iDelay             (iDelay),
        .driver_done        (driver_done),
        .driven_cycle_count (driven_cycle_count)
    );

    output_checker #(
        .DATA_WIDTH (DATA_WIDTH)
    ) output_check (
        .iClk                  (iClk),
        .iRsn                  (iRsn),
        .oDataEn               (oDataEn),
        .oData                 (oData),
        .checker_done          (checker_done),
        .error_count           (error_count),
        .compared_sample_count (compared_sample_count),
        .actual_valid_count    (actual_valid_count)
    );

    initial begin : TEST_CONTROL
        if (!$value$plusargs("SCENARIO=%d", scenario_id))
            scenario_id = 2;

        $display("============================================================");
        $display(" Project 3: Memory Based Delay Logic Verification");
        $display(" Scenario %0d", scenario_id);
        $display("============================================================");

        wait (checker_done === 1'b1);
        #10;

        if (error_count == 0) begin
            $display("[TEST PASS] Scenario %0d completed without errors", scenario_id);
            $finish;
        end
        else begin
            $fatal(1, "[TEST FAIL] Scenario %0d, errors=%0d",
                   scenario_id, error_count);
        end
    end

    // Watchdog for malformed files or a stalled test.
    initial begin : WATCHDOG
        #500000;
        $fatal(1, "[WATCHDOG] Simulation timeout");
    end

    // Optional VCD output for batch activity/debug runs.
    initial begin : OPTIONAL_VCD
        if ($test$plusargs("DUMP_VCD")) begin
            $dumpfile("results/memory_delay_logic.vcd");
            $dumpvars(0, tb_memory_delay_logic);
        end
    end

endmodule
