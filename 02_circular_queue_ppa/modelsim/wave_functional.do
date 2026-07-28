quietly WaveActivateNextPane {} 0
add wave -divider {TOP INPUT/OUTPUT}
add wave -radix binary  sim:/tb_circular_queue_delay_logic/iClk
add wave -radix binary  sim:/tb_circular_queue_delay_logic/iRsn
add wave -radix binary  sim:/tb_circular_queue_delay_logic/iDataEn
add wave -radix hexadecimal sim:/tb_circular_queue_delay_logic/iData
add wave -radix unsigned sim:/tb_circular_queue_delay_logic/iDelay
add wave -radix binary  sim:/tb_circular_queue_delay_logic/oDataEn
add wave -radix hexadecimal sim:/tb_circular_queue_delay_logic/oData
add wave -divider {CIRCULAR QUEUE INTERNAL}
add wave -radix unsigned sim:/tb_circular_queue_delay_logic/dut/write_ptr
add wave -radix unsigned sim:/tb_circular_queue_delay_logic/dut/read_ptr
add wave -radix binary sim:/tb_circular_queue_delay_logic/dut/valid_mem
configure wave -namecolwidth 220
configure wave -valuecolwidth 120
configure wave -timelineunits ns
WaveRestoreZoom {0 ns} {420 ns}
