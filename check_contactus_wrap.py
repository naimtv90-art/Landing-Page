import sys
sys.path.append(r"C:\Program Files\Odoo 19.0.20260902\server")
import odoo
from odoo.http import root
import urllib.request
from bs4 import BeautifulSoup

session = root.session_store.new()
session.db = 'Testdata'
session.uid = 2
session.login = 'admin'
root.session_store.save(session)

url = 'http://localhost:8069/contactus?enable_editor=1'
req = urllib.request.Request(url)
req.add_header('Cookie', f'session_id={session.sid}')
res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

wrap = soup.find(id="wrap")
if wrap:
    print("Contactus #wrap attributes:")
    for k, v in wrap.attrs.items():
        print(f"  {k}: {v}")
    print("\nContactus #wrap children:")
    for child in wrap.find_all(recursive=False):
        print(f"  <{child.name} class='{child.get('class')}' id='{child.get('id')}' data-oe-model='{child.get('data-oe-model')}'>")
else:
    print("No wrap found on contactus!")

