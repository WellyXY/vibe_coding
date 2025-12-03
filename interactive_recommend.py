#!/usr/bin/env python3
"""
互動式用戶推薦系統
允許用戶輸入條件並獲得推薦結果
"""

from recommendation_system import UserRecommendationSystem
import json


def get_input(prompt: str, required: bool = False, input_type: str = "str"):
    """獲取用戶輸入"""
    while True:
        value = input(prompt).strip()

        if not value and not required:
            return None

        if not value and required:
            print("❌ 此項為必填，請重新輸入")
            continue

        # 類型轉換
        if input_type == "int":
            try:
                return int(value)
            except ValueError:
                print("❌ 請輸入有效的數字")
                continue
        elif input_type == "list":
            # 支持逗號分隔的列表
            return [item.strip() for item in value.split(',') if item.strip()]

        return value


def display_welcome():
    """顯示歡迎信息"""
    print("=" * 80)
    print(" " * 25 + "🎯 用戶推薦系統")
    print("=" * 80)
    print("\n歡迎使用基於 Gemini AI 的智能用戶推薦系統！")
    print("請輸入您的篩選條件，系統將為您推薦最匹配的用戶。")
    print("\n提示：不需要的條件可以直接按 Enter 跳過")
    print("=" * 80)


def collect_criteria():
    """收集用戶輸入的篩選條件"""
    print("\n📝 請輸入篩選條件：\n")

    criteria = {}

    # 地區
    location = get_input("🌍 地區（例如：台北、New York）: ")
    if location:
        criteria["location"] = location

    # 興趣
    hobby_input = get_input("🎨 興趣（多個請用逗號分隔，例如：攝影, 旅遊）: ")
    if hobby_input:
        hobbies = [h.strip() for h in hobby_input.split(',') if h.strip()]
        criteria["hobby"] = hobbies if len(hobbies) > 1 else hobbies[0]

    # 職業
    occupation = get_input("💼 職業（例如：Engineer、Designer）: ")
    if occupation:
        criteria["occupation"] = occupation

    # 年齡範圍
    age_min = get_input("🎂 最小年齡: ", input_type="int")
    if age_min:
        criteria["age_min"] = age_min

    age_max = get_input("🎂 最大年齡: ", input_type="int")
    if age_max:
        criteria["age_max"] = age_max

    # 性別
    gender = get_input("⚧ 性別（Male/Female/Non-binary）: ")
    if gender:
        criteria["gender"] = gender

    return criteria


def display_summary(criteria: dict):
    """顯示篩選條件摘要"""
    print("\n" + "=" * 80)
    print("📋 您的篩選條件摘要：")
    print("=" * 80)

    if not criteria:
        print("  無特定條件（將返回隨機用戶）")
    else:
        for key, value in criteria.items():
            if key == "location":
                print(f"  🌍 地區: {value}")
            elif key == "hobby":
                hobbies = value if isinstance(value, list) else [value]
                print(f"  🎨 興趣: {', '.join(hobbies)}")
            elif key == "occupation":
                print(f"  💼 職業: {value}")
            elif key == "age_min":
                print(f"  🎂 最小年齡: {value} 歲")
            elif key == "age_max":
                print(f"  🎂 最大年齡: {value} 歲")
            elif key == "gender":
                print(f"  ⚧ 性別: {value}")

    print("=" * 80)


def main():
    """主程序"""
    display_welcome()

    # 初始化推薦系統
    try:
        rec_system = UserRecommendationSystem()
    except FileNotFoundError as e:
        print(f"\n❌ 錯誤: {e}")
        print("請先運行 generate_users.py 生成用戶數據庫")
        return
    except Exception as e:
        print(f"\n❌ 初始化失敗: {e}")
        return

    while True:
        # 收集篩選條件
        criteria = collect_criteria()

        # 顯示摘要
        display_summary(criteria)

        # 確認是否繼續
        confirm = get_input("\n是否開始推薦？(y/n): ")
        if confirm.lower() != 'y':
            print("已取消推薦")
            retry = get_input("\n是否重新輸入條件？(y/n): ")
            if retry.lower() == 'y':
                continue
            else:
                break

        # 獲取推薦數量
        top_k = get_input("\n想要推薦幾個用戶？(默認 5): ", input_type="int")
        if not top_k:
            top_k = 5

        # 執行推薦
        print(f"\n🔍 正在搜索匹配用戶...")
        recommendations = rec_system.recommend(criteria, top_k=top_k)

        # 顯示結果
        rec_system.print_recommendations(recommendations)

        # 保存結果
        save = get_input("\n是否保存推薦結果到文件？(y/n): ")
        if save.lower() == 'y':
            filename = get_input("文件名（默認 my_recommendations.json）: ")
            if not filename:
                filename = "my_recommendations.json"
            elif not filename.endswith('.json'):
                filename += '.json'

            rec_system.save_recommendations(recommendations, filename)

        # 是否繼續
        print("\n" + "=" * 80)
        continue_search = get_input("\n是否繼續搜索？(y/n): ")
        if continue_search.lower() != 'y':
            print("\n👋 感謝使用用戶推薦系統！再見！")
            break


if __name__ == "__main__":
    main()
