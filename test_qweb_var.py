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
    qweb = env['ir.qweb']
    template_str = """
    <t>
        <t t-set="variants_data" t-value="[{'id': v.id, 'price': v.lst_price} for v in product.product_variant_ids]"/>
        <t t-foreach="variants_data" t-as="item">
            <p><t t-out="item['id']"/>: <t t-out="item['price']"/></p>
        </t>
    </t>
    """
    res = qweb._render(qweb._compile(template_str), {'product': env['product.template'].browse(6)})
    print("QWeb render test result:")
    print(res)

