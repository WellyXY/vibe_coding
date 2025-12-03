#!/usr/bin/env python3
"""
基於 Gemini 的用戶推薦系統
根據用戶的正向信號（location, hobby, age, occupation 等）推薦最匹配的用戶
"""

import json
from typing import List, Dict, Any
from gemini_client import GeminiClient


class UserRecommendationSystem:
    """用戶推薦系統"""

    def __init__(self, database_path: str = "users_database.json"):
        """
        初始化推薦系統

        Args:
            database_path: 用戶數據庫 JSON 文件路徑
        """
        self.client = GeminiClient()
        self.database_path = database_path
        self.users = self._load_database()

    def _load_database(self) -> List[Dict]:
        """載入用戶數據庫"""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到用戶數據庫文件: {self.database_path}")

    def recommend(
        self,
        criteria: Dict[str, Any],
        top_k: int = 5,
        use_ai_ranking: bool = True
    ) -> List[Dict]:
        """
        根據條件推薦用戶

        Args:
            criteria: 推薦條件，例如 {"location": "台北", "hobby": "攝影"}
                     或 {"description": "looking for someone who..."}
            top_k: 返回前 k 個推薦結果
            use_ai_ranking: 是否使用 AI 進行智能排序

        Returns:
            推薦的用戶列表
        """
        # Check if this is a description-only search (free-form text)
        has_description = 'description' in criteria and criteria['description']
        other_criteria = {k: v for k, v in criteria.items() if k != 'description' and v}

        # If only description is provided, let AI handle all users
        if has_description and not other_criteria:
            print(f"🎯 使用描述搜索: {criteria['description'][:50]}...")
            filtered_users = self.users  # Use all users for AI ranking
            print(f"📊 將從 {len(filtered_users)} 個用戶中使用 AI 篩選")
        else:
            # 1. 基礎過濾：找出符合基本條件的用戶
            filtered_users = self._filter_users(criteria)

            print(f"📊 基礎過濾後找到 {len(filtered_users)} 個匹配用戶")

            if len(filtered_users) == 0:
                print("⚠️  沒有找到完全匹配的用戶，嘗試放寬條件...")
                filtered_users = self._filter_users(criteria, strict=False)
                print(f"📊 放寬條件後找到 {len(filtered_users)} 個用戶")

            # 確保至少有 top_k 個用戶
            if len(filtered_users) < top_k:
                print(f"⚠️  用戶數量不足 {top_k} 個，從所有用戶中隨機補充...")
                # 獲取所有用戶 ID
                filtered_ids = set(user['id'] for user in filtered_users)
                # 從剩餘用戶中隨機選擇
                remaining_users = [u for u in self.users if u['id'] not in filtered_ids]
                import random
                random.shuffle(remaining_users)
                # 補充到 top_k 個
                needed = top_k - len(filtered_users)
                filtered_users.extend(remaining_users[:needed])
                print(f"📊 補充後共有 {len(filtered_users)} 個用戶")

        # 2. 使用 Gemini 進行智能排序
        if use_ai_ranking and len(filtered_users) > 0:
            ranked_users = self._rank_with_ai(filtered_users, criteria, top_k)
        else:
            ranked_users = filtered_users[:top_k]

        return ranked_users

    def _filter_users(self, criteria: Dict[str, Any], strict: bool = True) -> List[Dict]:
        """
        過濾用戶

        Args:
            criteria: 過濾條件
            strict: 是否嚴格匹配（True=必須完全匹配，False=部分匹配即可）

        Returns:
            符合條件的用戶列表
        """
        filtered = []

        for user in self.users:
            match_count = 0
            total_criteria = 0

            for key, value in criteria.items():
                if value is None or value == "":
                    continue

                total_criteria += 1

                if key == "location":
                    # Exact match for location
                    if user["location"].lower() == value.lower():
                        match_count += 1
                elif key == "hobby":
                    # 支持單個興趣或興趣列表
                    target_hobbies = [value] if isinstance(value, str) else value
                    user_hobbies_str = " ".join(user["hobby"]).lower()

                    for hobby in target_hobbies:
                        if hobby.lower() in user_hobbies_str:
                            match_count += 1
                            break
                elif key == "occupation":
                    if value.lower() in user["occupation"].lower() or user["occupation"].lower() in value.lower():
                        match_count += 1
                elif key == "age_min":
                    if user["age"] >= value:
                        match_count += 1
                elif key == "age_max":
                    if user["age"] <= value:
                        match_count += 1
                elif key == "gender":
                    if user["gender"].lower() == value.lower():
                        match_count += 1
                else:
                    # 其他條件直接比對
                    if str(user.get(key, "")).lower() == str(value).lower():
                        match_count += 1

            # 嚴格模式：必須全部匹配；寬鬆模式：至少匹配一個
            if strict:
                if total_criteria > 0 and match_count == total_criteria:
                    filtered.append(user)
            else:
                if match_count > 0:
                    filtered.append(user)

        return filtered

    def _rank_with_ai(
        self,
        users: List[Dict],
        criteria: Dict[str, Any],
        top_k: int
    ) -> List[Dict]:
        """
        使用 Gemini AI 對用戶進行智能排序

        Args:
            users: 待排序的用戶列表
            criteria: 用戶的搜索條件
            top_k: 返回前 k 個結果

        Returns:
            排序後的用戶列表
        """
        print(f"🤖 使用 Gemini AI 進行智能排序...")

        # 構建提示詞
        prompt = self._build_ranking_prompt(users, criteria, top_k)

        # 調用 Gemini
        response = self.client.generate_text(
            prompt=prompt,
            temperature=0.3,  # 較低的溫度以獲得更穩定的結果
            max_tokens=2000
        )

        # 提取結果
        ai_response = self.client.extract_text(response)

        # 解析 AI 的排序結果
        ranked_users = self._parse_ranking_result(ai_response, users)

        return ranked_users[:top_k]

    def _build_ranking_prompt(
        self,
        users: List[Dict],
        criteria: Dict[str, Any],
        top_k: int
    ) -> str:
        """構建 Gemini 排序提示詞"""

        # 構建用戶信息字符串
        users_info = []
        for i, user in enumerate(users, 1):
            user_str = f"{i}. ID:{user['id']}, {user['name']}, {user['age']}歲, {user['occupation']}, {user['location']}, 興趣:{', '.join(user['hobby'])}, {user['gender']}"
            users_info.append(user_str)

        users_text = "\n".join(users_info)

        # 構建條件字符串
        criteria_parts = []
        user_description = None

        for key, value in criteria.items():
            if value is not None and value != "":
                if key == "description":
                    # Handle free-form description separately
                    user_description = value
                elif key == "location":
                    criteria_parts.append(f"地區在 {value}")
                elif key == "hobby":
                    hobbies = [value] if isinstance(value, str) else value
                    criteria_parts.append(f"興趣包含 {', '.join(hobbies)}")
                elif key == "occupation":
                    criteria_parts.append(f"職業是 {value}")
                elif key == "age_min":
                    criteria_parts.append(f"年齡至少 {value} 歲")
                elif key == "age_max":
                    criteria_parts.append(f"年齡最多 {value} 歲")
                elif key == "gender":
                    criteria_parts.append(f"性別是 {value}")

        # If user provided a description, use it as the main criteria
        if user_description:
            criteria_text = f"用戶描述：{user_description}"
            if criteria_parts:
                criteria_text += f"\n其他條件：{'、'.join(criteria_parts)}"
        else:
            criteria_text = "、".join(criteria_parts) if criteria_parts else "無特定條件"

        prompt = f"""你是一個專業的用戶推薦系統。我需要你根據以下條件，從候選用戶中選出最匹配的 {top_k} 個用戶，並按照匹配度從高到低排序。

搜索條件：
{criteria_text}

候選用戶列表：
{users_text}

請仔細分析每個用戶與搜索條件的匹配程度，考慮以下因素：
1. **性別（Gender）**：如果用戶描述中提到性別要求（如 "female", "male", "woman", "man"），這是最重要的過濾條件，必須嚴格匹配
2. **地區（Location）**：完全匹配的條件
3. **興趣（Hobbies）**：部分匹配的條件，興趣的重疊度
4. **年齡（Age）**：年齡的接近程度
5. **職業（Occupation）**：職業的相關性
6. **其他描述**：用戶自由描述中的其他偏好

**重要**：如果用戶描述中明確要求特定性別（如 "looking for female"），請只返回該性別的用戶。性別要求是硬性條件。

請按照以下格式輸出推薦結果（只輸出 ID，用逗號分隔，不要有其他說明）：
ID1, ID2, ID3, ID4, ID5

例如：42, 17, 89, 3, 56"""

        return prompt

    def _parse_ranking_result(self, ai_response: str, users: List[Dict]) -> List[Dict]:
        """
        解析 AI 的排序結果

        Args:
            ai_response: AI 的回應文本
            users: 原始用戶列表

        Returns:
            排序後的用戶列表
        """
        try:
            # 提取 ID
            # 尋找數字序列
            import re
            # 移除所有非數字和逗號的字符，然後分割
            numbers_line = ai_response.strip().split('\n')[-1]  # 取最後一行
            ids_str = re.sub(r'[^0-9,]', '', numbers_line)
            ranked_ids = [int(id_str.strip()) for id_str in ids_str.split(',') if id_str.strip()]

            # 根據 ID 排序用戶
            id_to_user = {user['id']: user for user in users}
            ranked_users = []

            for user_id in ranked_ids:
                if user_id in id_to_user:
                    ranked_users.append(id_to_user[user_id])

            # 如果 AI 沒有返回足夠的用戶，補充剩餘的用戶
            existing_ids = set(ranked_ids)
            for user in users:
                if user['id'] not in existing_ids and len(ranked_users) < len(users):
                    ranked_users.append(user)

            return ranked_users

        except Exception as e:
            print(f"⚠️  解析 AI 結果時出錯: {e}")
            print(f"AI 回應: {ai_response}")
            # 如果解析失敗，返回原始列表
            return users

    def save_recommendations(self, recommendations: List[Dict], output_file: str = "recommendations.json"):
        """
        保存推薦結果到 JSON 文件

        Args:
            recommendations: 推薦結果列表
            output_file: 輸出文件名
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=2)
        print(f"💾 推薦結果已保存至: {output_file}")

    def print_recommendations(self, recommendations: List[Dict]):
        """
        打印推薦結果

        Args:
            recommendations: 推薦結果列表
        """
        if not recommendations:
            print("❌ 沒有找到匹配的用戶")
            return

        print(f"\n✨ 推薦結果（共 {len(recommendations)} 個用戶）：\n")
        print("=" * 80)

        for i, user in enumerate(recommendations, 1):
            print(f"\n排名 {i}: {user['name']}")
            print(f"  年齡: {user['age']} 歲")
            print(f"  職業: {user['occupation']}")
            print(f"  地區: {user['location']}")
            print(f"  興趣: {', '.join(user['hobby'])}")
            print(f"  性別: {user['gender']}")
            print(f"  頭像: {user['image']}")
            print("-" * 80)


def main():
    """示例使用"""
    print("🚀 用戶推薦系統\n")

    # 初始化推薦系統
    rec_system = UserRecommendationSystem()

    # 示例 1: 尋找台北地區喜歡攝影的用戶
    print("\n" + "=" * 80)
    print("示例 1: 尋找台北地區喜歡攝影的用戶")
    print("=" * 80)

    criteria1 = {
        "location": "台北",
        "hobby": "攝影"
    }

    recommendations1 = rec_system.recommend(criteria1, top_k=5)
    rec_system.print_recommendations(recommendations1)
    rec_system.save_recommendations(recommendations1, "recommendations_example1.json")

    # 示例 2: 尋找 25-35 歲的工程師
    print("\n" + "=" * 80)
    print("示例 2: 尋找 25-35 歲，職業是工程師的用戶")
    print("=" * 80)

    criteria2 = {
        "age_min": 25,
        "age_max": 35,
        "occupation": "Engineer"
    }

    recommendations2 = rec_system.recommend(criteria2, top_k=5)
    rec_system.print_recommendations(recommendations2)
    rec_system.save_recommendations(recommendations2, "recommendations_example2.json")

    # 示例 3: 尋找喜歡旅遊和烹飪的用戶
    print("\n" + "=" * 80)
    print("示例 3: 尋找喜歡旅遊和烹飪的用戶")
    print("=" * 80)

    criteria3 = {
        "hobby": ["旅遊", "烹飪"]
    }

    recommendations3 = rec_system.recommend(criteria3, top_k=5)
    rec_system.print_recommendations(recommendations3)
    rec_system.save_recommendations(recommendations3, "recommendations_example3.json")


if __name__ == "__main__":
    main()
