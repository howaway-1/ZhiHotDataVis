import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_CONFIG, STORAGE_KEYS, ERROR_MESSAGES, getBaseURL } from '../constants/config';

// 创建axios实例
const apiClient = axios.create({
  baseURL: getBaseURL(),
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  async (config) => {
    // 添加认证token
    const token = await AsyncStorage.getItem(STORAGE_KEYS.USER_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 开发环境日志
    if (__DEV__) {
      console.log('API Request:', config.method?.toUpperCase(), config.url, config.data);
    }
    
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    // 开发环境日志
    if (__DEV__) {
      console.log('API Response:', response.status, response.data);
    }
    
    return response;
  },
  async (error) => {
    console.error('Response Error:', error);
    
    // 处理认证错误
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem(STORAGE_KEYS.USER_TOKEN);
      await AsyncStorage.removeItem(STORAGE_KEYS.USER_INFO);
      // 可以在这里触发登录页面跳转
    }
    
    return Promise.reject(error);
  }
);

// API服务类
class ApiService {
  // 健康检查
  static async healthCheck() {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.MOBILE_HEALTH);
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  // 用户认证
  static async login(username, password) {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.MOBILE_LOGIN, {
        username,
        password,
      });
      
      if (response.data.status === 'success') {
        // 保存用户信息和token
        await AsyncStorage.setItem(STORAGE_KEYS.USER_TOKEN, response.data.data.token);
        await AsyncStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(response.data.data));
        
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  static async register(username, email, password) {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.MOBILE_REGISTER, {
        username,
        email,
        password,
      });
      
      if (response.data.status === 'success') {
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  static async logout() {
    try {
      await AsyncStorage.removeItem(STORAGE_KEYS.USER_TOKEN);
      await AsyncStorage.removeItem(STORAGE_KEYS.USER_INFO);
      return { success: true };
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  // 热门文章
  static async getHotArticles(page = 1, perPage = 20) {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.MOBILE_HOT_ARTICLES, {
        params: { page, per_page: perPage },
      });
      
      if (response.data.status === 'success') {
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  static async refreshHotArticles() {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.MOBILE_REFRESH_ARTICLES);
      
      if (response.data.status === 'success') {
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  // 数据分析
  static async getHotWords(limit = 30) {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.MOBILE_HOT_WORDS, {
        params: { limit },
      });
      
      if (response.data.status === 'success') {
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  static async getSentimentAnalysis() {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.MOBILE_SENTIMENT);
      
      if (response.data.status === 'success') {
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  static async getStatistics() {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.MOBILE_STATS);
      
      if (response.data.status === 'success') {
        return { success: true, data: response.data.data };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  // 缓存管理
  static async getCachedData(key) {
    try {
      const cachedData = await AsyncStorage.getItem(key);
      if (cachedData) {
        const parsed = JSON.parse(cachedData);
        const now = Date.now();
        
        // 检查缓存是否过期
        if (now - parsed.timestamp < API_CONFIG.CACHE_DURATION) {
          return { success: true, data: parsed.data, fromCache: true };
        }
      }
      return { success: false, error: 'Cache expired or not found' };
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  static async setCachedData(key, data) {
    try {
      const cacheData = {
        data,
        timestamp: Date.now(),
      };
      await AsyncStorage.setItem(key, JSON.stringify(cacheData));
      return { success: true };
    } catch (error) {
      return { success: false, error: this.handleError(error) };
    }
  }

  // 错误处理
  static handleError(error) {
    if (error.response) {
      // 服务器响应错误
      const status = error.response.status;
      const message = error.response.data?.message || error.response.statusText;
      
      switch (status) {
        case 400:
          return `请求错误: ${message}`;
        case 401:
          return ERROR_MESSAGES.AUTH_ERROR;
        case 403:
          return '权限不足';
        case 404:
          return '请求的资源不存在';
        case 500:
          return ERROR_MESSAGES.SERVER_ERROR;
        default:
          return `服务器错误 (${status}): ${message}`;
      }
    } else if (error.request) {
      // 网络错误
      return ERROR_MESSAGES.NETWORK_ERROR;
    } else if (error.code === 'ECONNABORTED') {
      // 超时错误
      return ERROR_MESSAGES.TIMEOUT_ERROR;
    } else {
      // 其他错误
      return error.message || ERROR_MESSAGES.UNKNOWN_ERROR;
    }
  }

  // 重试机制
  static async retryRequest(requestFn, maxRetries = API_CONFIG.RETRY_COUNT) {
    let lastError;
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        const result = await requestFn();
        if (result.success) {
          return result;
        }
        lastError = result.error;
      } catch (error) {
        lastError = this.handleError(error);
      }
      
      // 等待一段时间后重试
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
      }
    }
    
    return { success: false, error: lastError };
  }
}

export default ApiService;
