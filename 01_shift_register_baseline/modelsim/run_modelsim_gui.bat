@echo off
setlocal
cd /d "%~dp0"
where vsim >nul 2>nul
if errorlevel 1 (
  echo [ERROR] vsim.exe was not found in PATH.
  echo Run this script from a ModelSim command prompt.
  exit /b 1
)
vsim -do run_sim.do
exit /b %errorlevel%
