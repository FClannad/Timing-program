@echo off
chcp 65001 >nul
title 拼豆计时系统 - Web版
echo ================================
echo   ♥ 拼豆店计时管理系统 ♥
echo        (Web 现代化版)
echo ================================
echo.
echo 正在启动服务器...
echo.
echo 启动后请在浏览器访问：
echo http://localhost:5000
echo.
python app.py
pause
