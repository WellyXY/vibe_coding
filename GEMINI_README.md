# Gemini API 客戶端使用說明

這是一個通用的 Python Gemini API 調用腳本，支持文本生成、對話、圖像分析等功能。

## 安裝

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 配置 API Key：

已經為您配置好了 `.env` 文件，包含您的 API key。

## 功能特性

- ✅ 文本生成
- ✅ 多輪對話
- ✅ 圖像分析（使用 Gemini Vision）
- ✅ Token 計數
- ✅ 完整的錯誤處理
- ✅ 類型提示支持

## 快速開始

### 1. 運行示例程序

```bash
python gemini_client.py
```

這將運行內置的示例，展示各種功能。

### 2. 在您的代碼中使用

```python
from gemini_client import GeminiClient

# 初始化客戶端（自動從 .env 加載 API key）
client = GeminiClient()

# 或者直接提供 API key
# client = GeminiClient(api_key="YOUR_API_KEY")
```

## 使用示例

### 文本生成

```python
from gemini_client import GeminiClient

client = GeminiClient()

# 生成文本
response = client.generate_text(
    prompt="寫一首關於春天的詩",
    temperature=0.8,
    max_tokens=500
)

# 提取文本
text = client.extract_text(response)
print(text)
```

### 多輪對話

```python
from gemini_client import GeminiClient

client = GeminiClient()

# 準備對話歷史
messages = [
    {"role": "user", "content": "什麼是機器學習？"},
    {"role": "assistant", "content": "機器學習是人工智能的一個分支..."},
    {"role": "user", "content": "它有哪些應用？"}
]

# 發送對話
response = client.chat(messages, temperature=0.7)
text = client.extract_text(response)
print(text)
```

### 圖像分析

```python
from gemini_client import GeminiClient

client = GeminiClient()

# 分析圖片
response = client.analyze_image(
    image_path="path/to/your/image.jpg",
    prompt="詳細描述這張圖片中的內容"
)

text = client.extract_text(response)
print(text)
```

### Token 計數

```python
from gemini_client import GeminiClient

client = GeminiClient()

# 計算 token 數
response = client.count_tokens("這是一段需要計算 token 的文本")
print(response)
```

## 完整 API 參考

### GeminiClient 類

#### `__init__(api_key: Optional[str] = None)`
初始化客戶端
- `api_key`: API key（可選，默認從環境變量讀取）

#### `generate_text(prompt, model="gemini-pro", temperature=0.7, max_tokens=None)`
生成文本
- `prompt`: 輸入提示詞
- `model`: 模型名稱
- `temperature`: 溫度參數 (0.0-1.0)
- `max_tokens`: 最大 token 數

#### `chat(messages, model="gemini-pro", temperature=0.7)`
多輪對話
- `messages`: 對話歷史列表
- `model`: 模型名稱
- `temperature`: 溫度參數

#### `analyze_image(image_path, prompt="描述這張圖片", model="gemini-pro-vision")`
圖像分析
- `image_path`: 圖片文件路徑
- `prompt`: 分析提示詞
- `model`: 模型名稱

#### `count_tokens(text, model="gemini-pro")`
計算 token 數量
- `text`: 要計算的文本
- `model`: 模型名稱

#### `extract_text(response)`
從 API 響應中提取文本
- `response`: API 響應字典

## 支持的模型

- `gemini-2.5-flash`: 最新的中型多模態模型（支持 1M tokens）
- `gemini-2.5-pro`: 最新的專業版模型
- `gemini-2.0-flash-001`: 穩定版本（默認使用）
- `gemini-2.0-flash`: 快速且多功能的多模態模型

所有這些模型都支持文本生成、對話和圖像分析功能。

## 支持的圖片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## 錯誤處理

所有方法都包含完整的錯誤處理。如果發生錯誤，響應中會包含 `error` 字段：

```python
response = client.generate_text("test")
if "error" in response:
    print(f"發生錯誤: {response['error']}")
else:
    text = client.extract_text(response)
    print(text)
```

## 實用腳本示例

### 簡單的命令行聊天機器人

```python
from gemini_client import GeminiClient

def chat_bot():
    client = GeminiClient()
    messages = []

    print("聊天機器人已啟動！輸入 'quit' 退出")

    while True:
        user_input = input("\n你: ")
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})
        response = client.chat(messages)
        bot_response = client.extract_text(response)

        messages.append({"role": "assistant", "content": bot_response})
        print(f"\n機器人: {bot_response}")

if __name__ == "__main__":
    chat_bot()
```

### 批量圖片分析

```python
from gemini_client import GeminiClient
from pathlib import Path

def analyze_images_in_folder(folder_path):
    client = GeminiClient()
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

    for image_path in Path(folder_path).glob('*'):
        if image_path.suffix.lower() in image_extensions:
            print(f"\n分析圖片: {image_path.name}")
            response = client.analyze_image(str(image_path))
            text = client.extract_text(response)
            print(f"分析結果: {text}\n")

if __name__ == "__main__":
    analyze_images_in_folder("./images")
```

### 內容生成器

```python
from gemini_client import GeminiClient

def generate_blog_post(topic):
    client = GeminiClient()

    # 生成標題
    title_prompt = f"為以下主題生成一個吸引人的部落格文章標題：{topic}"
    title_response = client.generate_text(title_prompt, temperature=0.8)
    title = client.extract_text(title_response)

    # 生成內容
    content_prompt = f"寫一篇關於 '{topic}' 的詳細部落格文章，標題為：{title}"
    content_response = client.generate_text(content_prompt, temperature=0.7, max_tokens=2000)
    content = client.extract_text(content_response)

    return {
        "title": title,
        "content": content
    }

if __name__ == "__main__":
    post = generate_blog_post("人工智能的未來發展")
    print(f"標題: {post['title']}\n")
    print(f"內容:\n{post['content']}")
```

## 注意事項

- API key 已經配置在 `.env` 文件中，請妥善保管
- 請勿將 `.env` 文件提交到版本控制系統
- Gemini API 有使用配額限制，請合理使用
- 大型圖片分析可能需要較長時間

## 故障排除

### 找不到 API key
確保 `.env` 文件存在且包含正確的 `GEMINI_API_KEY`

### 請求失敗
檢查網絡連接和 API key 是否有效

### 圖片分析失敗
確保圖片格式支持且文件路徑正確

## 參考資源

- [Gemini API 官方文檔](https://ai.google.dev/docs)
- [API 密鑰管理](https://makersuite.google.com/app/apikey)
