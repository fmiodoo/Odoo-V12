# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    length_multiplier = fields.Float(string="Length Cost Multiplier",
                                   default=1.0,
                                   help="Price per each unit above the single unit assembled price.")
    is_cable_product = fields.Boolean(string="Is a Cable Product")

    @api.constrains("length_multiplier")
    def _check_length_multiplier(self):
        if self.length_multiplier <= 0.0:
            raise ValidationError("Field Length Cost Multiplier must be a positive value.")
