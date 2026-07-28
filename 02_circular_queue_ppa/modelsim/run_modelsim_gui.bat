@echo off
setlocal
cd /d "%~dp0"
where vsim >nul 2>nul
if errorlevel 1 (
  echo [ERROR] vsim.exe was not found in PATH.
  echo Open an Altera/ModelSim command prompt or add the ModelSim win64 folder to PATH.
  pause
  exit /b 1
)
vsim -do run_functional_sim.do
endlocal
