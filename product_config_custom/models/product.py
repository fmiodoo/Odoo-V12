# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PTAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    code = fields.Char(copy=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def _create_product_variant(self, combination, log_warning=False):
        product = super(ProductTemplate, self)._create_product_variant(combination, log_warning=log_warning)
        attribute_value_codes = product.product_template_attribute_value_ids.mapped('code')
        product.default_code = '-'.join([code for code in attribute_value_codes if code])
        return product


class ProductTemplateAttributeLine(models.Model):
    """
    Sole purpose of inheriting this model is to order attribute values on id only.
    In standard the order is attribute_id, id which is not useful for this customer for generating
    code based on attribute values.
    """

    _inherit = "product.template.attribute.line"
    _order = 'id'