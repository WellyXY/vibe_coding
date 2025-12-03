#!/usr/bin/env python3
"""
生成用戶數據庫
使用隨機數據生成 100 個用戶
"""

import json
import random
from typing import List, Dict

# 配置數據
FIRST_NAMES = [
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William",
    "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Harper", "Henry", "Evelyn", "Alexander",
    "Abigail", "Michael", "Emily", "Daniel", "Elizabeth", "Matthew", "Sofia", "Jackson", "Avery", "Sebastian",
    "Ella", "David", "Madison", "Joseph", "Scarlett", "Carter", "Victoria", "Owen", "Aria", "Wyatt",
    "Grace", "John", "Chloe", "Jack", "Camila", "Luke", "Penelope", "Jayden", "Riley", "Dylan",
    "志明", "雅婷", "建宏", "淑芬", "家豪", "怡君", "承翰", "詩涵", "子軒", "欣怡",
    "俊傑", "雅筠", "冠宇", "佩玲", "宗翰", "思穎", "柏翰", "婉婷", "宥廷", "依婷"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "王", "李", "陳", "林", "黃", "張", "劉", "吳", "蔡", "楊"
]

OCCUPATIONS = [
    "Software Engineer", "Product Manager", "Designer", "Data Scientist", "Marketing Manager",
    "Teacher", "Doctor", "Nurse", "Lawyer", "Accountant", "Artist", "Writer", "Photographer",
    "Chef", "Entrepreneur", "Consultant", "Sales Manager", "HR Manager", "Financial Analyst",
    "UX Designer", "Full Stack Developer", "DevOps Engineer", "Project Manager", "Business Analyst",
    "Content Creator", "Social Media Manager", "Graphic Designer", "Student", "Researcher", "Architect"
]

LOCATIONS = [
    "台北", "新北", "台中", "台南", "高雄", "桃園", "新竹", "嘉義", "基隆", "宜蘭",
    "New York", "Los Angeles", "San Francisco", "Seattle", "Austin", "Boston", "Chicago",
    "London", "Paris", "Tokyo", "Seoul", "Singapore", "Hong Kong", "Shanghai", "Beijing"
]

HOBBIES = [
    "攝影", "旅遊", "閱讀", "烹飪", "運動", "音樂", "繪畫", "寫作", "電影", "登山",
    "游泳", "瑜伽", "跑步", "騎單車", "露營", "咖啡", "品酒", "園藝", "寵物", "手作",
    "Programming", "Gaming", "Dancing", "Singing", "Photography", "Hiking", "Surfing", "Skiing",
    "Meditation", "Fitness", "Basketball", "Tennis", "Golf", "Painting", "Crafting"
]

GENDERS = ["Male", "Female", "Non-binary"]

# 使用免費的頭像圖片服務
def generate_avatar_url(index: int, gender: str) -> str:
    """生成頭像 URL"""
    # 使用 UI Avatars 服務生成頭像
    seed = random.randint(1, 10000)
    return f"https://api.dicebear.com/7.x/avataaars/png?seed={seed}"

def generate_user(user_id: int) -> Dict:
    """生成單個用戶數據"""
    gender = random.choice(GENDERS)
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    # 隨機選擇 2-4 個興趣
    num_hobbies = random.randint(2, 4)
    hobbies = random.sample(HOBBIES, num_hobbies)

    user = {
        "id": user_id,
        "name": f"{first_name} {last_name}",
        "age": random.randint(20, 65),
        "occupation": random.choice(OCCUPATIONS),
        "location": random.choice(LOCATIONS),
        "hobby": hobbies,
        "gender": gender,
        "image": generate_avatar_url(user_id, gender)
    }

    return user

def generate_user_database(num_users: int = 100) -> List[Dict]:
    """生成用戶數據庫"""
    users = []
    for i in range(1, num_users + 1):
        users.append(generate_user(i))
    return users

def save_to_json(data: List[Dict], filename: str):
    """保存到 JSON 文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("正在生成 100 個用戶數據...")
    users = generate_user_database(100)

    output_file = "users_database.json"
    save_to_json(users, output_file)

    print(f"✅ 成功生成 {len(users)} 個用戶數據！")
    print(f"📁 數據已保存至: {output_file}")

    # 顯示一些統計信息
    print("\n統計信息:")
    locations = {}
    genders = {}
    occupations = {}

    for user in users:
        locations[user['location']] = locations.get(user['location'], 0) + 1
        genders[user['gender']] = genders.get(user['gender'], 0) + 1
        occupations[user['occupation']] = occupations.get(user['occupation'], 0) + 1

    print(f"\n地區分布: {dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])}")
    print(f"性別分布: {genders}")
    print(f"職業分布: {dict(sorted(occupations.items(), key=lambda x: x[1], reverse=True)[:5])}")

    # 顯示前 3 個用戶示例
    print("\n前 3 個用戶示例:")
    for user in users[:3]:
        print(f"\n{user['id']}. {user['name']}")
        print(f"   年齡: {user['age']}")
        print(f"   職業: {user['occupation']}")
        print(f"   地區: {user['location']}")
        print(f"   興趣: {', '.join(user['hobby'])}")
        print(f"   性別: {user['gender']}")

if __name__ == "__main__":
    main()
