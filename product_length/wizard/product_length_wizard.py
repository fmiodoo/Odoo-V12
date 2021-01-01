# coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductLengthWizard(models.TransientModel):
    _name = "product.length.wizard"
    _description = "Wizard: Assign a Desired Length to a Product"

    def _default_order_line(self):
        return self.env["sale.order.line"].browse(self._context.get("active_id"))

    order_line_id = fields.Many2one(comodel_name="sale.order.line",
                                 string="Order Line",
                                 default=_default_order_line)
    length = fields.Float(string="Desired Length",
                          default=1.0,
                          required=True)

    @api.multi
    def assign_length(self):
        self.order_line_id.product_id.desired_length = self.length
