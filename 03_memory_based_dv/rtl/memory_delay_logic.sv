`timescale 1ns/1ps

// -----------------------------------------------------------------------------
// Project 3 DUT: simple dual-port memory based delay logic
// - One write port: stores iData and iDataEn into the current time slot.
// - One read port : reads the slot located iDelay clocks behind write_ptr.
// - When the delayed valid bit is 0, oDataEn becomes 0 and oData holds the
//   most recently accepted output value. This matches the lecture reference
//   vector behavior (for example: 3, 4, 4, 6, 6, 6, 9).
// -----------------------------------------------------------------------------
module memory_delay_logic #(
    parameter integer DATA_WIDTH  = 16,
    parameter integer DEPTH       = 10,
    parameter integer ADDR_WIDTH  = (DEPTH <= 1) ? 1 : $clog2(DEPTH),
    parameter integer DELAY_WIDTH = (DEPTH <= 1) ? 1 : $clog2(DEPTH + 1)
) (
    input  logic                   iClk,
    input  logic                   iRsn,
    input  logic                   iDataEn,
    input  logic [DATA_WIDTH-1:0]  iData,
    input  logic [DELAY_WIDTH-1:0] iDelay,
    output logic                   oDataEn,
    output logic [DATA_WIDTH-1:0]  oData
);

    // The data array is coded as a simple dual-port RAM: one synchronous write
    // port and one synchronous read port. Quartus can map this array to device
    // memory resources when the selected device and synthesis settings allow.
    (* ramstyle = "MLAB" *) logic [DATA_WIDTH-1:0] data_mem [0:DEPTH-1];

    // Valid information is stored in parallel with the data time slots.
    logic valid_mem [0:DEPTH-1];

    logic [ADDR_WIDTH-1:0] write_ptr;
    logic [ADDR_WIDTH-1:0] read_addr;

    integer reset_index;

    // Calculate (write_ptr - iDelay) modulo DEPTH.
    function automatic [ADDR_WIDTH-1:0] calc_read_addr(
        input logic [ADDR_WIDTH-1:0]  wr_ptr,
        input logic [DELAY_WIDTH-1:0] delay_value
    );
        integer tmp_addr;
        integer wr_int;
        integer delay_int;
        begin
            wr_int    = wr_ptr;
            delay_int = delay_value;
            tmp_addr  = wr_int;

            if ((delay_int >= 1) && (delay_int <= DEPTH)) begin
                tmp_addr = wr_int - delay_int;
                if (tmp_addr < 0)
                    tmp_addr = tmp_addr + DEPTH;
            end

            calc_read_addr = tmp_addr[ADDR_WIDTH-1:0];
        end
    endfunction

    always_comb begin
        read_addr = calc_read_addr(write_ptr, iDelay);
    end

    // Write port and circular write-pointer control.
    always_ff @(posedge iClk or negedge iRsn) begin
        if (!iRsn) begin
            write_ptr <= '0;

            // Only the valid array requires deterministic reset. The data RAM
            // is ignored while its corresponding valid bit is 0.
            for (reset_index = 0; reset_index < DEPTH; reset_index = reset_index + 1)
                valid_mem[reset_index] <= 1'b0;
        end
        else begin
            valid_mem[write_ptr] <= iDataEn;

            // Input gating: invalid input cycles do not overwrite data_mem.
            if (iDataEn)
                data_mem[write_ptr] <= iData;

            if (write_ptr == DEPTH - 1)
                write_ptr <= '0;
            else
                write_ptr <= write_ptr + 1'b1;
        end
    end

    // Read port and output gating.
    always_ff @(posedge iClk or negedge iRsn) begin
        if (!iRsn) begin
            oDataEn <= 1'b0;
            oData   <= '0;
        end
        else if ((iDelay >= 1) && (iDelay <= DEPTH)) begin
            oDataEn <= valid_mem[read_addr];

            // Output gating: update oData only for a valid delayed sample.
            // Otherwise oData holds the previous valid value.
            if (valid_mem[read_addr])
                oData <= data_mem[read_addr];
        end
        else begin
            oDataEn <= 1'b0;
        end
    end

endmodule
