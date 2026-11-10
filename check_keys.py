import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT id, name, key, website_id, active FROM ir_ui_view WHERE key LIKE '%landing_page%' OR key LIKE '%single_product%'")
for r in cur.fetchall():
    print(r)

