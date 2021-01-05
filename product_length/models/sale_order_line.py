# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    desired_length = fields.Float(string="Length",
                                  related="product_id.desired_length",
                                  readonly=False)

    name = fields.Text(string="Description",
                       compute="_compute_name")

    @api.depends('product_id.name')
    def _compute_name(self):
        for line in self:
            if line.product_id.is_cable_product:
                line.name = line.product_id.name
            else:
                line.name = line.product_id.get_product_multiline_description_sale()

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'product_id.length_multiplier', 'product_id.desired_length')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        super(SaleOrderLine, self)._compute_amount()

        for line in self:
            extra_length = line.product_id.desired_length - 1.0
            line.price_subtotal += extra_length * line.product_id.length_multiplier
