import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry

reg = Registry('Testdata')
with reg.cursor() as cr:
    env = odoo.api.Environment(cr, 2, {'website_id': 1, 'rendering_bundle': True})
    try:
        res = env['ir.ui.view'].render_public_asset('website.snippets', {})
        print("Success! HTML length:", len(res))
        print("Contains 'Landing Blocks':", "Landing Blocks" in res)
        print("Contains 's_single_product_showcase':", "s_single_product_showcase" in res)
        print("Contains 'Product Showcase & Checkout':", "Product Showcase & Checkout" in res)
    except Exception as e:
        print("Error rendering snippets:", e)

