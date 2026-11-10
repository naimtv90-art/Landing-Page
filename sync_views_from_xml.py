import psycopg2
import json
import lxml.etree

conn = psycopg2.connect('dbname=Testdata user=odoo password=odoopwd host=localhost')
cur = conn.cursor()

def sync_xml(xml_path):
    tree = lxml.etree.parse(xml_path)
    for tmpl in tree.getroot().findall('.//template'):
        tmpl_id = tmpl.get('id')
        tmpl_key = f'theme_multiproduct_landing.{tmpl_id}'
        inherit_id = tmpl.get('inherit_id')
        
        # Clone and format
        tmpl_copy = lxml.etree.fromstring(lxml.etree.tostring(tmpl))
        if 'id' in tmpl_copy.attrib:
            del tmpl_copy.attrib['id']

        if inherit_id:
            # Inheriting view must have <data> as root, keeping inherit_id
            tmpl_copy.tag = 'data'
            if 't-name' in tmpl_copy.attrib:
                del tmpl_copy.attrib['t-name']
        else:
            # Primary template has <t t-name="..."> as root
            tmpl_copy.tag = 't'
            tmpl_copy.attrib['t-name'] = tmpl_key
            
        s = lxml.etree.tostring(tmpl_copy, encoding='utf-8').decode('utf-8')
        arch_json = json.dumps({'en_US': s})
        
        # Update theme_ir_ui_view
        cur.execute("UPDATE theme_ir_ui_view SET arch = %s, write_date = NOW() WHERE key = %s", (arch_json, tmpl_key))
        theme_cnt = cur.rowcount
        
        # Update ir_ui_view (normalize key and update arch_db)
        if inherit_id:
            cur.execute("UPDATE ir_ui_view SET key = %s, arch_db = %s, write_date = NOW() WHERE (key = %s OR key LIKE %s) AND inherit_id IS NOT NULL", 
                        (tmpl_key, arch_json, tmpl_key, tmpl_key + '_%'))
        else:
            # Delete any duplicate inheriting views accidentally created for primary templates
            cur.execute("DELETE FROM ir_ui_view WHERE key = %s AND inherit_id IS NOT NULL", (tmpl_key,))
            cur.execute("UPDATE ir_ui_view SET key = %s, arch_db = %s, write_date = NOW() WHERE (key = %s OR key LIKE %s) AND inherit_id IS NULL", 
                        (tmpl_key, arch_json, tmpl_key, tmpl_key + '_%'))
        ir_cnt = cur.rowcount
        
        print(f"Synced {tmpl_key}: updated {theme_cnt} theme views, {ir_cnt} ir views.")

def sync_product_views(xml_path):
    tree = lxml.etree.parse(xml_path)
    for rec in tree.getroot().findall('.//record'):
        rec_id = rec.get('id')
        if rec_id == 'product_template_landing_form_inherit':
            field_arch = rec.find('.//field[@name="arch"]')
            if field_arch is not None and len(field_arch) > 0:
                s = lxml.etree.tostring(field_arch[0], encoding='utf-8').decode('utf-8')
                arch_json = json.dumps({'en_US': s})
                cur.execute("UPDATE ir_ui_view SET arch_db = %s, write_date = NOW() WHERE id = 3707", (arch_json,))
                print(f"Synced {rec_id} (id=3707): {cur.rowcount} ir views updated.")

sync_xml(r'd:\Antigravity\Odoo theme\Landing Page\theme_multiproduct_landing\views\templates.xml')
sync_xml(r'd:\Antigravity\Odoo theme\Landing Page\theme_multiproduct_landing\views\snippets.xml')
sync_product_views(r'd:\Antigravity\Odoo theme\Landing Page\theme_multiproduct_landing\views\product_views.xml')

conn.commit()
conn.close()
print("All XML views successfully synced to database!")
