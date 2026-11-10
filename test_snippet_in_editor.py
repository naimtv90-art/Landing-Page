import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request
import re

session = root.session_store.new()
session.db = 'Testdata'
session.uid = 2
session.login = 'admin'
root.session_store.save(session)

req = urllib.request.Request('http://localhost:8069/?enable_editor=1')
req.add_header('Cookie', f'session_id={session.sid}')
html = urllib.request.urlopen(req).read().decode('utf-8')

# Search for s_single_product_showcase in html
print("Has s_single_product_showcase:", "s_single_product_showcase" in html)
print("Has landing-product-picker-select:", "landing-product-picker-select" in html)

