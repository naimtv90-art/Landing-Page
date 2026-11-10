import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT id, name, arch_db FROM ir_ui_view WHERE id IN (3708, 3709)")
for row in cur.fetchall():
    print(f"--- VIEW {row[0]} ({row[1]}) ---")
    val = row[2]
    text = str(val)
    print("Length:", len(text))
    print("Contains 'data-bs-target=\"#product-1-checkout\"'?", 'data-bs-target="#product-1-checkout"' in text)
    print("Contains 'landing-checkout-modal'?", 'landing-checkout-modal' in text)

