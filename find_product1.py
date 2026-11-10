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

# Search for product-1
idx = html.find('id="product-1"')
print("Snippet from product-1 (length 1000):")
print(html[idx:idx+1000])

# Search for product-1-checkout
idx2 = html.find('product-1-checkout')
while idx2 != -1:
    print(f"\nMatch at {idx2}:")
    print(html[max(0, idx2 - 50):min(len(html), idx2 + 150)])
    idx2 = html.find('product-1-checkout', idx2 + 1)

