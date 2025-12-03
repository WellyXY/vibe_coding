#!/usr/bin/env python3
"""
Convert all SVG files in assets folder to JPG format
"""
import os
from pathlib import Path

try:
    from PIL import Image
    from cairosvg import svg2png
except ImportError:
    print("Please install required packages:")
    print("pip install Pillow cairosvg")
    exit(1)

def convert_svg_to_jpg(svg_path, output_dir, size=(100, 100), bg_color=(255, 255, 255)):
    """Convert SVG to JPG"""
    try:
        # Convert SVG to PNG first (cairosvg doesn't do JPG directly)
        png_data = svg2png(url=str(svg_path), output_width=size[0], output_height=size[1])
        
        # Load PNG data with PIL
        from io import BytesIO
        img = Image.open(BytesIO(png_data))
        
        # Create white background for alpha channel
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, bg_color)
            background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            img = background
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as JPG
        jpg_path = output_dir / svg_path.stem
        jpg_path = jpg_path.with_suffix('.jpg')
        img.save(jpg_path, 'JPEG', quality=95)
        
        print(f"✓ Converted: {svg_path.name} -> {jpg_path.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to convert {svg_path.name}: {e}")
        return False

def main():
    assets_dir = Path(__file__).parent / 'assets'
    
    if not assets_dir.exists():
        print(f"Error: {assets_dir} not found")
        return
    
    # Find all SVG files
    svg_files = list(assets_dir.glob('*.svg'))
    
    if not svg_files:
        print("No SVG files found in assets/")
        return
    
    print(f"Found {len(svg_files)} SVG files")
    print("Converting to JPG...")
    print()
    
    success_count = 0
    for svg_file in svg_files:
        if convert_svg_to_jpg(svg_file, assets_dir):
            success_count += 1
    
    print()
    print(f"Conversion complete: {success_count}/{len(svg_files)} successful")
    
    # Ask if user wants to delete original SVG files
    response = input("\nDelete original SVG files? (y/n): ")
    if response.lower() == 'y':
        for svg_file in svg_files:
            svg_file.unlink()
            print(f"Deleted: {svg_file.name}")
        print(f"Deleted {len(svg_files)} SVG files")

if __name__ == '__main__':
    main()
