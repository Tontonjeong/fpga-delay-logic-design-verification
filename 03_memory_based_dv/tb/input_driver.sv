`timescale 1ns/1ps

// -----------------------------------------------------------------------------
// File-based Input Driver
//   1) Parses Input.txt and separates data/valid sections by data_type tag.
//   2) Parses register.txt and applies the initial Delay plus optional DelayAt
//      events used by the delay-change scenario.
//   3) Drives one vector per clock while preserving invalid time slots.
// -----------------------------------------------------------------------------
module input_driver #(
    parameter integer DATA_WIDTH       = 16,
    parameter integer DEPTH            = 10,
    parameter integer DELAY_WIDTH      = (DEPTH <= 1) ? 1 : $clog2(DEPTH + 1),
    parameter integer MAX_VECTORS      = 1024,
    parameter integer MAX_DELAY_EVENTS = 32
) (
    input  logic                   iClk,
    output logic                   iRsn,
    output logic                   iDataEn,
    output logic [DATA_WIDTH-1:0]  iData,
    output logic [DELAY_WIDTH-1:0] iDelay,
    output logic                   driver_done,
    output integer                 driven_cycle_count
);

    logic [DATA_WIDTH-1:0] data_vector  [0:MAX_VECTORS-1];
    logic                  valid_vector [0:MAX_VECTORS-1];

    integer data_count;
    integer valid_count;

    integer delay_event_cycle [0:MAX_DELAY_EVENTS-1];
    logic [DELAY_WIDTH-1:0] delay_event_value [0:MAX_DELAY_EVENTS-1];
    integer delay_event_count;
    logic [DELAY_WIDTH-1:0] initial_delay;

    integer scenario_id;
    string  input_filename;
    string  register_filename;

    task automatic parse_input_file(input string filename);
        integer fd;
        integer status;
        integer section_id;
        integer parsed_number;
        string  line;
        string  data_type;
        string  stage_name;
        begin
            data_count  = 0;
            valid_count = 0;
            section_id  = 0;

            fd = $fopen(filename, "r");
            if (fd == 0)
                $fatal(1, "[INPUT DRIVER] Cannot open %s", filename);

            while (!$feof(fd)) begin
                line   = "";
                status = $fgets(line, fd);

                if ($sscanf(line, "tag: data_type=%s stage=%s", data_type, stage_name) == 2) begin
                    if (data_type == "data")
                        section_id = 1;
                    else if (data_type == "valid")
                        section_id = 2;
                    else
                        section_id = 0;
                end
                else if ($sscanf(line, "%d", parsed_number) == 1) begin
                    if (section_id == 1) begin
                        if (data_count >= MAX_VECTORS)
                            $fatal(1, "[INPUT DRIVER] Data vector overflow");
                        data_vector[data_count] = parsed_number[DATA_WIDTH-1:0];
                        data_count = data_count + 1;
                    end
                    else if (section_id == 2) begin
                        if (valid_count >= MAX_VECTORS)
                            $fatal(1, "[INPUT DRIVER] Valid vector overflow");
                        valid_vector[valid_count] = (parsed_number != 0);
                        valid_count = valid_count + 1;
                    end
                end
            end

            $fclose(fd);

            if (data_count == 0)
                $fatal(1, "[INPUT DRIVER] No data vectors in %s", filename);

            if (data_count != valid_count)
                $fatal(1,
                    "[INPUT DRIVER] Data/valid count mismatch: data=%0d valid=%0d",
                    data_count, valid_count);

            $display("[INPUT DRIVER] Loaded %0d input cycles from %s",
                     data_count, filename);
        end
    endtask

    task automatic parse_register_file(input string filename);
        integer fd;
        integer status;
        integer parsed_cycle;
        logic [31:0] parsed_word;
        string line;
        begin
            initial_delay    = 1;
            delay_event_count = 0;

            fd = $fopen(filename, "r");
            if (fd == 0)
                $fatal(1, "[INPUT DRIVER] Cannot open %s", filename);

            while (!$feof(fd)) begin
                line   = "";
                status = $fgets(line, fd);

                // Optional extension for scenario 3:
                // DelayAt <1-based input cycle> <hex delay value>
                if ($sscanf(line, "DelayAt %d %h", parsed_cycle, parsed_word) == 2) begin
                    if (delay_event_count >= MAX_DELAY_EVENTS)
                        $fatal(1, "[INPUT DRIVER] Delay event overflow");

                    delay_event_cycle[delay_event_count] = parsed_cycle;
                    delay_event_value[delay_event_count] = parsed_word[DELAY_WIDTH-1:0];
                    delay_event_count = delay_event_count + 1;
                end
                else if ($sscanf(line, "Delay %h", parsed_word) == 1) begin
                    initial_delay = parsed_word[DELAY_WIDTH-1:0];
                end
            end

            $fclose(fd);

            if ((initial_delay < 1) || (initial_delay > DEPTH))
                $fatal(1, "[INPUT DRIVER] Initial Delay %0d is outside 1..%0d",
                       initial_delay, DEPTH);

            $display("[INPUT DRIVER] Initial iDelay=%0d, scheduled changes=%0d",
                     initial_delay, delay_event_count);
        end
    endtask

    task automatic apply_delay_events(input integer input_cycle);
        integer event_index;
        begin
            for (event_index = 0;
                 event_index < delay_event_count;
                 event_index = event_index + 1) begin
                if (delay_event_cycle[event_index] == input_cycle) begin
                    iDelay = delay_event_value[event_index];
                    $display("[INPUT DRIVER] cycle=%0d, iDelay changed to %0d",
                             input_cycle, iDelay);
                end
            end
        end
    endtask

    initial begin : DRIVER_MAIN
        integer vector_index;

        iRsn               = 1'b0;
        iDataEn            = 1'b0;
        iData              = '0;
        iDelay             = '0;
        driver_done        = 1'b0;
        driven_cycle_count = 0;

        if (!$value$plusargs("SCENARIO=%d", scenario_id))
            scenario_id = 2;

        input_filename    = $sformatf("vectors/scenario%0d/Input.txt", scenario_id);
        register_filename = $sformatf("vectors/scenario%0d/register.txt", scenario_id);

        parse_input_file(input_filename);
        parse_register_file(register_filename);

        // Keep active-low reset asserted for three complete negative edges.
        repeat (3) @(negedge iClk);

        // Release reset and present vector 1 before the next rising edge.
        iRsn   = 1'b1;
        iDelay = initial_delay;

        for (vector_index = 0;
             vector_index < data_count;
             vector_index = vector_index + 1) begin
            apply_delay_events(vector_index + 1);
            iData   = data_vector[vector_index];
            iDataEn = valid_vector[vector_index];
            driven_cycle_count = vector_index + 1;
            @(negedge iClk);
        end

        // Flush the memory delay line. The checker decides the exact end point
        // from output.txt, while the driver supplies enough idle clocks.
        iData   = '0;
        iDataEn = 1'b0;
        repeat (DEPTH + 4) @(negedge iClk);

        driver_done = 1'b1;
        $display("[INPUT DRIVER] Scenario %0d drive completed", scenario_id);
    end

endmodule
