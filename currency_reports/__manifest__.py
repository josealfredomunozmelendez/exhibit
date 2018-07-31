# -*- coding: utf-8 -*-
{
    'name': "Currency Reports",

    'summary': """
        Display Currency in reports.""",

    'description': """
        Module to display currency in purchase, sale, invoice and aged reports.
    """,

    'author': "Llacox",
    'website': "http://www.llacox.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '11.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account',
        'purchase',
        'sale',
        'web',
    ],

    # always loaded
    'data': [
        'views/purchase_order_templates.xml',
        'views/report_invoice.xml',
        'views/sale_report_templates.xml',
    ],
}
