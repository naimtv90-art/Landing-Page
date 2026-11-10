import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request
import urllib.error

session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)

req = urllib.request.Request('http://localhost:8069/')
req.add_header('Cookie', f'session_id={session.sid}')

try:
    resp = urllib.request.urlopen(req)
    print("Status:", resp.status)
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    body = e.read().decode('utf-8', errors='ignore')
    print("Body snippet:")
    print(body[:1000])

