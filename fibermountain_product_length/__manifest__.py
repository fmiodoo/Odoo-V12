# -*- coding: utf-8 -*-
{
    'name': "FiberMountain: Auto-Calculate Price based on Length",

    'summary': "Calculates the price of the product variant based on the entered length.",

    'description': """
Task ID: 2368045 jsz
Product Configurator to price based on a set of inputs.

Fiber Mountain sells custom length cables, and depending on different attributes, and the length, Odoo should 
be able to generate the new product, calculate the price (according to the attribute values and their price 
delta) and add it to the sales order.


- add catalog to product and sale order
    """,
    'author': "Odoo Inc",
    'website': "http://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': [
        'sale_management',
        'stock', 
        'base'
    ],

    # always loaded
    'data': [
        'views/product_template_views_inherit.xml',
        'views/sale_order_views_inherit.xml',
        'report/sale_report_templates.xml',
    ],

    'license': 'OPL-1'
}