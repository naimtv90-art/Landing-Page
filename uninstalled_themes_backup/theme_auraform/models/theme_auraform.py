# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class ThemeAuraform(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_auraform_post_copy(self, mod):
        # Configure default website parameters and palette presets
        self.enable_view('theme_auraform.s_3d_hero')
        self.enable_view('theme_auraform.s_3d_customizer')
