quietly WaveActivateNextPane {} 0

add wave -divider {CLOCK / RESET}
add wave sim:/tb_memory_delay_logic/iClk
add wave sim:/tb_memory_delay_logic/iRsn

add wave -divider {INPUT DRIVER}
add wave sim:/tb_memory_delay_logic/iDelay
add wave sim:/tb_memory_delay_logic/iDataEn
add wave -radix unsigned sim:/tb_memory_delay_logic/iData
add wave sim:/tb_memory_delay_logic/driver_done
add wave -radix unsigned sim:/tb_memory_delay_logic/driven_cycle_count

add wave -divider {DUT OUTPUT}
add wave sim:/tb_memory_delay_logic/oDataEn
add wave -radix unsigned sim:/tb_memory_delay_logic/oData

add wave -divider {DUT INTERNAL}
add wave -radix unsigned sim:/tb_memory_delay_logic/dut/write_ptr
add wave -radix unsigned sim:/tb_memory_delay_logic/dut/read_addr

add wave -divider {CHECKER}
add wave sim:/tb_memory_delay_logic/checker_done
add wave -radix unsigned sim:/tb_memory_delay_logic/compared_sample_count
add wave -radix unsigned sim:/tb_memory_delay_logic/actual_valid_count
add wave -radix unsigned sim:/tb_memory_delay_logic/error_count

configure wave -namecolwidth 260
configure wave -valuecolwidth 110
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -timelineunits ns
WaveRestoreZoom {0 ns} {250 ns}
