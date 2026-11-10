import sys
sys.path.append(r"C:\Program Files\Odoo 19.0.20260902\server")
import odoo
from odoo.http import root
import urllib.request
import re
from bs4 import BeautifulSoup

session = root.session_store.new()
session.db = 'Testdata'
session.uid = 2 # Administrator
session.login = 'admin'
root.session_store.save(session)

url = 'http://localhost:8069/?enable_editor=1'
req = urllib.request.Request(url)
req.add_header('Cookie', f'session_id={session.sid}')

res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

print("=== Elements with data-oe-model ===")
tags = soup.find_all(attrs={"data-oe-model": True})
for t in tags[:25]:
    parent_info = f"{t.parent.name}#{t.parent.get('id', '')}" if t.parent else "None"
    print(f"<{t.name} class='{t.get('class', [])}' id='{t.get('id', '')}' model='{t.get('data-oe-model')}' field='{t.get('data-oe-field')}' parent={parent_info}>")

print("\nTotal elements with data-oe-model:", len(tags))

wrap = soup.find(id="wrap")
if wrap:
    print("\nWrap tag attributes:", wrap.attrs)
    print("Wrap parent:", wrap.parent.name, wrap.parent.attrs)
    # Check dropzones inside wrap
    dropzones = wrap.find_all(class_="oe_structure")
    print(f"Total oe_structure inside wrap: {len(dropzones)}")
    for dz in dropzones:
        print(f"  dz id='{dz.get('id')}' class='{dz.get('class')}' data-oe-model='{dz.get('data-oe-model')}'")
else:
    print("No #wrap found!")
