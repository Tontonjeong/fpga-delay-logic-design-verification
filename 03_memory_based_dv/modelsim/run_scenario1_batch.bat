@echo off
cd /d "%~dp0.."
vsim -c -do "do modelsim/run_scenario1_batch.do"
exit /b %errorlevel%
