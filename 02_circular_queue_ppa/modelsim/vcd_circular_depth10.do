transcript on
if {[file exists work]} {vdel -lib work -all}
vlib work
vmap work work
vlog -sv ../rtl/circular_queue_delay_logic.sv
vlog -sv ../rtl/shift_register_delay_logic_ppa.sv
vlog -sv ../rtl/ppa_top_wrappers.sv
vlog -sv +define+PPA_CIRCULAR_D10 ../tb/tb_ppa_activity.sv
vsim -voptargs=+acc work.tb_ppa_activity
vcd file ../results/circular_depth10.vcd
vcd add -r sim:/tb_ppa_activity/dut/*
run -all
vcd flush
quit -f
