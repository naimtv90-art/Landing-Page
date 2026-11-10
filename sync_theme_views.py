import psycopg2
import json

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT id, arch FROM theme_ir_ui_view WHERE id IN (2777, 2778)")
theme_views = dict(cur.fetchall())

cur.execute("SELECT id, arch_db FROM ir_ui_view WHERE id IN (3708, 3709)")
website_views = dict(cur.fetchall())

print("Type of arch_db in ir_ui_view:", type(website_views[3708]))

# Update 3708 with 2777 arch
cur.execute("UPDATE ir_ui_view SET arch_db = %s WHERE id = 3708", (json.dumps({'en_US': theme_views[2777]}) if isinstance(website_views[3708], dict) else theme_views[2777],))

# Update 3709 with 2778 arch
cur.execute("UPDATE ir_ui_view SET arch_db = %s WHERE id = 3709", (json.dumps({'en_US': theme_views[2778]}) if isinstance(website_views[3709], dict) else theme_views[2778],))

conn.commit()
print("Updated ir_ui_view 3708 and 3709 successfully!")

