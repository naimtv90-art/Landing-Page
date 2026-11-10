import psycopg2

conn = psycopg2.connect(dbname='Testdata', user='odoo', password='odoopwd', host='localhost')
cur = conn.cursor()
cur.execute("SELECT name, state FROM ir_module_module WHERE name LIKE 'theme_%' AND state='installed';")
print('Installed themes:', cur.fetchall())
cur.execute("SELECT id, name, theme_id FROM website;")
print('Websites:', cur.fetchall())
conn.close()

