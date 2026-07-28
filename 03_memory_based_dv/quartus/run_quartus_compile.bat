@echo off
setlocal
cd /d "%~dp0"
quartus_sh --flow compile memory_delay_logic
exit /b %errorlevel%
