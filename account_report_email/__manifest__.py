# -*- coding: utf-8 -*-
{
    'name': "Followup Email",

    'summary': """
       Permite modificar el correo del reporte followup de la cuenta deudora""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Llacox",
    'website': "http://www.llacox.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account',
        'account_reports',
    ],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
}