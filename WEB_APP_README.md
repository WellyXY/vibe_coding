# 🎯 Discover - 對話式用戶推薦系統

## 使用說明

### 啟動應用

1. **啟動後端服務器**
   ```bash
   python3 app.py
   ```

2. **訪問網頁界面**

   在瀏覽器中打開：http://localhost:5000

   或運行：
   ```bash
   open http://localhost:5000
   ```

### 使用流程

1. **Agent 提問**
   - Agent 會問你："Looking for someone in xxx?"
   - 每次會給你多個選項按鈕

2. **選擇選項**
   - 點擊你想要的選項
   - 例如：選擇地區 "台北"、興趣 "攝影" 等

3. **跳過問題**（可選）
   - 如果不想回答某個問題，點擊 "Skip this question"

4. **查看推薦結果**
   - 回答完所有問題後，系統會推薦 Top 5 用戶
   - 每個用戶顯示：頭像、姓名、年齡、職業、地區、興趣

5. **重新開始**
   - 點擊 "Start Over" 按鈕重新搜索

## 對話流程

```
Agent: Hi! 👋 I'm here to help you find the perfect match.

Agent: Looking for someone in a specific location?
[台北] [新北] [台中] [高雄] [New York] [Tokyo]...
User: 點擊 "台北"

Agent: What kind of hobbies should they have?
[攝影] [旅遊] [閱讀] [運動] [音樂]...
User: 點擊 "攝影"

Agent: Any specific occupation in mind?
[Engineer] [Designer] [Teacher] [Doctor]...
User: 點擊 "Engineer"

Agent: What age range are you looking for?
[18-25] [26-35] [36-45] [46-60] [60+]
User: 點擊 "26-35"

Agent: Great! Let me find the best matches for you...
[顯示 Top 5 推薦用戶卡片]
```

## API 接口

### 獲取選項
```
GET /api/options
```

返回所有可用的地區、職業、興趣選項。

### 推薦用戶
```
POST /api/recommend
Content-Type: application/json

{
  "criteria": {
    "location": "台北",
    "hobby": "攝影",
    "occupation": "Engineer",
    "age_min": 26,
    "age_max": 35
  },
  "top_k": 5
}
```

返回推薦的用戶列表。

## 技術架構

```
前端（discover.html）
  ↓ HTTP Request
後端（Flask - app.py）
  ↓ 調用
推薦系統（recommendation_system.py）
  ↓ 調用
Gemini AI（gemini_client.py）
```

## 功能特點

✅ **對話式界面** - 像聊天機器人一樣互動
✅ **智能推薦** - 使用 Gemini AI 排序
✅ **美觀設計** - 現代化 UI，流暢動畫
✅ **即時反饋** - 點擊立即響應
✅ **可跳過問題** - 靈活的篩選條件
✅ **Top 5 展示** - 卡片式展示推薦結果

## 停止服務器

在終端按 `Ctrl+C` 停止服務器。

## 故障排除

### 問題：無法連接到服務器
**解決**：確保運行了 `python3 app.py`

### 問題：推薦結果為空
**解決**：
1. 嘗試跳過一些問題（條件太嚴格）
2. 選擇更常見的選項

### 問題：頭像無法顯示
**解決**：確保 `avatars/` 文件夾存在且包含圖片

## 自定義

### 修改問題數量
編輯 `discover.html` 中的 `steps` 數組。

### 修改選項數量
在 `showOptions()` 函數中修改 `.slice(0, 8)` 的數字。

### 修改推薦數量
在 `showRecommendations()` 函數中修改 `top_k: 5`。

---

**開始使用**: `python3 app.py` 然後訪問 http://localhost:5000 🚀
