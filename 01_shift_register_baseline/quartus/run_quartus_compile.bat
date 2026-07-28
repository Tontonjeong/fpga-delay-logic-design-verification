@echo off
cd /d "%~dp0"
quartus_sh -t create_project.tcl
if errorlevel 1 goto :error
quartus_sh --flow compile delay_logic
if errorlevel 1 goto :error
echo.
echo Quartus compilation completed.
pause
exit /b 0
:error
echo.
echo Quartus command failed. Check PATH, license, and the installed Agilex 5 device package.
pause
exit /b 1
