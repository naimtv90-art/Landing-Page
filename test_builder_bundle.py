import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry
from odoo.http import root
import requests
import re

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

r = s.get('http://localhost:8069/?enable_editor=1')
print('Editor page status:', r.status_code)

all_assets = re.findall(r'/web/assets/[^"\' ]+', r.text)
print('Total web assets found in HTML:', len(all_assets))
for a in all_assets[:15]:
    print('  Asset:', a)

