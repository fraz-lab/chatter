@echo off
REM ─────────────────────────────────────────────────────────────
REM run_clinet.bat — setup venv & run the Textual chat client
REM ─────────────────────────────────────────────────────────────

REM 1) Create virtual environment if missing
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo Creating virtual environment in .venv
    py -3 -m venv .venv
)

REM 2) Activate the venv
call .venv\Scripts\activate.bat

REM 3) Upgrade pip and install dependencies
echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
python -m pip install textual==0.15.0 
python -m pip install websockets

REM 4) Run the chat client
echo Starting chat client...
python client.py

REM 5) Pause so the window stays open after exit
echo.
echo Press any key to exit...
pause >nul
