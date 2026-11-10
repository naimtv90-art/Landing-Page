import psycopg2, json, re
import lxml.etree as etree

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT arch_db FROM ir_ui_view WHERE id = 3708;")
arch_json = cur.fetchone()[0]
arch = list(arch_json.values())[0] if isinstance(arch_json, dict) else str(arch_json)

# Check all t-* tags in view 3708
tree = etree.fromstring(arch.encode('utf-8'))
t_tags = tree.findall('.//t')
print(f"Total <t> tags in view 3708: {len(t_tags)}")
for t in t_tags[:15]:
    print("  <t", t.attrib, ">")

conn.close()

