transcript on
onerror {quit -code 1 -force}
if {[file exists work]} {
    vdel -lib work -all
}
vlib work
vmap work work

vlog -sv ../rtl/delay_logic.sv
vlog -sv ../tb/tb_delay_logic.sv

vsim -voptargs=+acc work.tb_delay_logic
do wave.do
run -all
wave zoom full
puts "Simulation completed. Verify scenarios 1-3 in the Wave window."
