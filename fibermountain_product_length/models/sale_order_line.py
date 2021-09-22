# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import float_round
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    length = fields.Float(string="Length",
                          default=1.0,
                          readonly=False)

    cable_catalog_number = fields.Char(string="Cable Catalog #",
                                       compute="_compute_cable_catalog_number")

    name = fields.Text(string='Description', required=True, default="")

    @api.constrains("length")
    def _check_length(self):
        for line in self:
            if line.length < 1.0:
                raise ValidationError("Field Length must be a value greater than or equal to 1.")
            else:
                if line.length % 1 != 0.5 or line.length % 1 != 0.0:
                    raise ValidationError("Field length may only contain increments of 0.5.")

    @api.depends("length")
    def _compute_cable_catalog_number(self):
        for line in self:
            if line.product_id.is_cable_product:
                formatted_length = "%07.1f" % line.length + "M"
                line.cable_catalog_number = (line.product_id.x_studio_catalog_ or "") + "-" + formatted_length
            else:
                line.cable_catalog_number = ""

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id", "product_id.length_multiplier", "length")
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.  If a line contains a cable product, the price will be computed based on
        the length input in the order line against the 1 UoM base sale price of the product.
        """
        super(SaleOrderLine, self)._compute_amount()

        for line in self.filtered(lambda l: l.product_id.is_cable_product):
            new_price = 0
            new_unit_price = line.product_id.list_price

            if line.length < 1.0:
                new_unit_price = float_round(new_unit_price * line.length, precision_digits=2)
                new_price = float_round(new_unit_price * (1 - (line.discount or 0.0) / 100), 2)

            elif line.length > 1.0:
                extra_length = line.length - 1.0
                new_unit_price += float_round(extra_length * line.product_id.length_multiplier, precision_digits=2)
                new_price = float_round(new_unit_price * (1 - (line.discount or 0.0) / 100), precision_digits=2)

            else:
                new_price = float_round(new_unit_price * (1 - (line.discount or 0.0) / 100), precision_digits=2)

            taxes = line.tax_id.compute_all(new_price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)

            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'price_unit': new_unit_price
            })

            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
