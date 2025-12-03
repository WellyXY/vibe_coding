# 快速開始指南

## 🎯 5 分鐘快速上手用戶推薦系統

### 步驟 1: 確認文件已準備好

確認以下文件存在：
- ✅ `users_database.json` - 用戶數據庫
- ✅ `avatars/` - 頭像文件夾（100 張照片）
- ✅ `gemini_client.py` - Gemini API 客戶端
- ✅ `recommendation_system.py` - 推薦系統
- ✅ `.env` - API key 配置

### 步驟 2: 安裝依賴

```bash
pip3 install -r requirements.txt
```

### 步驟 3: 開始使用推薦系統

#### 方法 A: 互動式推薦（最簡單）

```bash
python3 interactive_recommend.py
```

然後按照提示輸入條件：
```
🌍 地區（例如：台北、New York）: 台北
🎨 興趣（多個請用逗號分隔）: 攝影, 旅遊
💼 職業（例如：Engineer、Designer）: Designer
🎂 最小年齡: 25
🎂 最大年齡: 35
⚧ 性別（Male/Female/Non-binary）:
```

系統會返回最匹配的 5 個用戶！

#### 方法 B: 使用預設示例

```bash
python3 recommendation_system.py
```

這會運行 3 個預設的推薦示例。

#### 方法 C: 在代碼中使用

```python
from recommendation_system import UserRecommendationSystem

# 初始化
rec_system = UserRecommendationSystem()

# 設定條件
criteria = {
    "location": "台北",
    "hobby": "攝影"
}

# 獲取推薦
recommendations = rec_system.recommend(criteria, top_k=5)

# 顯示結果
rec_system.print_recommendations(recommendations)
```

### 步驟 4: 查看推薦結果（可視化）

推薦結果保存為 JSON 文件後，可以用瀏覽器查看：

```bash
# 在瀏覽器中打開
open view_recommendations.html
```

然後選擇推薦結果 JSON 文件（例如 `recommendations_example1.json`）。

---

## 📝 常用命令

### 重新生成用戶數據庫

```bash
python3 generate_users.py
```

### 重新下載頭像

```bash
python3 download_avatars.py
```

### 查看用戶數據庫統計

```bash
python3 -c "
import json
with open('users_database.json', 'r', encoding='utf-8') as f:
    users = json.load(f)
    print(f'總用戶數: {len(users)}')
    locations = {}
    for user in users:
        locations[user['location']] = locations.get(user['location'], 0) + 1
    print(f'地區分布: {dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])}')
"
```

---

## 🎨 自定義推薦條件

### 單一條件

```python
# 只找特定地區
{"location": "台北"}

# 只找特定興趣
{"hobby": "攝影"}

# 只找特定年齡
{"age_min": 25, "age_max": 35}
```

### 組合條件

```python
# 地區 + 興趣
{"location": "台北", "hobby": "攝影"}

# 年齡 + 職業
{"age_min": 25, "age_max": 35, "occupation": "Engineer"}

# 多個興趣
{"hobby": ["攝影", "旅遊", "烹飪"]}

# 完整條件
{
    "location": "台北",
    "hobby": ["攝影", "旅遊"],
    "age_min": 25,
    "age_max": 40,
    "occupation": "Designer",
    "gender": "Female"
}
```

---

## 🚀 進階使用

### 批量推薦

創建文件 `batch_recommend.py`:

```python
from recommendation_system import UserRecommendationSystem

rec_system = UserRecommendationSystem()

# 定義多組條件
criteria_list = [
    {"location": "台北", "hobby": "攝影"},
    {"age_min": 25, "age_max": 35, "occupation": "Engineer"},
    {"hobby": ["旅遊", "烹飪"]},
]

# 批量執行
for i, criteria in enumerate(criteria_list, 1):
    print(f"\n=== 推薦組 {i} ===")
    recommendations = rec_system.recommend(criteria)
    rec_system.print_recommendations(recommendations)
    rec_system.save_recommendations(recommendations, f"batch_{i}.json")
```

運行：
```bash
python3 batch_recommend.py
```

### 整合到 Web API

創建文件 `api_server.py`:

```python
from flask import Flask, request, jsonify
from recommendation_system import UserRecommendationSystem

app = Flask(__name__)
rec_system = UserRecommendationSystem()

@app.route('/recommend', methods=['POST'])
def recommend():
    criteria = request.json
    top_k = criteria.pop('top_k', 5)
    recommendations = rec_system.recommend(criteria, top_k=top_k)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(port=5000)
```

運行：
```bash
pip install flask
python3 api_server.py
```

使用 API：
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"location": "台北", "hobby": "攝影", "top_k": 3}'
```

---

## ❓ 常見問題

### Q: 推薦結果太少怎麼辦？
A: 可以：
1. 減少篩選條件
2. 放寬年齡範圍
3. 使用更通用的關鍵詞（如用 "Engineer" 代替 "Software Engineer"）

### Q: 如何提高推薦準確度？
A:
1. 使用多個條件組合
2. 提供更具體的條件
3. 確保 `use_ai_ranking=True`

### Q: 可以自定義用戶數據嗎？
A: 當然！直接編輯 `users_database.json` 或修改 `generate_users.py` 重新生成。

### Q: 如何更換頭像？
A:
1. 將新照片放入 `avatars/` 文件夾
2. 更新 `users_database.json` 中的 `image` 字段

---

## 📚 更多資源

- 詳細文檔: `RECOMMENDATION_README.md`
- Gemini API 文檔: `GEMINI_README.md`
- 源代碼: `recommendation_system.py`, `gemini_client.py`

---

## 🎉 開始體驗！

```bash
python3 interactive_recommend.py
```

祝您使用愉快！
