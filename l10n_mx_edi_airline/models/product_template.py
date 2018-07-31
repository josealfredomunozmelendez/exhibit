# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_mx_edi_airline_type = fields.Selection([
        ('tua', 'TUA'),
        ('extra', 'Extra Charge'),
    ],
        string='Product Type',
        help='Select a product type if the product is and Airport Use Fee or '
        'an IATA extra charge'
    )
