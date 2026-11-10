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
    v1 = env.ref('theme_multiproduct_landing.landing_page')
    v2 = env.ref('theme_multiproduct_landing.single_product_block')
    
    print("v1 arch has data-bs-target?", 'data-bs-target="#product-1-checkout"' in v1.arch)
    print("v2 arch has landing-checkout-modal?", 'landing-checkout-modal' in v2.arch)

    print("v1 copy_ids:", v1.copy_ids)
    print("v2 copy_ids:", v2.copy_ids)

    # Let's update copy_ids arch directly via Odoo ORM!
    for copy in v1.copy_ids:
        copy.write({'arch': v1.arch})
        print(f"Updated copy {copy.id} for v1")

    for copy in v2.copy_ids:
        copy.write({'arch': v2.arch})
        print(f"Updated copy {copy.id} for v2")

    cr.commit()
    print("Changes committed to database via ORM!")

