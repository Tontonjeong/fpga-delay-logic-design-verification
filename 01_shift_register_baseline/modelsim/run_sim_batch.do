transcript file questa_batch_transcript.log
onerror {quit -code 1 -force}
if {[file exists work]} {
    vdel -lib work -all
}
vlib work
vmap work work
vlog -sv ../rtl/delay_logic.sv
vlog -sv ../tb/tb_delay_logic.sv
vsim -voptargs=+acc work.tb_delay_logic
run -all
quit -code 0 -force
