# Quartus: Tools -> Tcl Scripts -> create_project.tcl -> Run
package require ::quartus::project

set project_name delay_logic
set revision_name delay_logic

if {[is_project_open]} {
    project_close
}

project_new $project_name -revision $revision_name -overwrite
set_global_assignment -name FAMILY "Agilex 5"
set_global_assignment -name DEVICE A5ED065BB32AE6SR0
set_global_assignment -name TOP_LEVEL_ENTITY delay_logic
set_global_assignment -name SYSTEMVERILOG_FILE ../rtl/delay_logic.sv
set_global_assignment -name SDC_FILE ../constraints/delay_logic.sdc
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name NUM_PARALLEL_PROCESSORS ALL
set_global_assignment -name OPTIMIZATION_MODE "BALANCED"

foreach signal {iClk iRsn iDataEn {iData[*]} {iDelay[*]} oDataEn {oData[*]}} {
    set_instance_assignment -name VIRTUAL_PIN ON -to $signal
}

export_assignments
project_close
puts "Created delay_logic.qpf / delay_logic.qsf."
