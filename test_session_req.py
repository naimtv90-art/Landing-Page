import sys
sys.path.append(r"C:\Program Files\Odoo 19.0.20260902\server")
import odoo
from odoo.http import root

# Let's inspect root.session_store
session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)
print('Created valid session:', session.sid)

# Now let's make an HTTP request to localhost:8069/ with Cookie: session_id=<sid>
import urllib.request
req = urllib.request.Request('http://localhost:8069/')
req.add_header('Cookie', f'session_id={session.sid}')

try:
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    print('Status:', res.status)
    print('HTML length:', len(html))
    print('Has Product 01:', 'Product 01' in html)
    print('Has Heavy Twill Utility Overshirt:', 'Heavy Twill Utility Overshirt' in html)
    print('Has Instant Checkout:', 'Instant Checkout' in html)
    print('Preview:', html[:500])
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.headers.get('Location'))
    print(e.read().decode('utf-8')[:500])

