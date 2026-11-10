import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

registry = Registry('Testdata')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    v1 = env.ref('theme_multiproduct_landing.landing_page')
    v2 = env.ref('theme_multiproduct_landing.single_product_block')
    print("env.ref v1:", v1._name, v1.id, getattr(v1, 'key', None))
    print("env.ref v2:", v2._name, v2.id, getattr(v2, 'key', None))

