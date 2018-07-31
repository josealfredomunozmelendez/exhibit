# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_mx_edi_np_curp = fields.Char(
        'CURP', help='Express the CURP of each alienator, or owner, or '
        'possessor of the servant property, in case of rights of way.'
    )
