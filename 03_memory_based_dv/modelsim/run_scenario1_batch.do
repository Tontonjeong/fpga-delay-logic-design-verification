transcript on
do modelsim/compile.do
vsim -c work.tb_memory_delay_logic +SCENARIO=1
onfinish stop
run -all
quit -f
