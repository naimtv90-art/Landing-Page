# -*- coding: utf-8 -*-
{
    'name': 'Bookmart',
    'summary': '3D Book Showcase & COD Checkout - High-Converting Single Page eCommerce Theme for Odoo 19',
    'description': """
Bookmart by Metamorphosis
=====================================
A high-converting, interactive 3D Book Showcase and Cash-on-Delivery eCommerce single-page landing solution engineered for Odoo 19.

Key Features:
-------------
* Interactive 3D Book Showcase on Golden Diamond Lattice Stand
* Detailed Bangla Book Specification Tables & Author bio integration
* Instant Inline Cash on Delivery (COD) order checkout forms
* Live Slide-Out Multi-Product Cart drawer with dynamic delivery calculation
* Seamless Light Mode & Obsidian Dark Mode with frosted glass sticky navigation
* Native Odoo 19 Website Builder Drag & Drop building block snippets
* Real-time backend Odoo ERP Sales Orders, Inventory, Partner & Invoice automation
* Ultra-responsive, mobile-first design optimized for high conversion
    """,
    'category': 'Theme/eCommerce',
    'version': '19.0.1.0.0',
    'author': 'Metamorphosis',
    'company': 'Metamorphosis',
    'maintainer': 'Metamorphosis',
    'website': 'https://metamorphosis.com.bd',
    'license': 'LGPL-3',
    'icon': '/bookmart/static/description/icon.png',
    'images': [
        'static/description/banner.gif',
        'static/description/bookmart_cover.png',
        'static/description/screenshot_hero_dark.png',
    ],
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
            'bookmart/static/src/css/landing.css',
            'bookmart/static/src/js/landing.js',
        ],
        'website.website_builder_assets': [
            'bookmart/static/src/website_builder/**/*',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}
