# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']

    cable_catalog_number = fields.Char(string="Cable Catalog #", compute="_compute_cable_catalog_number")

    def _compute_cable_catalog_number(self):
        for line in self:
            if line.product_id.is_cable_product:
                relevant_order = self.env['sale.order'].search([('name', '=', line.move_id.invoice_origin)])
                for order_line in relevant_order.order_line:
                    if line.product_id == order_line.product_id:
                        line.cable_catalog_number = order_line.cable_catalog_number
                if not line.cable_catalog_number:
                    line.cable_catalog_number = ""
            else:
                line.cable_catalog_number = ""
