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
    
    # 1. Remove attribute lines from templates 6, 8, 11
    PTAL = env['product.template.attribute.line']
    for pid in [6, 8, 11]:
        tmpl = env['product.template'].browse(pid)
        lines = PTAL.search([('product_tmpl_id', '=', tmpl.id)])
        if lines:
            print(f"Unlinking attribute lines from {tmpl.name}...")
            lines.unlink()
        tmpl._create_variant_ids()
        print(f"Product {tmpl.name} (ID {tmpl.id}) now has {len(tmpl.product_variant_ids)} variant(s). Default ID: {tmpl.product_variant_ids[:1].id}")

    # 2. Set warehouse stock for the single variant of each book
    warehouse = env['stock.warehouse'].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    
    for pid in [6, 8, 11]:
        tmpl = env['product.template'].browse(pid)
        for v in tmpl.product_variant_ids:
            if v.qty_available < 50:
                diff = 100.0 - v.qty_available
                env['stock.quant']._update_available_quantity(v, stock_loc, diff)
            print(f"  Variant {v.display_name} (ID {v.id}): Stock = {v.qty_available}, Price = {v.list_price}")

    cr.commit()
    print("\nSuccessfully removed Small, Medium, Large variants from all books!")

