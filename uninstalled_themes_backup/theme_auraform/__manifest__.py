# -*- coding: utf-8 -*-
{
    'name': 'AuraForm 3D - Kinetic Ergonomics Theme',
    'summary': 'Next-Gen 3D eCommerce Website Theme for Ergonomic Furniture & Kinetic Workstations',
    'description': """
Theme AuraForm - High-Performance 3D Web Theme
==============================================
Designed for luxury ergonomic seating, architectural office furniture, and bespoke product builders.
Includes drag-and-drop Three.js 3D snippets, live PBR customizer, kinetic feature reveals, and direct eCommerce cart integration.

Key Features:
-------------
* 3D Interactive Hero Banner (`s_3d_hero`) with mouse-parallax & turntable preview
* Live 3D Product Customizer Studio (`s_3d_customizer`) with PBR material swaps, dynamic pricing & direct cart bridge
* Scroll-Driven Feature Reveal Cards (`s_scroll_features`)
* Interactive 3D Product Teaser Cards (`s_3d_product_teaser`)
* Native Odoo Website Editor snippet options (model URL, background tint, auto-rotate, camera zoom)
* 100% Mobile Responsive & WebGL Fallback handling
    """,
    'category': 'Website/Theme',
    'version': '19.0.1.0.0',
    'author': 'AuraForm Creative Technologies',
    'website': 'https://www.auraform.design',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'website_sale',
    ],
    'data': [
        'views/snippets.xml',
        'views/pages.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # Local Three.js Libraries
            'theme_auraform/static/lib/three/three.min.js',
            'theme_auraform/static/lib/three/OrbitControls.js',
            'theme_auraform/static/lib/three/GLTFLoader.js',
            'theme_auraform/static/lib/three/RGBELoader.js',
            
            # Theme & Snippet CSS Styles
            'theme_auraform/static/src/css/theme.css',
            'theme_auraform/static/src/css/snippets.css',
            
            # Custom 3D Odoo Public Widgets
            'theme_auraform/static/src/js/snippets/s_3d_hero.js',
            'theme_auraform/static/src/js/snippets/s_3d_customizer.js',
            'theme_auraform/static/src/js/snippets/s_3d_product_teaser.js',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'application': True,
    'auto_install': False,
    'installable': True,
}
