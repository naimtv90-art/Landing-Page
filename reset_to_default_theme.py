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
    
    custom_theme_names = [
        'theme_auraform',
        'theme_threadora',
        'theme_aardvark',
        'theme_metamorphosis_industrial',
        'theme_octaboot',
        'theme_threadcraft_garments',
    ]
    
    # 1. Uninstall custom themes
    modules = env['ir.module.module'].search([('name', 'in', custom_theme_names), ('state', '=', 'installed')])
    if modules:
        print("Uninstalling custom themes:", modules.mapped('name'))
        modules.button_immediate_uninstall()
        print("Uninstallation completed!")

    # 2. Set Default Theme on Website
    theme_default = env['ir.module.module'].search([('name', '=', 'theme_default')], limit=1)
    if theme_default:
        print(f"Applying theme_default (ID {theme_default.id}) to website 1...")
        website.theme_id = theme_default.id
        theme_default._theme_load(website)
        print("theme_default loaded successfully!")

    # 3. Update Website Name
    website.write({
        'name': 'Aura Store',
        'homepage_url': False,
    })
    print("Website name set to 'Aura Store' and homepage_url set to False.")

    # 4. Ensure our single page landing view is attached to root website_page
    landing_view = env['ir.ui.view'].search([('key', '=', 'theme_multiproduct_landing.landing_page')], limit=1)
    if landing_view:
        root_page = env['website.page'].search([('url', '=', '/'), ('website_id', '=', website.id)], limit=1)
        if not root_page:
            root_page = env['website.page'].search([('url', '=', '/')], limit=1)
        if root_page:
            root_page.write({
                'view_id': landing_view.id,
                'is_published': True,
            })
            print(f"Root website_page (ID {root_page.id}) linked to landing_view {landing_view.id}")

    cr.commit()
    print("ALL DONE: Clean default theme applied and landing page configured!")

