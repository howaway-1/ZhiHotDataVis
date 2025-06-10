#!/bin/bash

# 知乎热榜数据可视化系统 - 快速部署脚本
# 作者: AI Assistant
# 版本: 1.0.0

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装 $1"
        return 1
    fi
    return 0
}

# 显示欢迎信息
show_welcome() {
    echo "=================================================="
    echo "  知乎热榜数据可视化系统 - 快速部署脚本"
    echo "=================================================="
    echo ""
    echo "本脚本将帮助您："
    echo "1. 检查环境依赖"
    echo "2. 优化Flask后端代码"
    echo "3. 创建React Native移动端项目"
    echo "4. 生成部署配置文件"
    echo "5. 提供详细的部署指导"
    echo ""
    read -p "按回车键继续..."
}

# 检查环境依赖
check_environment() {
    log_info "检查环境依赖..."
    
    # 检查Python
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python版本: $PYTHON_VERSION"
    else
        log_error "请安装Python 3.8+"
        exit 1
    fi
    
    # 检查pip
    if check_command pip3; then
        log_success "pip3 已安装"
    else
        log_error "请安装pip3"
        exit 1
    fi
    
    # 检查Node.js
    if check_command node; then
        NODE_VERSION=$(node --version)
        log_success "Node.js版本: $NODE_VERSION"
    else
        log_warning "Node.js未安装，移动端开发需要Node.js 18+"
    fi
    
    # 检查npm
    if check_command npm; then
        NPM_VERSION=$(npm --version)
        log_success "npm版本: $NPM_VERSION"
    else
        log_warning "npm未安装"
    fi
    
    # 检查Docker
    if check_command docker; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        log_success "Docker版本: $DOCKER_VERSION"
    else
        log_warning "Docker未安装，部署时需要Docker"
    fi
    
    # 检查Git
    if check_command git; then
        log_success "Git已安装"
    else
        log_warning "Git未安装，建议安装用于版本控制"
    fi
}

# 安装Python依赖
install_python_deps() {
    log_info "安装Python依赖..."
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        log_info "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate || source venv/Scripts/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Python依赖安装完成"
    else
        log_error "requirements.txt文件不存在"
        exit 1
    fi
}

# 测试Flask应用
test_flask_app() {
    log_info "测试Flask应用..."
    
    # 激活虚拟环境
    source venv/bin/activate || source venv/Scripts/activate
    
    # 设置环境变量
    export FLASK_APP=app.py
    export FLASK_ENV=development
    
    # 初始化数据库
    python app.py init-db
    
    # 创建测试管理员用户
    python app.py create-admin admin admin@example.com admin123
    
    log_success "Flask应用配置完成"
}

# 创建React Native项目
create_react_native_project() {
    log_info "创建React Native项目..."
    
    if [ ! -d "ZhihuHotVis" ]; then
        # 检查React Native CLI
        if ! command -v npx &> /dev/null; then
            log_error "npx未安装，请先安装Node.js"
            return 1
        fi
        
        # 创建项目
        npx react-native init ZhihuHotVis --version 0.72.0
        
        # 复制移动端代码
        if [ -d "mobile_app" ]; then
            cp -r mobile_app/* ZhihuHotVis/
            log_success "移动端代码复制完成"
        fi
        
        # 安装依赖
        cd ZhihuHotVis
        npm install
        cd ..
        
        log_success "React Native项目创建完成"
    else
        log_warning "React Native项目已存在，跳过创建"
    fi
}

# 生成部署配置
generate_deployment_config() {
    log_info "生成部署配置..."
    
    # 获取用户输入
    read -p "请输入您的域名（可选，直接回车跳过）: " DOMAIN_NAME
    read -p "请输入腾讯云地域（默认ap-beijing）: " REGION
    REGION=${REGION:-ap-beijing}
    
    # 更新nginx配置
    if [ ! -z "$DOMAIN_NAME" ]; then
        sed -i "s/your-domain.com/$DOMAIN_NAME/g" nginx.conf
        log_success "域名配置已更新: $DOMAIN_NAME"
    fi
    
    # 更新部署脚本
    sed -i "s/ap-beijing/$REGION/g" deploy_tencent.sh
    log_success "地域配置已更新: $REGION"
    
    # 生成环境变量文件
    cat > .env << EOF
# Flask应用配置
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# 数据库配置
DATABASE_URL=sqlite:///instance/app.db

# API配置
API_BASE_URL=http://localhost:5000

# 腾讯云配置
TENCENT_REGION=$REGION
DOMAIN_NAME=$DOMAIN_NAME
EOF
    
    log_success "环境变量文件已生成"
}

# 显示下一步操作
show_next_steps() {
    echo ""
    echo "=================================================="
    echo "  🎉 快速配置完成！"
    echo "=================================================="
    echo ""
    echo "下一步操作："
    echo ""
    echo "1. 【后端部署】"
    echo "   cd $(pwd)"
    echo "   chmod +x deploy_tencent.sh"
    echo "   ./deploy_tencent.sh"
    echo ""
    echo "2. 【移动端开发】"
    echo "   cd ZhihuHotVis"
    echo "   # 修改 src/constants/config.js 中的服务器地址"
    echo "   npx react-native start"
    echo "   # 新终端运行："
    echo "   npx react-native run-android"
    echo ""
    echo "3. 【APP打包】"
    echo "   cd ZhihuHotVis/android"
    echo "   ./gradlew assembleRelease"
    echo ""
    echo "4. 【详细文档】"
    echo "   查看 DEPLOYMENT_GUIDE.md 获取完整部署指南"
    echo ""
    echo "=================================================="
    echo "  📞 需要帮助？"
    echo "=================================================="
    echo ""
    echo "- 查看日志: docker-compose logs -f"
    echo "- 测试API: curl http://YOUR_SERVER_IP:5000/api/mobile/health"
    echo "- 重启服务: docker-compose restart"
    echo ""
    
    # 显示重要文件位置
    echo "重要文件位置："
    echo "- Flask应用: $(pwd)/app.py"
    echo "- 移动端项目: $(pwd)/ZhihuHotVis/"
    echo "- 部署脚本: $(pwd)/deploy_tencent.sh"
    echo "- 配置文件: $(pwd)/.env"
    echo ""
}

# 主函数
main() {
    show_welcome
    
    log_info "开始快速部署配置..."
    
    # 检查环境
    check_environment
    
    # 安装Python依赖
    install_python_deps
    
    # 测试Flask应用
    test_flask_app
    
    # 创建React Native项目
    if command -v node &> /dev/null; then
        create_react_native_project
    else
        log_warning "跳过React Native项目创建（Node.js未安装）"
    fi
    
    # 生成部署配置
    generate_deployment_config
    
    # 显示下一步操作
    show_next_steps
    
    log_success "快速配置完成！"
}

# 错误处理
trap 'log_error "脚本执行失败，请检查错误信息"; exit 1' ERR

# 运行主函数
main "$@"
