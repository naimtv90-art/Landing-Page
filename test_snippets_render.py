import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry

reg = Registry('Testdata')
with reg.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    rendered = env['ir.ui.view'].render_public_asset('website.snippets')
    print("Rendered length:", len(rendered))
    print("Has landing group:", "snippet-group=\"landing\"" in rendered or "group=\"landing\"" in rendered)
    print("Has s_single_product_showcase:", "s_single_product_showcase" in rendered)
    print("Has Product Showcase & Checkout:", "Product Showcase & Checkout" in rendered)

