// API Configuration
// 自動檢測環境並設置正確的 API URL

const API_CONFIG = {
    // 開發環境：本地後端
    development: 'http://localhost:5000',

    // 生產環境：Railway 後端
    production: 'https://vibe-coding-production-cdb4.up.railway.app'
};

// 自動檢測當前環境
const isLocalhost = window.location.hostname === 'localhost' ||
                    window.location.hostname === '127.0.0.1' ||
                    window.location.hostname === '';

// 導出 API 基礎 URL
export const API_BASE_URL = isLocalhost ? API_CONFIG.development : API_CONFIG.production;

// 導出完整的 API 端點
export const API_ENDPOINTS = {
    options: `${API_BASE_URL}/api/options`,
    generateQuestion: `${API_BASE_URL}/api/generate-question`,
    recommend: `${API_BASE_URL}/api/recommend`,
    health: `${API_BASE_URL}/api/health`
};

console.log('🔧 API Config:', {
    environment: isLocalhost ? 'development' : 'production',
    baseURL: API_BASE_URL
});
