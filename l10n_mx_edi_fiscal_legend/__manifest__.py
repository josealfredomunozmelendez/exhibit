# -*- coding: utf-8 -*-
# Copyright 2017 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EDI Fiscal Legend Complement for the Mexican Localization',
    'version': '11.0.0.0.0',
    'author': 'Vauxoo',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'website': 'http://www.vauxoo.com/',
    'depends': [
        'l10n_mx_edi',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/fiscal_legend_template.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
}
