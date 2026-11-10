import xmlrpc.client

common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
print('Version:', common.version())

