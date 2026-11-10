# -*- coding: utf-8 -*-
from odoo import models, fields, api


DEFAULT_BOOK_SPECS = """মূল লেখক: 
প্রকাশনা: 
পৃষ্ঠা সংখ্যা: 
কাগজের মান: 
বাঁধাই: 
ভাষা: """


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    landing_featured = fields.Boolean(
        string="Feature on Landing Page",
        default=False,
        help="Check this to display this product in the 3-Product Single Page Landing showcase."
    )
    landing_sequence = fields.Integer(
        string="Landing Sequence",
        default=10,
        help="Order of display on the single landing page (1 = First, 2 = Second, 3 = Third)."
    )
    landing_badge = fields.Char(
        string="Badge / Tag",
        help="E.g., 'Best Seller', 'Signature Edition', 'Popular Choice'"
    )
    landing_tagline = fields.Char(
        string="Tagline / Short Hook",
        help="E.g., 'Engineered with Precision Japanese Craftsmanship'"
    )
    landing_headline = fields.Char(
        string="Feature Headline",
        help="Main feature title shown in the showcase section."
    )
    landing_benefits = fields.Text(
        string="Product Benefits",
        help="Enter key benefits, one per line. They will render as styled checklist points."
    )
    landing_specs = fields.Text(
        string="Specifications",
        default=DEFAULT_BOOK_SPECS,
        help="Enter specifications. Only lines with filled values will be shown on the frontend."
    )
    author_id = fields.Many2one(
        'book.author',
        string="লেখক",
        help="বইটির লেখক নির্বাচন করুন। ড্রপডাউন থেকে নির্বাচন করতে পারেন অথবা নতুন লেখক তৈরি করতে পারেন।"
    )
    book_author = fields.Char(
        string="মূল লেখক",
        help="যেমন: জেমস ক্লিয়ার (James Clear)"
    )
    book_publisher = fields.Char(
        string="প্রকাশনা",
        help="যেমন: প্রিমিয়াম পাবলিকেশন্স (রয়েল এডিশন)"
    )
    book_pages = fields.Char(
        string="পৃষ্ঠা সংখ্যা",
        help="যেমন: ৩২০ পৃষ্ঠা"
    )
    book_paper = fields.Char(
        string="কাগজের মান",
        help="যেমন: ৮০ জিএসএম সুইডিশ প্রিমিয়াম ক্রিম পেপার"
    )
    book_binding = fields.Char(
        string="বাঁধাই",
        help="যেমন: সুতার নিখুঁত সেলাই ও শক্ত বাইন্ডিং (পৃষ্ঠা খোলার ভয় নেই)"
    )
    book_language = fields.Char(
        string="ভাষা",
        help="যেমন: প্রাঞ্জল ও আকর্ষণীয় বাংলা অনুবাদ"
    )
    landing_original_price = fields.Float(
        string="Original / Compare Price",
        help="Higher reference price displayed as strikethrough to showcase savings."
    )
    landing_rating = fields.Float(
        string="Customer Rating",
        default=4.9,
        help="Average rating score out of 5.0"
    )
    landing_reviews_count = fields.Integer(
        string="Customer Reviews Count",
        default=142,
        help="Total verified buyer reviews."
    )

    def get_landing_benefits_list(self):
        """Returns clean list of benefits from text lines."""
        self = self.sudo()
        self.ensure_one()
        if not self.landing_benefits:
            return []
        lines = [line.strip() for line in self.landing_benefits.split('\n') if line.strip()]
        return lines

    def get_landing_specs_list(self):
        """Returns structured specifications list [ {'label': ..., 'value': ...}, ... ]
        Left side: Title (label), Right side: Description (value).
        Only items with non-empty values are returned for frontend display."""
        self = self.sudo()
        self.ensure_one()
        specs = []

        # 1. মূল লেখক
        author_val = self.author_id.name if self.author_id else self.book_author
        if author_val and author_val.strip():
            specs.append({'label': 'মূল লেখক', 'value': author_val.strip()})

        # 2. প্রকাশনা
        if self.book_publisher and self.book_publisher.strip():
            specs.append({'label': 'প্রকাশনা', 'value': self.book_publisher.strip()})

        # 3. পৃষ্ঠা সংখ্যা
        if self.book_pages and self.book_pages.strip():
            specs.append({'label': 'পৃষ্ঠা সংখ্যা', 'value': self.book_pages.strip()})

        # 4. কাগজের মান
        if self.book_paper and self.book_paper.strip():
            specs.append({'label': 'কাগজের মান', 'value': self.book_paper.strip()})

        # 5. বাঁধাই
        if self.book_binding and self.book_binding.strip():
            specs.append({'label': 'বাঁধাই', 'value': self.book_binding.strip()})

        # 6. ভাষা
        if self.book_language and self.book_language.strip():
            specs.append({'label': 'ভাষা', 'value': self.book_language.strip()})

        # 7. Additional custom specifications from landing_specs if any
        if self.landing_specs:
            for line in self.landing_specs.split('\n'):
                line = line.strip()
                if not line:
                    continue
                separator = None
                for sep in [':', 'ঃ', '\t', '|']:
                    if sep in line:
                        separator = sep
                        break
                if separator:
                    parts = line.split(separator, 1)
                    lbl = parts[0].strip()
                    val = parts[1].strip()
                    if val and not any(s['label'] == lbl for s in specs):
                        specs.append({'label': lbl, 'value': val})

        return specs

    def get_landing_variants_data(self):
        """Returns structured variant data for frontend JavaScript variant switching."""
        self = self.sudo()
        self.ensure_one()
        variants_data = []
        for variant in self.product_variant_ids:
            variant_sudo = variant.sudo()
            variant_name = variant_sudo.product_template_attribute_value_ids.mapped('name')
            display_name = " / ".join(variant_name) if variant_name else variant_sudo.name
            
            in_stock = True
            try:
                if hasattr(variant_sudo, 'qty_available'):
                    in_stock = variant_sudo.qty_available > 0
            except Exception:
                in_stock = True

            var_price = float(variant_sudo.lst_price)
            variants_data.append({
                'id': variant_sudo.id,
                'name': display_name,
                'price': var_price,
                'price_formatted': f"{self.currency_id.symbol}{var_price:.2f}",
                'in_stock': in_stock,
                'attribute_values': [
                    {
                        'attribute_id': ptav.attribute_id.id,
                        'attribute_name': ptav.attribute_id.name,
                        'value_id': ptav.id,
                        'value_name': ptav.name,
                        'html_color': ptav.product_attribute_value_id.html_color or False,
                    }
                    for ptav in variant_sudo.product_template_attribute_value_ids
                ]
            })
        return variants_data

