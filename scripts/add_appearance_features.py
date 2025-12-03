#!/usr/bin/env python3
"""
为用户数据库添加外观特征
分析头像图片并添加发型、发色、风格等特征
"""

import json
import os
from pathlib import Path

def analyze_avatar_features():
    """
    根据头像文件名和类型分析特征
    avatar_001-070.jpg = 真人照片
    avatar_071-100.png = 动漫风格
    """

    # 读取用户数据库
    with open('users_database.json', 'r', encoding='utf-8') as f:
        users = json.load(f)

    print(f"📊 读取了 {len(users)} 个用户")

    # 为每个用户添加外观特征
    for user in users:
        avatar_num = user['id']

        # 基础特征：判断是真人还是动漫
        if avatar_num <= 70:
            style = "realistic"
        else:
            style = "anime"

        # 根据性别和ID分配发型发色等特征
        # 这里使用模式化分配，实际项目中可以用 AI 图像识别
        appearance = generate_appearance_features(user, avatar_num, style)

        # 添加到用户数据
        user['appearance'] = appearance

    # 保存更新后的数据库
    with open('users_database.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    print("✅ 外观特征已添加完成！")
    print("\n📝 示例用户:")
    for user in users[:3]:
        print(f"\n{user['name']} ({user['id']}):")
        print(f"  Style: {user['appearance']['style']}")
        print(f"  Hair: {user['appearance']['hair_length']}, {user['appearance']['hair_color']}")
        print(f"  Tags: {', '.join(user['appearance']['tags'])}")


def generate_appearance_features(user, avatar_num, style):
    """
    根据用户信息生成外观特征
    """
    gender = user['gender']
    age = user['age']

    # 发色选项
    hair_colors_realistic = ['black', 'brown', 'blonde', 'red', 'gray']
    hair_colors_anime = ['black', 'brown', 'blonde', 'pink', 'blue', 'purple', 'red', 'white', 'silver']

    # 发长
    if gender == 'Female':
        hair_lengths = ['short', 'medium', 'long', 'very long']
        # 女性更倾向长发
        hair_length = hair_lengths[avatar_num % len(hair_lengths)]
        if avatar_num % 3 == 0:
            hair_length = 'long'
    else:
        hair_lengths = ['short', 'medium', 'buzz cut']
        hair_length = hair_lengths[avatar_num % len(hair_lengths)]

    # 发色
    if style == 'realistic':
        hair_color = hair_colors_realistic[avatar_num % len(hair_colors_realistic)]
    else:
        hair_color = hair_colors_anime[avatar_num % len(hair_colors_anime)]

    # 标签（基于年龄、性别、风格）
    tags = [style]

    # 年龄相关标签
    if age < 25:
        tags.append('youthful')
    elif age > 35:
        tags.append('mature')

    # 性别相关标签
    if gender == 'Female':
        female_tags = ['elegant', 'cute', 'stylish', 'natural', 'sophisticated']
        tags.append(female_tags[avatar_num % len(female_tags)])
    else:
        male_tags = ['casual', 'professional', 'sporty', 'artistic', 'rugged']
        tags.append(male_tags[avatar_num % len(male_tags)])

    # 风格相关标签
    if style == 'anime':
        anime_tags = ['colorful', 'fantasy', 'vibrant', 'kawaii']
        tags.append(anime_tags[avatar_num % len(anime_tags)])
    else:
        realistic_tags = ['photogenic', 'authentic', 'candid']
        tags.append(realistic_tags[avatar_num % len(realistic_tags)])

    # 发型风格
    hairstyles_female = ['straight', 'wavy', 'curly', 'braided', 'ponytail', 'bun']
    hairstyles_male = ['straight', 'messy', 'slicked back', 'textured', 'spiky']

    if gender == 'Female':
        hairstyle = hairstyles_female[avatar_num % len(hairstyles_female)]
    else:
        hairstyle = hairstyles_male[avatar_num % len(hairstyles_male)]

    # 眼睛颜色（主要用于动漫）
    if style == 'anime':
        eye_colors = ['brown', 'blue', 'green', 'red', 'purple', 'amber', 'gray']
        eye_color = eye_colors[avatar_num % len(eye_colors)]
    else:
        eye_colors = ['brown', 'blue', 'green', 'hazel', 'gray']
        eye_color = eye_colors[avatar_num % len(eye_colors)]

    return {
        'style': style,
        'hair_length': hair_length,
        'hair_color': hair_color,
        'hairstyle': hairstyle,
        'eye_color': eye_color,
        'tags': tags
    }


if __name__ == '__main__':
    print("🎨 开始为用户添加外观特征...")
    analyze_avatar_features()
    print("\n✨ 完成！")
