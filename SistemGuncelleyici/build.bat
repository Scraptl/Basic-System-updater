@echo off
chcp 65001
echo.
echo ========================================
echo    SISTEM GUNCELLEYICI EXE YAPICI
echo ========================================
echo.

echo 📦 1. Kutuphaneler kontrol ediliyor...
pip install pyinstaller customtkinter

echo.
echo 🔨 2. EXE dosyasi yapiliyor...
echo    (Bu 5-10 dakika surebilir, bekleyin...)
echo.

pyinstaller --onefile --windowed --name "SistemGuncelleyici" updater_gui.py

echo.
if exist "dist\SistemGuncelleyici.exe" (
    echo ✅ ✅ ✅ BASARILI! ✅ ✅ ✅
    echo.
    echo 📍 EXE dosyasi: dist\SistemGuncelleyici.exe
    echo 📏 Dosya boyutu: 
    for %%F in ("dist\SistemGuncelleyici.exe") do echo    %%~zF byte
    echo.
    echo 🎯 TEST ETMEK ICIN:
    echo   1. dist klasorune git
    echo   2. SistemGuncelleyici.exe dosyasina cift tikla
    echo.
    echo ⚠️  Antivirus uyarisi gelebilir, "Calistir" deyin
    echo.
    pause
) else (
    echo ❌❌❌ HATA: EXE olusturulamadi! ❌❌❌
    echo.
    echo 🔧 Cozum deneyin:
    echo   1. Python kurulu mu? (python --version)
    echo   2. Internet baglantisi var mi?
    echo   3. updater_gui.py ayni klasorde mi?
    echo.
    pause
)