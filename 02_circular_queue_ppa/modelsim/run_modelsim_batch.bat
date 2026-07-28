@echo off
setlocal
cd /d "%~dp0"
where vsim >nul 2>nul
if errorlevel 1 (
  echo [ERROR] vsim.exe was not found in PATH.
  pause
  exit /b 1
)
vsim -c -do run_functional_batch.do
endlocal
