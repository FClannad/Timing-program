@echo off
echo ================================
echo   正在打包拼豆计时系统...
echo ================================
echo.

pyinstaller --onefile --windowed ^
    --name "拼豆计时系统Web版" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=sqlite3 ^
    app_standalone.py

echo.
echo ================================
echo   打包完成！
echo   程序位于: dist\拼豆计时系统Web版.exe
echo ================================
pause
