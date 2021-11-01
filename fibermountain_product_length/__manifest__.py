# -*- coding: utf-8 -*-
{
    'name': "FiberMountain: Auto-Calculate Price based on Length",

    'summary': """
        Calculates the price of the product variant based on the entered length.""",

    'description': """
        Task ID: 2368045 jsz
        
        Product Configurator to price based on a set of inputs.

        Fiber Mountain sells custom length cables, and depending on different attributes, and the length, Odoo should 
        be able to generate the new product, calculate the price (according to the attribute values and their price 
        delta) and add it to the sales order.
    """,

    'author': "Odoo Inc",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Custom Development',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management', 'web_studio', 'stock', 'base'],

    # always loaded
    'data': [
        'views/product_template_views_inherit.xml',
        'views/sale_order_views_inherit.xml',
        'report/sale_report_templates.xml',
    ],

    'license': 'OEEL-1'
}