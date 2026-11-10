import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request
import re

session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)

req = urllib.request.Request('http://localhost:8069/')
req.add_header('Cookie', f'session_id={session.sid}')
html = urllib.request.urlopen(req).read().decode('utf-8')

print("Page Title / Branding:")
print("  Has 'Atomic Habits'?", 'Atomic Habits' in html)
print("  Has 'The Psychology of Money'?", 'The Psychology of Money' in html)
print("  Has 'Deep Work'?", 'Deep Work' in html)
print("  Has 'BOOXTREE'?", 'BOOXTREE' in html)

print("\nVariant Buttons with Prices:")
matches = re.findall(r'landing-variant-btn.*?data-variant-id="(\d+)".*?data-price="([^"]+)".*?data-name="([^"]+)"', html)
for m in matches:
    print(f"  Variant ID {m[0]}: {m[2]} => Price: ৳{m[1]}")

