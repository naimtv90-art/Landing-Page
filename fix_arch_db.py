import psycopg2
import json

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

cur.execute("SELECT id, arch FROM theme_ir_ui_view WHERE id IN (2777, 2778)")
theme_views = dict(cur.fetchall())

# theme_views[2777] is already dict: {'en_US': '<xml string...>'}
xml_2777 = theme_views[2777]['en_US'] if isinstance(theme_views[2777], dict) else theme_views[2777]
xml_2778 = theme_views[2778]['en_US'] if isinstance(theme_views[2778], dict) else theme_views[2778]

print("XML 2777 type:", type(xml_2777), "Length:", len(xml_2777))
print("XML 2778 type:", type(xml_2778), "Length:", len(xml_2778))
print("Contains 'data-bs-target=\"#product-1-checkout\"' in 2777?", 'data-bs-target="#product-1-checkout"' in xml_2777)
print("Contains 'landing-checkout-modal' in 2778?", 'landing-checkout-modal' in xml_2778)

# Now update ir_ui_view arch_db with {'en_US': xml_string}
arch_db_3708 = json.dumps({'en_US': xml_2777})
arch_db_3709 = json.dumps({'en_US': xml_2778})

cur.execute("UPDATE ir_ui_view SET arch_db = %s, write_date = NOW() WHERE id = 3708", (arch_db_3708,))
cur.execute("UPDATE ir_ui_view SET arch_db = %s, write_date = NOW() WHERE id = 3709", (arch_db_3709,))
conn.commit()

print("Successfully updated ir_ui_view 3708 and 3709 with correct JSONB string!")

