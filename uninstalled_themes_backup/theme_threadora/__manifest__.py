# -*- coding: utf-8 -*-
{
    'name': 'Theme THREADORA Garments',
    'summary': 'Premium Garments, Fashion, Apparel & Manufacturing Theme for Odoo 19',
    'description': '''
Theme THREADORA Garments for Odoo 19
===================================
A high-end, responsive Fashion, Garments, Apparel & B2B Manufacturing website theme for Odoo 19.

Features:
* 3D Garment Interactive Canvas Hero
* Light Mode / Dark Mode with instant toggle
* 14+ Drag & Drop Website Builder snippets
* B2B Wholesale & Private Label OEM/ODM Showcase
* Garments eCommerce & Variants
* Manufacturing Process, Quality Control & Sustainability
    ''',
    'category': 'Theme/Ecommerce',
    'version': '19.0.1.0.0',
    'author': 'THREADORA Apparel',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale'],
    'data': [
        'data/menu.xml',
        'data/products.xml',
        'views/header_footer_templates.xml',
        'views/snippets/s_garment_hero.xml',
        'views/snippets/s_garment_stats.xml',
        'views/snippets/s_garment_categories.xml',
        'views/snippets/s_garment_products.xml',
        'views/snippets/s_garment_collection.xml',
        'views/snippets/s_garment_manufacturing.xml',
        'views/snippets/s_garment_wholesale.xml',
        'views/snippets/s_garment_private_label.xml',
        'views/snippets/s_garment_quality.xml',
        'views/snippets/s_garment_sustainability.xml',
        'views/snippets/s_garment_testimonials.xml',
        'views/snippets/s_garment_faq.xml',
        'views/snippets/s_garment_newsletter.xml',
        'views/snippets/s_garment_cta.xml',
        'views/snippets.xml',
        'views/homepage.xml',
        'views/aboutus.xml',
        'views/faq.xml',
        'views/contactus.xml',
        'views/wholesale.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_threadora/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'theme_threadora/static/src/scss/theme_garments.scss',
            'theme_threadora/static/src/scss/snippets.scss',
            'theme_threadora/static/src/js/theme_garments.js',
        ],
    },
    'application': False,
    'auto_install': False,
    'installable': True,
}