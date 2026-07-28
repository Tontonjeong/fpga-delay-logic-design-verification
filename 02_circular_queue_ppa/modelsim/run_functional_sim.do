transcript on
if {[file exists work]} {vdel -lib work -all}
vlib work
vmap work work
vlog -sv ../rtl/circular_queue_delay_logic.sv
vlog -sv ../tb/tb_circular_queue_delay_logic.sv
vsim -voptargs=+acc work.tb_circular_queue_delay_logic
do wave_functional.do
run -all
wave zoom full
