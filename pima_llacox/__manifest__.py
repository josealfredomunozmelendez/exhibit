# -*- coding: utf-8 -*-
{
    'name': "Pima Llacox",

    'summary': """
        MRP""",

    'description': """
        TBD
    """,

    'author': "Llacox",
    'website': "http://www.llacox.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'quality_mrp', 'mrp', 'stock','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/purchase_order_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
