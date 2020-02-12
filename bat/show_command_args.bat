@echo off
setlocal enabledelayedexpansion

set num=0
echo -----Test WAAPI args (from %%APPDATA%%)-----
echo.
echo "%0"
echo.

if "%1"=="" echo arg is not found.

for %%i in (%*) do (
    set /a num = num + 1
    echo arg:!num! is %%i
)

echo -----   end of args   -----

pause