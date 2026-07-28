transcript on
do modelsim/compile.do
vsim -voptargs=+acc work.tb_memory_delay_logic +SCENARIO=1
do modelsim/wave.do
onfinish stop
run -all
wave zoom full
