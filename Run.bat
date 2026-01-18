@echo off
setlocal enabledelayedexpansion

echo ---------------------------------------
echo Searching for Python in common folders...
echo ---------------------------------------

:: 1. Try the 'where' command first
for /f "delims=" %%i in ('where python 2^>nul') do (
    set "PY_PATH=%%i"
    goto :FOUND
)

:: 2. Check the standard User AppData folder (Most common)
set "SEARCH_PATH=%USERPROFILE%\AppData\Local\Programs\Python"
if exist "!SEARCH_PATH!" (
    for /d %%D in ("!SEARCH_PATH!\Python*") do (
        if exist "%%D\python.exe" (
            set "PY_PATH=%%D\python.exe"
            goto :FOUND
        )
    )
)

:: 3. Check Program Files
if exist "C:\Program Files\Python313\python.exe" (
    set "PY_PATH=C:\Program Files\Python313\python.exe"
    goto :FOUND
)

:NOTFOUND
echo [ERROR] Python is still not found.
echo 1. Please open the Python Installer again.
echo 2. Select 'Modify' or 'Repair'.
echo 3. ENSURE YOU CHECK 'Add Python to PATH'.
pause
exit

:FOUND
echo Success! Found Python at: !PY_PATH!
echo Launching AI Sales Analyst...
"!PY_PATH!" -m streamlit run Analysis.py
pause