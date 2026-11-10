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
print(f"Scripts found in HTML ({len(scripts)}):")
for s in scripts:
    print(" ", s)

print("\nIs landing.js directly linked or in asset bundle?")
for s in scripts:
    if 'landing' in s:
        print("  Found landing script:", s)

