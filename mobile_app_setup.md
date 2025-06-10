# React Native移动端开发指南

## 1. 环境准备

### 1.1 安装Node.js
```bash
# 下载并安装Node.js 18+
# https://nodejs.org/

# 验证安装
node --version
npm --version
```

### 1.2 安装React Native CLI
```bash
npm install -g react-native-cli
# 或者使用npx (推荐)
npx react-native --version
```

### 1.3 安装Android开发环境
1. 下载并安装Android Studio
2. 安装Android SDK (API 30+)
3. 配置环境变量:
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

## 2. 创建React Native项目

```bash
# 创建新项目
npx react-native init ZhihuHotVis --version 0.72.0

# 进入项目目录
cd ZhihuHotVis

# 安装依赖
npm install
```

## 3. 安装必要的第三方库

```bash
# 导航库
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs

# React Navigation依赖
npm install react-native-screens react-native-safe-area-context

# 网络请求
npm install axios

# 状态管理
npm install @reduxjs/toolkit react-redux

# UI组件库
npm install react-native-elements react-native-vector-icons

# WebView组件
npm install react-native-webview

# 图表库
npm install react-native-chart-kit react-native-svg

# 异步存储
npm install @react-native-async-storage/async-storage

# 启动屏
npm install react-native-splash-screen

# 状态栏
npm install react-native-status-bar-height

# 下拉刷新
npm install react-native-pull-to-refresh

# 图片选择器
npm install react-native-image-picker

# 权限管理
npm install react-native-permissions
```

## 4. Android配置

### 4.1 配置图标权限 (android/app/src/main/AndroidManifest.xml)
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

### 4.2 配置网络安全 (android/app/src/main/res/xml/network_security_config.xml)
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">your-api-domain.com</domain>
    </domain-config>
</network-security-config>
```

## 5. 项目结构

```
ZhihuHotVis/
├── src/
│   ├── components/          # 通用组件
│   │   ├── Header.js
│   │   ├── LoadingSpinner.js
│   │   └── ErrorMessage.js
│   ├── screens/            # 页面组件
│   │   ├── HomeScreen.js
│   │   ├── LoginScreen.js
│   │   ├── AnalysisScreen.js
│   │   └── ProfileScreen.js
│   ├── navigation/         # 导航配置
│   │   └── AppNavigator.js
│   ├── services/          # API服务
│   │   └── api.js
│   ├── store/             # Redux状态管理
│   │   ├── store.js
│   │   └── slices/
│   ├── utils/             # 工具函数
│   │   └── helpers.js
│   └── constants/         # 常量定义
│       └── config.js
├── android/               # Android原生代码
├── ios/                   # iOS原生代码 (如需要)
└── package.json
```

## 6. 运行项目

```bash
# 启动Metro服务器
npx react-native start

# 在新终端运行Android应用
npx react-native run-android

# 或者运行iOS应用 (macOS)
npx react-native run-ios
```

## 7. 调试

```bash
# 开启调试模式
# 在模拟器中按 Ctrl+M (Android) 或 Cmd+D (iOS)
# 选择 "Debug JS Remotely"

# 查看日志
npx react-native log-android
npx react-native log-ios
```

## 8. 打包发布

### Android APK
```bash
# 生成签名密钥
keytool -genkeypair -v -keystore my-upload-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# 配置gradle.properties
# 添加签名配置到android/app/build.gradle

# 生成APK
cd android
./gradlew assembleRelease

# APK位置: android/app/build/outputs/apk/release/app-release.apk
```

### Android AAB (Google Play)
```bash
cd android
./gradlew bundleRelease

# AAB位置: android/app/build/outputs/bundle/release/app-release.aab
```
