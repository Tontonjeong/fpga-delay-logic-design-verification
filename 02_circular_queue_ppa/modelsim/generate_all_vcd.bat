@echo off
setlocal
cd /d "%~dp0"
where vsim >nul 2>nul
if errorlevel 1 (
  echo [ERROR] vsim.exe was not found in PATH.
  pause
  exit /b 1
)
echo [VCD] circular_depth10
vsim -c -do vcd_circular_depth10.do
if errorlevel 1 exit /b 1
echo [VCD] circular_depth100
vsim -c -do vcd_circular_depth100.do
if errorlevel 1 exit /b 1
echo [VCD] shift_depth10
vsim -c -do vcd_shift_depth10.do
if errorlevel 1 exit /b 1
echo [VCD] shift_depth100
vsim -c -do vcd_shift_depth100.do
if errorlevel 1 exit /b 1
echo [DONE] Four VCD files were generated in ..\results.
pause
endlocal
