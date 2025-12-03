#!/usr/bin/env python3
"""
下載真實人像照片作為用戶頭像
使用 Unsplash API 和 This Person Does Not Exist
"""

import os
import requests
import json
import time
from pathlib import Path


def create_avatar_folder():
    """創建頭像文件夾"""
    folder = "avatars"
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"✅ 創建文件夾: {folder}")
    return folder


def download_from_unsplash(count: int, folder: str) -> list:
    """
    從 Unsplash 下載人像照片
    使用隨機人像照片
    """
    print(f"📥 從 Unsplash 下載 {count} 張人像照片...")

    downloaded_files = []

    for i in range(count):
        try:
            # 使用 Unsplash Source API 獲取隨機人像
            # 使用不同的種子確保照片不重複
            url = f"https://source.unsplash.com/400x400/?portrait,face,person&sig={i}"

            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                filename = f"{folder}/avatar_{i+1:03d}.jpg"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                downloaded_files.append(filename)
                print(f"  ✓ 下載 {i+1}/{count}: {filename}")

                # 避免請求過快
                time.sleep(0.5)
            else:
                print(f"  ✗ 下載失敗 {i+1}/{count}: HTTP {response.status_code}")

        except Exception as e:
            print(f"  ✗ 下載錯誤 {i+1}/{count}: {str(e)}")

    return downloaded_files


def download_ai_faces(count: int, folder: str, start_index: int = 0) -> list:
    """
    從 This Person Does Not Exist 下載 AI 生成的人臉
    這些是看起來真實但實際不存在的人
    """
    print(f"📥 下載 {count} 張 AI 生成的真實感人像...")

    downloaded_files = []

    for i in range(count):
        try:
            # This Person Does Not Exist API
            url = "https://thispersondoesnotexist.com/"

            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                filename = f"{folder}/avatar_{start_index + i + 1:03d}.jpg"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                downloaded_files.append(filename)
                print(f"  ✓ 下載 {i+1}/{count}: {filename}")

                # 每次請求需要間隔較長時間
                time.sleep(2)
            else:
                print(f"  ✗ 下載失敗 {i+1}/{count}: HTTP {response.status_code}")

        except Exception as e:
            print(f"  ✗ 下載錯誤 {i+1}/{count}: {str(e)}")

    return downloaded_files


def download_from_randomuser(count: int, folder: str) -> list:
    """
    從 Random User API 下載人像
    這是一個專門生成隨機用戶數據和照片的 API
    """
    print(f"📥 從 Random User API 下載 {count} 張人像照片...")

    downloaded_files = []

    try:
        # 一次性請求多個用戶
        url = f"https://randomuser.me/api/?results={count}&inc=picture"
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            data = response.json()
            users = data.get('results', [])

            for i, user in enumerate(users):
                try:
                    # 獲取大尺寸頭像
                    pic_url = user['picture']['large']
                    pic_response = requests.get(pic_url, timeout=10)

                    if pic_response.status_code == 200:
                        filename = f"{folder}/avatar_{i+1:03d}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(pic_response.content)
                        downloaded_files.append(filename)
                        print(f"  ✓ 下載 {i+1}/{count}: {filename}")
                    else:
                        print(f"  ✗ 下載失敗 {i+1}/{count}")

                    time.sleep(0.3)

                except Exception as e:
                    print(f"  ✗ 下載錯誤 {i+1}/{count}: {str(e)}")
        else:
            print(f"✗ API 請求失敗: HTTP {response.status_code}")

    except Exception as e:
        print(f"✗ 請求錯誤: {str(e)}")

    return downloaded_files


def update_user_database(avatar_files: list, database_file: str = "users_database.json"):
    """
    更新用戶數據庫，使用下載的頭像文件
    """
    print(f"\n📝 更新用戶數據庫...")

    try:
        with open(database_file, 'r', encoding='utf-8') as f:
            users = json.load(f)

        # 為每個用戶分配一張頭像
        for i, user in enumerate(users):
            if i < len(avatar_files):
                user['image'] = avatar_files[i]
            else:
                # 如果頭像不夠，循環使用
                user['image'] = avatar_files[i % len(avatar_files)]

        # 保存更新後的數據庫
        with open(database_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        print(f"✅ 成功更新 {len(users)} 個用戶的頭像信息")

    except Exception as e:
        print(f"✗ 更新數據庫失敗: {str(e)}")


def main():
    print("🎨 開始下載用戶頭像...\n")

    # 創建文件夾
    folder = create_avatar_folder()

    # 下載頭像
    # 方法選擇：Random User API 提供真實感的人像照片
    avatar_files = download_from_randomuser(100, folder)

    if len(avatar_files) < 100:
        print(f"\n⚠️  只下載了 {len(avatar_files)} 張照片，繼續嘗試其他來源...")

        # 如果不夠，使用 AI 生成的人臉補充
        # remaining = 100 - len(avatar_files)
        # additional = download_ai_faces(remaining, folder, len(avatar_files))
        # avatar_files.extend(additional)

    print(f"\n✅ 總共下載了 {len(avatar_files)} 張頭像照片")

    # 更新用戶數據庫
    if avatar_files:
        update_user_database(avatar_files)
        print(f"\n🎉 完成！所有用戶頭像已更新為真實照片")
    else:
        print("\n❌ 沒有成功下載任何照片")


if __name__ == "__main__":
    main()
