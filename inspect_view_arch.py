import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT arch_db FROM ir_ui_view WHERE id = 3708")
row = cur.fetchone()
print("3708 arch_db has 'data-bs-toggle=\"modal\"'?", 'data-bs-toggle="modal"' in str(row[0]))

cur.execute("SELECT arch_db FROM ir_ui_view WHERE id = 3709")
row2 = cur.fetchone()
print("3709 arch_db has 'landing-checkout-modal'?", 'landing-checkout-modal' in str(row2[0]))

