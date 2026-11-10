import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request

session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)

req = urllib.request.Request('http://localhost:8069/web/assets/1/364cae2/web.assets_frontend_lazy.min.js')
req.add_header('Cookie', f'session_id={session.sid}')
content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

idx = content.find('initLandingPage')
print("Snippet around initLandingPage:")
print(content[max(0, idx - 200):min(len(content), idx + 500)])
