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

checks = [
    ('Modal 1 exists with id product-1-checkout', 'id="product-1-checkout"' in html and 'landing-checkout-modal' in html),
    ('Modal 2 exists with id product-2-checkout', 'id="product-2-checkout"' in html and 'landing-checkout-modal' in html),
    ('Modal 3 exists with id product-3-checkout', 'id="product-3-checkout"' in html and 'landing-checkout-modal' in html),
    ('Header Order Now button has modal target', 'data-bs-target="#product-1-checkout"' in html),
    ('Product 01 Order button has modal target', 'data-bs-target="#product-1-checkout"' in html and 'Order Product 01' in html),
    ('Product 02 Order button has modal target', 'data-bs-target="#product-2-checkout"' in html and 'Order Product 02' in html),
    ('Product 03 Order button has modal target', 'data-bs-target="#product-3-checkout"' in html and 'Order Product 03' in html),
    ('Success Receipt modal exists', 'id="landingOrderSuccessModal"' in html),
]

all_passed = True
print("=== CHECKOUT POPUP MARKUP VERIFICATION ===")
for label, passed in checks:
    status = "PASS [OK]" if passed else "FAIL [X]"
    print(f"  {label:<50} : {status}")
    if not passed:
        all_passed = False

print("\nALL POPUP MODAL CHECKS PASSED!" if all_passed else "\nSOME CHECKS FAILED!")
