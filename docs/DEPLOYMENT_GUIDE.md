# 部署指南 Deployment Guide

## 問題原因

你遇到的 CORS 錯誤有兩個根本原因：

1. **架構問題**：前端部署在 Vercel (`https://vibe-coding-one-pink.vercel.app`)，但代碼中使用了 `http://localhost:5000`。當用戶訪問你的網站時，他們的瀏覽器無法連接到你本地電腦上的服務器。

2. **CORS 配置**：雖然後端已配置 CORS，但需要確保允許來自 Vercel 域名的請求。

## 解決方案

### 選項 1：將後端也部署到 Vercel（推薦）

這個項目已經配置好可以同時部署前端和後端到 Vercel。

#### 步驟：

1. **更新 `config.js`**：
   ```javascript
   // 將 production URL 改為你的 Vercel 應用 URL
   production: window.location.origin  // 這樣前後端在同一域名下
   ```

2. **部署到 Vercel**：
   ```bash
   # 安裝 Vercel CLI
   npm install -g vercel

   # 登入 Vercel
   vercel login

   # 部署
   vercel
   ```

3. **設置環境變量**（在 Vercel Dashboard）：
   - 進入你的項目設置
   - 添加環境變量：
     - `FLASK_ENV` = `production`
     - `GEMINI_API_KEY` = 你的 Gemini API Key（如果需要）

4. **重新部署**：
   ```bash
   vercel --prod
   ```

### 選項 2：將後端部署到其他服務（Heroku, Railway, Render 等）

如果你想將後端部署到其他平台：

1. **部署後端到你選擇的平台**（例如 Heroku）

2. **更新 `config.js`**：
   ```javascript
   production: 'https://your-backend-url.herokuapp.com'
   ```

3. **更新後端 CORS 配置** (`app.py`)：
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": ["https://vibe-coding-one-pink.vercel.app"],
           "methods": ["GET", "POST", "OPTIONS"],
           "allow_headers": ["Content-Type"]
       }
   })
   ```

4. **重新部署前端到 Vercel**

### 選項 3：僅在本地測試

如果只是想在本地測試：

1. **啟動後端**：
   ```bash
   python app.py
   ```

2. **在本地打開前端**：
   - 直接打開 `index.html`
   - 或使用本地服務器：`python -m http.server 8000`

3. 配置會自動檢測到 `localhost` 並使用本地 API

## 部署檢查清單

- [ ] 後端已部署到可公開訪問的服務器
- [ ] `config.js` 中的 `production` URL 已更新
- [ ] 後端 CORS 配置允許你的前端域名
- [ ] 環境變量已正確設置（API keys 等）
- [ ] 測試所有 API 端點是否正常工作

## 常見問題

### Q: 為什麼不能直接訪問 localhost？
A: `localhost` 是本地主機地址，只能在你自己的電腦上訪問。當其他人訪問你的 Vercel 網站時，他們無法連接到你電腦上的服務器。

### Q: CORS 錯誤是什麼意思？
A: CORS（跨源資源共享）是瀏覽器的安全機制。它防止網站訪問不同域名的資源，除非服務器明確允許。

### Q: 如何檢查部署是否成功？
A: 打開瀏覽器的開發者工具（F12），查看 Console 標籤。如果看到 "🔧 API Config" 消息顯示正確的環境和 URL，說明配置成功。

## 需要幫助？

如果遇到問題：
1. 檢查瀏覽器控制台的錯誤消息
2. 確認後端服務器正在運行
3. 驗證 API URL 配置正確
4. 測試後端 health check 端點：`/api/health`
