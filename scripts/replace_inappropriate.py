#!/usr/bin/env python3
"""替換不合適的頭像"""

import requests
import time
from pathlib import Path

def download_safe_anime_avatar(avatar_number, save_path, max_retries=5):
    """下載安全的動漫頭像（重試直到成功）"""
    for attempt in range(max_retries):
        try:
            # 使用 waifu.pics SFW API
            response = requests.get("https://api.waifu.pics/sfw/waifu", timeout=15)
            if response.status_code == 200:
                data = response.json()
                img_url = data.get('url')
                if img_url:
                    img_response = requests.get(img_url, timeout=15)
                    if img_response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            f.write(img_response.content)
                        return True
            time.sleep(1)
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"❌ 錯誤: {e}")
            time.sleep(1)
    return False

def main():
    # 需要替換的頭像（可能不太適合的）
    replace_numbers = [71, 75, 77, 82, 85, 88, 91, 94, 97]

    print("🔄 替換不合適的頭像為更適合的動漫角色頭像...\n")

    success_count = 0
    for num in replace_numbers:
        save_path = Path(f"avatars/avatar_{num:03d}.png")
        print(f"📥 重新下載頭像 {num}...", end=" ")

        if download_safe_anime_avatar(num, save_path):
            print("✅ 成功")
            success_count += 1
        else:
            print("❌ 失敗")

        time.sleep(1.5)

    print(f"\n✅ 成功替換: {success_count}/{len(replace_numbers)}")

if __name__ == "__main__":
    main()
