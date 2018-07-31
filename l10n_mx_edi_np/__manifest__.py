# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Notary Public Complement',
    'version': '11.0.1.0.0',
    "author": "Vauxoo",
    "license": "LGPL-3",
    'category': 'Hidden',
    'summary': 'Mexican Localization for EDI documents',
    'depends': [
        'base_automation',
        'l10n_mx_edi',
    ],
    'data': [
        "data/category.xml",
        "data/notary_public.xml",
        "data/server_action_partner_other_address.xml",
        "views/account_invoice_view.xml",
        "views/res_partner_view.xml",
    ],
    'demo': [
    ],
    "post_init_hook": "post_init_hook",
    'installable': True,
    'auto_install': False,
}
