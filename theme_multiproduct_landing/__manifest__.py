# -*- coding: utf-8 -*-
{
    'name': 'Single Page Multi-Product Landing Page',
    'summary': 'Premium Apple/Shopify-style Single Page eCommerce Experience for 3 Curated Products',
    'description': """
Modern High-Converting Single Page Multi-Product Landing Page for Odoo 19
========================================================================
- Showcase exactly 3 curated products on a seamless vertical scrolling single page.
- Each product features high-resolution gallery, variants, technical specs, benefits, and an instant inline checkout form.
- Real Odoo eCommerce integration: creates real Sales Orders, Customer Partners, Delivery calculations, and Payment transactions.
- Admin management: feature and manage products, descriptions, badges, specs, and variants directly from Odoo ERP backend.
- Mobile-first, responsive, ultra-clean typography, and instant modal order confirmation receipts.
    """,
    'version': '19.0.1.0.0',
    'category': 'Website/Theme',
    'author': 'Antigravity Premium Engineering',
    'website': 'https://antigravity.odoo.store',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'website',
        'website_sale',
        'sale',
        'payment',
        'delivery',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/templates.xml',
        'views/snippets.xml',
        'data/landing_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_multiproduct_landing/static/src/css/landing.css',
            'theme_multiproduct_landing/static/src/js/landing.js',
        ],
        'website.website_builder_assets': [
            'theme_multiproduct_landing/static/src/website_builder/**/*',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}

