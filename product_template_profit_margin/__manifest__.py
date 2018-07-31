# -*- coding: utf-8 -*-
{
    'name': "Margen de Utilidad",

    'summary': """
        Calculo de utilidad""",

    'description': """
        Se agrego un campo en el formulario del producto para calcular la utilidad en base a un porcentaje.
    """,

    'author': "Llacox",
    'website': "http://www.llacox.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}