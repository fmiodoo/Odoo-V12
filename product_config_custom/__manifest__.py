# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Customized Product Configurator",
    'version': '1.0',
    'depends': ['sale_product_configurator'],
    'author': 'Odoo Inc',
    'license': 'OEEL-1',
    'mainainer': 'Odoo Inc',
    'category': 'Custom',
    'description': """
Customized Product Configurator
================================

    """,
    # data files always loaded at installation
    'data': [
        # Security files
        'security/ir.model.access.csv',
        # Views
        'views/product_views.xml',
    ],
}