// 应用配置文件

// API配置
export const API_CONFIG = {
  // 开发环境
  DEV_BASE_URL: 'http://10.0.2.2:5000',  // Android模拟器
  DEV_BASE_URL_IOS: 'http://localhost:5000',  // iOS模拟器
  
  // 生产环境 - 替换为您的腾讯云服务器地址
  PROD_BASE_URL: 'https://your-domain.com',
  
  // API端点
  ENDPOINTS: {
    // 移动端API
    MOBILE_HEALTH: '/api/mobile/health',
    MOBILE_LOGIN: '/api/mobile/auth/login',
    MOBILE_REGISTER: '/api/mobile/auth/register',
    MOBILE_HOT_ARTICLES: '/api/mobile/hot_articles',
    MOBILE_REFRESH_ARTICLES: '/api/mobile/hot_articles/refresh',
    MOBILE_HOT_WORDS: '/api/mobile/analysis/hot_words',
    MOBILE_SENTIMENT: '/api/mobile/analysis/sentiment',
    MOBILE_STATS: '/api/mobile/analysis/stats',
    
    // Web API (兼容)
    HOT_ARTICLES: '/api/hot_articles',
    REFRESH_ARTICLES: '/api/refresh_hot_articles',
  },
  
  // 请求超时时间
  TIMEOUT: 10000,
  
  // 重试次数
  RETRY_COUNT: 3,
};

// 应用配置
export const APP_CONFIG = {
  NAME: '知乎热榜数据可视化',
  VERSION: '1.0.0',
  DESCRIPTION: '实时获取知乎热榜数据，提供数据分析和可视化功能',
  
  // 分页配置
  PAGE_SIZE: 20,
  
  // 缓存配置
  CACHE_DURATION: 5 * 60 * 1000, // 5分钟
  
  // 主题配置
  THEME: {
    PRIMARY_COLOR: '#1890ff',
    SECONDARY_COLOR: '#52c41a',
    ERROR_COLOR: '#ff4d4f',
    WARNING_COLOR: '#faad14',
    SUCCESS_COLOR: '#52c41a',
    BACKGROUND_COLOR: '#f5f5f5',
    CARD_BACKGROUND: '#ffffff',
    TEXT_COLOR: '#333333',
    SECONDARY_TEXT_COLOR: '#666666',
    BORDER_COLOR: '#d9d9d9',
  },
  
  // 字体大小
  FONT_SIZES: {
    SMALL: 12,
    MEDIUM: 14,
    LARGE: 16,
    XLARGE: 18,
    XXLARGE: 20,
    TITLE: 24,
  },
  
  // 间距
  SPACING: {
    SMALL: 8,
    MEDIUM: 16,
    LARGE: 24,
    XLARGE: 32,
  },
  
  // 圆角
  BORDER_RADIUS: {
    SMALL: 4,
    MEDIUM: 8,
    LARGE: 12,
  },
};

// 存储键名
export const STORAGE_KEYS = {
  USER_TOKEN: 'user_token',
  USER_INFO: 'user_info',
  CACHED_ARTICLES: 'cached_articles',
  CACHED_ANALYSIS: 'cached_analysis',
  APP_SETTINGS: 'app_settings',
  LAST_REFRESH_TIME: 'last_refresh_time',
};

// 错误消息
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  SERVER_ERROR: '服务器错误，请稍后重试',
  TIMEOUT_ERROR: '请求超时，请稍后重试',
  AUTH_ERROR: '认证失败，请重新登录',
  VALIDATION_ERROR: '输入数据格式错误',
  UNKNOWN_ERROR: '未知错误，请稍后重试',
};

// 成功消息
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: '登录成功',
  REGISTER_SUCCESS: '注册成功',
  REFRESH_SUCCESS: '数据刷新成功',
  LOGOUT_SUCCESS: '退出登录成功',
};

// 导航路由名称
export const ROUTES = {
  // 主要页面
  HOME: 'Home',
  LOGIN: 'Login',
  REGISTER: 'Register',
  PROFILE: 'Profile',
  
  // 分析页面
  ANALYSIS: 'Analysis',
  HOT_WORDS: 'HotWords',
  SENTIMENT: 'Sentiment',
  STATISTICS: 'Statistics',
  
  // 详情页面
  ARTICLE_DETAIL: 'ArticleDetail',
  WEB_VIEW: 'WebView',
  
  // 设置页面
  SETTINGS: 'Settings',
  ABOUT: 'About',
};

// 底部导航配置
export const TAB_CONFIG = {
  HOME: {
    name: ROUTES.HOME,
    title: '首页',
    icon: 'home',
  },
  ANALYSIS: {
    name: ROUTES.ANALYSIS,
    title: '分析',
    icon: 'analytics',
  },
  PROFILE: {
    name: ROUTES.PROFILE,
    title: '我的',
    icon: 'person',
  },
};

// 开发模式配置
export const DEV_CONFIG = {
  ENABLE_LOGS: __DEV__,
  ENABLE_REDUX_LOGS: __DEV__,
  ENABLE_NETWORK_LOGS: __DEV__,
  MOCK_DATA: false,
};

// 获取当前环境的API基础URL
export const getBaseURL = () => {
  if (__DEV__) {
    // 开发环境
    return Platform.OS === 'ios' ? API_CONFIG.DEV_BASE_URL_IOS : API_CONFIG.DEV_BASE_URL;
  } else {
    // 生产环境
    return API_CONFIG.PROD_BASE_URL;
  }
};

// 导出默认配置
export default {
  API_CONFIG,
  APP_CONFIG,
  STORAGE_KEYS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  ROUTES,
  TAB_CONFIG,
  DEV_CONFIG,
  getBaseURL,
};
