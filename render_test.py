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
    website = env['website'].browse(1)
    try:
        html = env['ir.qweb'].with_context(website_id=1)._render('theme_multiproduct_landing.landing_page', {
            'website': website,
            'company': website.company_id,
            'products': website.get_landing_products(),
            'currency': website.currency_id,
        })
        print("Render WITH website_id=1 SUCCEEDED! Length:", len(html))
    except Exception as e:
        import traceback
        traceback.print_exc()
