# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'product_id.per_meter_adder', 'product_id.desired_length')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        super(SaleOrderLine, self)._compute_amount()

        for line in self:
            extra_length = line.product_id.desired_length - 1.0
            line.price_subtotal += extra_length * line.product_id.per_meter_adder
