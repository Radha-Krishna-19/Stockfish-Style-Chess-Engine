@echo off
REM Set PYTHONPATH to current directory for this session
set PYTHONPATH=.
REM Run pytest on tests folder with verbose output
pytest -v tests
REM Pause to keep window open so you can read output
pause
