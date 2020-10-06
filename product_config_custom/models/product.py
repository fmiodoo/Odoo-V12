# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductAttributeGroup(models.Model):
    _name = 'product.attribute.group'
    _order = 'sequence'
    _description = """
    Object to handle sequence of attribute values and grouping when generating default code.
    """

    name = fields.Char(string="Group Name")
    sequence = fields.Integer()
    attribute_ids = fields.One2many(comodel_name='product.attribute', inverse_name='group_id', string='Attributes')


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    group_id = fields.Many2one(comodel_name='product.attribute.group', string="Attribute Group")
    value_is_code = fields.Boolean()

class PTAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    code = fields.Char(copy=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def _create_product_variant(self, combination, log_warning=False):
        product = super(ProductTemplate, self)._create_product_variant(combination, log_warning=log_warning)
        groups = []
        pavs = product.product_template_attribute_value_ids.mapped('product_attribute_value_id')
        product_attributes = pavs.mapped('attribute_id')
        for attr_group in product_attributes.mapped('group_id'):
            codes = [(pav.name if pav.attribute_id.value_is_code else pav.code) for pav in pavs.filtered(lambda v: v.attribute_id in attr_group.attribute_ids)]
            groups.append(''.join([code for code in codes if code]))
        product.default_code = '-'.join(groups)
        return product


class ProductTemplateAttributeLine(models.Model):
    """
    Sole purpose of inheriting this model is to order attribute values on id only.
    In standard the order is attribute_id, id which is not useful for this customer for generating
    code based on attribute values.
    """

    _inherit = "product.template.attribute.line"
    _order = 'id'