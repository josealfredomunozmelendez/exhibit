# -*- coding: utf-8 -*-
{
    'name': "Renta-Reserva",

    'summary': """
        Reservar el producto el dia solicitado.""",

    'description': """
    """,

    'author': "Llacox",
    'website': "http://www.llacox.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
}