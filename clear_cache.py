import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])

from odoo.modules.registry import Registry

registry = Registry('Testdata')
registry.clear_cache()
registry.signal_changes()
print("Registry cleared and signal_changes() called successfully!")
