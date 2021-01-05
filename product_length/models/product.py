# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    length_multiplier = fields.Float(string="Length Cost Multiplier",
                                   default=1.0,
                                   help="Price per each unit above the single unit assembled price.")
    is_cable_product = fields.Boolean(string="Is a Cable Product")

    @api.one
    @api.constrains("length_multiplier")
    def _check_length_multiplier(self):
        if self.length_multiplier <= 0.0:
            raise ValidationError("Field Length Cost Multiplier must be a positive value.")


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
        if self.desired_length <= 0.0:
            raise ValidationError("Field Desired Length must be a positive value.")

    @api.depends("desired_length", "product_tmpl_id")
    def _compute_product_name(self):
        for product in self:
            if product.is_cable_product:
                formatted_length = "%07.1f" % product.desired_length + product.uom_id.name
                product.name = product.product_tmpl_id.name + "-" + formatted_length

                if product.x_studio_catalog_:
                    product.x_studio_catalog_ = product.product_tmpl_id.x_studio_catalog_ + "-" + formatted_length
            else:
                product.name = product.product_tmpl_id.name
                if product.x_studio_catalog_:
                    product.x_studio_catalog_ = product.product_tmpl_id.x_studio_catalog_
