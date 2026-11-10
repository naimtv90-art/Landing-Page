import psycopg2, json
conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT id, key, arch_db FROM ir_ui_view WHERE id = 2934;")
row = cur.fetchone()
arch = row[2]
s = list(arch.values())[0] if isinstance(arch, dict) else str(arch)
idx = s.find('id="wrap"')
if idx != -1:
    print("Found wrap:\n", s[idx-20:idx+250])
else:
    print("Wrap not found directly in arch!")
conn.close()
