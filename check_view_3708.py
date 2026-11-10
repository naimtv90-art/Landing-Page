import psycopg2, json
conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT id, key, arch_db FROM ir_ui_view WHERE id = 3708;")
row = cur.fetchone()
print("ID:", row[0], "KEY:", row[1])
arch = row[2]
if isinstance(arch, dict):
    print("dict arch:", list(arch.keys()))
    s = list(arch.values())[0]
else:
    s = str(arch)
print("First 500 chars of arch:\n", s[:500])
print("\nCheck if oe_structure is in arch:\n", 'oe_structure' in s)
conn.close()

