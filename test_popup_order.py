import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request
import json

session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)

payload = {
    'product_id': 20, # Cashmere Wool Blend Trench Coat - Medium (M)
    'quantity': 1,
    'name': 'Emma Watson',
    'phone': '+1 (555) 789-0123',
    'email': 'emma.watson@example.com',
    'street': '742 Evergreen Terrace',
    'city': 'Springfield',
    'order_notes': 'Please ring the doorbell upon arrival.',
    'delivery_carrier_id': False,
    'payment_method': 'cod',
}

req_data = json.dumps({
    'jsonrpc': '2.0',
    'method': 'call',
    'params': payload,
    'id': 999
}).encode('utf-8')

req = urllib.request.Request(
    'http://localhost:8069/landing/submit_order',
    data=req_data,
    headers={
        'Content-Type': 'application/json',
        'Cookie': f'session_id={session.sid}'
    }
)

resp = urllib.request.urlopen(req)
result = json.loads(resp.read().decode('utf-8'))
res = result.get('result', {})

print("Order creation test result:")
print("Status:", res.get('status'))
print("Order Name:", res.get('order_name'))
print("Amount untaxed:", res.get('amount_untaxed'))
print("Customer:", res.get('customer_name'))
