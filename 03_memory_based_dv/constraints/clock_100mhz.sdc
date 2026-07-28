create_clock -name iClk -period 10.000 [get_ports {iClk}]
set_false_path -from [get_ports {iRsn}]
