import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("""
    SELECT name, state 
    FROM ir_module_module 
    WHERE name IN (
        'theme_auraform', 'theme_threadora', 'theme_aardvark', 
        'theme_metamorphosis_industrial', 'theme_octaboot', 
        'theme_threadcraft_garments', 'theme_default', 'theme_multiproduct_landing'
    )
    ORDER BY name
""")
print("=== MODULE STATUSES IN TESTDATA ===")
for row in cur.fetchall():
    print(f"  {row[0]:<35} : {row[1]}")

cur.execute("SELECT id, name, theme_id, homepage_url FROM website WHERE id = 1")
print("\n=== WEBSITE CONFIGURATION ===")
for row in cur.fetchall():
    print(f"  Website ID={row[0]}, Name='{row[1]}', theme_id={row[2]}, homepage_url={row[3]}")

cur.execute("""
    SELECT so.name, so.state, so.amount_total, rp.name 
    FROM sale_order so 
    LEFT JOIN res_partner rp ON rp.id = so.partner_id 
    ORDER BY so.id DESC 
    LIMIT 5
""")
print("\n=== RECENT SALES ORDERS IN ODOO ===")
for row in cur.fetchall():
    print(f"  Order {row[0]}: Status={row[1]}, Total={row[2]}, Customer={row[3]}")

