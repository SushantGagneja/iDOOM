"""
iDOOM Graph Integrity & Health Verification Script
Validates all navigation graph links, menu links, and image assets.
"""

import re
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
GAME_DIR = BASE_DIR / "game"
MENU_DIR = BASE_DIR / "menu"
ASSETS_DIR = BASE_DIR / "assets"
STATIC_DIR = BASE_DIR / "static"
MAP_DATA = BASE_DIR / "map_data.json"

def verify():
    print("=" * 60)
    print("iDOOM Graph Integrity & Link Verification")
    print("=" * 60)

    errors = []

    # 1. Verify map_data.json
    if not MAP_DATA.exists():
        print("[-] Missing map_data.json")
        return False
        
    with open(MAP_DATA, "r") as f:
        data = json.load(f)
        
    positions = data.get("positions", [])
    angles = data.get("angles", [])
    print(f"[+] Loaded map_data.json: {len(positions)} positions, {len(angles)} angles.")

    # 2. Verify all game navigation markdown files exist
    total_states = len(positions) * len(angles)
    missing_game_files = 0
    missing_assets = 0

    for x, y in positions:
        for ang in angles:
            md_name = f"{x}_{y}_{ang}.md"
            webp_name = f"doom_{x}_{y}_{ang}.webp"
            
            if not (GAME_DIR / md_name).exists():
                missing_game_files += 1
            if not (ASSETS_DIR / webp_name).exists():
                missing_assets += 1

    if missing_game_files > 0:
        errors.append(f"Missing {missing_game_files}/{total_states} game markdown files")
    else:
        print(f"[+] All {total_states} game markdown files present on disk.")

    if missing_assets > 0:
        errors.append(f"Missing {missing_assets}/{total_states} asset webp files")
    else:
        print(f"[+] All {total_states} WebP screenshot assets present on disk.")

    # 3. Check for broken internal links in game/ markdown files
    print("[*] Validating internal links in all game/ files...")
    broken_links = 0
    link_pattern = re.compile(r'href="([^"]+)"')
    img_pattern = re.compile(r'src="([^"]+)"')

    game_files = list(GAME_DIR.glob("*.md"))
    for file in game_files:
        content = file.read_text(encoding="utf-8")
        
        # Check href links
        for link in link_pattern.findall(content):
            if link.startswith("http://") or link.startswith("https://"):
                continue
            target_path = (file.parent / link).resolve()
            if not target_path.exists():
                broken_links += 1
                if broken_links <= 5:
                    errors.append(f"Broken link in {file.name} -> {link}")

        # Check img src
        for img in img_pattern.findall(content):
            if img.startswith("http://") or img.startswith("https://"):
                continue
            target_img = (file.parent / img).resolve()
            if not target_img.exists():
                broken_links += 1
                if broken_links <= 5:
                    errors.append(f"Broken image in {file.name} -> {img}")

    if broken_links == 0:
        print(f"[+] All hyperlinks and image references in {len(game_files)} game files are valid.")
    else:
        errors.append(f"Total broken links found: {broken_links}")

    # 4. Check menu files
    print("[*] Validating menu files...")
    menu_files = list(MENU_DIR.glob("*.md"))
    menu_broken = 0
    for file in menu_files:
        content = file.read_text(encoding="utf-8")
        for link in link_pattern.findall(content):
            if link.startswith("http://") or link.startswith("https://"):
                continue
            target_path = (file.parent / link).resolve()
            if not target_path.exists():
                menu_broken += 1
                errors.append(f"Broken menu link in {file.name} -> {link}")

        for img in img_pattern.findall(content):
            if img.startswith("http://") or img.startswith("https://"):
                continue
            target_img = (file.parent / img).resolve()
            if not target_img.exists():
                menu_broken += 1
                errors.append(f"Broken menu image in {file.name} -> {img}")

    if menu_broken == 0:
        print(f"[+] All hyperlinks and image references in {len(menu_files)} menu files are valid.")

    print("=" * 60)
    if not errors:
        print("[SUCCESS] All graph checks passed with 100% integrity!")
        print("=" * 60)
        return True
    else:
        print(f"[FAILED] Found {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
