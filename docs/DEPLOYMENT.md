# 🚀 部署指南

本指南將幫助你將 Vibe Coding 部署到雲平台，讓任何人都可以通過網址訪問。

## 📋 部署前準備

1. **GitHub 倉庫已準備好** ✅
   - 代碼已推送到: `git@github.com:WellyXY/vibe_coding.git`

2. **獲取 Gemini API Key**
   - 訪問: https://makersuite.google.com/app/apikey
   - 創建一個新的 API key
   - 保存好這個 key，稍後需要用到

## 🎯 方案 1: Render（推薦，完全免費）

### 步驟 1: 創建 Render 帳號

1. 訪問 https://render.com
2. 點擊 "Get Started" 註冊帳號
3. 使用 GitHub 帳號登錄（推薦）

### 步驟 2: 創建新的 Web Service

1. 在 Render Dashboard 點擊 **"New +"** → **"Web Service"**

2. 連接 GitHub 倉庫:
   - 選擇 "Connect a repository"
   - 找到並選擇 `WellyXY/vibe_coding`
   - 點擊 "Connect"

3. 配置服務:
   ```
   Name: vibe-coding
   Region: Singapore (或選擇離你最近的)
   Branch: main
   Root Directory: (留空)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. 選擇方案:
   - 選擇 **"Free"** 方案

### 步驟 3: 設置環境變數

在 "Environment Variables" 區域添加:

```
GEMINI_API_KEY = 你的_Gemini_API_Key
FLASK_ENV = production
```

### 步驟 4: 部署

1. 點擊 **"Create Web Service"**
2. Render 會自動:
   - 從 GitHub 拉取代碼
   - 安裝依賴
   - 啟動服務

3. 等待 3-5 分鐘，部署完成後你會得到一個網址:
   ```
   https://vibe-coding.onrender.com
   ```

### 步驟 5: 測試

訪問你的網址，應該能看到應用運行！

---

## 🎯 方案 2: Railway

### 步驟 1: 創建 Railway 帳號

1. 訪問 https://railway.app
2. 使用 GitHub 登錄

### 步驟 2: 部署

1. 點擊 "New Project"
2. 選擇 "Deploy from GitHub repo"
3. 選擇 `WellyXY/vibe_coding`
4. Railway 會自動檢測到 Python 項目

### 步驟 3: 設置環境變數

1. 在項目設置中點擊 "Variables"
2. 添加:
   ```
   GEMINI_API_KEY = 你的_Gemini_API_Key
   PORT = 5000
   ```

### 步驟 4: 生成公開 URL

1. 在 Settings 中找到 "Domains"
2. 點擊 "Generate Domain"
3. 你會得到一個 `.railway.app` 的網址

---

## 🎯 方案 3: Vercel（適合前端優化）

Vercel 主要針對前端，但可以通過 Serverless Functions 運行 Python：

1. 訪問 https://vercel.com
2. 使用 GitHub 登錄
3. Import Project → 選擇倉庫
4. 需要額外配置 `vercel.json` (較複雜)

**注意**: Vercel 對 Python 後端支持有限，不推薦。

---

## ⚠️ 注意事項

### Render 免費方案限制

- **休眠機制**: 15 分鐘無活動後會休眠
- **啟動時間**: 休眠後首次訪問需要 30-50 秒啟動
- **解決方案**: 使用 UptimeRobot 定期 ping（每 14 分鐘一次）

### Railway 免費方案限制

- 每月 $5 免費額度（約 500 小時運行時間）
- 額度用完後服務會暫停

---

## 🔄 自動部署

配置好後，每次你推送代碼到 GitHub：

```bash
git add .
git commit -m "Update features"
git push origin main
```

Render/Railway 會自動:
1. 檢測到更新
2. 重新構建
3. 自動部署新版本

---

## 🐛 常見問題

### Q: 部署後顯示 "Application Error"

**解決方案**:
1. 檢查 Render Logs 查看錯誤信息
2. 確認環境變數 `GEMINI_API_KEY` 已設置
3. 確認 `gunicorn` 在 requirements.txt 中

### Q: API 調用失敗

**解決方案**:
1. 檢查 Gemini API Key 是否正確
2. 確認 API Key 沒有過期
3. 查看 Render Logs 中的錯誤信息

### Q: 頭像圖片無法顯示

**解決方案**:
- Render 會自動處理靜態文件
- 確認 avatars 文件夾在 GitHub 中
- 檢查 .gitignore 沒有排除 avatars/

### Q: 如何查看日誌？

在 Render Dashboard:
1. 進入你的 Web Service
2. 點擊 "Logs" 標籤
3. 實時查看運行日誌

---

## 🎨 自定義域名（可選）

### Render

1. 在 Settings → Custom Domain
2. 添加你的域名（需要先購買域名）
3. 按照指示配置 DNS

### Railway

1. 在 Settings → Domains
2. Add Custom Domain
3. 配置 DNS CNAME 記錄

---

## 📊 性能優化建議

### 1. 使用 CDN 加速靜態資源

將頭像上傳到:
- Cloudinary (免費)
- AWS S3 + CloudFront
- Imgur

### 2. 防止休眠

使用 UptimeRobot:
1. 訪問 https://uptimerobot.com
2. 添加 HTTP(s) Monitor
3. 設置每 5 分鐘 ping 一次你的 URL

### 3. 數據庫（如需要）

Render 免費提供 PostgreSQL:
- 在 Dashboard 添加 PostgreSQL
- 更新代碼使用數據庫而非 JSON 文件

---

## 🚀 生產環境檢查清單

- [ ] ✅ GEMINI_API_KEY 已設置
- [ ] ✅ debug mode 已關閉 (FLASK_ENV=production)
- [ ] ✅ requirements.txt 包含所有依賴
- [ ] ✅ gunicorn 已添加到 requirements.txt
- [ ] ✅ .env 文件已在 .gitignore 中
- [ ] ✅ 測試所有 API 端點
- [ ] ✅ 測試前端功能
- [ ] ✅ 檢查錯誤日誌

---

## 📞 支援

如果遇到問題:
1. 查看 Render/Railway 的日誌
2. 檢查 GitHub Issues
3. 參考 Render 文檔: https://render.com/docs

---

**部署成功後，你的應用就可以在全球任何地方訪問了！🌍**
