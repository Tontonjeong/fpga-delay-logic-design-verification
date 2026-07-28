@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0.."

where quartus_sh >nul 2>nul
if errorlevel 1 (
  echo [ERROR] quartus_sh.exe was not found in PATH.
  echo Run this file from the Quartus Prime Pro Command Prompt.
  echo Alternatively, add quartus\bin64 to the Windows PATH.
  pause
  exit /b 1
)

where quartus_pow >nul 2>nul
if errorlevel 1 (
  echo [ERROR] quartus_pow.exe was not found in PATH.
  pause
  exit /b 1
)

call :RUN_CASE circular_depth10
if errorlevel 1 goto :FAIL
call :RUN_CASE circular_depth100
if errorlevel 1 goto :FAIL
call :RUN_CASE shift_depth10
if errorlevel 1 goto :FAIL
call :RUN_CASE shift_depth100
if errorlevel 1 goto :FAIL

where python >nul 2>nul
if errorlevel 1 (
  echo [WARNING] Python was not found. Quartus reports are complete, but CSV collection was skipped.
) else (
  python scripts\collect_ppa_results.py
)

echo.
echo [DONE] Four compilation and vectorless Power Analyzer runs completed.
echo Results: results\PPA_results.csv
pause
exit /b 0

:RUN_CASE
set CASE=%~1
echo.
echo ==============================================================
echo [CASE] !CASE!
echo ==============================================================
pushd "quartus\!CASE!"
quartus_sh --flow compile !CASE!
if errorlevel 1 (
  popd
  exit /b 1
)
rem Same 100 MHz SDC and identical vectorless toggle assumptions for all cases.
quartus_pow !CASE! --no_input_file --default_input_io_toggle_rate=12.5%% --use_vectorless_estimation=on --default_toggle_rate=12.5%%
if errorlevel 1 (
  popd
  exit /b 1
)
popd
exit /b 0

:FAIL
echo.
echo [FAILED] Check the Quartus messages above.
pause
exit /b 1
