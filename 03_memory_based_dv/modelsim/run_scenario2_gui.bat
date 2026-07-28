@echo off
cd /d "%~dp0.."
vsim -do "do modelsim/run_scenario2.do"
