import psycopg2
conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT id, key, name, type, mode FROM ir_ui_view WHERE key LIKE '%multiproduct%' OR key LIKE '%s_single%' ORDER BY id;")
for r in cur.fetchall():
    print('ir_ui_view:', r)
cur.execute("SELECT id, key, name FROM theme_ir_ui_view WHERE key LIKE '%multiproduct%' OR key LIKE '%s_single%' ORDER BY id;")
for r in cur.fetchall():
    print('theme_ir_ui_view:', r)
conn.close()

