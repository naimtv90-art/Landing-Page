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

sections = soup.find_all('section')
print(f"Total sections: {len(sections)}")
for s in sections:
    has_model = s.has_attr('data-oe-model')
    print(f"Section id='{s.get('id')}' class='{s.get('class')}' data-oe-model={has_model}")
    # check children with data-oe-model
    children_with_model = s.find_all(attrs={'data-oe-model': True})
    print(f"   Children with data-oe-model: {len(children_with_model)}")

print("\n--- Check why user said text cannot be edited ---")
# Check product 1 card:
p1 = soup.find(id='product-1')
if p1:
    h2 = p1.find_all(['h2', 'h3', 'h4', 'p', 'span'])
    print(f"Text elements inside product-1: {len(h2)}")
    with_model = [el for el in h2 if el.has_attr('data-oe-model')]
    print(f"Text elements with data-oe-model: {len(with_model)}")
    for el in with_model[:5]:
        print("  ", el.name, el.get('class'), el.get('data-oe-model'), el.text[:30].strip())
    without_model = [el for el in h2 if not el.has_attr('data-oe-model')]
    print(f"Text elements WITHOUT data-oe-model: {len(without_model)}")
    for el in without_model[:5]:
        print("   NO MODEL:", el.name, el.get('class'), el.text[:30].strip())

