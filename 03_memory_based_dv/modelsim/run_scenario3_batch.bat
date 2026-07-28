@echo off
cd /d "%~dp0.."
vsim -c -do "do modelsim/run_scenario3_batch.do"
exit /b %errorlevel%
