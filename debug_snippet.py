import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request

session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)

req = urllib.request.Request('http://localhost:8069/')
req.add_header('Cookie', f'session_id={session.sid}')
html = urllib.request.urlopen(req).read().decode('utf-8')

print("Length of html:", len(html))
print("Has 'product-1-checkout'?", 'product-1-checkout' in html)
print("Has 'checkoutModalLabel'?", 'checkoutModalLabel' in html)
print("Has 'modal fade'?", 'modal fade' in html)

idx = html.find('product-1-checkout')
if idx != -1:
    print("\n--- SNIPPET AROUND product-1-checkout ---")
    print(html[max(0, idx - 100):min(len(html), idx + 250)])
else:
    print("Not found!")

