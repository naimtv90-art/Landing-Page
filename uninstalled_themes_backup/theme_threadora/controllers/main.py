# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ThreadoraGarmentsController(http.Controller):

    @http.route(['/about-us', '/aboutus'], type='http', auth='public', website=True, sitemap=True)
    def threadora_aboutus(self, **kw):
        return request.render('theme_threadora.garment_aboutus_page', {})

    @http.route(['/contactus', '/contact-us'], type='http', auth='public', website=True, sitemap=True)
    def threadora_contactus(self, **kw):
        return request.render('theme_threadora.garment_contactus_page', {})

    @http.route(['/faq'], type='http', auth='public', website=True, sitemap=True)
    def threadora_faq(self, **kw):
        return request.render('theme_threadora.garment_faq_page', {})

    @http.route(['/wholesale', '/private-label'], type='http', auth='public', website=True, sitemap=True)
    def threadora_wholesale(self, **kw):
        return request.render('theme_threadora.garment_wholesale_page', {})
