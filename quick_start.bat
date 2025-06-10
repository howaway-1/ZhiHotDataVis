@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 知乎热榜数据可视化系统 - Windows快速部署脚本
:: 作者: AI Assistant
:: 版本: 1.0.0

echo ==================================================
echo   知乎热榜数据可视化系统 - 快速部署脚本
echo ==================================================
echo.
echo 本脚本将帮助您：
echo 1. 检查环境依赖
echo 2. 安装Python依赖
echo 3. 初始化Flask应用
echo 4. 创建React Native移动端项目
echo 5. 生成部署配置文件
echo.
pause

:: 检查Python
echo [INFO] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python未安装，请先安装Python 3.8+
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo [SUCCESS] Python版本: %%i
)

:: 检查pip
echo [INFO] 检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip未安装
    pause
    exit /b 1
) else (
    echo [SUCCESS] pip已安装
)

:: 创建虚拟环境
echo [INFO] 创建Python虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] 虚拟环境创建完成
) else (
    echo [WARNING] 虚拟环境已存在，跳过创建
)

:: 激活虚拟环境并安装依赖
echo [INFO] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo [SUCCESS] Python依赖安装完成

:: 初始化数据库
echo [INFO] 初始化数据库...
if not exist "instance" mkdir instance
python app.py init-db
echo [SUCCESS] 数据库初始化完成

:: 创建管理员用户
echo [INFO] 创建管理员用户...
python app.py create-admin admin admin@example.com admin123
echo [SUCCESS] 管理员用户创建完成 (用户名: admin, 密码: admin123)

:: 检查Node.js
echo [INFO] 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Node.js未安装，跳过React Native项目创建
    echo [INFO] 请访问 https://nodejs.org/ 下载安装Node.js 18+
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do echo [SUCCESS] Node.js版本: %%i
    
    :: 创建React Native项目
    echo [INFO] 创建React Native项目...
    if not exist "ZhihuHotVis" (
        npx react-native init ZhihuHotVis --version 0.72.0
        
        :: 复制移动端代码
        if exist "mobile_app" (
            xcopy /E /I /Y mobile_app ZhihuHotVis
            echo [SUCCESS] 移动端代码复制完成
        )
        
        :: 安装依赖
        cd ZhihuHotVis
        npm install
        cd ..
        echo [SUCCESS] React Native项目创建完成
    ) else (
        echo [WARNING] React Native项目已存在，跳过创建
    )
)

:: 生成环境变量文件
echo [INFO] 生成环境变量文件...
(
echo # Flask应用配置
echo FLASK_APP=app.py
echo FLASK_ENV=production
echo SECRET_KEY=your-secret-key-here
echo.
echo # 数据库配置
echo DATABASE_URL=sqlite:///instance/app.db
echo.
echo # API配置
echo API_BASE_URL=http://localhost:5000
echo.
echo # 腾讯云配置
echo TENCENT_REGION=ap-beijing
echo DOMAIN_NAME=
) > .env
echo [SUCCESS] 环境变量文件已生成

:: 显示完成信息
echo.
echo ==================================================
echo   🎉 快速配置完成！
echo ==================================================
echo.
echo 下一步操作：
echo.
echo 1. 【启动Flask应用】
echo    python app.py
echo    访问: http://localhost:5000
echo.
echo 2. 【移动端开发】（如果已安装Node.js）
echo    cd ZhihuHotVis
echo    修改 src\constants\config.js 中的服务器地址
echo    npx react-native start
echo    在新命令行窗口运行: npx react-native run-android
echo.
echo 3. 【腾讯云部署】
echo    安装腾讯云CLI: pip install tccli
echo    配置凭证: tccli configure
echo    运行部署: bash deploy_tencent.sh （需要Git Bash或WSL）
echo.
echo 4. 【详细文档】
echo    查看 DEPLOYMENT_GUIDE.md 获取完整部署指南
echo    查看 README_MOBILE.md 获取项目说明
echo.
echo ==================================================
echo   📞 重要信息
echo ==================================================
echo.
echo 管理员账号:
echo   用户名: admin
echo   密码: admin123
echo   邮箱: admin@example.com
echo.
echo API测试:
echo   健康检查: http://localhost:5000/api/mobile/health
echo   登录接口: http://localhost:5000/api/mobile/auth/login
echo.
echo 重要文件:
echo   Flask应用: %CD%\app.py
echo   移动端项目: %CD%\ZhihuHotVis\
echo   环境配置: %CD%\.env
echo.
echo [SUCCESS] 快速配置完成！现在可以启动应用了。
echo.
pause
