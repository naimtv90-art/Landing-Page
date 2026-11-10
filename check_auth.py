import requests
s = requests.Session()
r = s.post('http://localhost:8069/web/session/authenticate', json={
    'jsonrpc': '2.0',
    'params': {'db': 'Testdata', 'login': 'admin', 'password': 'admin'}
})
print("Auth status:", r.status_code)
print("Auth text:", r.text[:300])

