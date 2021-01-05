# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    length = fields.Float(string="Length",
                          default=1.0,
                          readonly=False)

    name = fields.Text(string="Description",
                       compute="_compute_name")

    @api.one
    @api.constrains("length")
    def _check_length(self):
        if self.length <= 0.0:
            raise ValidationError("Field Length must be a positive value.")

    @api.depends('length')
    def _compute_name(self):
        for line in self:
            if line.product_id.is_cable_product:
                formatted_length = "%07.2f" % line.length + line.product_id.uom_id.name
                line.name = line.product_id.name + "-" + formatted_length
            else:
                line.name = line.product_id.get_product_multiline_description_sale()

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id", "product_id.length_multiplier", "length")
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.  If a line contains a cable product, the price will be computed based on
        the length input in the order line against the 1 UoM base sale price of the product.
        """
        super(SaleOrderLine, self)._compute_amount()

        for line in self:
            if line.product_id.is_cable_product:
                if line.length < 1.0:
                    line.price_subtotal *= line.length
                elif line.length > 1.0:
                    extra_length = line.length - 1.0
                    line.price_subtotal += extra_length * line.product_id.length_multiplier
