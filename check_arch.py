import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT id, arch FROM theme_ir_ui_view WHERE id IN (2777, 2778)")
theme_views = cur.fetchall()
print("theme_ir_ui_view:")
for tid, arch in theme_views:
    print(f"  ID {tid}: 'landing-checkout-modal' in arch? {'landing-checkout-modal' in str(arch)}")

cur.execute("SELECT id, arch_db FROM ir_ui_view WHERE id IN (3708, 3709)")
website_views = cur.fetchall()
print("\nir_ui_view:")
for wid, arch in website_views:
    print(f"  ID {wid}: 'landing-checkout-modal' in arch? {'landing-checkout-modal' in str(arch)}")
