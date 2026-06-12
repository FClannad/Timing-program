@echo off
echo 正在打包拼豆计时系统...
echo.

REM 检查 pyinstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

echo.
echo 开始打包...
pyinstaller --onefile --windowed --name "拼豆计时系统" --add-data "static;static" --add-data "templates;templates" --icon=NONE app_standalone.py

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位于: dist\拼豆计时系统.exe
echo ========================================
echo.
pause
