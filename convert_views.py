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
    View = env['ir.ui.view']
    
    theme_views = env['theme.ir.ui.view'].search([('key', 'like', 'theme_multiproduct_landing%')])
    created_views = {}
    
    for tv in theme_views:
        vals = tv._convert_to_base_model(website)
        if not vals:
            continue
        existing = View.search([('key', '=', tv.key), ('website_id', '=', website.id)], limit=1)
        if not existing:
            existing = View.search([('key', '=', tv.key), ('website_id', '=', False)], limit=1)
            
        if existing:
            existing.write(vals)
            base_view = existing
            print(f"Updated view: {tv.key} (ID {base_view.id})")
        else:
            base_view = View.create(vals)
            print(f"Created view: {tv.key} (ID {base_view.id})")
        created_views[tv.key] = base_view

    # Link to website_page for /landing
    landing_view = created_views.get('theme_multiproduct_landing.landing_page')
    if landing_view:
        WebPage = env['website.page']
        landing_page = WebPage.search([('url', '=', '/landing'), ('website_id', '=', website.id)], limit=1)
        if not landing_page:
            landing_page = WebPage.create({
                'url': '/landing',
                'view_id': landing_view.id,
                'website_id': website.id,
                'is_published': True,
                'website_indexed': True,
            })
            print(f"Created website_page for /landing (ID {landing_page.id})")
        else:
            landing_page.write({
                'view_id': landing_view.id,
                'is_published': True,
            })
            print(f"Updated website_page for /landing (ID {landing_page.id})")

    # Also update website homepage_url or root page if desired
    website.write({
        'homepage_url': '/landing'
    })
    print("Website homepage_url set to /landing")

    cr.commit()
    print("Views & pages configured successfully!")
