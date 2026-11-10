# -*- coding: utf-8 -*-
{
    'name': 'Theme Aardvark',
    'summary': 'Cloned theme of Aardvark Book Club for Odoo 19',
    'description': '''
Theme Aardvark Book Club for Odoo 19
===================================
A vibrant, playful, and high-conversion book subscription club theme cloned from https://www.aardvarkbookclub.com/.

Features:
* Bold retro-editorial typography and handwritten cursive accents
* Signature electric yellow, vibrant hot-pink, periwinkle, olive and dark color palette
* Signature pill-shaped button-alt elements with interactive arrow indicators
* Ear-tab cutout book cards for monthly drops
* 4-Step "How It Works" visual cards with numbered stamp illustrations
* Interactive "Choose from" genre pill wall
* "Why Aardvark?" floating momentum benefit badges
* Annual Members' Choice Winners showcase
* Exclusive book anthology showcase with Goodreads rating badge
* Gifting subscription cards and verified press mentions
* Interactive FAQ accordions
* Full Odoo 19 Website Builder drag-and-drop snippet blocks
* 100% mobile responsive and editable
    ''',
    'category': 'Theme/Ecommerce',
    'version': '19.0.1.0.0',
    'author': 'Antigravity',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale'],
    'data': [
        'data/menu.xml',
        'views/header_footer_templates.xml',
        'views/snippets/s_aardvark_hero.xml',
        'views/snippets/s_aardvark_promo_ribbon.xml',
        'views/snippets/s_aardvark_books_slider.xml',
        'views/snippets/s_aardvark_how_it_works.xml',
        'views/snippets/s_aardvark_box_showcase.xml',
        'views/snippets/s_aardvark_genres.xml',
        'views/snippets/s_aardvark_benefits.xml',
        'views/snippets/s_aardvark_choice_winners.xml',
        'views/snippets/s_aardvark_exclusive.xml',
        'views/snippets/s_aardvark_gifting.xml',
        'views/snippets/s_aardvark_faq.xml',
        'views/snippets/s_aardvark_cta.xml',
        'views/snippets.xml',
        'views/homepage.xml',
        'views/faq.xml',
        'views/gifting.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_aardvark/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'theme_aardvark/static/src/scss/theme_aardvark.scss',
            'theme_aardvark/static/src/scss/snippets.scss',
            'theme_aardvark/static/src/js/theme_aardvark.js',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'application': False,
    'auto_install': False,
    'installable': True,
}
