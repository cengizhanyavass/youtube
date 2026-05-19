@echo off
chcp 65001 >nul
title BeastTales Video Maker

echo.
echo ========================================
echo   BeastTales Video Maker - Kurulum
echo ========================================
echo.

:: Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Python bulunamadi!
    echo.
    echo Lutfen once Python yukleyin:
    echo https://www.python.org/downloads/
    echo.
    echo Kurulum sirasinda "Add Python to PATH" kutusunu isaretle!
    pause
    exit /b 1
)

echo [OK] Python bulundu
echo.

:: Klasöre git
cd /d "%~dp0"

:: pip güncelle
echo pip guncelleniyor...
python -m pip install --upgrade pip --quiet

:: Bağımlılıkları kur
echo Kutuphaneler kuruluyor (ilk seferinde 2-3 dk surebilir)...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo [HATA] Kurulum basarisiz oldu!
    pause
    exit /b 1
)

echo.
echo [OK] Kurulum tamamlandi!
echo.
echo Uygulama baslatiliyor...
echo Tarayicinizda otomatik acilacak: http://localhost:8501
echo.
echo Kapatmak icin bu pencereyi kapatin.
echo.

streamlit run app.py --server.maxUploadSize 2000

pause
