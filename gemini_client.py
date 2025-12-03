#!/usr/bin/env python3
"""
Gemini API Client - 通用調用腳本
支持文本生成、對話、圖像分析等功能
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any
from pathlib import Path
import base64
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()


class GeminiClient:
    """Gemini API 客戶端"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Gemini 客戶端

        Args:
            api_key: Gemini API key，如果不提供則從環境變量 GEMINI_API_KEY 讀取
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("請提供 API key 或設置環境變量 GEMINI_API_KEY")

        self.base_url = "https://generativelanguage.googleapis.com/v1"

    def generate_text(
        self,
        prompt: str,
        model: str = "gemini-2.0-flash-001",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        生成文本

        Args:
            prompt: 輸入提示詞
            model: 模型名稱，默認 gemini-pro
            temperature: 溫度參數 (0.0-1.0)
            max_tokens: 最大生成 token 數

        Returns:
            API 響應結果
        """
        url = f"{self.base_url}/models/{model}:generateContent"

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
            }
        }

        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens

        return self._make_request(url, payload)

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-2.0-flash-001",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        對話功能

        Args:
            messages: 對話歷史，格式：[{"role": "user", "content": "..."}, ...]
            model: 模型名稱
            temperature: 溫度參數

        Returns:
            API 響應結果
        """
        url = f"{self.base_url}/models/{model}:generateContent"

        # 轉換消息格式為 Gemini 格式
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
            }
        }

        return self._make_request(url, payload)

    def analyze_image(
        self,
        image_path: str,
        prompt: str = "描述這張圖片",
        model: str = "gemini-2.0-flash-001"
    ) -> Dict[str, Any]:
        """
        圖像分析

        Args:
            image_path: 圖片文件路徑
            prompt: 分析提示詞
            model: 模型名稱，默認 gemini-pro-vision

        Returns:
            API 響應結果
        """
        url = f"{self.base_url}/models/{model}:generateContent"

        # 讀取並編碼圖片
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        # 獲取圖片 MIME 類型
        mime_type = self._get_mime_type(image_path)

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_data
                        }
                    }
                ]
            }]
        }

        return self._make_request(url, payload)

    def count_tokens(self, text: str, model: str = "gemini-2.0-flash-001") -> Dict[str, Any]:
        """
        計算 token 數量

        Args:
            text: 要計算的文本
            model: 模型名稱

        Returns:
            Token 計數結果
        """
        url = f"{self.base_url}/models/{model}:countTokens"

        payload = {
            "contents": [{
                "parts": [{"text": text}]
            }]
        }

        return self._make_request(url, payload)

    def _make_request(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        發送 API 請求

        Args:
            url: 請求 URL
            payload: 請求負載

        Returns:
            API 響應
        """
        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "key": self.api_key
        }

        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None),
                "response": getattr(e.response, 'text', None)
            }

    def _get_mime_type(self, file_path: str) -> str:
        """獲取文件 MIME 類型"""
        extension = Path(file_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        return mime_types.get(extension, 'image/jpeg')

    def extract_text(self, response: Dict[str, Any]) -> str:
        """
        從 API 響應中提取文本

        Args:
            response: API 響應

        Returns:
            提取的文本內容
        """
        try:
            if "error" in response:
                return f"錯誤: {response['error']}"

            candidates = response.get("candidates", [])
            if not candidates:
                return "沒有生成內容"

            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                return "沒有生成內容"

            return parts[0].get("text", "")

        except Exception as e:
            return f"解析響應時出錯: {str(e)}"


def main():
    """示例用法"""

    # 初始化客戶端
    # 方法 1: 直接提供 API key
    # client = GeminiClient(api_key="YOUR_API_KEY")

    # 方法 2: 使用環境變量 GEMINI_API_KEY
    try:
        client = GeminiClient()
    except ValueError as e:
        print(f"錯誤: {e}")
        print("請設置環境變量 GEMINI_API_KEY 或在代碼中提供 API key")
        return

    print("=" * 50)
    print("Gemini API 客戶端示例")
    print("=" * 50)

    # 示例 1: 文本生成
    print("\n1. 文本生成示例:")
    response = client.generate_text("用一句話介紹台灣")
    text = client.extract_text(response)
    print(f"回應: {text}")

    # 示例 2: 對話
    print("\n2. 對話示例:")
    messages = [
        {"role": "user", "content": "你好，請介紹一下你自己"},
        {"role": "assistant", "content": "你好！我是 Gemini，一個大型語言模型。"},
        {"role": "user", "content": "你能做什麼？"}
    ]
    response = client.chat(messages)
    text = client.extract_text(response)
    print(f"回應: {text}")

    # 示例 3: Token 計數
    print("\n3. Token 計數示例:")
    response = client.count_tokens("這是一段測試文本，用來計算 token 數量。")
    print(f"Token 計數結果: {json.dumps(response, indent=2, ensure_ascii=False)}")

    # 示例 4: 圖像分析（需要提供圖片路徑）
    # print("\n4. 圖像分析示例:")
    # response = client.analyze_image("path/to/image.jpg", "描述這張圖片中的內容")
    # text = client.extract_text(response)
    # print(f"回應: {text}")


if __name__ == "__main__":
    main()
