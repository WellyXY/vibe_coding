# 🚀 部署快速啟動指南

## ✅ 已完成的配置

你的項目已經配置好連接 Railway 後端了！

- **Railway 後端**: `https://vibe-coding-production-cdb4.up.railway.app`
- **Vercel 前端**: `https://vibe-coding-one-pink.vercel.app`

### 已修改的文件：
- ✅ `config.js` - 配置 Railway URL
- ✅ `app.py` - CORS 允許 Vercel 域名
- ✅ `index.html` - 使用動態 API URL
- ✅ `Procfile` - Railway 啟動配置
- ✅ `test-connection.html` - API 測試工具

## 🎯 接下來要做的事

### 步驟 1: 確保 Railway 後端正在運行

打開瀏覽器測試：
```
https://vibe-coding-production-cdb4.up.railway.app/api/health
```

**應該看到**:
```json
{"status": "ok", "version": "1.0.0"}
```

**如果沒有響應**，你需要：
1. 登入 Railway Dashboard
2. 檢查部署狀態
3. 查看部署日誌
4. 確保所有文件已推送到 Git

### 步驟 2: 部署更新到 Vercel

```bash
# 1. 提交所有更改
git add .
git commit -m "Fix CORS: Connect to Railway backend"

# 2. 推送到 Git
git push

# Vercel 會自動重新部署
```

### 步驟 3: 測試完整流程

#### 方法 1: 使用測試頁面
訪問: `https://vibe-coding-one-pink.vercel.app/test-connection.html`

點擊所有測試按鈕，確保都成功 ✅

#### 方法 2: 測試主應用
1. 訪問: `https://vibe-coding-one-pink.vercel.app`
2. 按 F12 打開開發者工具
3. 點擊 Agent 頭像
4. 確認沒有 CORS 錯誤

## ✨ 成功標誌

當一切正常時，你會看到：

1. ✅ Railway health check 返回 `{"status": "ok"}`
2. ✅ Vercel 網站正常打開
3. ✅ Console 顯示: `🔧 API Config: { baseURL: "https://vibe-coding-production-cdb4.up.railway.app" }`
4. ✅ Agent 能正常提問
5. ✅ **沒有任何 CORS 錯誤**

## 🔧 Railway 部署檢查

### 必要的環境變量

在 Railway Dashboard 設置：

```
FLASK_ENV=production
PORT=5000
GEMINI_API_KEY=你的_API_Key
```

### 確認文件已推送

確保這些文件在你的 Git 倉庫中：
- `app.py`
- `requirements.txt`
- `Procfile`
- `recommendation_system.py`
- `gemini_client.py`
- `users_database.json`

## 🐛 常見問題

### 問題: CORS 錯誤仍然存在

**解決方案**:
```bash
# 1. 確認後端已重新部署（包含新的 CORS 配置）
cd /path/to/your/backend
git add app.py
git commit -m "Update CORS config"
git push

# 2. 確認前端已重新部署
cd /path/to/your/frontend
git add config.js index.html
git commit -m "Update API config"
git push

# 3. 清除瀏覽器緩存或使用無痕模式測試
```

### 問題: 連接超時

**檢查**:
1. Railway 服務是否正在運行
2. 域名是否正確
3. 網絡連接是否正常

### 問題: 404 Not Found

**檢查**:
1. Railway 日誌中是否有錯誤
2. `Procfile` 啟動命令是否正確
3. API 路由是否正確定義

## 📋 部署清單

在標記為完成前，確認：

- [ ] Railway 後端正在運行
- [ ] Health check 端點返回成功
- [ ] 所有代碼已推送到 Git
- [ ] Vercel 已自動重新部署
- [ ] 測試頁面所有測試通過
- [ ] 主應用沒有 CORS 錯誤
- [ ] Agent 能正常工作

## 📞 測試命令

### 測試 Railway API

```bash
# Health Check
curl https://vibe-coding-production-cdb4.up.railway.app/api/health

# Get Options
curl https://vibe-coding-production-cdb4.up.railway.app/api/options

# Generate Question
curl -X POST https://vibe-coding-production-cdb4.up.railway.app/api/generate-question \
  -H "Content-Type: application/json" \
  -d '{"previous_answers": ["Taipei"], "question_number": 2}'
```

### 本地測試

如果想在本地測試：

```bash
# 1. 啟動後端
python app.py

# 2. 打開前端
# 直接打開 index.html 或 test-connection.html
# config.js 會自動檢測 localhost
```

## 📚 詳細文檔

- `DEPLOYMENT_GUIDE.md` - 完整部署指南
- `RAILWAY_DEPLOYMENT.md` - Railway 詳細配置
- `test-connection.html` - API 測試工具

## 🎉 完成！

一旦所有測試通過，你的應用就完全部署好了！

用戶現在可以訪問:
- **前端**: https://vibe-coding-one-pink.vercel.app
- **後端**: https://vibe-coding-production-cdb4.up.railway.app

享受你的推薦系統吧！🎊
