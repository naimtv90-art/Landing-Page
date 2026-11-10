import psycopg2

conn = psycopg2.connect(dbname='Testdata', user='odoo', password='odoopwd', host='localhost')
cur = conn.cursor()
cur.execute("""
    SELECT so.id, so.name, so.state, so.amount_total, rp.name, rp.email, rp.phone
    FROM sale_order so
    JOIN res_partner rp ON rp.id = so.partner_id
    ORDER BY so.id DESC
    LIMIT 5;
""")
for r in cur.fetchall():
    print("Order:", r)
conn.close()
