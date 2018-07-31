# coding: utf-8

from odoo import fields, models


class City(models.Model):
    _inherit = 'res.city'

    l10n_mx_edi_code = fields.Char('Code')
