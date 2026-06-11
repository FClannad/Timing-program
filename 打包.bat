@echo off
echo 正在打包拼豆计时系统（美化版）...
pyinstaller --onefile --windowed --name "拼豆计时系统" "拼豆计时系统_美化版.py"
echo.
echo 打包完成！可执行文件位于 dist 文件夹中
pause
