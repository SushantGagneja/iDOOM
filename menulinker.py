"""
DOOM Menu Linker (Tactile Keyboard Buttons)
Generates menu markdown with arcade <kbd> button styling.
"""

from pathlib import Path

MENU_DIR = Path(__file__).parent / "menu"
MENU_DIR.mkdir(exist_ok=True)

def make_btn(target_md: str, label: str) -> str:
    return f'<a href="{target_md}"><kbd>&nbsp;{label}&nbsp;</kbd></a>'

def generate_menus():
    print("Generating enhanced menu markdown...")

    # 1. Episode Selection (1, 2, 3)
    episodes = [1, 2, 3]
    for i in episodes:
        lines = []
        lines.append(f'<p align="center"><img src="../static/{i}.png" width="640"></p>\n')
        
        up_link = f"episode_{max(1, i-1)}.md"
        down_link = f"episode_{min(3, i+1)}.md"
        
        if i == 1:
            enter_target = "difficulty_1.md"
            enter_label = "SELECT ➔"
        else:
            enter_target = f"episode_{i}_error.md"
            enter_label = "🔒 LOCKED"
            
        lines.append('<p align="center">')
        lines.append(f'{make_btn(up_link, "⬆️")} &nbsp;&nbsp; {make_btn(enter_target, enter_label)} &nbsp;&nbsp; {make_btn(down_link, "⬇️")}')
        lines.append('</p>\n')
        lines.append('<p align="center"><sub><a href="../README.md">🏠 Main Menu</a></sub></p>')
        
        with open(MENU_DIR / f"episode_{i}.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # 2. Error Pages for Ep 2 & 3
    for i in [2, 3]:
        lines = []
        lines.append(f'<p align="center"><img src="../static/{i}-error.png" width="640"></p>\n')
        lines.append('<p align="center">')
        lines.append(f'{make_btn(f"episode_{i}.md", "⬅️ BACK")} &nbsp;&nbsp; {make_btn("../README.md", "🏠 MAIN MENU")}')
        lines.append('</p>')
        
        with open(MENU_DIR / f"episode_{i}_error.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # 3. Difficulty Selection (1-5)
    spawn_node = "../game/1024_-3584_90.md"
    for i in range(1, 6):
        lines = []
        lines.append(f'<p align="center"><img src="../static/1-{i}.png" width="640"></p>\n')
        
        up_link = f"difficulty_{max(1, i-1)}.md"
        down_link = f"difficulty_{min(5, i+1)}.md"
        
        lines.append('<p align="center">')
        lines.append(f'{make_btn(up_link, "⬆️")} &nbsp;&nbsp; {make_btn(spawn_node, "💥 START MISSION")} &nbsp;&nbsp; {make_btn(down_link, "⬇️")}')
        lines.append('</p>\n')
        lines.append('<p align="center"><sub><a href="episode_1.md">⬅️ Episode Select</a> &nbsp;|&nbsp; <a href="../README.md">🏠 Main Menu</a></sub></p>')
        
        with open(MENU_DIR / f"difficulty_{i}.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
    print("Done. Menu structure updated with tactile buttons.")

if __name__ == "__main__":
    generate_menus()
