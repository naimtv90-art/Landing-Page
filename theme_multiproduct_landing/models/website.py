# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    landing_product_1_id = fields.Many2one(
        'product.template',
        string="Featured Product 01",
        help="Primary product displayed at the top of the single-page landing showcase."
    )
    landing_product_2_id = fields.Many2one(
        'product.template',
        string="Featured Product 02",
        help="Second product displayed in the single-page landing showcase."
    )
    landing_product_3_id = fields.Many2one(
        'product.template',
        string="Featured Product 03",
        help="Third product displayed in the single-page landing showcase."
    )
    landing_hero_badge = fields.Char(
        string="Hero Badge",
        default="Curated Signature Collection",
        help="Subtle badge pill above hero headline."
    )
    landing_hero_title = fields.Char(
        string="Hero Headline",
        default="Three Masterpieces. One Elevated Experience.",
        help="Main headline in the landing hero section."
    )
    landing_hero_subtitle = fields.Text(
        string="Hero Subtitle",
        default="Explore three masterfully crafted products designed for uncompromising quality, timeless aesthetics, and everyday performance. Experience each creation below and order directly from this single page.",
        help="Supporting description in hero section."
    )
    landing_announcement = fields.Char(
        string="Top Announcement Bar",
        default="★ Free Worldwide Express Shipping & Cash On Delivery Available Today Only",
        help="Top notification bar text."
    )

    def get_landing_products(self):
        """Retrieves exactly 3 products to be presented in vertical scroll order."""
        self = self.sudo()
        self.ensure_one()
        products = []

        # 1. Check if explicitly configured in website settings
        configured = [self.landing_product_1_id, self.landing_product_2_id, self.landing_product_3_id]
        valid_configured = [p for p in configured if p and p.exists() and p.sale_ok]
        if len(valid_configured) == 3:
            return self.env['product.template'].sudo().browse([p.id for p in valid_configured])

        # 2. Check products marked with landing_featured
        featured = self.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('landing_featured', '=', True),
        ], order='landing_sequence asc, id asc', limit=3)
        if len(featured) == 3:
            return featured

        # 3. Fallback: published products
        fallback = self.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('is_published', '=', True),
        ], order='id asc', limit=3)
        return fallback

