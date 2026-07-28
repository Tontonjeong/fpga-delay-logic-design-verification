@echo off
setlocal
cd /d "%~dp0.."

where vsim >nul 2>nul
if errorlevel 1 (
  echo [ERROR] vsim.exe was not found in PATH.
  echo Run this script from a ModelSim command prompt.
  exit /b 1
)

call modelsim\run_scenario1_batch.bat
if errorlevel 1 exit /b 1

call modelsim\run_scenario2_batch.bat
if errorlevel 1 exit /b 1

call modelsim\run_scenario3_batch.bat
if errorlevel 1 exit /b 1

echo.
echo All three scenarios completed.
exit /b 0
