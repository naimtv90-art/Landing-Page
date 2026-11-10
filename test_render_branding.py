import sys
sys.path.append(r"C:\Program Files\Odoo 19.0.20260902\server")
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry
from bs4 import BeautifulSoup

reg = Registry('Testdata')
with reg.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    website = env['website'].get_current_website()
    
    # Render contactus with branding
    irqweb = env['ir.qweb'].with_context(website_id=website.id, inherit_branding=True)
    html_contact = irqweb._render('website.contactus', {'website': website, 'res_company': website.company_id})
    soup_c = BeautifulSoup(html_contact, 'html.parser')
    wrap_c = soup_c.find(id="wrap")
    print("Contactus wrap attrs:\n", wrap_c.attrs if wrap_c else "None")
    
    # Render landing_page with branding
    html_landing = irqweb._render('theme_multiproduct_landing.landing_page', {'website': website, 'company': website.company_id, 'products': website.get_landing_products()})
    soup_l = BeautifulSoup(html_landing, 'html.parser')
    wrap_l = soup_l.find(id="wrap")
    print("Landing wrap attrs:\n", wrap_l.attrs if wrap_l else "None")

