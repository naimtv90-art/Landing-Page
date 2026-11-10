import sys
sys.path.append(r"C:\Program Files\Odoo 19.0.20260902\server")
import odoo
from odoo.modules.registry import Registry
from odoo import api

odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
registry = Registry('Testdata')

with registry.cursor() as cr:
    env = api.Environment(cr, odoo.SUPERUSER_ID, {})
    website = env['website'].browse(1)
    
    values = {
        'website': website,
        'company': website.company_id,
        'products': website.get_landing_products(),
        'delivery_methods': env['delivery.carrier'].search([('is_published', '=', True)]),
        'payment_providers': env['payment.provider'].search([('is_published', '=', True)]),
        'cart_qty': 0,
        'currency': website.currency_id,
        'lang': 'en_US',
        'editable': False,
        'translatable': False,
        'edit_translations': False,
    }
    
    try:
        rendered = env['ir.ui.view'].with_context(website_id=1, lang='en_US')._render_template('theme_multiproduct_landing.landing_page', values)
        print("Render SUCCESS! Length:", len(rendered))
        print("Has Heavy Twill:", 'Heavy Twill Utility Overshirt' in rendered)
        print("Has French Terry:", '500GSM French Terry' in rendered)
        print("Has Trench Coat:", 'Cashmere Wool Blend Trench Coat' in rendered)
        print("Has Instant Checkout:", 'Instant Checkout' in rendered)
    except Exception as e:
        import traceback
        traceback.print_exc()
