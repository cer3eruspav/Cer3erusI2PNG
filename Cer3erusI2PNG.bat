@echo off
chcp 65001 >nul

if "%~1"=="" goto wait_drop

py -3 "%~dp0Image 2 png.py" %*

:wait_drop
echo.
echo --------------------------------------------------
echo  PNG conversion completed! Closing window...
echo --------------------------------------------------

for /L %%i in (10,-1,1) do (
    <nul set /p "=  ^> Closing in %%i seconds...   "
    timeout /t 1 /nobreak >nul
)

echo.
echo Process finished.
