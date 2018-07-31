# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_mx_edi_curp = fields.Char(
        'CURP', size=18, help="Unique Population Registry Code")
