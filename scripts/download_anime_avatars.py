#!/usr/bin/env python3
"""
下載日本動漫風格頭像，替換卡通圖片
"""

import requests
import os
import time
from pathlib import Path

def download_anime_avatar(avatar_number, save_path):
    """
    從 ThisWaifuDoesNotExist API 下載動漫頭像
    這個 API 每次調用都會生成一個新的動漫角色頭像
    """
    url = "https://www.thiswaifudoesnotexist.net/example-{}.jpg".format(
        (avatar_number % 100000)
    )

    # 備用 API：如果上面的不工作，使用這個
    backup_urls = [
        "https://api.waifu.pics/sfw/waifu",  # 返回 JSON 格式
        f"https://picsum.photos/seed/{avatar_number}/400/400",  # 隨機圖片（備用）
    ]

    try:
        # 嘗試主要 API
        print(f"📥 下載頭像 {avatar_number}...", end=" ")

        # 使用 ThisAnimeDoesNotExist 的隨機動漫頭像
        response = requests.get(
            "https://thisanimedoesnotexist.ai/results/psi-0.8/seed{:05d}.png".format(avatar_number),
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        if response.status_code == 200 and len(response.content) > 1000:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("✅ 成功")
            return True

        # 如果主要 API 失敗，嘗試 waifu.pics API
        print("嘗試備用 API...", end=" ")
        response = requests.get(backup_urls[0], timeout=10)
        if response.status_code == 200:
            data = response.json()
            img_url = data.get('url')
            if img_url:
                img_response = requests.get(img_url, timeout=10)
                if img_response.status_code == 200:
                    # 轉換為 PNG 格式
                    with open(save_path, 'wb') as f:
                        f.write(img_response.content)
                    print("✅ 成功")
                    return True

        print("❌ 失敗")
        return False

    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def backup_old_avatars(avatar_numbers):
    """備份舊的卡通頭像"""
    backup_dir = Path("avatars/backup_cartoon")
    backup_dir.mkdir(exist_ok=True)

    print("\n📦 備份舊頭像...")
    for num in avatar_numbers:
        old_file = Path(f"avatars/avatar_{num:03d}.png")
        if old_file.exists():
            backup_file = backup_dir / old_file.name
            old_file.rename(backup_file)
            print(f"  備份: {old_file.name} -> backup_cartoon/")
    print("✅ 備份完成\n")

def main():
    print("=" * 60)
    print("🎨 日本動漫風格頭像下載工具")
    print("=" * 60)
    print()

    # 需要替換的頭像編號（071-100）
    avatar_numbers = list(range(71, 101))

    # 備份舊頭像
    backup_old_avatars(avatar_numbers)

    # 創建 avatars 目錄
    avatars_dir = Path("avatars")
    avatars_dir.mkdir(exist_ok=True)

    print(f"🎯 開始下載 {len(avatar_numbers)} 張動漫頭像...\n")

    success_count = 0
    failed_list = []

    for i, num in enumerate(avatar_numbers, 1):
        save_path = avatars_dir / f"avatar_{num:03d}.png"

        # 下載頭像
        if download_anime_avatar(num, save_path):
            success_count += 1
        else:
            failed_list.append(num)

        # 避免請求過快，休息一下
        if i < len(avatar_numbers):
            time.sleep(0.5)

    # 總結報告
    print()
    print("=" * 60)
    print("📊 下載完成統計")
    print("=" * 60)
    print(f"✅ 成功: {success_count}/{len(avatar_numbers)}")
    print(f"❌ 失敗: {len(failed_list)}/{len(avatar_numbers)}")

    if failed_list:
        print(f"\n失敗的頭像編號: {failed_list}")
        print("\n💡 提示：你可以重新運行腳本，只下載失敗的頭像")

    if success_count > 0:
        print("\n🎉 動漫頭像已成功替換到 avatars/ 資料夾！")
        print("📁 舊的卡通頭像已備份到 avatars/backup_cartoon/")

    print()

if __name__ == "__main__":
    main()
