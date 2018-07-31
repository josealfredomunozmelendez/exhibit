# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo Mexico Localization for Stock/Landing',
    'summary': '''
        Generate Electronic Invoice with Customs Number
    ''',
    'version': '11.0.1.0.0',
    'author': 'Jarsa Sistemas, Vauxoo',
    'category': 'Accounting',
    'license': 'OEEL-1',
    'depends': [
        'stock_landed_costs',
        'l10n_mx_edi',
        'sale_management',
        'account_accountant',
        'l10n_mx_customs',
    ],
    'data': [
        'views/stock_landed_cost.xml',
    ],
    'installable': True,
}
