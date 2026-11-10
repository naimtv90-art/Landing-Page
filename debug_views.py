import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("""
    SELECT id, name, key, website_id 
    FROM ir_ui_view 
    WHERE key LIKE '%single_product_block%' OR key LIKE '%landing_page%'
""")
print("ir_ui_view records:")
for row in cur.fetchall():
    print(" ", row)

cur.execute("""
    SELECT id, name, key 
    FROM theme_ir_ui_view 
    WHERE key LIKE '%single_product_block%' OR key LIKE '%landing_page%'
""")
print("\ntheme_ir_ui_view records:")
for row in cur.fetchall():
    print(" ", row)

