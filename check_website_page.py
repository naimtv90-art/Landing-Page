import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("""
    SELECT wp.id, wp.url, wp.view_id, v.key, v.name 
    FROM website_page wp 
    JOIN ir_ui_view v ON v.id = wp.view_id 
    WHERE wp.url = '/'
""")
for row in cur.fetchall():
    print("Page / view:", row)

cur.execute("""
    SELECT id, name, key, website_id, write_date 
    FROM ir_ui_view 
    WHERE key = 'theme_multiproduct_landing.landing_page' 
       OR key = 'theme_multiproduct_landing.single_product_block'
""")
for row in cur.fetchall():
    print("Landing view:", row)

