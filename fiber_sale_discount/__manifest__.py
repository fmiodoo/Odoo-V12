# -*- coding: utf-8 -*-
{
    'name': "Quotations/Sales Orders Discount Approval",
    'summary': """
        Sales Discount Control
        """,
    'description': """
        Sales Discount Control
        """,
    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",
    'category': 'Customization',
    'version': '0.1',
    'depends': ['sale'],
    'data': [
        'views/sale_views.xml',
        'data/mail_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
