# -*- coding: utf-8 -*-
{
    'name': "Exhibit",

    'summary': """
        Módulos de Exhibit""",

    'description': """
        Módulos necesarios para instalar el servicio de la instancia de Exhibit
    """,

    'author': "Llacox",
    'website': "http://www.llacox.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Exhibit',
    'version': '11.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'website_quote',
    ],

    # always loaded
    'data': [
        'data/company.xml',
        #'data/config.xml',
        'views/calendar.xml',
        'views/sale_order.xml',
        'views/website_quote_templates.xml',
        'report/sale_report_templates.xml',
    ],
}