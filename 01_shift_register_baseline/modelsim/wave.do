quietly WaveActivateNextPane {} 0
add wave -divider {CLOCK / RESET}
add wave -logic sim:/tb_delay_logic/iClk
add wave -logic sim:/tb_delay_logic/iRsn
add wave -divider {INPUT}
add wave -logic sim:/tb_delay_logic/iDataEn
add wave -radix hexadecimal sim:/tb_delay_logic/iData
add wave -radix unsigned sim:/tb_delay_logic/iDelay
add wave -divider {OUTPUT}
add wave -logic sim:/tb_delay_logic/oDataEn
add wave -radix hexadecimal sim:/tb_delay_logic/oData
configure wave -namecolwidth 220
configure wave -valuecolwidth 120
configure wave -timelineunits ns
WaveRestoreZoom {0 ns} {320 ns}
