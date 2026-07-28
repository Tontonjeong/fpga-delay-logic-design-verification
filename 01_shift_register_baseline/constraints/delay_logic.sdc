# 100 MHz clock constraint
create_clock -name iClk -period 10.000 [get_ports {iClk}]
# iRsn is implemented as an asynchronous active-low reset.
set_false_path -from [get_ports {iRsn}]
