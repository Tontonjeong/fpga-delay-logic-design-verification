transcript on

if {[file exists work]} {
    vdel -lib work -all
}

vlib work
vmap work work

vlog -sv rtl/memory_delay_logic.sv
vlog -sv tb/input_driver.sv
vlog -sv tb/output_checker.sv
vlog -sv tb/tb_memory_delay_logic.sv
