# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    per_meter_adder = fields.Float(string="Per Meter Adder",
                                   default=1.0,
                                   help="Price per meter above the 1m assembled price.")

    @api.one
    @api.constrains("per_meter_adder")
    def _check_per_meter_adder(self):
        if self.per_meter_adder <= 0.0:
            raise ValidationError("Field Per Meter Adder must contain a positive value.")


class ProductProduct(models.Model):
    _inherit = "product.product"

    desired_length = fields.Float(string="Desired Length",
                                  default=1.0)
    name = fields.Char(string="Name",
                       compute="_compute_product_name")
    x_studio_catalog_ = fields.Char(string="Catalog #",
                                    compute="_compute_product_name")

    @api.one
    @api.constrains("desired_length")
    def _check_desired_length(self):
        # TODO: Confirm that minimum length is 1M
        if self.desired_length < 1.0:
            raise ValidationError("Field Desired Length must be at least 1.0M.")

    @api.depends("desired_length", "product_tmpl_id")
    def _compute_product_name(self):
        for product in self:
            formatted_length = str(product.desired_length).zfill(5) + "M"
            product.name = product.product_tmpl_id.name + "-" + formatted_length
            product.x_studio_catalog_ = product.product_tmpl_id.x_studio_catalog_ + "-" + formatted_length

