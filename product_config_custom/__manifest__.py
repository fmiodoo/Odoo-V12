# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Customized Product Configurator",
    'description': """
Customized Product Configurator
================================
    """,
    'version': '1.0',
    'author': 'Odoo Inc',
    'license': 'OPL-1',
    'mainainer': 'Odoo Inc',
    'category': 'Custom Developments',    
    'depends': [
        'sale_product_configurator'
    ],
    'data': [
        # Security files
        'security/ir.model.access.csv',
        # Views
        'views/product_views.xml',
    ],
}