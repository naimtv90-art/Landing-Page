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

url = 'http://localhost:8069/?enable_editor=1'
req = urllib.request.Request(url)
req.add_header('Cookie', f'session_id={session.sid}')
res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

for el in soup.find_all(attrs={'data-oe-xpath': True}):
    xp = el.get('data-oe-xpath')
    if 'div[1]' in xp or 'wrap' in str(el.attrs):
        print(f"Tag: <{el.name}> id='{el.get('id')}' class='{el.get('class')}' xpath='{xp}'")

