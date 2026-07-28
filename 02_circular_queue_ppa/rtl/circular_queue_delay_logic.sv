`timescale 1ns/1ps

// -----------------------------------------------------------------------------
// Circular Queue based programmable delay logic
// - iDelay = N: outputs the input/valid pair stored N clock edges earlier.
// - iDataEn gates the input slot.
// - oDataEn gates oData; invalid output slots are forced to zero.
// - The data memory is intentionally not reset. valid_mem is reset, so stale
//   memory contents can never be observed as valid data. This also allows the
//   storage array to map efficiently to FPGA memory resources.
// -----------------------------------------------------------------------------
module circular_queue_delay_logic #(
    parameter int DATA_WIDTH  = 16,
    parameter int DEPTH       = 10,
    parameter int PTR_WIDTH   = (DEPTH <= 2) ? 1 : $clog2(DEPTH),
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

    // The queue stores one data word and one valid bit per clock slot.
    // Quartus may infer distributed memory/MLAB depending on DEPTH and device.
    logic [DATA_WIDTH-1:0] data_mem [0:DEPTH-1];
    logic [DEPTH-1:0]      valid_mem;

    logic [PTR_WIDTH-1:0] write_ptr;
    logic [PTR_WIDTH-1:0] read_ptr;
    logic                 delay_is_valid;

    integer read_index_int;

    // Read address = current write pointer - iDelay (mod DEPTH).
    // write_ptr points to the slot that will receive the next input word.
    always_comb begin
        read_index_int = 0;
        read_ptr       = '0;
        delay_is_valid = 1'b0;

        if ((iDelay >= 1) && (iDelay <= DEPTH)) begin
            delay_is_valid = 1'b1;
            if (write_ptr >= iDelay) begin
                read_index_int = write_ptr - iDelay;
            end else begin
                read_index_int = write_ptr + DEPTH - iDelay;
            end
            read_ptr = read_index_int[PTR_WIDTH-1:0];
        end
    end

    // Circular write operation: only one queue entry is updated each clock.
    always_ff @(posedge iClk or negedge iRsn) begin
        if (!iRsn) begin
            write_ptr <= '0;
            valid_mem <= '0;
        end else begin
            data_mem[write_ptr]  <= iDataEn ? iData : '0;
            valid_mem[write_ptr] <= iDataEn;

            if (write_ptr == DEPTH-1) begin
                write_ptr <= '0;
            end else begin
                write_ptr <= write_ptr + 1'b1;
            end
        end
    end

    // Output gating: invalid queue slots never propagate stale data.
    always_comb begin
        oDataEn = 1'b0;
        oData   = '0;

        if (iRsn && delay_is_valid) begin
            oDataEn = valid_mem[read_ptr];
            oData   = valid_mem[read_ptr] ? data_mem[read_ptr] : '0;
        end
    end

endmodule
