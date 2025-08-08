@echo off
if exist config.py (
    echo Starting client...
    python main.py
) else (
    echo config.py not found, running setup...
    python setup.py
)
pause
