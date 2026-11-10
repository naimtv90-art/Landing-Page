import psycopg2
conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT id, key, arch_db FROM ir_ui_view WHERE key = 'website.homepage';")
row = cur.fetchone()
if row:
    print("website.homepage id:", row[0])
    arch = row[2]
    s = list(arch.values())[0] if isinstance(arch, dict) else str(arch)
    print("website.homepage arch:\n", s[:1000])
else:
    print("website.homepage not found")
conn.close()

