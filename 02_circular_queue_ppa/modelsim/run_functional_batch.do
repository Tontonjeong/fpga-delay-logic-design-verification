transcript on
if {[file exists work]} {vdel -lib work -all}
vlib work
vmap work work
vlog -sv ../rtl/circular_queue_delay_logic.sv
vlog -sv ../tb/tb_circular_queue_delay_logic.sv
vsim -c work.tb_circular_queue_delay_logic
run -all
quit -f
