@echo off
REM One-command launch on Windows: set up a local venv, install the one
REM dependency, start the hub, and open the dashboard in your browser.
cd /d "%~dp0"

if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate
pip install -q -r requirements.txt
python -m plant_memory hub
