@echo off
title Crypto Stock Analyzer - PRO Version
echo ========================================
echo Crypto Stock Analyzer - PRO Version
echo ========================================
echo.
echo Starting application...
echo.

python app.py

if errorlevel 1 (
    echo.
    echo Error: Python not found or missing dependencies
    echo Please ensure Python 3.8+ is installed
    pause
)

echo.
echo Application closed.