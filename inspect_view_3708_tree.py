import psycopg2, json, lxml.etree
conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()
cur.execute("SELECT id, key, arch_db FROM ir_ui_view WHERE id = 3708;")
row = cur.fetchone()
arch = row[2]
s = list(arch.values())[0] if isinstance(arch, dict) else str(arch)
tree = lxml.etree.fromstring(s.encode('utf-8'))
for elem in tree.iter():
    print(elem.tag, elem.attrib.get('id'), elem.attrib.get('class'), elem.attrib.get('name'))
    if elem.tag == 'div' and elem.attrib.get('id') == 'wrap':
        print("FOUND WRAP:", elem.attrib)
        break
conn.close()

