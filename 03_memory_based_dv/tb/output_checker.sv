`timescale 1ns/1ps

// -----------------------------------------------------------------------------
// File-based Output Checker
//   1) Parses output.txt reference data and valid sections.
//   2) Compares DUT oData/oDataEn on every checked clock.
//   3) Counts valid output samples and checks the final count.
// -----------------------------------------------------------------------------
module output_checker #(
    parameter integer DATA_WIDTH  = 16,
    parameter integer MAX_VECTORS = 2048
) (
    input  logic                  iClk,
    input  logic                  iRsn,
    input  logic                  oDataEn,
    input  logic [DATA_WIDTH-1:0] oData,
    output logic                  checker_done,
    output integer                error_count,
    output integer                compared_sample_count,
    output integer                actual_valid_count
);

    logic [DATA_WIDTH-1:0] expected_data  [0:MAX_VECTORS-1];
    logic                  expected_valid [0:MAX_VECTORS-1];

    integer expected_data_count;
    integer expected_valid_vector_count;
    integer expected_valid_count;

    integer scenario_id;
    string  output_filename;
    string  log_filename;

    task automatic parse_output_file(input string filename);
        integer fd;
        integer status;
        integer section_id;
        integer parsed_number;
        string  line;
        string  data_type;
        string  stage_name;
        begin
            expected_data_count         = 0;
            expected_valid_vector_count = 0;
            expected_valid_count        = 0;
            section_id                  = 0;

            fd = $fopen(filename, "r");
            if (fd == 0)
                $fatal(1, "[CHECKER] Cannot open %s", filename);

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
                        if (expected_data_count >= MAX_VECTORS)
                            $fatal(1, "[CHECKER] Expected data overflow");
                        expected_data[expected_data_count] = parsed_number[DATA_WIDTH-1:0];
                        expected_data_count = expected_data_count + 1;
                    end
                    else if (section_id == 2) begin
                        if (expected_valid_vector_count >= MAX_VECTORS)
                            $fatal(1, "[CHECKER] Expected valid overflow");
                        expected_valid[expected_valid_vector_count] = (parsed_number != 0);
                        if (parsed_number != 0)
                            expected_valid_count = expected_valid_count + 1;
                        expected_valid_vector_count = expected_valid_vector_count + 1;
                    end
                end
            end

            $fclose(fd);

            if (expected_data_count == 0)
                $fatal(1, "[CHECKER] No reference values in %s", filename);

            if (expected_valid_vector_count != expected_data_count)
                $fatal(1,
                    "[CHECKER] output.txt data/valid count mismatch: data=%0d valid=%0d",
                    expected_data_count, expected_valid_vector_count);

            $display("[CHECKER] Loaded %0d reference cycles, valid outputs=%0d",
                     expected_data_count, expected_valid_count);
        end
    endtask

    initial begin : CHECKER_MAIN
        integer sample_index;
        integer log_fd;

        checker_done         = 1'b0;
        error_count          = 0;
        compared_sample_count = 0;
        actual_valid_count   = 0;

        if (!$value$plusargs("SCENARIO=%d", scenario_id))
            scenario_id = 2;

        output_filename = $sformatf("vectors/scenario%0d/output.txt", scenario_id);
        log_filename    = $sformatf("results/scenario%0d_simulation.log", scenario_id);

        parse_output_file(output_filename);

        log_fd = $fopen(log_filename, "w");
        if (log_fd != 0) begin
            $fdisplay(log_fd, "Project 3 memory delay logic checker");
            $fdisplay(log_fd, "Scenario: %0d", scenario_id);
            $fdisplay(log_fd, "Reference cycles: %0d", expected_data_count);
        end

        // The first output.txt value corresponds to the first rising edge after
        // active-low reset is released by the Input Driver.
        wait (iRsn === 1'b1);

        for (sample_index = 0;
             sample_index < expected_data_count;
             sample_index = sample_index + 1) begin
            @(posedge iClk);
            #1;

            compared_sample_count = compared_sample_count + 1;

            if (oDataEn)
                actual_valid_count = actual_valid_count + 1;

            if (oData !== expected_data[sample_index]) begin
                error_count = error_count + 1;
                $display("[CHECKER][DATA ERROR] sample=%0d expected=%0d actual=%0d",
                         sample_index + 1, expected_data[sample_index], oData);
                if (log_fd != 0)
                    $fdisplay(log_fd,
                        "DATA ERROR sample=%0d expected=%0d actual=%0d",
                        sample_index + 1, expected_data[sample_index], oData);
            end

            if (oDataEn !== expected_valid[sample_index]) begin
                error_count = error_count + 1;
                $display("[CHECKER][VALID ERROR] sample=%0d expected=%0b actual=%0b",
                         sample_index + 1, expected_valid[sample_index], oDataEn);
                if (log_fd != 0)
                    $fdisplay(log_fd,
                        "VALID ERROR sample=%0d expected=%0b actual=%0b",
                        sample_index + 1, expected_valid[sample_index], oDataEn);
            end
        end

        // Explicit output-count check required by the assignment.
        if (actual_valid_count != expected_valid_count) begin
            error_count = error_count + 1;
            $display("[CHECKER][COUNT ERROR] expected valid outputs=%0d actual=%0d",
                     expected_valid_count, actual_valid_count);
            if (log_fd != 0)
                $fdisplay(log_fd,
                    "COUNT ERROR expected=%0d actual=%0d",
                    expected_valid_count, actual_valid_count);
        end

        if (compared_sample_count != expected_data_count) begin
            error_count = error_count + 1;
            $display("[CHECKER][SAMPLE COUNT ERROR] expected=%0d actual=%0d",
                     expected_data_count, compared_sample_count);
        end

        if (error_count == 0) begin
            $display("[CHECKER][PASS] Scenario %0d: %0d cycles, %0d valid outputs",
                     scenario_id, compared_sample_count, actual_valid_count);
            if (log_fd != 0)
                $fdisplay(log_fd,
                    "PASS cycles=%0d valid_outputs=%0d errors=0",
                    compared_sample_count, actual_valid_count);
        end
        else begin
            $display("[CHECKER][FAIL] Scenario %0d: errors=%0d",
                     scenario_id, error_count);
            if (log_fd != 0)
                $fdisplay(log_fd, "FAIL errors=%0d", error_count);
        end

        if (log_fd != 0)
            $fclose(log_fd);

        checker_done = 1'b1;
    end

endmodule
