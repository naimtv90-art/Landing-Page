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
        'theme_aardvark',
        'theme_octaboot',
        'theme_threadcraft_garments',
        'theme_threadora',
        'theme_metamorphosis_industrial',
    ]
    
    modules = env['ir.module.module'].search([('name', 'in', custom_theme_names), ('state', '=', 'installed')])
    print("Custom themes to remove:", modules.mapped('name'))
    
    # Check if any other module depends on them
    for m in modules:
        downstream = m.downstream_dependencies()
        # filter out itself
        downstream = [d.name for d in downstream if d != m]
        print(f"Module {m.name} downstream dependencies:", downstream)

