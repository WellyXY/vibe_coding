#!/usr/bin/env python3
"""
簡單的 Gemini 聊天機器人示例
"""

from gemini_client import GeminiClient


def main():
    print("=" * 50)
    print("Gemini 聊天機器人")
    print("=" * 50)
    print("輸入 'quit' 或 'exit' 離開")
    print("輸入 'clear' 清除對話歷史")
    print("=" * 50)

    # 初始化客戶端
    try:
        client = GeminiClient()
    except ValueError as e:
        print(f"\n錯誤: {e}")
        print("請確保 .env 文件中包含有效的 GEMINI_API_KEY")
        return

    messages = []

    while True:
        # 獲取用戶輸入
        user_input = input("\n你: ").strip()

        if not user_input:
            continue

        # 檢查退出命令
        if user_input.lower() in ['quit', 'exit']:
            print("\n再見！")
            break

        # 檢查清除命令
        if user_input.lower() == 'clear':
            messages = []
            print("\n對話歷史已清除！")
            continue

        # 添加用戶消息
        messages.append({"role": "user", "content": user_input})

        # 調用 Gemini API
        try:
            response = client.chat(messages)
            bot_response = client.extract_text(response)

            # 檢查是否有錯誤
            if bot_response.startswith("錯誤:"):
                print(f"\nGemini: {bot_response}")
                # 移除失敗的用戶消息
                messages.pop()
            else:
                # 添加助手回應到對話歷史
                messages.append({"role": "assistant", "content": bot_response})
                print(f"\nGemini: {bot_response}")

        except Exception as e:
            print(f"\n發生錯誤: {str(e)}")
            # 移除失敗的用戶消息
            messages.pop()


if __name__ == "__main__":
    main()
