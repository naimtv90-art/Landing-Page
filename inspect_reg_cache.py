import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry

registry = Registry('Testdata')
cache_attrs = [x for x in dir(registry) if 'cache' in x.lower()]
print("Registry cache attrs:", cache_attrs)
if hasattr(registry, 'clear_cache'):
    print("clear_cache exists")

