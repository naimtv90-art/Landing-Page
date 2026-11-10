import psycopg2

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT arch_db FROM ir_ui_view WHERE key = 'website.snippets' AND website_id IS NULL")
arch = cur.fetchone()[0]
s = arch['en_US'] if isinstance(arch, dict) else arch
idx = s.find('id="snippet_structure"')
print(s[idx:idx+600])
conn.close()

