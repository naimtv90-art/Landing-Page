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
    view = env['ir.ui.view']._get('theme_multiproduct_landing.landing_page')
    print("Resolved view for 'theme_multiproduct_landing.landing_page':", view.id, view.key, view.website_id)
    view_sub = env['ir.ui.view']._get('theme_multiproduct_landing.single_product_block')
    print("Resolved view for 'theme_multiproduct_landing.single_product_block':", view_sub.id, view_sub.key, view_sub.website_id)

