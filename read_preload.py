with open(r'C:\Program Files\Odoo 19.0.20260902\server\odoo\addons\base\models\ir_ui_view.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def _preload_views' in line:
        print(f"--- Line {i+1} ---")
        print("".join(lines[i:i+40]))

