@echo off
chcp 65001 >nul
title 拼豆计时系统 - Hello Kitty 卡通版
echo ================================
echo   ♥ 拼豆店计时管理系统 ♥
echo     (Hello Kitty 卡通风格)
echo ================================
echo.
echo 正在启动程序...
echo.
python "拼豆计时系统_卡通版.py"
if errorlevel 1 (
    echo.
    echo 程序运行出错！
    pause
)
