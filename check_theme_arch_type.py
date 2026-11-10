import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT id, name, arch FROM theme_ir_ui_view WHERE id IN (2777, 2778)")
for row in cur.fetchall():
    print(row[0], row[1], "Type of arch:", type(row[2]))
    if isinstance(row[2], dict):
        print("  Keys:", list(row[2].keys()))
        for k in row[2]:
            print(f"  Key {k} len: {len(str(row[2][k]))}")
    else:
        print("  Length:", len(str(row[2])))

