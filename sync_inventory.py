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
    website = env['website'].browse(1)
    
    # 1. Get the 3 landing products
    products = website.get_landing_products()
    print("Found landing products:", [p.name for p in products])
    
    # Main warehouse internal stock location
    warehouse = env['stock.warehouse'].search([('company_id', '=', website.company_id.id)], limit=1)
    if not warehouse:
        warehouse = env['stock.warehouse'].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    print(f"Using Warehouse: {warehouse.name} ({warehouse.code}), Location: {stock_loc.name} (ID {stock_loc.id})")
    
    # 2. Convert templates to storable products
    for tmpl in products:
        tmpl.write({
            'is_storable': True,
        })
        print(f"Set is_storable=True for template: {tmpl.name} (ID {tmpl.id})")
        
        # 3. For each variant, update stock quantity to 100 units if current qty <= 0
        for variant in tmpl.product_variant_ids:
            current_qty = variant.qty_available
            print(f"  Variant: {variant.display_name} (ID {variant.id}) current stock: {current_qty}")
            if current_qty < 50:
                diff = 100.0 - current_qty
                env['stock.quant']._update_available_quantity(variant, stock_loc, diff)
                print(f"    Added {diff} units. New available: {variant.qty_available}")

    cr.commit()
    print("\nInventory sync complete! All products and variants are now storable and stocked in Odoo Inventory.")

