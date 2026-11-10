import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry
reg = Registry('Testdata')
with reg.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    wp = env['website.page'].search([('url', 'in', ['/', '/landing'])])
    print('website.page for / or /landing:', wp)
    for p in wp:
        print(p.id, p.name, p.url, p.view_id.id, p.view_id.key)
    
    # check homepage
    website = env['website'].get_current_website()
    print("Website homepage_url:", website.homepage_url)
    
    # Check ir.ui.view for website.homepage
    home_view = env['ir.ui.view'].search([('key', '=', 'website.homepage')])
    print("website.homepage view:", home_view.id if home_view else None)
    
    # Check contactus
    contact = env['website.page'].search([('url', '=', '/contactus')])
    print("contactus page:", contact.id, contact.view_id.key, contact.view_id.id)

