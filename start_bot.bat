@echo off
title OLX Gadgets 24/7 Telegram Bot
color 0A
chcp 65001 > nul

echo ========================================================
echo   OLX GADGETS TELEGRAM BOT 24/7 (APPLE, SAMSUNG, LAPTOPS)
echo ========================================================
echo.
echo Python tekshirilmoqda...
python --version
if %errorlevel% neq 0 (
    echo [XATOLIK] Python topilmadi! Iltimos, Python o'rnating.
    pause
    exit /b
)

echo.
echo Kerakli kutubxonalar tekshirilmoqda...
python -m pip install -r requirements.txt --quiet

echo.
echo [OK] Bot 24/7 nazorat rejimida ishga tushirilmoqda...
python runner.py
pause
