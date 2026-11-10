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
    ('Section 01: Sticky Header', 'landing-header sticky-top' in html),
    ('Section 01: Cart live quantity badge', 'landing-cart-badge' in html),
    ('Section 01: Announcement Bar', 'landing-announcement-bar' in html),
    ('Section 02: Hero Section', 'landing-hero-section' in html),
    ('Section 02: Quick Jump Strip Removed', 'landing-product-strip-wrapper' not in html),
    ('Section 03: Book 01 Showcase (Atomic Habits)', ('বই ০১' in html or 'Product 01' in html) and 'Atomic Habits' in html),
    ('Section 04: Book 01 Checkout', 'id="product-1-checkout"' in html and 'checkout-form-1' in html),
    ('Section 05: Book 02 Showcase (Psychology of Money)', ('বই ০২' in html or 'Product 02' in html) and 'Psychology of Money' in html),
    ('Section 05: Book 02 Checkout', 'id="product-2-checkout"' in html and 'checkout-form-2' in html),
    ('Section 06: Book 03 Showcase (Deep Work)', ('বই ০৩' in html or 'Product 03' in html) and 'Deep Work' in html),
    ('Section 06: Book 03 Checkout', 'id="product-3-checkout"' in html and 'checkout-form-3' in html),
    ('No Apparel Size Variants (Clean Books)', 'Small (S)' not in html and 'Medium (M)' not in html and 'Large (L)' not in html),
    ('Card Deck Auto Slide-Up Style', 'landing-product-card' in html and 'landing-products-wrapper' in html),
    ('Section 07: Trust & Why Choose Us', 'id="trust-section"' in html),
    ('Section 08: Customer Reviews', 'id="reviews-section"' in html),
    ('Section 09: FAQ Accordion', 'id="faq-section"' in html and 'landingFaqAccordion' in html),
    ('Section 10: Footer', 'landing-footer' in html),
    ('Order Confirmation Receipt Modal', 'id="landingOrderSuccessModal"' in html),
]

all_passed = True
for label, passed in checks:
    status = "PASS [OK]" if passed else "FAIL [X]"
    print(f"{label:45} : {status}")
    if not passed:
        all_passed = False

print("\nOVERALL STATUS:", "ALL 18 CHECKS PASSED!" if all_passed else "SOME CHECKS FAILED")

