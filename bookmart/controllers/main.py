# -*- coding: utf-8 -*-
import json
import re
from odoo import http, fields, _
from odoo.http import request


class LandingPageController(http.Controller):

    @http.route(['/', '/bookmart', '/landing'], type='http', auth='public', website=True, sitemap=True)
    def landing_page(self, **post):
        """Renders the single-page multi-product showcase."""
        website = request.website
        products = website.get_landing_products()

        # Delivery methods
        delivery_methods = request.env['delivery.carrier'].sudo().search([
            ('is_published', '=', True)
        ])

        # Payment providers
        payment_providers = request.env['payment.provider'].sudo().search([
            ('state', 'in', ['enabled', 'test']),
            ('is_published', '=', True)
        ])

        # Active cart quantity
        cart = request.cart
        cart_qty = cart.cart_quantity if cart else 0

        values = {
            'website': website,
            'company': website.company_id,
            'products': products,
            'delivery_methods': delivery_methods,
            'payment_providers': payment_providers,
            'cart_qty': cart_qty,
            'currency': website.currency_id,
        }
        return request.render('bookmart.landing_page', values)

    @http.route('/landing/get_variants/<int:product_tmpl_id>', type='jsonrpc', auth='public', website=True)
    def get_product_variants(self, product_tmpl_id, **kwargs):
        """Returns variant data and combination options for a product template."""
        tmpl = request.env['product.template'].sudo().browse(product_tmpl_id).exists()
        if not tmpl:
            return {'status': 'error', 'message': 'Product template not found'}

        variants = []
        for p in tmpl.product_variant_ids:
            ptavs = p.product_template_attribute_value_ids
            name_parts = [v.name for v in ptavs]
            variant_name = " - ".join(name_parts) if name_parts else p.name
            price_val = float(p.lst_price)
            variants.append({
                'id': p.id,
                'name': variant_name,
                'price': price_val,
                'price_formatted': f"{tmpl.currency_id.symbol}{price_val:.2f}",
                'attribute_values': [ptav.id for ptav in ptavs],
            })

        return {
            'status': 'success',
            'product_tmpl_id': tmpl.id,
            'name': tmpl.name,
            'variants': variants,
        }

    @http.route('/landing/calculate_summary', type='jsonrpc', auth='public', website=True)
    def calculate_summary(self, product_id, quantity=1, carrier_id=None, **kwargs):
        """Calculates live subtotal, shipping charge, and grand total."""
        product = request.env['product.product'].sudo().browse(int(product_id)).exists()
        if not product:
            return {'status': 'error', 'message': 'Product not found'}

        quantity = max(1, int(quantity))
        subtotal = float(product.lst_price * quantity)

        delivery_charge = 0.0
        carrier_name = "Standard Delivery"
        if carrier_id:
            carrier = request.env['delivery.carrier'].sudo().browse(int(carrier_id)).exists()
            if carrier:
                delivery_charge = float(carrier.fixed_price or 0.0)
                carrier_name = carrier.name
        else:
            default_carrier = request.env['delivery.carrier'].sudo().search([('is_published', '=', True)], limit=1)
            if default_carrier:
                delivery_charge = float(default_carrier.fixed_price or 0.0)
                carrier_name = default_carrier.name

        total = subtotal + delivery_charge
        currency = product.currency_id or request.website.currency_id

        return {
            'status': 'success',
            'subtotal': subtotal,
            'subtotal_formatted': f"{currency.symbol}{subtotal:.2f}",
            'delivery_charge': delivery_charge,
            'delivery_formatted': f"{currency.symbol}{delivery_charge:.2f}" if delivery_charge > 0 else "FREE",
            'carrier_name': carrier_name,
            'total': total,
            'total_formatted': f"{currency.symbol}{total:.2f}",
            'currency_symbol': currency.symbol,
        }

    @http.route('/landing/add_to_cart', type='jsonrpc', auth='public', website=True)
    def add_to_cart(self, product_id=None, product_template_id=None, quantity=1, **kwargs):
        """Adds a product to the active shopping cart and returns updated cart quantity."""
        quantity = max(1, int(quantity or 1))
        product = None
        if product_id:
            product = request.env['product.product'].sudo().browse(int(product_id)).exists()
        if not product and product_template_id:
            tmpl = request.env['product.template'].sudo().browse(int(product_template_id)).exists()
            if tmpl:
                product = tmpl.product_variant_id or (tmpl.product_variant_ids and tmpl.product_variant_ids[0])

        if not product:
            return {'status': 'error', 'message': 'Product not found'}

        # Get or create current cart
        order_sudo = request.cart or request.website._create_cart()
        order_sudo.with_context(skip_cart_verification=True)._cart_add(
            product_id=product.id,
            quantity=quantity
        )
        request.session['sale_order_id'] = order_sudo.id

        return {
            'status': 'success',
            'product_id': product.id,
            'product_name': product.name,
            'quantity': quantity,
            'cart_quantity': int(order_sudo.cart_quantity or 0),
            'message': f"'{product.name}' কার্টে যোগ করা হয়েছে!"
        }

    @http.route('/landing/submit_order', type='jsonrpc', auth='public', website=True)
    def submit_order(self, **post):
        """
        Creates and processes a REAL Odoo Sales Order from the inline checkout form.
        Validates inputs, connects/creates partner, adds line, sets delivery, and confirms order.
        """
        product_id = post.get('product_id')
        quantity = post.get('quantity', 1)
        name = (post.get('name') or post.get('customer_name') or '').strip()
        phone = (post.get('phone') or post.get('customer_phone') or '').strip()
        email = (post.get('email') or '').strip()
        street = (post.get('street') or post.get('customer_address') or '').strip()
        city = (post.get('city') or 'Local Area').strip()
        order_notes = (post.get('order_notes') or '').strip()
        carrier_id = post.get('delivery_carrier_id') or post.get('carrier_id')
        payment_method = post.get('payment_method', 'cod')

        # --- Validation ---
        errors = {}
        if not name:
            errors['name'] = "Full name is required."
        if not phone:
            errors['phone'] = "Phone number is required."
        elif len(re.sub(r'[^0-9]', '', phone)) < 6:
            errors['phone'] = "Please enter a valid phone number."

        # Email is optional: generate clean guest email if empty
        if not email:
            clean_digits = re.sub(r'[^0-9]', '', phone) or 'customer'
            email = f"guest_{clean_digits}@order.local"
        elif not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            errors['email'] = "Please enter a valid email address."

        if not street:
            errors['street'] = "Delivery address is required."
        if not city:
            city = "Local Area"

        if not product_id:
            errors['product'] = "Please select a product."

        try:
            quantity = int(quantity)
            if quantity < 1:
                errors['quantity'] = "Quantity must be at least 1."
        except (ValueError, TypeError):
            errors['quantity'] = "Invalid quantity."

        if errors:
            return {
                'status': 'error',
                'errors': errors,
                'message': "Please fill in all required fields accurately."
            }

        product = request.env['product.product'].sudo().browse(int(product_id)).exists()
        if not product:
            return {
                'status': 'error',
                'message': "The selected product or variant is currently unavailable."
            }

        website = request.website
        company = website.company_id
        PartnerSudo = request.env['res.partner'].sudo()

        # --- Step 1: Find or Create Customer Partner ---
        partner = PartnerSudo.search([
            ('email', '=ilike', email)
        ], limit=1)

        if not partner and phone:
            partner = PartnerSudo.search([
                ('phone', '=', phone)
            ], limit=1)

        if not partner:
            partner = PartnerSudo.create({
                'name': name,
                'email': email,
                'phone': phone,
                'street': street,
                'city': city,
                'type': 'contact',
                'customer_rank': 1,
                'company_id': company.id,
            })
        else:
            update_vals = {}
            if not partner.phone or partner.phone != phone:
                update_vals['phone'] = phone
            if street and partner.street != street:
                update_vals['street'] = street
            if city and partner.city != city:
                update_vals['city'] = city
            if update_vals:
                partner.write(update_vals)

        # --- Step 2: Create Sales Order in Odoo ---
        OrderSudo = request.env['sale.order'].sudo()
        order = OrderSudo.create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'website_id': website.id,
            'company_id': company.id,
            'note': order_notes,
            'state': 'draft',
        })

        # --- Step 3: Add Selected Product Line ---
        request.env['sale.order.line'].sudo().create({
            'order_id': order.id,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'price_unit': product.lst_price,
        })

        # --- Step 4: Apply Delivery Carrier ---
        carrier = False
        if carrier_id:
            carrier = request.env['delivery.carrier'].sudo().browse(int(carrier_id)).exists()
        if not carrier:
            carrier = request.env['delivery.carrier'].sudo().search([('is_published', '=', True)], limit=1)

        delivery_charge = 0.0
        if carrier:
            try:
                order.set_delivery_line(carrier, carrier.fixed_price or 0.0)
                delivery_charge = float(carrier.fixed_price or 0.0)
            except Exception:
                pass

        # Recompute totals
        order._compute_amounts()

        # --- Step 5: Process Payment / Confirmation ---
        # Find active Cash on Delivery provider or first active provider
        cod_provider = request.env['payment.provider'].sudo().search([
            ('custom_mode', '=', 'cash_on_delivery'),
            ('state', 'in', ['enabled', 'test'])
        ], limit=1)

        if not cod_provider:
            cod_provider = request.env['payment.provider'].sudo().search([
                ('state', 'in', ['enabled', 'test'])
            ], limit=1)

        payment_method_name = "Cash on Delivery"
        if cod_provider:
            payment_method_name = cod_provider.name

        try:
            # Confirm the order in Odoo Sales workflow
            order.action_confirm()
        except Exception:
            # If standard confirmation needs quotation state, keep as quotation
            pass

        # Update website session so Odoo ecommerce cart reflects the latest state
        request.session['sale_last_order_id'] = order.id
        request.website.sale_reset()

        currency = order.currency_id

        return {
            'status': 'success',
            'order_id': order.id,
            'order_name': order.name,
            'customer_name': partner.name,
            'customer_phone': partner.phone,
            'customer_email': partner.email,
            'delivery_address': f"{partner.street}, {partner.city}",
            'product_name': product.display_name,
            'quantity': quantity,
            'price_unit': float(product.lst_price),
            'amount_untaxed': float(order.amount_untaxed),
            'amount_delivery': delivery_charge,
            'amount_total': float(order.amount_total),
            'currency_symbol': currency.symbol,
            'amount_total_formatted': f"{currency.symbol}{order.amount_total:.2f}",
            'payment_method': payment_method_name,
            'order_date': fields.Datetime.now().strftime('%B %d, %Y - %I:%M %p'),
            'confirmation_url': f"/shop/confirmation",
            'message': f"Order #{order.name} placed successfully! Thank you for your purchase."
        }

    @http.route('/landing/get_cart_data', type='jsonrpc', auth='public', website=True)
    def get_cart_data(self, carrier_id=None, **kwargs):
        """Returns the full active cart items, pricing breakdown, and totals."""
        order_sudo = request.cart
        currency = request.website.currency_id

        if not order_sudo or not order_sudo.order_line:
            return {
                'status': 'success',
                'cart_quantity': 0,
                'items': [],
                'subtotal': 0.0,
                'subtotal_formatted': f"{currency.symbol}0.00",
                'delivery_charge': 0.0,
                'delivery_formatted': "ফ্রি",
                'total': 0.0,
                'total_formatted': f"{currency.symbol}0.00",
                'currency_symbol': currency.symbol,
            }

        delivery_charge = 60.0
        carrier_name = "ঢাকার ভেতরে"
        if carrier_id:
            try:
                carrier = request.env['delivery.carrier'].sudo().browse(int(carrier_id)).exists()
                if carrier:
                    delivery_charge = float(carrier.fixed_price or 0.0)
                    carrier_name = carrier.name
            except Exception:
                pass
        else:
            default_carrier = request.env['delivery.carrier'].sudo().search([('is_published', '=', True)], limit=1)
            if default_carrier:
                delivery_charge = float(default_carrier.fixed_price or 0.0)
                carrier_name = default_carrier.name

        items = []
        product_subtotal = 0.0
        for line in order_sudo.order_line:
            if getattr(line, 'is_delivery', False):
                continue
            prod = line.product_id
            if not prod:
                continue
            qty = int(line.product_uom_qty)
            price = float(line.price_unit)
            line_sub = float(line.price_subtotal or (price * qty))
            product_subtotal += line_sub

            img_url = f"/web/image/product.product/{prod.id}/image_128"

            items.append({
                'line_id': line.id,
                'product_id': prod.id,
                'name': prod.name,
                'price': price,
                'price_formatted': f"{currency.symbol}{price:.2f}",
                'quantity': qty,
                'subtotal': line_sub,
                'subtotal_formatted': f"{currency.symbol}{line_sub:.2f}",
                'image_url': img_url,
            })

        total = product_subtotal + delivery_charge

        return {
            'status': 'success',
            'cart_quantity': sum(item['quantity'] for item in items),
            'items': items,
            'subtotal': product_subtotal,
            'subtotal_formatted': f"{currency.symbol}{product_subtotal:.2f}",
            'delivery_charge': delivery_charge,
            'delivery_formatted': f"{currency.symbol}{delivery_charge:.2f}" if delivery_charge > 0 else "ফ্রি",
            'carrier_name': carrier_name,
            'total': total,
            'total_formatted': f"{currency.symbol}{total:.2f}",
            'currency_symbol': currency.symbol,
        }

    @http.route('/landing/update_cart_line', type='jsonrpc', auth='public', website=True)
    def update_cart_line(self, line_id, quantity=1, carrier_id=None, **kwargs):
        """Updates line quantity or removes it from active cart."""
        order_sudo = request.cart
        if not order_sudo:
            return {'status': 'error', 'message': 'কোনো সক্রিয় কার্ট পাওয়া যায়নি।'}

        line = order_sudo.order_line.filtered(lambda l: l.id == int(line_id))
        if not line:
            return {'status': 'error', 'message': 'কার্ট থেকে আইটেমটি পাওয়া যায়নি।'}

        quantity = float(quantity)
        if quantity <= 0:
            line.unlink()
        else:
            try:
                order_sudo._cart_update_line_quantity(line_id=line.id, quantity=quantity)
            except Exception:
                line.product_uom_qty = quantity

        order_sudo._compute_amounts()
        return self.get_cart_data(carrier_id=carrier_id)

    @http.route('/landing/submit_cart_order', type='jsonrpc', auth='public', website=True)
    def submit_cart_order(self, **post):
        """
        Confirms the active multi-product cart order in 1 step from the popup form.
        """
        name = (post.get('name') or post.get('customer_name') or '').strip()
        phone = (post.get('phone') or post.get('customer_phone') or '').strip()
        email = (post.get('email') or '').strip()
        street = (post.get('street') or post.get('customer_address') or '').strip()
        city = (post.get('city') or 'Local Area').strip()
        order_notes = (post.get('order_notes') or '').strip()
        carrier_id = post.get('delivery_carrier_id') or post.get('carrier_id')

        errors = {}
        if not name:
            errors['name'] = "আপনার পুরো নাম লিখুন।"
        if not phone:
            errors['phone'] = "মোবাইল নম্বর লিখুন।"
        elif len(re.sub(r'[^0-9]', '', phone)) < 6:
            errors['phone'] = "সঠিক মোবাইল নম্বর লিখুন।"

        if not email:
            clean_digits = re.sub(r'[^0-9]', '', phone) or 'customer'
            email = f"guest_{clean_digits}@order.local"

        if not street:
            errors['street'] = "ডেলিভারি ঠিকানা লিখুন।"

        if errors:
            return {
                'status': 'error',
                'errors': errors,
                'message': "অনুগ্রহ করে সকল প্রয়োজনীয় তথ্য সঠিকভাবে পূরণ করুন।"
            }

        order_sudo = request.cart
        if not order_sudo or not order_sudo.order_line:
            return {
                'status': 'error',
                'message': "আপনার কার্ট বর্তমানে খালি আছে।"
            }

        website = request.website
        company = website.company_id
        PartnerSudo = request.env['res.partner'].sudo()

        partner = PartnerSudo.search([('email', '=ilike', email)], limit=1)
        if not partner and phone:
            partner = PartnerSudo.search([('phone', '=', phone)], limit=1)

        if not partner:
            partner = PartnerSudo.create({
                'name': name,
                'email': email,
                'phone': phone,
                'street': street,
                'city': city,
                'type': 'contact',
                'customer_rank': 1,
                'company_id': company.id,
            })
        else:
            update_vals = {}
            if not partner.phone or partner.phone != phone:
                update_vals['phone'] = phone
            if street and partner.street != street:
                update_vals['street'] = street
            if update_vals:
                partner.write(update_vals)

        order_sudo.write({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'note': order_notes,
        })

        carrier = False
        if carrier_id:
            try:
                carrier = request.env['delivery.carrier'].sudo().browse(int(carrier_id)).exists()
            except Exception:
                pass
        if not carrier:
            carrier = request.env['delivery.carrier'].sudo().search([('is_published', '=', True)], limit=1)

        delivery_charge = 0.0
        if carrier:
            try:
                order_sudo.set_delivery_line(carrier, carrier.fixed_price or 0.0)
                delivery_charge = float(carrier.fixed_price or 0.0)
            except Exception:
                pass

        order_sudo._compute_amounts()

        try:
            order_sudo.action_confirm()
        except Exception:
            pass

        items_summary = []
        for line in order_sudo.order_line:
            if getattr(line, 'is_delivery', False):
                continue
            items_summary.append(f"{line.product_id.name} (x{int(line.product_uom_qty)})")

        summary_text = ", ".join(items_summary) if items_summary else "অর্ডারকৃত বইসমূহ"

        currency = order_sudo.currency_id
        amount_total = float(order_sudo.amount_total)
        order_name = order_sudo.name

        request.session['sale_last_order_id'] = order_sudo.id
        request.website.sale_reset()

        return {
            'status': 'success',
            'order_id': order_sudo.id,
            'order_name': order_name,
            'customer_name': partner.name,
            'customer_phone': partner.phone,
            'customer_email': partner.email,
            'delivery_address': f"{partner.street}, {partner.city}",
            'product_name': summary_text,
            'quantity': sum(int(l.product_uom_qty) for l in order_sudo.order_line if not getattr(l, 'is_delivery', False)),
            'price_unit': amount_total - delivery_charge,
            'amount_untaxed': float(order_sudo.amount_untaxed),
            'amount_delivery': delivery_charge,
            'amount_total': amount_total,
            'currency_symbol': currency.symbol,
            'amount_total_formatted': f"{currency.symbol}{amount_total:.2f}",
            'payment_method': "ক্যাশ অন ডেলিভারি",
            'order_date': fields.Datetime.now().strftime('%B %d, %Y - %I:%M %p'),
            'confirmation_url': f"/shop/confirmation",
            'message': f"আপনার অর্ডার #{order_name} সফলভাবে গ্রহণ করা হয়েছে!"
        }

