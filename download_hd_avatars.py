#!/usr/bin/env python3
"""
Download HD avatars using DiceBear API and Pravatar
"""

import os
import requests
import time

def create_avatar_folder():
    """Create avatar folder"""
    folder = "avatars"
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"✅ Created folder: {folder}")
    return folder

def download_from_pravatar(count: int, folder: str) -> list:
    """
    Download from Pravatar.cc
    Size: 800x800 (high quality)
    """
    print(f"📥 Downloading {count} HD avatars from Pravatar (800x800)...")

    downloaded_files = []

    for i in range(1, count + 1):
        try:
            # Pravatar provides real photos at specified size
            url = f"https://i.pravatar.cc/800?img={i}"

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                filename = f"{folder}/avatar_{i:03d}.jpg"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                downloaded_files.append(filename)
                print(f"  ✓ Downloaded {i}/{count}: {filename}")

                # Small delay to avoid rate limiting
                time.sleep(0.2)
            else:
                print(f"  ✗ Download failed {i}/{count}: HTTP {response.status_code}")

        except Exception as e:
            print(f"  ✗ Download error {i}/{count}: {str(e)}")

    return downloaded_files

def download_from_dicebear(count: int, folder: str, start_index: int = 0) -> list:
    """
    Download from DiceBear API (generates avatars)
    Size: 800x800
    """
    print(f"📥 Downloading {count} HD generated avatars from DiceBear (800x800)...")

    downloaded_files = []

    styles = ['avataaars', 'big-smile', 'bottts', 'personas']

    for i in range(count):
        try:
            style = styles[i % len(styles)]
            seed = f"user{i+start_index}"
            # DiceBear v7 API
            url = f"https://api.dicebear.com/7.x/{style}/png?seed={seed}&size=800"

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                filename = f"{folder}/avatar_{i+start_index+1:03d}.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                downloaded_files.append(filename)
                print(f"  ✓ Downloaded {i+1}/{count}: {filename}")

                time.sleep(0.3)
            else:
                print(f"  ✗ Download failed {i+1}/{count}: HTTP {response.status_code}")

        except Exception as e:
            print(f"  ✗ Download error {i+1}/{count}: {str(e)}")

    return downloaded_files

def main():
    print("🎨 Downloading HD avatars...\n")

    # Create folder
    folder = create_avatar_folder()

    # Try Pravatar first (real photos, higher quality)
    avatar_files = download_from_pravatar(70, folder)

    # If we need more, use DiceBear for the rest
    if len(avatar_files) < 100:
        remaining = 100 - len(avatar_files)
        print(f"\nDownloading {remaining} more from DiceBear...")
        additional = download_from_dicebear(remaining, folder, len(avatar_files))
        avatar_files.extend(additional)

    print(f"\n✅ Total downloaded: {len(avatar_files)} HD avatars")
    print(f"\n🎉 Complete! All avatars are now high resolution (800x800)")

if __name__ == "__main__":
    main()
