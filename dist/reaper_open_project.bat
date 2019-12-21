@echo off

REM Check 1st argument.
if "%1"=="" (
    echo Usage:
    echo reaper_recall_project.bat [Reaper Project^(rpp^) Path]
    echo Description:Open Reaper Project.
    echo.
    pause
    exit
)

REM Format REAPROJ path and check reaproject exists.
set REAPROJ=%1
set REAPROJ=%REAPROJ:"\"=%
set REAPROJ="%REAPROJ:\""=%"

if not exist %REAPROJ% (
    echo ERROR:
    echo Following reaproject path is not existed.
    echo %REAPROJ%
    echo.
    pause
    exit
)


REM Open reaper.exe with arg(reaproject path).
if exist "[Your reaper.exe install path]" (
    "[Your reaper.exe install path]" %REAPROJ%
) else if exist "C:/Program Files/REAPER (x64)" (
    "%ProgramFiles%/REAPER (x64)/reaper.exe" %REAPROJ%
    exit
) else if exist C:/REAPER (
    C:/REAPER/reaper.exe %REAPROJ%
    exit
) else (
    REM reaper.exe is not found:(
    echo ERROR:
    echo Reaper.exe is not found.
    echo Please make sure that Reaper exists in following folder or your original install path.
    echo.
    echo "(Normal) %ProgramFiles%\REAPER (x64)"
    echo "(Portable) C:\REAPER"
    echo.
    pause
)
