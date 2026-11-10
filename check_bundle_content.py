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

scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
print("Found scripts:", scripts)

for s in scripts:
    url = f'http://localhost:8069{s}'
    r = urllib.request.Request(url)
    r.add_header('Cookie', f'session_id={session.sid}')
    try:
        content = urllib.request.urlopen(r).read().decode('utf-8', errors='ignore')
        print(f"\nScript: {s} (Length: {len(content)})")
        print("  Has 'initQuantityControls'?", 'initQuantityControls' in content)
        print("  Has 'landing-qty-btn'?", 'landing-qty-btn' in content)
        print("  Has 'submit_order'?", 'submit_order' in content)
        print("  Has 'theme_multiproduct_landing'?", 'theme_multiproduct_landing' in content)
    except Exception as e:
        print(f"Error fetching {s}: {e}")

