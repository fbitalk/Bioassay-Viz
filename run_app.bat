@echo off
chcp 65001 >nul
echo ==========================================
echo       正在启动生测数据可视化工具...
echo ==========================================
echo.

REM 检查是否安装了 streamlit
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 检测到未安装 streamlit，正在自动安装...
    pip install streamlit pandas matplotlib seaborn openpyxl
)

echo 正在启动网页服务，请稍候...
echo 启动后将自动在浏览器中打开。
echo.

streamlit run app.py

pause