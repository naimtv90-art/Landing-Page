# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BookAuthor(models.Model):
    _name = 'book.author'
    _description = 'বইয়ের লেখক (Book Author)'
    _order = 'name asc'

    name = fields.Char(
        string="লেখকের নাম",
        required=True,
        help="যেমন: জেমস ক্লিয়ার (James Clear)"
    )
    image_1920 = fields.Image(
        string="লেখকের ছবি",
        max_width=1024,
        max_height=1024
    )
    bio = fields.Text(
        string="সংক্ষিপ্ত পরিচিতি / বায়োগ্রাফি",
        help="লেখক সম্পর্কিত সংক্ষিপ্ত বিবরণ"
    )
    product_ids = fields.One2many(
        'product.template',
        'author_id',
        string="বইসমূহ"
    )
    product_count = fields.Integer(
        string="মোট বইয়ের সংখ্যা",
        compute='_compute_product_count',
        store=False
    )
    active = fields.Boolean(
        string="সক্রিয়",
        default=True
    )

    @api.depends('product_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_ids)

