import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry
from odoo.http import root
import requests

reg = Registry('Testdata')
with reg.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    user = env['res.users'].browse(2)
    session = root.session_store.new()
    session.db = 'Testdata'
    session.uid = 2
    session.login = user.login
    session.session_token = user._compute_session_token(session.sid)
    root.session_store.save(session)
    sid = session.sid

s = requests.Session()
s.cookies.set('session_id', sid)

r = s.post('http://localhost:8069/web/dataset/call_kw/ir.ui.view/render_public_asset', json={
    'jsonrpc': '2.0',
    'params': {
        'model': 'ir.ui.view',
        'method': 'render_public_asset',
        'args': ['website.snippets', {}],
        'kwargs': {'context': {'rendering_bundle': True, 'website_id': 1}}
    }
})

data = r.json()
if 'error' in data:
    print('Error:', data['error']['data']['message'])
else:
    html = data.get('result', '')
    print('Success! Snippets HTML length:', len(html))
    print('Has Landing Blocks:', 'Landing Blocks' in html)
    print('Has s_single_product_showcase:', 's_single_product_showcase' in html)
    print('Has Product Showcase:', 'Product Showcase' in html)
    print('Has 3-Product Quick Strip:', '3-Product Quick Strip' in html)
    print('Has Trust & Why Choose Us:', 'Trust' in html)
    print('Has Reader Reviews:', 'Reader Reviews' in html)
    print('Has Landing FAQ:', 'Landing FAQ' in html)
