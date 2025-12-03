# Railway 部署指南

## ✅ 已完成的配置

你的項目已經配置好連接到 Railway 後端：

- **Railway 域名**: `https://vibe-coding-production-cdb4.up.railway.app`
- **Vercel 前端**: `https://vibe-coding-one-pink.vercel.app`

## 🚀 部署步驟

### 1. 確保 Railway 後端正確部署

在 Railway 項目中，確保以下配置：

#### 環境變量設置
進入 Railway Dashboard > 你的項目 > Variables，添加：

```bash
FLASK_ENV=production
PORT=5000
GEMINI_API_KEY=你的_Gemini_API_Key（如果需要）
```

#### 確認部署文件
確保項目根目錄有以下文件：

- ✅ `requirements.txt` - Python 依賴
- ✅ `app.py` - 主應用程序
- ✅ `Procfile` 或 `railway.toml` - 啟動配置

**Procfile 示例**（如果還沒有，創建一個）:
```
web: gunicorn app:app
```

**railway.toml 示例**（或使用這個）:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn app:app"
healthcheckPath = "/api/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
```

### 2. 更新並重新部署 Vercel

```bash
# 在項目根目錄執行
git add .
git commit -m "Update API config for Railway backend"
git push

# Vercel 會自動重新部署
# 或手動觸發部署：
vercel --prod
```

### 3. 測試連接

#### 方法 1：使用測試頁面
1. 在本地打開 `test-connection.html`
2. 點擊測試按鈕驗證連接

#### 方法 2：直接測試 Railway API
在瀏覽器中打開：
```
https://vibe-coding-production-cdb4.up.railway.app/api/health
```

應該看到：
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

#### 方法 3：測試 CORS
在瀏覽器控制台（F12）執行：
```javascript
fetch('https://vibe-coding-production-cdb4.up.railway.app/api/options')
  .then(r => r.json())
  .then(d => console.log(d))
  .catch(e => console.error(e))
```

## 🔍 常見問題排查

### 問題 1: Railway 後端無法訪問

**症狀**:
```
Failed to fetch
ERR_CONNECTION_REFUSED
```

**解決方案**:
1. 檢查 Railway 部署狀態（Dashboard > Deployments）
2. 確認服務正在運行（綠色勾號）
3. 查看部署日誌是否有錯誤

### 問題 2: 仍然有 CORS 錯誤

**症狀**:
```
Access to fetch has been blocked by CORS policy
```

**解決方案**:
1. 確保 `app.py` 中的 CORS 配置包含你的 Vercel 域名
2. 在 Railway 上重新部署後端：
   ```bash
   # 觸發重新部署
   git commit --allow-empty -m "Redeploy with CORS fix"
   git push
   ```

### 問題 3: API 返回 404

**症狀**:
```
GET https://vibe-coding-production-cdb4.up.railway.app/api/options 404
```

**解決方案**:
1. 確認 Railway 啟動命令正確
2. 檢查 `app.py` 中的路由定義
3. 查看 Railway 部署日誌

### 問題 4: 環境變量未生效

**解決方案**:
1. 在 Railway Dashboard 確認變量已設置
2. 重新部署服務
3. 在 Railway 日誌中檢查變量是否正確加載

## 📊 部署檢查清單

在推送到生產環境前，確認：

- [ ] Railway 後端已部署並運行
- [ ] 訪問 `https://vibe-coding-production-cdb4.up.railway.app/api/health` 返回成功
- [ ] `config.js` 使用正確的 Railway URL
- [ ] `app.py` CORS 配置包含 Vercel 域名
- [ ] 所有環境變量已在 Railway 設置
- [ ] Vercel 前端已重新部署
- [ ] 測試頁面所有測試通過

## 🎯 驗證部署成功

1. **打開 Vercel 網站**: `https://vibe-coding-one-pink.vercel.app`
2. **打開瀏覽器開發者工具** (F12)
3. **查看 Console**，應該看到：
   ```
   🔧 API Config: {
     environment: "production",
     baseURL: "https://vibe-coding-production-cdb4.up.railway.app"
   }
   ```
4. **點擊 Agent 頭像**，應該能正常獲取問題
5. **沒有 CORS 錯誤**

## 🆘 需要幫助？

如果遇到問題：

1. 檢查 Railway 部署日誌
2. 檢查瀏覽器 Console 錯誤
3. 使用 `test-connection.html` 測試連接
4. 確認所有文件已正確推送到 Git

## 📝 快速命令參考

```bash
# 查看 Railway 日誌
railway logs

# 重新部署 Railway
railway up

# 重新部署 Vercel
vercel --prod

# 本地測試
python app.py
# 然後打開 test-connection.html
```
