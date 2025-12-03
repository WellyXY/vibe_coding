#!/usr/bin/env python3
"""重新下載失敗的頭像"""

import requests
import time
from pathlib import Path

def download_from_waifu_api(avatar_number, save_path):
    """使用 waifu.pics API 下載動漫頭像"""
    try:
        print(f"📥 下載頭像 {avatar_number}...", end=" ")

        # 使用 waifu.pics API
        response = requests.get("https://api.waifu.pics/sfw/waifu", timeout=15)
        if response.status_code == 200:
            data = response.json()
            img_url = data.get('url')
            if img_url:
                img_response = requests.get(img_url, timeout=15)
                if img_response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(img_response.content)
                    print("✅ 成功")
                    return True

        print("❌ 失敗")
        return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def main():
    failed_numbers = [80, 93, 100]

    print("🔄 重新下載失敗的頭像...\n")

    success_count = 0
    for num in failed_numbers:
        save_path = Path(f"avatars/avatar_{num:03d}.png")
        if download_from_waifu_api(num, save_path):
            success_count += 1
        time.sleep(1)

    print(f"\n✅ 成功下載: {success_count}/{len(failed_numbers)}")

if __name__ == "__main__":
    main()
