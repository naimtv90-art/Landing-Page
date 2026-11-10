import sys
sys.path.append(r"C:\Program Files\Odoo 19.0.20260902\server")
import odoo
from odoo.modules.registry import Registry
from odoo import api

odoo.tools.config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
registry = Registry('Testdata')

with registry.cursor() as cr:
    env = api.Environment(cr, odoo.SUPERUSER_ID, {})

    # 1. Attribute: Size
    Attribute = env['product.attribute']
    AttrValue = env['product.attribute.value']
    
    size_attr = Attribute.search([('name', '=', 'Size')], limit=1)
    if not size_attr:
        size_attr = Attribute.create({
            'name': 'Size',
            'display_type': 'pills',
            'create_variant': 'always',
        })
        print("Created Size attribute")

    # Values
    sizes = ['Small (S)', 'Medium (M)', 'Large (L)']
    value_ids = []
    for s in sizes:
        val = AttrValue.search([('attribute_id', '=', size_attr.id), ('name', '=', s)], limit=1)
        if not val:
            val = AttrValue.create({
                'attribute_id': size_attr.id,
                'name': s,
            })
        value_ids.append(val.id)
    print("Size value IDs:", value_ids)

    # 2. Attach to Products 6, 8, 11 if not already attached
    PTAL = env['product.template.attribute.line']
    for p_id in [6, 8, 11]:
        tmpl = env['product.template'].browse(p_id)
        existing_line = PTAL.search([('product_tmpl_id', '=', tmpl.id), ('attribute_id', '=', size_attr.id)], limit=1)
        if not existing_line:
            PTAL.create({
                'product_tmpl_id': tmpl.id,
                'attribute_id': size_attr.id,
                'value_ids': [(6, 0, value_ids)],
            })
            tmpl._create_variant_ids()
            print(f"Created Size attribute line on product {tmpl.name}")
        else:
            print(f"Product {tmpl.name} already has Size attribute")

    cr.commit()
    print("Attribute setup completed successfully!")
