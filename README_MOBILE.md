# 📱 知乎热榜数据可视化 - 移动端APP

> 将您的Flask Web应用封装成安卓APP，并部署到腾讯云的完整解决方案

## 🚀 快速开始

### 一键部署
```bash
# 给脚本执行权限
chmod +x quick_start.sh

# 运行快速部署脚本
./quick_start.sh
```

### 手动部署
```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 初始化数据库
python app.py init-db

# 3. 创建管理员用户
python app.py create-admin admin admin@example.com admin123

# 4. 启动Flask应用
python app.py

# 5. 创建React Native项目
npx react-native init ZhihuHotVis
cd ZhihuHotVis
npm install

# 6. 运行移动端应用
npx react-native run-android
```

## 📋 项目结构

```
ZhiHotDataVis/
├── app/                          # Flask后端应用
│   ├── controllers/              # 控制器
│   │   ├── mobile_api.py        # 移动端API接口 ✨
│   │   ├── main.py              # 主页控制器
│   │   ├── auth.py              # 认证控制器
│   │   └── analysis.py          # 分析控制器
│   ├── models/                   # 数据模型
│   ├── services/                 # 业务服务
│   └── templates/                # Web模板
├── mobile_app/                   # React Native移动端 ✨
│   ├── src/
│   │   ├── components/          # 通用组件
│   │   ├── screens/             # 页面组件
│   │   ├── services/            # API服务
│   │   ├── store/               # 状态管理
│   │   └── constants/           # 配置常量
│   └── package.json
├── Dockerfile                    # Docker配置 ✨
├── docker-compose.yml           # Docker Compose配置 ✨
├── nginx.conf                   # Nginx配置 ✨
├── deploy_tencent.sh            # 腾讯云部署脚本 ✨
├── quick_start.sh               # 快速开始脚本 ✨
├── DEPLOYMENT_GUIDE.md          # 详细部署指南 ✨
└── requirements.txt             # Python依赖
```

## 🌟 新增功能

### 1. 移动端API接口
- **健康检查**: `GET /api/mobile/health`
- **用户认证**: `POST /api/mobile/auth/login`
- **热门文章**: `GET /api/mobile/hot_articles`
- **数据分析**: `GET /api/mobile/analysis/hot_words`
- **情感分析**: `GET /api/mobile/analysis/sentiment`

### 2. React Native移动端
- 📱 原生移动端体验
- 🔄 下拉刷新功能
- 📊 数据可视化图表
- 🔐 用户认证系统
- 💾 本地数据缓存

### 3. 腾讯云部署支持
- 🐳 Docker容器化部署
- 🌐 Nginx反向代理
- 🔒 HTTPS安全配置
- 📈 自动扩容支持

## 🛠️ 技术栈

### 后端
- **框架**: Flask 2.2.3
- **数据库**: SQLite/MySQL
- **部署**: Docker + Nginx
- **云平台**: 腾讯云CVM

### 移动端
- **框架**: React Native 0.72.0
- **状态管理**: Redux Toolkit
- **导航**: React Navigation 6
- **网络**: Axios
- **图表**: React Native Chart Kit

### 部署工具
- **容器化**: Docker & Docker Compose
- **反向代理**: Nginx
- **CI/CD**: 腾讯云CLI
- **监控**: Docker日志

## 📱 移动端功能

### 主要页面
1. **首页** - 知乎热榜列表
   - 实时热榜数据
   - 下拉刷新
   - 点击查看详情

2. **数据分析** - 数据可视化
   - 热词分析
   - 情感分析
   - 统计图表

3. **用户中心** - 个人信息
   - 登录/注册
   - 个人设置
   - 关于应用

### 核心特性
- ✅ 离线缓存
- ✅ 下拉刷新
- ✅ 无限滚动
- ✅ 错误重试
- ✅ 加载状态
- ✅ 响应式设计

## 🌐 API接口文档

### 认证接口
```http
POST /api/mobile/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### 热门文章接口
```http
GET /api/mobile/hot_articles?page=1&per_page=20
Authorization: Bearer <token>
```

### 数据分析接口
```http
GET /api/mobile/analysis/hot_words?limit=30
GET /api/mobile/analysis/sentiment
GET /api/mobile/analysis/stats
```

## 🚀 部署指南

### 1. 腾讯云部署
```bash
# 配置腾讯云CLI
tccli configure

# 运行部署脚本
chmod +x deploy_tencent.sh
./deploy_tencent.sh
```

### 2. 本地开发
```bash
# 启动后端
python app.py

# 启动移动端
cd ZhihuHotVis
npx react-native start
npx react-native run-android
```

### 3. 生产环境
```bash
# 使用Docker部署
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 📦 APP打包

### Android APK
```bash
cd ZhihuHotVis/android
./gradlew assembleRelease

# APK位置: android/app/build/outputs/apk/release/app-release.apk
```

### Android AAB (Google Play)
```bash
cd ZhihuHotVis/android
./gradlew bundleRelease

# AAB位置: android/app/build/outputs/bundle/release/app-release.aab
```

## 🔧 配置说明

### 环境变量
```bash
# Flask配置
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key

# 数据库配置
DATABASE_URL=sqlite:///instance/app.db

# API配置
API_BASE_URL=https://your-domain.com
```

### 移动端配置
```javascript
// src/constants/config.js
export const API_CONFIG = {
  PROD_BASE_URL: 'https://your-domain.com',
  DEV_BASE_URL: 'http://10.0.2.2:5000',
  TIMEOUT: 10000,
};
```

## 🧪 测试

### 后端测试
```bash
# 健康检查
curl http://localhost:5000/api/mobile/health

# API测试
curl -X POST http://localhost:5000/api/mobile/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 移动端测试
```bash
# 运行测试
cd ZhihuHotVis
npm test

# 端到端测试
npm run e2e
```

## 📊 性能优化

### 后端优化
- 使用Gunicorn多进程部署
- Redis缓存热点数据
- 数据库查询优化
- 静态资源CDN

### 移动端优化
- 图片懒加载
- 列表虚拟化
- 代码分割
- Bundle优化

## 🔒 安全配置

### 网络安全
- HTTPS强制跳转
- CORS跨域配置
- 请求频率限制
- SQL注入防护

### 移动端安全
- 代码混淆
- 证书绑定
- 本地存储加密
- API签名验证

## 📞 技术支持

### 常见问题
1. **网络连接失败** - 检查服务器IP和端口
2. **构建失败** - 清理项目重新构建
3. **权限问题** - 检查AndroidManifest.xml配置
4. **性能问题** - 启用生产模式构建

### 获取帮助
- 📖 查看 [详细部署指南](DEPLOYMENT_GUIDE.md)
- 🐛 提交Issue报告问题
- 💬 加入技术交流群

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**🎉 恭喜！您已成功将Flask Web应用封装成了安卓APP并可部署到腾讯云！**
