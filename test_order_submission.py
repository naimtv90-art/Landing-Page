import sys
sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.http import root
import urllib.request
import json

session = root.session_store.new()
session.db = 'Testdata'
root.session_store.save(session)

# 1. Product 02 Order
payload2 = {
    "product_id": 18, # 500GSM French Terry Hoodie (Large)
    "quantity": 1,
    "name": "Sarah Jenkins",
    "phone": "+1 415 890 2345",
    "email": "sarah.j@example.com",
    "street": "100 Market St, Floor 12",
    "city": "San Francisco",
    "order_notes": "Leave with reception",
    "delivery_carrier_id": 1,
    "payment_method": "cod"
}

body2 = json.dumps({"jsonrpc": "2.0", "method": "call", "params": payload2, "id": 102}).encode('utf-8')
req2 = urllib.request.Request('http://localhost:8069/landing/submit_order', data=body2, headers={'Content-Type': 'application/json', 'Cookie': f'session_id={session.sid}'})
res2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
print("Product 02 Order Response:", res2['result']['status'], res2['result']['order_name'], res2['result']['amount_total_formatted'])

# 2. Product 03 Order
payload3 = {
    "product_id": 21, # Cashmere Trench Coat (Medium)
    "quantity": 1,
    "name": "Julian Montgomery",
    "phone": "+1 212 901 8877",
    "email": "julian.m@luxuryestate.com",
    "street": "432 Park Avenue, Penthouse 6",
    "city": "New York",
    "order_notes": "Call upon delivery",
    "delivery_carrier_id": 1,
    "payment_method": "cod"
}

body3 = json.dumps({"jsonrpc": "2.0", "method": "call", "params": payload3, "id": 103}).encode('utf-8')
req3 = urllib.request.Request('http://localhost:8069/landing/submit_order', data=body3, headers={'Content-Type': 'application/json', 'Cookie': f'session_id={session.sid}'})
res3 = json.loads(urllib.request.urlopen(req3).read().decode('utf-8'))
print("Product 03 Order Response:", res3['result']['status'], res3['result']['order_name'], res3['result']['amount_total_formatted'])
